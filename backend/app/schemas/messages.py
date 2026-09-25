"""Message intake schemas — API_SPECIFICATION."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    conversation_id: Optional[UUID] = None
    external_message_id: Optional[str] = Field(None, max_length=128)
    customer_name: Optional[str] = Field(None, max_length=255)
    customer_email: Optional[str] = Field(None, max_length=255)
    customer_phone: Optional[str] = Field(None, max_length=64)
    channel: str = Field(default="web", max_length=32)


class MessageOut(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_type: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageIntakeResponse(BaseModel):
    conversation_id: UUID
    message_id: UUID
    lead_id: Optional[UUID] = None
    response: str
    qualification_level: Optional[str] = None
    urgency: Optional[str] = None
