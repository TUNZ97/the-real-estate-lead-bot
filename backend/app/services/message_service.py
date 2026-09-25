"""Lead intake vertical slice service."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.entities import (
    Conversation,
    Customer,
    Lead,
    LeadActivity,
    Message,
)
from app.models.enums import (
    ConversationStatus,
    LeadStatus,
    MessageSender,
)
from app.schemas.messages import MessageCreate, MessageIntakeResponse
from app.services.extraction_heuristics import extract_from_text
from app.services.n8n_client import n8n_client
from app.services.qualification import qualify_lead

logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _build_response(
    *,
    extracted_intent: str,
    location: str | None,
    missing: list[str],
) -> str:
    parts: list[str] = []
    parts.append("Thanks for reaching out to PrimeHomes!")

    known: list[str] = []
    if extracted_intent not in ("UNKNOWN", "GENERAL_ENQUIRY"):
        known.append(f"you're interested in **{extracted_intent.lower()}**")
    if location:
        known.append(f"around **{location}**")
    if known:
        parts.append("I noted that " + " and ".join(known) + ".")

    question_map = {
        "intent": "Are you looking to buy, rent, or sell?",
        "location": "Which area or neighbourhood are you considering?",
        "property_type": "What type of property (apartment, house, land, etc.)?",
        "bedrooms": "How many bedrooms do you need?",
        "budget": "What budget range should we work with (in Naira)?",
        "timeframe": "When are you hoping to move or complete this?",
        "contact": "Could you share a phone number or email so our team can follow up?",
    }
    for key in missing:
        if key in question_map:
            parts.append(question_map[key])
            break
    else:
        parts.append(
            "A sales specialist can take it from here. "
            "Reply anytime if you'd like to adjust your requirements."
        )

    parts.append("You can also ask to speak with a human agent at any time.")
    return " ".join(parts)


class MessageService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def intake(self, payload: MessageCreate) -> MessageIntakeResponse:
        # Idempotency: same external_message_id → return existing flow snapshot
        if payload.external_message_id:
            existing = await self.db.scalar(
                select(Message).where(
                    Message.external_message_id == payload.external_message_id
                )
            )
            if existing:
                conv = await self.db.get(Conversation, existing.conversation_id)
                lead_id = conv.lead_id if conv else None
                return MessageIntakeResponse(
                    conversation_id=existing.conversation_id,
                    message_id=existing.id,
                    lead_id=lead_id,
                    response="Message already received.",
                )

        conversation = await self._resolve_conversation(payload)
        customer = await self.db.get(Customer, conversation.customer_id)
        assert customer is not None

        # Update customer contact if provided
        if payload.customer_name:
            customer.name = payload.customer_name
        if payload.customer_email:
            customer.email = payload.customer_email
        if payload.customer_phone:
            customer.phone = payload.customer_phone

        customer_msg = Message(
            id=uuid.uuid4(),
            conversation_id=conversation.id,
            sender_type=MessageSender.CUSTOMER.value,
            content=payload.message,
            external_message_id=payload.external_message_id,
            created_at=_utcnow(),
        )
        self.db.add(customer_msg)

        extracted = extract_from_text(payload.message)
        lead = await self._resolve_lead(conversation, customer, extracted)

        qual = qualify_lead(
            intent=lead.intent,
            property_type=lead.property_type,
            location_text=lead.location_text,
            bedrooms=lead.bedrooms,
            budget_min=lead.budget_min,
            budget_max=lead.budget_max,
            timeframe=lead.timeframe,
            customer_name=customer.name,
            customer_email=customer.email,
            customer_phone=customer.phone,
        )
        lead.qualification_score = qual.score
        lead.qualification_level = qual.level
        lead.urgency = qual.urgency
        lead.qualification_version = qual.version

        self.db.add(
            LeadActivity(
                id=uuid.uuid4(),
                lead_id=lead.id,
                activity_type="MESSAGE_RECEIVED",
                description="Customer message ingested",
                meta={
                    "message_id": str(customer_msg.id),
                    "qualification_score": qual.score,
                },
                created_at=_utcnow(),
            )
        )

        bot_text = _build_response(
            extracted_intent=lead.intent,
            location=lead.location_text,
            missing=qual.missing_information,
        )
        bot_msg = Message(
            id=uuid.uuid4(),
            conversation_id=conversation.id,
            sender_type=MessageSender.BOT.value,
            content=bot_text,
            created_at=_utcnow(),
        )
        self.db.add(bot_msg)

        await self.db.flush()

        # Fire n8n (non-blocking for customer path; errors are logged)
        await n8n_client.trigger_lead_intake(
            conversation_id=conversation.id,
            message_id=customer_msg.id,
            lead_id=lead.id,
            message=payload.message,
            correlation_id=str(customer_msg.id),
        )

        return MessageIntakeResponse(
            conversation_id=conversation.id,
            message_id=customer_msg.id,
            lead_id=lead.id,
            response=bot_text,
            qualification_level=qual.level,
            urgency=qual.urgency,
        )

    async def _resolve_conversation(self, payload: MessageCreate) -> Conversation:
        if payload.conversation_id:
            conv = await self.db.get(Conversation, payload.conversation_id)
            if conv:
                return conv

        customer = Customer(
            id=uuid.uuid4(),
            name=payload.customer_name,
            email=payload.customer_email,
            phone=payload.customer_phone,
        )
        self.db.add(customer)
        await self.db.flush()

        conv = Conversation(
            id=uuid.uuid4(),
            customer_id=customer.id,
            status=ConversationStatus.ACTIVE.value,
            channel=payload.channel or "web",
        )
        self.db.add(conv)
        await self.db.flush()
        return conv

    async def _resolve_lead(
        self, conversation: Conversation, customer: Customer, extracted
    ) -> Lead:
        if conversation.lead_id:
            lead = await self.db.get(Lead, conversation.lead_id)
            if lead:
                self._merge_extracted(lead, extracted)
                return lead

        lead = Lead(
            id=uuid.uuid4(),
            customer_id=customer.id,
            status=LeadStatus.NEW.value,
            intent=extracted.intent,
            property_type=extracted.property_type,
            location_text=extracted.location_text,
            bedrooms=extracted.bedrooms,
            budget_min=extracted.budget_min,
            budget_max=extracted.budget_max,
            currency=extracted.currency,
            timeframe=extracted.timeframe,
        )
        self.db.add(lead)
        await self.db.flush()
        conversation.lead_id = lead.id
        return lead

    def _merge_extracted(self, lead: Lead, extracted) -> None:
        # Only fill unknowns / improve known fields carefully
        if extracted.intent != "UNKNOWN":
            lead.intent = extracted.intent
        if extracted.property_type != "UNKNOWN":
            lead.property_type = extracted.property_type
        if extracted.location_text:
            lead.location_text = extracted.location_text
        if extracted.bedrooms is not None:
            lead.bedrooms = extracted.bedrooms
        if extracted.budget_min is not None:
            lead.budget_min = extracted.budget_min
        if extracted.budget_max is not None:
            lead.budget_max = extracted.budget_max
        if extracted.timeframe != "UNKNOWN":
            lead.timeframe = extracted.timeframe

    async def get_conversation_messages(
        self, conversation_id: uuid.UUID
    ) -> list[Message]:
        result = await self.db.scalars(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return list(result)

    async def get_conversation(
        self, conversation_id: uuid.UUID
    ) -> Conversation | None:
        result = await self.db.scalar(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        return result
