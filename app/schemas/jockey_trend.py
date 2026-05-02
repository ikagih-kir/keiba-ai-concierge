from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


MeetingType = Literal["central", "local"]


class JockeyTrendBase(BaseModel):
    race_date: date
    venue: Optional[str] = None
    meeting_type: MeetingType = "central"

    race_no: int = Field(..., ge=1, le=12)
    race_name: Optional[str] = None

    jockey_name: str = Field(..., min_length=1, max_length=100)
    horse_name: Optional[str] = None

    memo: Optional[str] = None
    is_published: bool = True


class JockeyTrendCreate(JockeyTrendBase):
    pass


class JockeyTrendUpdate(BaseModel):
    race_date: Optional[date] = None
    venue: Optional[str] = None
    meeting_type: Optional[MeetingType] = None

    race_no: Optional[int] = Field(None, ge=1, le=12)
    race_name: Optional[str] = None

    jockey_name: Optional[str] = Field(None, min_length=1, max_length=100)
    horse_name: Optional[str] = None

    memo: Optional[str] = None
    is_published: Optional[bool] = None


class JockeyTrendItem(BaseModel):
    id: int
    race_date: date
    venue: Optional[str]
    meeting_type: MeetingType

    race_no: int
    race_name: Optional[str]

    jockey_name: str
    horse_name: Optional[str]

    memo: Optional[str]
    is_published: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JockeyTrendPublicItem(BaseModel):
    id: int
    race_no: int
    race_name: Optional[str]
    jockey_name: str
    horse_name: Optional[str]
    venue: Optional[str]


class JockeyTrendRankingItem(BaseModel):
    rank: int
    jockey_name: str
    win_count: int


class JockeyTrendTopJockey(BaseModel):
    jockey_name: str
    win_count: int


class JockeyTrendPublicResponse(BaseModel):
    race_date: date
    meeting_type: MeetingType
    venue: Optional[str] = None

    items: List[JockeyTrendPublicItem]
    ranking: List[JockeyTrendRankingItem]
    top_jockey: Optional[JockeyTrendTopJockey] = None

class JockeyMonthlyChampionItem(BaseModel):
    month: int
    jockey_name: str
    win_count: int


class JockeyYearlyMonthlyChampionsResponse(BaseModel):
    year: int
    meeting_type: Literal["central", "local", "all"]
    items: List[JockeyMonthlyChampionItem]    