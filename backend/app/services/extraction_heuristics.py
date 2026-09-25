"""Lightweight rule-based extraction for local MVP testing.

When AI/n8n is not available, this provides grounded partial extraction
so the vertical slice still works. AI path (n8n) can refine later.
Never invents listings or prices beyond what the customer stated.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from app.models.enums import Intent, PropertyType, Timeframe


@dataclass
class ExtractedFields:
    intent: str = Intent.UNKNOWN.value
    property_type: str = PropertyType.UNKNOWN.value
    location_text: Optional[str] = None
    bedrooms: Optional[int] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    currency: str = "NGN"
    timeframe: str = Timeframe.UNKNOWN.value
    missing_hint: list[str] = field(default_factory=list)


_LOCATION_HINTS = [
    "lekki",
    "ikoyi",
    "victoria island",
    "vi",
    "ikeja",
    "yaba",
    "surulere",
    "ajah",
    "ibadan",
    "abuja",
    "gbagada",
    "maryland",
    "magodo",
    "banana island",
    "oniru",
    "sangotedo",
]


def _detect_intent(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ("rent", "rental", "lease", "to let")):
        return Intent.RENT.value
    if any(w in t for w in ("sell", "selling", "list my")):
        return Intent.SELL.value
    if any(w in t for w in ("buy", "purchase", "looking for", "need a", "want a")):
        return Intent.BUY.value
    if any(w in t for w in ("apartment", "house", "land", "duplex", "office")):
        return Intent.PROPERTY_ENQUIRY.value
    return Intent.UNKNOWN.value


def _detect_property(text: str) -> str:
    t = text.lower()
    if "apartment" in t or "flat" in t:
        return PropertyType.APARTMENT.value
    if "duplex" in t:
        return PropertyType.DUPLEX.value
    if "land" in t or "plot" in t:
        return PropertyType.LAND.value
    if "office" in t:
        return PropertyType.OFFICE.value
    if "commercial" in t:
        return PropertyType.COMMERCIAL.value
    if "house" in t or "home" in t or "bungalow" in t:
        return PropertyType.HOUSE.value
    return PropertyType.UNKNOWN.value


def _detect_bedrooms(text: str) -> Optional[int]:
    m = re.search(r"(\d+)\s*[- ]?\s*(?:bed|bedroom|br)\b", text.lower())
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d+)\s*bedroom", text.lower())
    if m:
        return int(m.group(1))
    return None


def _detect_location(text: str) -> Optional[str]:
    t = text.lower()
    for loc in _LOCATION_HINTS:
        if loc in t:
            return loc.title() if loc != "vi" else "Victoria Island"
    m = re.search(
        r"(?:in|around|at|near)\s+([A-Za-z][A-Za-z\s]{1,30}?)(?:[.,]|\s+with|\s+my|\s+budget|\s*$)",
        text,
        re.I,
    )
    if m:
        return m.group(1).strip().title()
    return None


def _parse_money_token(raw: str) -> Optional[Decimal]:
    s = raw.lower().replace(",", "").replace("₦", "").replace("n", "").strip()
    mult = Decimal(1)
    if s.endswith("m") or "million" in s:
        mult = Decimal(1_000_000)
        s = s.replace("million", "").rstrip("m").strip()
    elif s.endswith("k"):
        mult = Decimal(1_000)
        s = s.rstrip("k").strip()
    try:
        return Decimal(s) * mult
    except Exception:
        return None


def _detect_budget(text: str) -> tuple[Optional[Decimal], Optional[Decimal]]:
    t = text.lower()
    # range: between X and Y / X - Y
    m = re.search(
        r"(?:between|from)\s*(₦?\s*[\d.,]+\s*(?:m|million|k)?)\s*(?:and|to|-)\s*"
        r"(₦?\s*[\d.,]+\s*(?:m|million|k)?)",
        t,
    )
    if m:
        a, b = _parse_money_token(m.group(1)), _parse_money_token(m.group(2))
        if a and b:
            return (min(a, b), max(a, b))

    m = re.search(
        r"(?:below|under|up to|max(?:imum)?)\s*(₦?\s*[\d.,]+\s*(?:m|million|k)?)",
        t,
    )
    if m:
        v = _parse_money_token(m.group(1))
        if v:
            return (None, v)

    m = re.search(
        r"(?:around|about|budget(?:\s+of|\s+is)?)\s*(₦?\s*[\d.,]+\s*(?:m|million|k)?)",
        t,
    )
    if m:
        v = _parse_money_token(m.group(1))
        if v:
            return (v * Decimal("0.9"), v * Decimal("1.1"))

    m = re.search(r"(₦\s*[\d.,]+\s*(?:m|million|k)?|[\d.,]+\s*(?:m|million)\b)", t)
    if m:
        v = _parse_money_token(m.group(1))
        if v:
            return (None, v)

    return (None, None)


def _detect_timeframe(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ("asap", "immediately", "urgent", "right away")):
        return Timeframe.IMMEDIATE.value
    if "this month" in t or "within a month" in t or "1 month" in t:
        return Timeframe.WITHIN_1_MONTH.value
    if "3 month" in t or "three month" in t:
        return Timeframe.WITHIN_3_MONTHS.value
    if "research" in t or "just looking" in t:
        return Timeframe.RESEARCHING.value
    return Timeframe.UNKNOWN.value


def extract_from_text(message: str) -> ExtractedFields:
    intent = _detect_intent(message)
    property_type = _detect_property(message)
    bedrooms = _detect_bedrooms(message)
    location = _detect_location(message)
    budget_min, budget_max = _detect_budget(message)
    timeframe = _detect_timeframe(message)

    return ExtractedFields(
        intent=intent,
        property_type=property_type,
        location_text=location,
        bedrooms=bedrooms,
        budget_min=budget_min,
        budget_max=budget_max,
        timeframe=timeframe,
    )
