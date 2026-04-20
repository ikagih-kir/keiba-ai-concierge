from sqlalchemy.orm import Session

from app.models.chat_faq import ChatFaq
from app.schemas.chat_faq import ChatFaqCreate, ChatFaqUpdate


def list_chat_faqs(db: Session):
    return (
        db.query(ChatFaq)
        .order_by(ChatFaq.priority.desc(), ChatFaq.id.desc())
        .all()
    )


def get_chat_faq(db: Session, faq_id: int):
    return db.query(ChatFaq).filter(ChatFaq.id == faq_id).first()


def find_active_faq_by_normalized_question(db: Session, normalized_question: str):
    return (
        db.query(ChatFaq)
        .filter(
            ChatFaq.is_active == True,
            ChatFaq.normalized_question == normalized_question,
        )
        .order_by(ChatFaq.priority.desc(), ChatFaq.id.desc())
        .first()
    )


def create_chat_faq(db: Session, data: ChatFaqCreate):
    item = ChatFaq(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_chat_faq(db: Session, item: ChatFaq, data: ChatFaqUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete_chat_faq(db: Session, item: ChatFaq):
    db.delete(item)
    db.commit()