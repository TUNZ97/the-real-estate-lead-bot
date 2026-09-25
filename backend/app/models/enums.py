"""Domain enumerations — aligned with DATABASE_DATA_MODEL_SPECIFICATION."""

import enum


class Intent(str, enum.Enum):
    BUY = "BUY"
    RENT = "RENT"
    SELL = "SELL"
    PROPERTY_ENQUIRY = "PROPERTY_ENQUIRY"
    GENERAL_ENQUIRY = "GENERAL_ENQUIRY"
    UNKNOWN = "UNKNOWN"


class PropertyType(str, enum.Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    DUPLEX = "DUPLEX"
    LAND = "LAND"
    OFFICE = "OFFICE"
    COMMERCIAL = "COMMERCIAL"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class Timeframe(str, enum.Enum):
    IMMEDIATE = "IMMEDIATE"
    WITHIN_1_MONTH = "WITHIN_1_MONTH"
    WITHIN_3_MONTHS = "WITHIN_3_MONTHS"
    OVER_3_MONTHS = "OVER_3_MONTHS"
    RESEARCHING = "RESEARCHING"
    UNKNOWN = "UNKNOWN"


class QualificationLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


class Urgency(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


class ConversationStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    WAITING_FOR_CUSTOMER = "WAITING_FOR_CUSTOMER"
    ESCALATED = "ESCALATED"
    CLOSED = "CLOSED"


class MessageSender(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    BOT = "BOT"
    SALES_AGENT = "SALES_AGENT"
    SYSTEM = "SYSTEM"


class FollowUpStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    OVERDUE = "OVERDUE"


class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    FOLLOW_UP = "FOLLOW_UP"
    PROPERTY_MATCHED = "PROPERTY_MATCHED"
    VIEWING_SCHEDULED = "VIEWING_SCHEDULED"
    NEGOTIATION = "NEGOTIATION"
    CONVERTED = "CONVERTED"
    LOST = "LOST"
    CLOSED = "CLOSED"
    NOT_INTERESTED = "NOT_INTERESTED"
    UNQUALIFIED = "UNQUALIFIED"


class UserRole(str, enum.Enum):
    SALES_AGENT = "SALES_AGENT"
    SALES_MANAGER = "SALES_MANAGER"
    ADMIN = "ADMIN"


class NotificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    FAILED = "FAILED"
