"""Lead schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class LeadOut(BaseModel):
    id: UUID
    customer_id: UUID
    status: str
    intent: str
    property_type: str
    location_text: Optional[str] = None
    bedrooms: Optional[int] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: str
    timeframe: str
    qualification_level: str
    qualification_score: Optional[int] = None
    urgency: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None

    model_config = {"from_attributes": True}


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    intent: Optional[str] = None
    property_type: Optional[str] = None
    location_text: Optional[str] = None
    bedrooms: Optional[int] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: Optional[str] = None
    timeframe: Optional[str] = None
    notes: Optional[str] = None


class LeadStatusUpdate(BaseModel):
    status: str = Field(..., min_length=1)
    reason: Optional[str] = None


class LeadListResponse(BaseModel):
    items: list[LeadOut]
    total: int
    page: int
    limit: int
