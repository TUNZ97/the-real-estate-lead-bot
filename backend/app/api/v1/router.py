"""API v1 router — mount domain routers here in Phase 3."""

from fastapi import APIRouter

api_router = APIRouter()

# Phase 3+:
# from app.api.v1.endpoints import messages, leads, conversations, follow_ups, notifications
# api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
# api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
# ...
