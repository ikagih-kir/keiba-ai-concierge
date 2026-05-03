from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

from app.schemas.product import ProductOut
from app.schemas.site import SiteOut


class ReviewBase(BaseModel):
    # 段階移行中なので両方残す
    product_id: Optional[int] = None
    site_id: Optional[int] = None

    user_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    image_url: Optional[str] = None
    is_public: bool = True
    helpful_count: int = Field(0, ge=0)


class ReviewCreate(ReviewBase):
    created_at: Optional[datetime] = None


class ReviewUpdate(BaseModel):
    product_id: Optional[int] = None
    site_id: Optional[int] = None
    user_name: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    image_url: Optional[str] = None
    is_public: Optional[bool] = None
    admin_reply: Optional[str] = None
    replied_at: Optional[datetime] = None
    helpful_count: Optional[int] = Field(None, ge=0)
    created_at: Optional[datetime] = None


class ReviewReply(BaseModel):
    admin_reply: str


class ReviewOut(BaseModel):
    id: int

    product_id: Optional[int]
    site_id: Optional[int]

    user_name: str
    rating: int
    comment: str
    admin_reply: Optional[str]
    replied_at: Optional[datetime]
    is_public: bool
    image_url: Optional[str]
    helpful_count: int
    created_at: datetime

    # 既存互換 + 新仕様
    product: Optional[ProductOut] = None
    site: Optional[SiteOut] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewPublicToggle(BaseModel):
    is_public: bool


class PublicReviewOut(BaseModel):
    id: int
    user_name: str
    rating: int
    comment: str
    admin_reply: Optional[str] = None
    replied_at: Optional[datetime] = None
    image_url: Optional[str] = None
    helpful_count: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicReviewListItemOut(BaseModel):
    id: int
    product_id: Optional[int] = None
    site_id: Optional[int] = None

    user_name: str
    rating: int
    comment: str
    admin_reply: Optional[str] = None
    replied_at: Optional[datetime] = None
    image_url: Optional[str] = None
    helpful_count: int = 0
    created_at: datetime

    site: Optional[SiteOut] = None
    product: Optional[ProductOut] = None

    model_config = ConfigDict(from_attributes=True)


class PublicReviewCreate(BaseModel):
    site_id: int
    user_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    image_url: Optional[str] = None


class ReviewHelpfulVoteIn(BaseModel):
    device_id: str = Field(..., min_length=10, max_length=255)
    is_helpful: bool = True


class MessageOut(BaseModel):
    message: str