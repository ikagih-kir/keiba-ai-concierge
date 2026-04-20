from sqlalchemy.orm import Session

from app.models.chat_thread import ChatThread


def create_thread(db: Session, user_id: int | None = None, title: str | None = None):
    item = ChatThread(
        user_id=user_id,
        title=title,
        message_count=0,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_thread(db: Session, thread_id: int):
    return db.query(ChatThread).filter(ChatThread.id == thread_id).first()


def update_thread_after_user_message(db: Session, item: ChatThread, last_user_message: str):
    item.last_user_message = last_user_message[:1000]
    item.message_count = (item.message_count or 0) + 1
    db.commit()
    db.refresh(item)
    return item