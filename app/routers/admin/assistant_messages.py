from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.assistant_message import (
    AssistantMessageCreate,
    AssistantMessageOut,
    AssistantMessagePublicToggle,
    AssistantMessageUpdate,
)
from app.services import assistant_message_service

router = APIRouter(
    prefix="/assistant-messages",
    tags=["Admin Assistant Messages"],
)


@router.get("", response_model=List[AssistantMessageOut])
def list_assistant_messages(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return assistant_message_service.list_assistant_messages(db)


@router.get("/{item_id}", response_model=AssistantMessageOut)
def get_assistant_message(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return assistant_message_service.get_assistant_message(db, item_id)


@router.post("", response_model=AssistantMessageOut)
def create_assistant_message(
    data: AssistantMessageCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return assistant_message_service.create_assistant_message(db, data)


@router.put("/{item_id}", response_model=AssistantMessageOut)
def update_assistant_message(
    item_id: int,
    data: AssistantMessageUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return assistant_message_service.update_assistant_message(db, item_id, data)


@router.delete("/{item_id}")
def delete_assistant_message(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return assistant_message_service.delete_assistant_message(db, item_id)


@router.post("/{item_id}/toggle_public", response_model=AssistantMessageOut)
def toggle_assistant_message_public(
    item_id: int,
    data: AssistantMessagePublicToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return assistant_message_service.toggle_assistant_message_public(
        db,
        item_id,
        data.is_public,
    )