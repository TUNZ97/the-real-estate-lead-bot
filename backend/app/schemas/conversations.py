"""Conversation schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.schemas.messages import MessageOut


class ConversationOut(BaseModel):
    id: UUID
    customer_id: UUID
    lead_id: Optional[UUID] = None
    status: str
    channel: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageOut] = []

    model_config = {"from_attributes": True}
