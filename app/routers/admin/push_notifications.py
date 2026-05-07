from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.push_notification import (
    PushNotificationSendIn,
    PushNotificationSendOut,
)
from app.services import push_notification_service
from typing import List
from fastapi import HTTPException
from app.schemas.scheduled_push_notification import (
    ScheduledPushNotificationCreate,
    ScheduledPushNotificationOut,
)
from app.services import scheduled_push_notification_service



router = APIRouter(
    prefix="/push-notifications",
    tags=["Admin Push Notifications"],
)


@router.post("/send", response_model=PushNotificationSendOut)
def send_push_notification(
    data: PushNotificationSendIn,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return push_notification_service.send_push_notification(
        db,
        title=data.title,
        body=data.body,
        target_path=data.target_path,
    )

@router.get("/scheduled", response_model=List[ScheduledPushNotificationOut])
def list_scheduled_push_notifications(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return scheduled_push_notification_service.list_scheduled_pushes(db)


@router.post("/scheduled", response_model=ScheduledPushNotificationOut)
def create_scheduled_push_notification(
    data: ScheduledPushNotificationCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return scheduled_push_notification_service.create_scheduled_push(db, data)


@router.post("/scheduled/{item_id}/cancel", response_model=ScheduledPushNotificationOut)
def cancel_scheduled_push_notification(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    item = scheduled_push_notification_service.cancel_scheduled_push(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Scheduled push not found")
    return item