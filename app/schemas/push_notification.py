from typing import Literal, Optional

from pydantic import BaseModel, Field


class PushNotificationSendIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    body: str = Field(..., min_length=1, max_length=255)
    target_path: Optional[str] = None

    # まずは全員配信のみ
    target: Literal["all"] = "all"


class PushNotificationSendOut(BaseModel):
    success_count: int
    failure_count: int
    total_count: int