from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class FrameTrendVenueMonthlyTopFrameItem(BaseModel):
    venue: str = Field(..., description="競馬場")
    year: int = Field(..., description="年")
    month: int = Field(..., description="月")
    top_frame: Optional[int] = Field(None, description="その月その競馬場で1着が最も多かった枠")
    top_win_count: int = Field(0, description="その枠の1着数")
    sample_size: int = Field(0, description="集計レース数")


class FrameTrendVenueMonthlyTopFrameResponse(BaseModel):
    meeting_type: Literal["central", "local", "all"]
    items: List[FrameTrendVenueMonthlyTopFrameItem]