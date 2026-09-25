"""Lead query and update services."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.entities import Customer, Lead, LeadActivity
from app.models.enums import LeadStatus
from app.schemas.leads import LeadOut, LeadStatusUpdate, LeadUpdate
from app.services.qualification import qualify_lead


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class LeadService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _to_out(self, lead: Lead, customer: Optional[Customer] = None) -> LeadOut:
        c = customer or lead.customer
        return LeadOut(
            id=lead.id,
            customer_id=lead.customer_id,
            status=lead.status,
            intent=lead.intent,
            property_type=lead.property_type,
            location_text=lead.location_text,
            bedrooms=lead.bedrooms,
            budget_min=lead.budget_min,
            budget_max=lead.budget_max,
            currency=lead.currency,
            timeframe=lead.timeframe,
            qualification_level=lead.qualification_level,
            qualification_score=lead.qualification_score,
            urgency=lead.urgency,
            notes=lead.notes,
            created_at=lead.created_at,
            updated_at=lead.updated_at,
            customer_name=c.name if c else None,
            customer_email=c.email if c else None,
            customer_phone=c.phone if c else None,
        )

    async def list_leads(
        self,
        *,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        qualification: Optional[str] = None,
        urgency: Optional[str] = None,
    ) -> tuple[list[LeadOut], int]:
        page = max(1, page)
        limit = min(100, max(1, limit))
        offset = (page - 1) * limit

        filters = []
        if status:
            filters.append(Lead.status == status)
        if qualification:
            filters.append(Lead.qualification_level == qualification)
        if urgency:
            filters.append(Lead.urgency == urgency)

        count_q = select(func.count(Lead.id))
        list_q = (
            select(Lead)
            .options(selectinload(Lead.customer))
            .order_by(Lead.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        for f in filters:
            count_q = count_q.where(f)
            list_q = list_q.where(f)

        total = int(await self.db.scalar(count_q) or 0)
        rows = list(await self.db.scalars(list_q))
        return [self._to_out(r) for r in rows], total

    async def get_lead(self, lead_id: uuid.UUID) -> Optional[LeadOut]:
        lead = await self.db.scalar(
            select(Lead)
            .options(selectinload(Lead.customer))
            .where(Lead.id == lead_id)
        )
        if not lead:
            return None
        return self._to_out(lead)

    async def update_lead(
        self, lead_id: uuid.UUID, data: LeadUpdate
    ) -> Optional[LeadOut]:
        lead = await self.db.scalar(
            select(Lead)
            .options(selectinload(Lead.customer))
            .where(Lead.id == lead_id)
        )
        if not lead:
            return None

        changes = data.model_dump(exclude_unset=True)
        for k, v in changes.items():
            setattr(lead, k, v)

        customer = lead.customer
        qual = qualify_lead(
            intent=lead.intent,
            property_type=lead.property_type,
            location_text=lead.location_text,
            bedrooms=lead.bedrooms,
            budget_min=lead.budget_min,
            budget_max=lead.budget_max,
            timeframe=lead.timeframe,
            customer_name=customer.name if customer else None,
            customer_email=customer.email if customer else None,
            customer_phone=customer.phone if customer else None,
        )
        lead.qualification_score = qual.score
        lead.qualification_level = qual.level
        lead.urgency = qual.urgency

        self.db.add(
            LeadActivity(
                id=uuid.uuid4(),
                lead_id=lead.id,
                activity_type="LEAD_UPDATED",
                description="Lead fields updated",
                meta=changes,
                created_at=_utcnow(),
            )
        )
        await self.db.flush()
        return self._to_out(lead)

    async def update_status(
        self, lead_id: uuid.UUID, data: LeadStatusUpdate
    ) -> Optional[LeadOut]:
        lead = await self.db.scalar(
            select(Lead)
            .options(selectinload(Lead.customer))
            .where(Lead.id == lead_id)
        )
        if not lead:
            return None

        # Validate status is a known enum value
        valid = {s.value for s in LeadStatus}
        if data.status not in valid:
            raise ValueError(f"Invalid status: {data.status}")

        old = lead.status
        lead.status = data.status
        self.db.add(
            LeadActivity(
                id=uuid.uuid4(),
                lead_id=lead.id,
                activity_type="STATUS_CHANGED",
                description=data.reason or f"{old} → {data.status}",
                meta={"from": old, "to": data.status},
                created_at=_utcnow(),
            )
        )
        await self.db.flush()
        return self._to_out(lead)

    async def requalify(self, lead_id: uuid.UUID) -> Optional[LeadOut]:
        lead = await self.db.scalar(
            select(Lead)
            .options(selectinload(Lead.customer))
            .where(Lead.id == lead_id)
        )
        if not lead:
            return None
        customer = lead.customer
        qual = qualify_lead(
            intent=lead.intent,
            property_type=lead.property_type,
            location_text=lead.location_text,
            bedrooms=lead.bedrooms,
            budget_min=lead.budget_min,
            budget_max=lead.budget_max,
            timeframe=lead.timeframe,
            customer_name=customer.name if customer else None,
            customer_email=customer.email if customer else None,
            customer_phone=customer.phone if customer else None,
        )
        lead.qualification_score = qual.score
        lead.qualification_level = qual.level
        lead.urgency = qual.urgency
        lead.qualification_version = qual.version
        self.db.add(
            LeadActivity(
                id=uuid.uuid4(),
                lead_id=lead.id,
                activity_type="REQUALIFIED",
                description=f"Score {qual.score} ({qual.level})",
                meta={"score": qual.score, "level": qual.level, "urgency": qual.urgency},
                created_at=_utcnow(),
            )
        )
        await self.db.flush()
        return self._to_out(lead)
