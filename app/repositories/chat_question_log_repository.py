from sqlalchemy.orm import Session

from app.models.chat_question_log import ChatQuestionLog


def create_question_log(
    db: Session,
    thread_id: int | None,
    message_id: int | None,
    user_id: int | None,
    raw_question: str,
    normalized_question: str | None,
    intent: str | None,
    sub_intent: str | None,
    answered_by: str | None,
    faq_id: int | None,
    is_answered_successfully: bool,
    needs_improvement: bool,
):
    item = ChatQuestionLog(
        thread_id=thread_id,
        message_id=message_id,
        user_id=user_id,
        raw_question=raw_question,
        normalized_question=normalized_question,
        intent=intent,
        sub_intent=sub_intent,
        answered_by=answered_by,
        faq_id=faq_id,
        is_answered_successfully=is_answered_successfully,
        needs_improvement=needs_improvement,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_chat_question_logs(db: Session):
    return (
        db.query(ChatQuestionLog)
        .order_by(ChatQuestionLog.id.desc())
        .all()
    )


def get_chat_question_log(db: Session, log_id: int):
    return (
        db.query(ChatQuestionLog)
        .filter(ChatQuestionLog.id == log_id)
        .first()
    )