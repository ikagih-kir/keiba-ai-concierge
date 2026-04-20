from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.models.chat_message import ChatMessage

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/send")
def send_chat_message(
    message: str,
    db: Session = Depends(get_db),
):
    chat = ChatMessage(
        sender="user",
        message=message,
    )
    db.add(chat)
    db.commit()

    return {"success": True}
