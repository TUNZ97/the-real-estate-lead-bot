"""n8n integration client.

n8n orchestrates; backend owns domain rules and DB.
Failures are logged and do not break the customer response path.
"""

from __future__ import annotations

import logging
from typing import Any, Optional
from uuid import UUID

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class N8nClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def enabled(self) -> bool:
        return bool(self.settings.n8n_webhook_url)

    async def trigger_lead_intake(
        self,
        *,
        conversation_id: UUID,
        message_id: UUID,
        lead_id: Optional[UUID],
        message: str,
        correlation_id: Optional[str] = None,
    ) -> None:
        if not self.enabled:
            logger.debug("n8n webhook not configured; skipping intake trigger")
            return

        payload: dict[str, Any] = {
            "event": "lead.intake",
            "conversation_id": str(conversation_id),
            "message_id": str(message_id),
            "lead_id": str(lead_id) if lead_id else None,
            "message": message,
            "correlation_id": correlation_id,
        }
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Secret": self.settings.n8n_webhook_secret,
        }
        url = f"{self.settings.n8n_webhook_url.rstrip('/')}/lead-intake"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code >= 400:
                    logger.warning(
                        "n8n intake webhook returned %s: %s",
                        resp.status_code,
                        resp.text[:300],
                    )
                else:
                    logger.info("n8n lead-intake triggered for message %s", message_id)
        except Exception as exc:  # noqa: BLE001 — never fail customer path
            logger.warning("n8n intake webhook failed: %s", exc)


n8n_client = N8nClient()
