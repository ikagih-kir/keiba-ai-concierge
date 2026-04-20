from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.chat_faq import ChatFaqCreate, ChatFaqUpdate, ChatFaqOut
from app.services import chat_faq_service

router = APIRouter(
    prefix="/chat-faqs",
    tags=["Admin Chat FAQs"],
)


@router.get("", response_model=List[ChatFaqOut])
def list_faqs(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return chat_faq_service.list_chat_faqs(db)


@router.get("/{faq_id}", response_model=ChatFaqOut)
def get_faq(
    faq_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return chat_faq_service.get_chat_faq(db, faq_id)


@router.post("", response_model=ChatFaqOut)
def create_faq(
    data: ChatFaqCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return chat_faq_service.create_chat_faq(db, data)


@router.put("/{faq_id}", response_model=ChatFaqOut)
def update_faq(
    faq_id: int,
    data: ChatFaqUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return chat_faq_service.update_chat_faq(db, faq_id, data)


@router.delete("/{faq_id}")
def delete_faq(
    faq_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return chat_faq_service.delete_chat_faq(db, faq_id)