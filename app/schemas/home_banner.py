from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class HomeBannerBase(BaseModel):
    title: str = Field(..., max_length=100)
    image_url: str = Field(..., max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    placement: str = Field(default="home_middle", max_length=50)
    is_active: bool = True
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    sort_order: int = 0


class HomeBannerCreate(HomeBannerBase):
    pass


class HomeBannerUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = Field(None, max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    placement: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    sort_order: Optional[int] = None


class HomeBannerOut(HomeBannerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class HomeBannerPublicOut(BaseModel):
    id: int
    title: str
    image_url: str
    link_url: Optional[str] = None
    placement: str
    sort_order: int = 0

    model_config = ConfigDict(from_attributes=True)


class HomeBannerToggle(BaseModel):
    is_active: bool