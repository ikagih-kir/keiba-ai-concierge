from datetime import datetime

from sqlalchemy.orm import Session

from app.models.scheduled_push_notification import ScheduledPushNotification
from app.schemas.scheduled_push_notification import ScheduledPushNotificationCreate


def create_scheduled_push(db: Session, data: ScheduledPushNotificationCreate):
    obj = ScheduledPushNotification(
        title=data.title,
        body=data.body,
        target_path=data.target_path,
        scheduled_at=data.scheduled_at,
        status="scheduled",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_scheduled_pushes(db: Session):
    return (
        db.query(ScheduledPushNotification)
        .order_by(ScheduledPushNotification.scheduled_at.desc())
        .all()
    )


def get_scheduled_push(db: Session, item_id: int):
    return (
        db.query(ScheduledPushNotification)
        .filter(ScheduledPushNotification.id == item_id)
        .first()
    )


def cancel_scheduled_push(db: Session, item_id: int):
    obj = get_scheduled_push(db, item_id)
    if not obj:
        return None

    if obj.status != "scheduled":
        return obj

    obj.status = "canceled"
    obj.canceled_at = datetime.now()

    db.commit()
    db.refresh(obj)
    return obj


def list_due_scheduled_pushes(db: Session, now: datetime):
    return (
        db.query(ScheduledPushNotification)
        .filter(ScheduledPushNotification.status == "scheduled")
        .filter(ScheduledPushNotification.scheduled_at <= now)
        .order_by(ScheduledPushNotification.scheduled_at.asc())
        .all()
    )