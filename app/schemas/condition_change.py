from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class ConditionChangeHorseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    horse_name: str
    race_name: str
    race_date: date
    venue: str
    race_number: int

    prev_race_date: Optional[date] = None
    prev_race_name: Optional[str] = None
    prev_surface: Optional[str] = None
    prev_distance: Optional[int] = None
    prev_finish_position: Optional[int] = None

    current_surface: str
    current_distance: int

    distance_diff: int
    surface_changed: bool

    blinkers_first_time: bool
    blinkers_reapplied: bool
    blinkers_removed: bool

    layoff_days: Optional[int] = None

    change_flags: List[str] = Field(default_factory=list)
    change_score: int

    short_comment: Optional[str] = None
    ai_comment: Optional[str] = None

    is_featured: bool
    display_order: int

    created_at: datetime


class ConditionChangeHorseListResponse(BaseModel):
    items: List[ConditionChangeHorseResponse]


class RunBatchRequest(BaseModel):
    target_date: date


class UpdateConditionChangeRequest(BaseModel):
    is_featured: Optional[bool] = None
    display_order: Optional[int] = None
    short_comment: Optional[str] = None
    ai_comment: Optional[str] = None