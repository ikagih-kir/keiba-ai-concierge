from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.chat_message import ChatMessage
from app.core.auth import get_current_admin

router = APIRouter(prefix="/chat", tags=["Admin Chat"])

class ChatReplyRequest(BaseModel):
    message: str
    user_id: int | None = None  # 会員ID（将来拡張）

@router.post("/reply")
def reply_chat(
    req: ChatReplyRequest,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    chat = ChatMessage(
        user_id=req.user_id,
        sender="admin",
        message=req.message,
    )
    db.add(chat)
    db.commit()

    return {"success": True}
