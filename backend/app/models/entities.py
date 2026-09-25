"""Core business entities — MySQL for local dev; portable SQLAlchemy types."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import (
    ConversationStatus,
    FollowUpStatus,
    Intent,
    LeadStatus,
    NotificationStatus,
    PropertyType,
    QualificationLevel,
    Timeframe,
    Urgency,
    UserRole,
)


class Customer(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "customers"

    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)

    leads: Mapped[list[Lead]] = relationship(back_populates="customer")
    conversations: Mapped[list[Conversation]] = relationship(back_populates="customer")


class Lead(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "leads"
    __table_args__ = (
        Index("ix_leads_status", "status"),
        Index("ix_leads_qualification", "qualification_level"),
        Index("ix_leads_urgency", "urgency"),
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(32), default=LeadStatus.NEW.value, nullable=False
    )
    intent: Mapped[str] = mapped_column(
        String(32), default=Intent.UNKNOWN.value, nullable=False
    )
    property_type: Mapped[str] = mapped_column(
        String(32), default=PropertyType.UNKNOWN.value, nullable=False
    )
    location_text: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bedrooms: Mapped[Optional[int]] = mapped_column(nullable=True)
    budget_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    budget_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(8), default="NGN", nullable=False)
    timeframe: Mapped[str] = mapped_column(
        String(32), default=Timeframe.UNKNOWN.value, nullable=False
    )
    qualification_level: Mapped[str] = mapped_column(
        String(16), default=QualificationLevel.UNKNOWN.value, nullable=False
    )
    qualification_score: Mapped[Optional[int]] = mapped_column(nullable=True)
    urgency: Mapped[str] = mapped_column(
        String(16), default=Urgency.UNKNOWN.value, nullable=False
    )
    qualification_version: Mapped[str] = mapped_column(
        String(32), default="v1", nullable=False
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    customer: Mapped[Customer] = relationship(back_populates="leads")
    conversations: Mapped[list[Conversation]] = relationship(back_populates="lead")
    activities: Mapped[list[LeadActivity]] = relationship(back_populates="lead")
    follow_ups: Mapped[list[FollowUp]] = relationship(back_populates="lead")
    notifications: Mapped[list[Notification]] = relationship(back_populates="lead")


class Conversation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "conversations"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True
    )
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("leads.id"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(
        String(32), default=ConversationStatus.ACTIVE.value, nullable=False
    )
    channel: Mapped[str] = mapped_column(String(32), default="web", nullable=False)

    customer: Mapped[Customer] = relationship(back_populates="conversations")
    lead: Mapped[Optional[Lead]] = relationship(back_populates="conversations")
    messages: Mapped[list[Message]] = relationship(
        back_populates="conversation", order_by="Message.created_at"
    )


class Message(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "messages"
    __table_args__ = (
        UniqueConstraint("external_message_id", name="uq_messages_external_id"),
        Index("ix_messages_conversation_id", "conversation_id"),
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversations.id"), nullable=False
    )
    sender_type: Mapped[str] = mapped_column(String(32), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    external_message_id: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    meta: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    conversation: Mapped[Conversation] = relationship(back_populates="messages")


class LeadActivity(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "lead_activities"

    lead_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("leads.id"), nullable=False, index=True
    )
    activity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meta: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    lead: Mapped[Lead] = relationship(back_populates="activities")


class FollowUp(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "follow_ups"
    __table_args__ = (Index("ix_follow_ups_due_at", "due_at"),)

    lead_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("leads.id"), nullable=False, index=True
    )
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default=FollowUpStatus.PENDING.value, nullable=False
    )
    reason: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    assigned_to: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    lead: Mapped[Lead] = relationship(back_populates="follow_ups")


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(32), default=UserRole.SALES_AGENT.value, nullable=False
    )
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notifications"

    lead_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("leads.id"), nullable=False, index=True
    )
    channel: Mapped[str] = mapped_column(String(32), default="internal", nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), default=NotificationStatus.PENDING.value, nullable=False
    )

    lead: Mapped[Lead] = relationship(back_populates="notifications")
