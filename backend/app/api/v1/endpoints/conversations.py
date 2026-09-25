"""Conversation endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.conversations import ConversationOut
from app.schemas.messages import MessageOut
from app.services.message_service import MessageService

router = APIRouter()


@router.get("/{conversation_id}", response_model=ConversationOut)
async def get_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ConversationOut:
    conv = await MessageService(db).get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationOut(
        id=conv.id,
        customer_id=conv.customer_id,
        lead_id=conv.lead_id,
        status=conv.status,
        channel=conv.channel,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=[
            MessageOut(
                id=m.id,
                conversation_id=m.conversation_id,
                sender_type=m.sender_type,
                content=m.content,
                created_at=m.created_at,
            )
            for m in (conv.messages or [])
        ],
    )


@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
async def list_messages(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> list[MessageOut]:
    msgs = await MessageService(db).get_conversation_messages(conversation_id)
    return [
        MessageOut(
            id=m.id,
            conversation_id=m.conversation_id,
            sender_type=m.sender_type,
            content=m.content,
            created_at=m.created_at,
        )
        for m in msgs
    ]
