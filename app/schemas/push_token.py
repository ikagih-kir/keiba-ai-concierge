from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PushTokenCreate(BaseModel):
    device_id: Optional[str] = None
    fcm_token: str
    platform: Optional[str] = None
    app_version: Optional[str] = None


class PushTokenOut(BaseModel):
    id: int
    device_id: Optional[str] = None
    fcm_token: str
    platform: Optional[str] = None
    app_version: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)