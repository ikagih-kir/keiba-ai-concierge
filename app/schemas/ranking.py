from pydantic import BaseModel
from typing import List, Optional


class SiteRankingItem(BaseModel):
    site_id: int
    site_name: str
    logo_url: Optional[str] = None
    hit_amount: int
    hit_rate: float
    recovery_rate: float
    rank: int


class SiteRankingListResponse(BaseModel):
    items: List[SiteRankingItem]