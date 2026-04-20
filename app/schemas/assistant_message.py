from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class AssistantMessageBase(BaseModel):
    target_date: date = Field(..., description="表示対象日")

    title: str = Field(..., max_length=255, description="タイトル")
    message: str = Field(..., description="本文")

    message_type: Optional[str] = Field(None, max_length=50, description="メッセージ種別")
    priority: int = Field(default=0, description="優先度")
    sort_order: int = Field(default=0, description="表示順")

    is_featured: bool = Field(default=False, description="注目表示")
    is_public: bool = Field(default=True, description="公開フラグ")

    action_type: Optional[str] = Field(None, max_length=20, description="導線種別")
    action_label: Optional[str] = Field(None, max_length=100, description="導線ボタン文言")
    action_path: Optional[str] = Field(None, max_length=255, description="導線パス")

    target_segment: Optional[str] = Field(None, max_length=50, description="対象セグメント")
    related_content_type: Optional[str] = Field(None, max_length=50, description="関連コンテンツ種別")
    related_content_id: Optional[int] = Field(None, description="関連コンテンツID")

    note: Optional[str] = Field(None, description="管理メモ")


class AssistantMessageCreate(AssistantMessageBase):
    pass


class AssistantMessageUpdate(BaseModel):
    target_date: Optional[date] = None

    title: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = None

    message_type: Optional[str] = Field(None, max_length=50)
    priority: Optional[int] = None
    sort_order: Optional[int] = None

    is_featured: Optional[bool] = None
    is_public: Optional[bool] = None

    action_type: Optional[str] = Field(None, max_length=20)
    action_label: Optional[str] = Field(None, max_length=100)
    action_path: Optional[str] = Field(None, max_length=255)

    target_segment: Optional[str] = Field(None, max_length=50)
    related_content_type: Optional[str] = Field(None, max_length=50)
    related_content_id: Optional[int] = None

    note: Optional[str] = None


class AssistantMessageOut(AssistantMessageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssistantMessagePublicToggle(BaseModel):
    is_public: bool