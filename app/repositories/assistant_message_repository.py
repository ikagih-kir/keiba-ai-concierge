from datetime import date
from sqlalchemy.orm import Session

from app.models.assistant_message import AssistantMessage
from app.schemas.assistant_message import (
    AssistantMessageCreate,
    AssistantMessageUpdate,
)


def list_assistant_messages(db: Session):
    return (
        db.query(AssistantMessage)
        .order_by(
            AssistantMessage.target_date.desc(),
            AssistantMessage.priority.desc(),
            AssistantMessage.sort_order.asc(),
            AssistantMessage.id.desc(),
        )
        .all()
    )


def list_public_assistant_messages(
    db: Session,
    target_date: date | None = None,
    target_segment: str | None = None,
):
    query = db.query(AssistantMessage).filter(AssistantMessage.is_public == True)

    if target_date is not None:
        query = query.filter(AssistantMessage.target_date == target_date)

    if target_segment is not None:
        query = query.filter(
            (AssistantMessage.target_segment == target_segment)
            | (AssistantMessage.target_segment == None)
            | (AssistantMessage.target_segment == "all")
        )

    return (
        query.order_by(
            AssistantMessage.priority.desc(),
            AssistantMessage.sort_order.asc(),
            AssistantMessage.id.desc(),
        )
        .all()
    )


def get_assistant_message_by_id(db: Session, item_id: int):
    return (
        db.query(AssistantMessage)
        .filter(AssistantMessage.id == item_id)
        .first()
    )


def get_public_assistant_message_by_id(db: Session, item_id: int):
    return (
        db.query(AssistantMessage)
        .filter(
            AssistantMessage.id == item_id,
            AssistantMessage.is_public == True,
        )
        .first()
    )


def create_assistant_message(db: Session, data: AssistantMessageCreate):
    item = AssistantMessage(
        target_date=data.target_date,
        title=data.title,
        message=data.message,
        message_type=data.message_type,
        priority=data.priority,
        sort_order=data.sort_order,
        is_featured=data.is_featured,
        is_public=data.is_public,
        action_type=data.action_type,
        action_label=data.action_label,
        action_path=data.action_path,
        target_segment=data.target_segment,
        related_content_type=data.related_content_type,
        related_content_id=data.related_content_id,
        note=data.note,
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_assistant_message(
    db: Session,
    item: AssistantMessage,
    data: AssistantMessageUpdate,
):
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_assistant_message(db: Session, item: AssistantMessage):
    db.delete(item)
    db.commit()


def toggle_assistant_message_public(
    db: Session,
    item: AssistantMessage,
    is_public: bool,
):
    item.is_public = is_public
    db.commit()
    db.refresh(item)
    return item