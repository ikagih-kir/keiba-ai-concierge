from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.scheduled_push_notification import RunDuePushNotificationsOut
from app.services import scheduled_push_notification_service

router = APIRouter(
    prefix="/internal/push-notifications",
    tags=["Internal Push Notifications"],
)


@router.post("/run-due", response_model=RunDuePushNotificationsOut)
def run_due_push_notifications(
    db: Session = Depends(get_db),
):
    return scheduled_push_notification_service.run_due_scheduled_pushes(db)