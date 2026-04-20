from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.chat_message import ChatMessage
from app.core.deps import get_current_admin

router = APIRouter(
    prefix="/chat-logs",
    tags=["Admin ChatLogs"],
)

@router.get("", response_model=list[dict])
def list_chat_logs(
    limit: int = 100,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    logs = (
        db.query(ChatMessage)
        .order_by(ChatMessage.id.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": log.id,
            "sender": log.sender,
            "message": log.message,
            "created_at": log.created_at,
        }
        for log in logs
    ]


@router.get("/{chat_id}")
def get_chat_log(
    chat_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    log = db.get(ChatMessage, chat_id)
    if not log:
        raise HTTPException(status_code=404, detail="Chat log not found")

    return {
        "id": log.id,
        "sender": log.sender,
        "message": log.message,
        "created_at": log.created_at,
    }


@router.delete("/{chat_id}")
def delete_chat_log(
    chat_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    log = db.get(ChatMessage, chat_id)
    if not log:
        raise HTTPException(status_code=404, detail="Chat log not found")

    db.delete(log)
    db.commit()
    return {"success": True}
