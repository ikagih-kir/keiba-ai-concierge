from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class FrameTrendSnapshotBase(BaseModel):
    target_date: date = Field(..., description="表示対象日")

    title: str = Field(..., max_length=255, description="タイトル")
    race_scope: Optional[str] = Field(None, max_length=100, description="集計対象範囲")

    lucky_frame: Optional[int] = Field(None, ge=1, le=8, description="ラッキー枠")
    trend_summary: Optional[str] = Field(None, max_length=255, description="傾向要約")
    trend_note: Optional[str] = Field(None, description="補足文")
    recommended_style: Optional[str] = Field(None, max_length=20, description="おすすめスタイル")

    sample_size: Optional[int] = Field(None, ge=0, description="サンプル数")
    win_frame_data: Optional[str] = Field(None, description="1着枠集計JSON文字列")
    place_frame_data: Optional[str] = Field(None, description="複勝圏枠集計JSON文字列")

    ai_comment: Optional[str] = Field(None, description="AIコメント")

    is_featured: bool = Field(default=False, description="注目表示")
    sort_order: int = Field(default=0, description="表示順")
    is_public: bool = Field(default=True, description="公開フラグ")


class FrameTrendSnapshotCreate(FrameTrendSnapshotBase):
    pass


class FrameTrendSnapshotUpdate(BaseModel):
    target_date: Optional[date] = None

    title: Optional[str] = Field(None, max_length=255)
    race_scope: Optional[str] = Field(None, max_length=100)

    lucky_frame: Optional[int] = Field(None, ge=1, le=8)
    trend_summary: Optional[str] = Field(None, max_length=255)
    trend_note: Optional[str] = None
    recommended_style: Optional[str] = Field(None, max_length=20)

    sample_size: Optional[int] = Field(None, ge=0)
    win_frame_data: Optional[str] = None
    place_frame_data: Optional[str] = None

    ai_comment: Optional[str] = None

    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None
    is_public: Optional[bool] = None


class FrameTrendSnapshotOut(FrameTrendSnapshotBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FrameTrendSnapshotPublicToggle(BaseModel):
    is_public: bool