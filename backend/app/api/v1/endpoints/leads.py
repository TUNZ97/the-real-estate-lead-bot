"""Lead endpoints."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.leads import (
    LeadListResponse,
    LeadOut,
    LeadStatusUpdate,
    LeadUpdate,
)
from app.services.lead_service import LeadService

router = APIRouter()


@router.get("", response_model=LeadListResponse)
async def list_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    qualification: Optional[str] = None,
    urgency: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> LeadListResponse:
    items, total = await LeadService(db).list_leads(
        page=page,
        limit=limit,
        status=status,
        qualification=qualification,
        urgency=urgency,
    )
    return LeadListResponse(items=items, total=total, page=page, limit=limit)


@router.get("/{lead_id}", response_model=LeadOut)
async def get_lead(lead_id: UUID, db: AsyncSession = Depends(get_db)) -> LeadOut:
    lead = await LeadService(db).get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}", response_model=LeadOut)
async def patch_lead(
    lead_id: UUID,
    data: LeadUpdate,
    db: AsyncSession = Depends(get_db),
) -> LeadOut:
    lead = await LeadService(db).update_lead(lead_id, data)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("/{lead_id}/status", response_model=LeadOut)
async def change_status(
    lead_id: UUID,
    data: LeadStatusUpdate,
    db: AsyncSession = Depends(get_db),
) -> LeadOut:
    try:
        lead = await LeadService(db).update_status(lead_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("/{lead_id}/qualify", response_model=LeadOut)
async def requalify(lead_id: UUID, db: AsyncSession = Depends(get_db)) -> LeadOut:
    lead = await LeadService(db).requalify(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
