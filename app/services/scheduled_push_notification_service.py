from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories import scheduled_push_notification_repository
from app.schemas.scheduled_push_notification import ScheduledPushNotificationCreate
from app.services import push_notification_service


def create_scheduled_push(db: Session, data: ScheduledPushNotificationCreate):
    return scheduled_push_notification_repository.create_scheduled_push(db, data)


def list_scheduled_pushes(db: Session):
    return scheduled_push_notification_repository.list_scheduled_pushes(db)


def cancel_scheduled_push(db: Session, item_id: int):
    return scheduled_push_notification_repository.cancel_scheduled_push(db, item_id)


def run_due_scheduled_pushes(db: Session):
    now = datetime.now()
    items = scheduled_push_notification_repository.list_due_scheduled_pushes(db, now)

    processed_count = 0

    for item in items:
        try:
            result = push_notification_service.send_push_notification(
                db,
                title=item.title,
                body=item.body,
                target_path=item.target_path,
            )

            item.status = "sent"
            item.sent_at = datetime.now()
            item.success_count = result["success_count"]
            item.failure_count = result["failure_count"]
            item.total_count = result["total_count"]
            item.error_message = None

        except Exception as e:
            item.status = "failed"
            item.error_message = str(e)

        processed_count += 1

    db.commit()

    return {"processed_count": processed_count}