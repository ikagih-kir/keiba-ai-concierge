from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import chat_question_log_repository


def list_chat_question_logs(db: Session):
    return chat_question_log_repository.list_chat_question_logs(db)


def get_chat_question_log(db: Session, log_id: int):
    item = chat_question_log_repository.get_chat_question_log(db, log_id)
    if not item:
        raise HTTPException(status_code=404, detail="質問ログが見つかりません")
    return item