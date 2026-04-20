from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class FrameTrendInputItem(BaseModel):
    race_number: int = Field(..., ge=1, le=6, description="レース番号")
    winning_frame: int = Field(..., ge=1, le=8, description="1着枠")


class FrameTrendInputBatchCreate(BaseModel):
    target_date: date = Field(..., description="対象日")
    venue: str = Field(..., max_length=50, description="競馬場")
    results: List[FrameTrendInputItem] = Field(..., min_length=1, max_length=6)


class FrameTrendInputOut(BaseModel):
    id: int
    target_date: date
    venue: str
    race_number: int
    winning_frame: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)