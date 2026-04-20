from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import assistant_message_repository
from app.schemas.assistant_message import (
    AssistantMessageCreate,
    AssistantMessageUpdate,
)


def list_assistant_messages(db: Session):
    return assistant_message_repository.list_assistant_messages(db)


def list_public_assistant_messages(
    db: Session,
    target_date: date | None = None,
    target_segment: str | None = None,
):
    return assistant_message_repository.list_public_assistant_messages(
        db,
        target_date=target_date,
        target_segment=target_segment,
    )


def get_assistant_message(db: Session, item_id: int):
    item = assistant_message_repository.get_assistant_message_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="秘書メッセージが見つかりません")
    return item


def get_public_assistant_message(db: Session, item_id: int):
    item = assistant_message_repository.get_public_assistant_message_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="秘書メッセージが見つかりません")
    return item


def create_assistant_message(db: Session, data: AssistantMessageCreate):
    return assistant_message_repository.create_assistant_message(db, data)


def update_assistant_message(
    db: Session,
    item_id: int,
    data: AssistantMessageUpdate,
):
    item = assistant_message_repository.get_assistant_message_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="秘書メッセージが見つかりません")

    return assistant_message_repository.update_assistant_message(db, item, data)


def delete_assistant_message(db: Session, item_id: int):
    item = assistant_message_repository.get_assistant_message_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="秘書メッセージが見つかりません")

    assistant_message_repository.delete_assistant_message(db, item)
    return {"message": "秘書メッセージを削除しました"}


def toggle_assistant_message_public(db: Session, item_id: int, is_public: bool):
    item = assistant_message_repository.get_assistant_message_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="秘書メッセージが見つかりません")

    return assistant_message_repository.toggle_assistant_message_public(
        db,
        item,
        is_public,
    )