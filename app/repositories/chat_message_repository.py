from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


def create_message(
    db: Session,
    thread_id: int,
    role: str,
    content: str,
    intent: str | None = None,
    normalized_question: str | None = None,
    answered_by: str | None = None,
    source_summary: str | None = None,
    suggested_actions_json: str | None = None,
    model_name: str | None = None,
    response_ms: int | None = None,
    user_id: int | None = None,
):
    item = ChatMessage(
        thread_id=thread_id,
        role=role,
        content=content,
        intent=intent,
        normalized_question=normalized_question,
        answered_by=answered_by,
        source_summary=source_summary,
        suggested_actions_json=suggested_actions_json,
        model_name=model_name,
        response_ms=response_ms,
        user_id=user_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_messages_by_thread(db: Session, thread_id: int):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.thread_id == thread_id)
        .order_by(ChatMessage.id.asc())
        .all()
    )