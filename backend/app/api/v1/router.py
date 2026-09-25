"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import conversations, leads, messages

api_router = APIRouter()

api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(
    conversations.router, prefix="/conversations", tags=["conversations"]
)
