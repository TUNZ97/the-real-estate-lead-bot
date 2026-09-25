"""Deterministic lead qualification — LEAD_QUALIFICATION_SPECIFICATION.

AI does NOT own this score. Only validated fields affect scoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from app.models.enums import (
    Intent,
    PropertyType,
    QualificationLevel,
    Timeframe,
    Urgency,
)

QUALIFICATION_VERSION = "v1"


@dataclass
class QualificationResult:
    score: int
    level: str
    urgency: str
    missing_information: list[str]
    version: str = QUALIFICATION_VERSION


def _intent_points(intent: str) -> int:
    if intent in {Intent.BUY.value, Intent.RENT.value, Intent.SELL.value}:
        return 20
    if intent == Intent.PROPERTY_ENQUIRY.value:
        return 12
    if intent == Intent.GENERAL_ENQUIRY.value:
        return 6
    return 0


def _budget_points(
    budget_min: Optional[Decimal], budget_max: Optional[Decimal]
) -> int:
    if budget_min is not None or budget_max is not None:
        return 20
    return 0


def _timeframe_points(timeframe: str) -> int:
    mapping = {
        Timeframe.IMMEDIATE.value: 20,
        Timeframe.WITHIN_1_MONTH.value: 18,
        Timeframe.WITHIN_3_MONTHS.value: 14,
        Timeframe.OVER_3_MONTHS.value: 8,
        Timeframe.RESEARCHING.value: 6,
    }
    return mapping.get(timeframe, 0)


def _location_points(location: Optional[str]) -> int:
    if location and location.strip():
        return 15
    return 0


def _property_points(property_type: str, bedrooms: Optional[int]) -> int:
    points = 0
    if property_type and property_type != PropertyType.UNKNOWN.value:
        points += 6
    if bedrooms is not None and bedrooms > 0:
        points += 4
    return points


def _contact_points(
    name: Optional[str], email: Optional[str], phone: Optional[str]
) -> int:
    if email or phone:
        return 10
    if name:
        return 4
    return 0


def _urgency_from_timeframe(timeframe: str) -> str:
    if timeframe in {Timeframe.IMMEDIATE.value, Timeframe.WITHIN_1_MONTH.value}:
        return Urgency.HIGH.value
    if timeframe == Timeframe.WITHIN_3_MONTHS.value:
        return Urgency.MEDIUM.value
    if timeframe in {Timeframe.OVER_3_MONTHS.value, Timeframe.RESEARCHING.value}:
        return Urgency.LOW.value
    return Urgency.UNKNOWN.value


def _level_from_score(score: int) -> str:
    if score >= 70:
        return QualificationLevel.HIGH.value
    if score >= 40:
        return QualificationLevel.MEDIUM.value
    if score > 0:
        return QualificationLevel.LOW.value
    return QualificationLevel.UNKNOWN.value


def _missing(
    intent: str,
    location: Optional[str],
    property_type: str,
    bedrooms: Optional[int],
    budget_min: Optional[Decimal],
    budget_max: Optional[Decimal],
    timeframe: str,
    email: Optional[str],
    phone: Optional[str],
) -> list[str]:
    missing: list[str] = []
    if intent in {Intent.UNKNOWN.value, Intent.GENERAL_ENQUIRY.value}:
        missing.append("intent")
    if not location:
        missing.append("location")
    if property_type == PropertyType.UNKNOWN.value:
        missing.append("property_type")
    if bedrooms is None and property_type not in {
        PropertyType.LAND.value,
        PropertyType.UNKNOWN.value,
    }:
        missing.append("bedrooms")
    if budget_min is None and budget_max is None:
        missing.append("budget")
    if timeframe == Timeframe.UNKNOWN.value:
        missing.append("timeframe")
    if not email and not phone:
        missing.append("contact")
    return missing


def qualify_lead(
    *,
    intent: str = Intent.UNKNOWN.value,
    property_type: str = PropertyType.UNKNOWN.value,
    location_text: Optional[str] = None,
    bedrooms: Optional[int] = None,
    budget_min: Optional[Decimal] = None,
    budget_max: Optional[Decimal] = None,
    timeframe: str = Timeframe.UNKNOWN.value,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
    customer_phone: Optional[str] = None,
    engagement_bonus: int = 5,
) -> QualificationResult:
    score = 0
    score += _intent_points(intent)
    score += _budget_points(budget_min, budget_max)
    score += _timeframe_points(timeframe)
    score += _location_points(location_text)
    score += _property_points(property_type, bedrooms)
    score += _contact_points(customer_name, customer_email, customer_phone)
    score += max(0, min(5, engagement_bonus))
    score = max(0, min(100, score))

    return QualificationResult(
        score=score,
        level=_level_from_score(score),
        urgency=_urgency_from_timeframe(timeframe),
        missing_information=_missing(
            intent,
            location_text,
            property_type,
            bedrooms,
            budget_min,
            budget_max,
            timeframe,
            customer_email,
            customer_phone,
        ),
    )
