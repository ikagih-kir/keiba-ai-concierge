from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assistant_chat import (
    ChatSendRequest,
    ChatSendResponse,
    ChatThreadCreateResponse,
    ChatThreadDetailResponse,
)
from app.services import assistant_chat_service

router = APIRouter(
    prefix="/v1/assistant",
    tags=["Public Assistant Chat"],
)


@router.post("/threads", response_model=ChatThreadCreateResponse)
def create_thread(
    user_id: int | None = None,
    db: Session = Depends(get_db),
):
    thread = assistant_chat_service.create_thread(db, user_id=user_id)
    return {"thread_id": thread.id}


@router.get("/threads/{thread_id}", response_model=ChatThreadDetailResponse)
def get_thread_detail(
    thread_id: int,
    db: Session = Depends(get_db),
):
    result = assistant_chat_service.get_thread_detail(db, thread_id)
    if not result:
        raise HTTPException(status_code=404, detail="スレッドが見つかりません")
    return result


@router.post("/chat", response_model=ChatSendResponse)
def send_chat(
    data: ChatSendRequest,
    db: Session = Depends(get_db),
):
    return assistant_chat_service.send_chat_message(
        db=db,
        thread_id=data.thread_id,
        message=data.message,
        user_id=data.user_id,
    )