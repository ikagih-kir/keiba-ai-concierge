from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ScheduledPushNotificationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    body: str = Field(..., min_length=1, max_length=255)
    target_path: Optional[str] = None
    scheduled_at: datetime


class ScheduledPushNotificationOut(BaseModel):
    id: int
    title: str
    body: str
    target_path: Optional[str] = None
    status: str
    scheduled_at: datetime
    sent_at: Optional[datetime] = None
    canceled_at: Optional[datetime] = None
    success_count: int
    failure_count: int
    total_count: int
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RunDuePushNotificationsOut(BaseModel):
    processed_count: int