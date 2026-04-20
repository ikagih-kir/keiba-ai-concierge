from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.chat_question_log import ChatQuestionLogOut
from app.services import chat_question_log_service

router = APIRouter(
    prefix="/chat-question-logs",
    tags=["Admin Chat Question Logs"],
)


@router.get("", response_model=List[ChatQuestionLogOut])
def list_logs(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return chat_question_log_service.list_chat_question_logs(db)


@router.get("/{log_id}", response_model=ChatQuestionLogOut)
def get_log(
    log_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return chat_question_log_service.get_chat_question_log(db, log_id)