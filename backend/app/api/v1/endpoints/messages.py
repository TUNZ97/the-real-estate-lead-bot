"""Message intake endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.messages import MessageCreate, MessageIntakeResponse
from app.services.message_service import MessageService

router = APIRouter()


@router.post("", response_model=MessageIntakeResponse)
async def create_message(
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db),
) -> MessageIntakeResponse:
    service = MessageService(db)
    try:
        return await service.intake(payload)
    except Exception as exc:  # surface cleanly; full stack in logs
        raise HTTPException(status_code=500, detail=str(exc)) from exc
