from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class RaceChangeHighlightBase(BaseModel):
    target_date: date = Field(..., description="表示対象日")

    race_name: str = Field(..., max_length=255, description="レース名")
    race_course: Optional[str] = Field(None, max_length=100, description="開催/レース情報")
    horse_name: str = Field(..., max_length=255, description="馬名")

    previous_surface: Optional[str] = Field(None, max_length=20, description="前走馬場種別")
    current_surface: Optional[str] = Field(None, max_length=20, description="今回馬場種別")

    previous_distance: Optional[int] = Field(None, ge=0, description="前走距離")
    current_distance: Optional[int] = Field(None, ge=0, description="今回距離")

    previous_jockey: Optional[str] = Field(None, max_length=100, description="前走騎手")
    current_jockey: Optional[str] = Field(None, max_length=100, description="今回騎手")

    surface_changed: bool = Field(default=False, description="芝ダート変更")
    distance_changed: bool = Field(default=False, description="距離変更")
    distance_direction: Optional[str] = Field(None, max_length=20, description="距離変化方向")
    gear_changed: bool = Field(default=False, description="馬具変更")
    jockey_changed: bool = Field(default=False, description="騎手変更")
    class_changed: bool = Field(default=False, description="クラス変更")

    change_summary: Optional[str] = Field(None, max_length=255, description="変化要約")
    ai_comment: Optional[str] = Field(None, description="AIコメント")
    note: Optional[str] = Field(None, description="補足メモ")

    impact_level: Optional[str] = Field(None, max_length=20, description="注目度")
    is_featured: bool = Field(default=False, description="注目表示")
    sort_order: int = Field(default=0, description="表示順")
    is_public: bool = Field(default=True, description="公開フラグ")


class RaceChangeHighlightCreate(RaceChangeHighlightBase):
    pass


class RaceChangeHighlightUpdate(BaseModel):
    target_date: Optional[date] = None

    race_name: Optional[str] = Field(None, max_length=255)
    race_course: Optional[str] = Field(None, max_length=100)
    horse_name: Optional[str] = Field(None, max_length=255)

    previous_surface: Optional[str] = Field(None, max_length=20)
    current_surface: Optional[str] = Field(None, max_length=20)

    previous_distance: Optional[int] = Field(None, ge=0)
    current_distance: Optional[int] = Field(None, ge=0)

    previous_jockey: Optional[str] = Field(None, max_length=100)
    current_jockey: Optional[str] = Field(None, max_length=100)

    surface_changed: Optional[bool] = None
    distance_changed: Optional[bool] = None
    distance_direction: Optional[str] = Field(None, max_length=20)
    gear_changed: Optional[bool] = None
    jockey_changed: Optional[bool] = None
    class_changed: Optional[bool] = None

    change_summary: Optional[str] = Field(None, max_length=255)
    ai_comment: Optional[str] = None
    note: Optional[str] = None

    impact_level: Optional[str] = Field(None, max_length=20)
    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None
    is_public: Optional[bool] = None


class RaceChangeHighlightOut(RaceChangeHighlightBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RaceChangeHighlightPublicToggle(BaseModel):
    is_public: bool