from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import chat_faq_repository
from app.schemas.chat_faq import ChatFaqCreate, ChatFaqUpdate


def list_chat_faqs(db: Session):
    return chat_faq_repository.list_chat_faqs(db)


def get_chat_faq(db: Session, faq_id: int):
    item = chat_faq_repository.get_chat_faq(db, faq_id)
    if not item:
        raise HTTPException(status_code=404, detail="FAQが見つかりません")
    return item


def create_chat_faq(db: Session, data: ChatFaqCreate):
    return chat_faq_repository.create_chat_faq(db, data)


def update_chat_faq(db: Session, faq_id: int, data: ChatFaqUpdate):
    item = chat_faq_repository.get_chat_faq(db, faq_id)
    if not item:
        raise HTTPException(status_code=404, detail="FAQが見つかりません")
    return chat_faq_repository.update_chat_faq(db, item, data)


def delete_chat_faq(db: Session, faq_id: int):
    item = chat_faq_repository.get_chat_faq(db, faq_id)
    if not item:
        raise HTTPException(status_code=404, detail="FAQが見つかりません")
    chat_faq_repository.delete_chat_faq(db, item)
    return {"message": "FAQを削除しました"}