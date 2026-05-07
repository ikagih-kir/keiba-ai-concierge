from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.push_notification import (
    PushNotificationSendIn,
    PushNotificationSendOut,
)
from app.services import push_notification_service

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