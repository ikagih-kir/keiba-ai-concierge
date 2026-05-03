from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HomeDialogBase(BaseModel):
    title: str
    body: str
    primary_button_text: Optional[str] = None
    primary_button_path: Optional[str] = None
    secondary_button_text: Optional[str] = "閉じる"
    is_active: bool = True
    show_once_per_day: bool = True
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    sort_order: int = 0


class HomeDialogCreate(HomeDialogBase):
    pass


class HomeDialogUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    primary_button_text: Optional[str] = None
    primary_button_path: Optional[str] = None
    secondary_button_text: Optional[str] = None
    is_active: Optional[bool] = None
    show_once_per_day: Optional[bool] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    sort_order: Optional[int] = None


class HomeDialogOut(HomeDialogBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class HomeDialogPublicOut(BaseModel):
    id: int
    title: str
    body: str
    primary_button_text: Optional[str] = None
    primary_button_path: Optional[str] = None
    secondary_button_text: Optional[str] = None
    show_once_per_day: bool = True

    model_config = ConfigDict(from_attributes=True)


class HomeDialogToggle(BaseModel):
    is_active: bool