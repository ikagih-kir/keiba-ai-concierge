from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class SiteBase(BaseModel):
    name: str = Field(..., max_length=255, description="掲載サイト名")
    slug: str = Field(..., max_length=255, description="URL識別子")

    catch_copy: Optional[str] = Field(None, max_length=255, description="キャッチコピー")
    description: Optional[str] = Field(None, description="説明文")
    body: Optional[str] = Field(None, description="詳細本文")

    logo_url: Optional[str] = Field(None, max_length=500, description="ロゴ画像URL")
    thumbnail_url: Optional[str] = Field(None, max_length=500, description="サムネイル画像URL")
    banner_url: Optional[str] = Field(None, max_length=500, description="バナー画像URL")

    external_url: str = Field(..., max_length=500, description="外部リンクURL")
    affiliate_url: Optional[str] = Field(None, max_length=500, description="アフィリエイトURL")

    rating: Decimal = Field(default=0.0, ge=0, le=5, description="平均評価")
    review_count: int = Field(default=0, ge=0, description="口コミ件数")

    sort_order: int = Field(default=0, description="表示順")
    is_featured: bool = Field(default=False, description="注目掲載")
    is_recommended: bool = Field(default=False, description="おすすめ掲載")
    is_public: bool = Field(default=True, description="公開フラグ")

    # 追加
    style_type: Optional[str] = Field(None, max_length=50, description="診断用スタイル")
    free_level: Optional[str] = Field(None, max_length=50, description="無料情報レベル")
    prediction_type: Optional[str] = Field(None, max_length=50, description="予想タイプ")

    published_at: Optional[datetime] = Field(None, description="公開日時")

    hit_amount: int = Field(0, description="的中金額")
    hit_rate: Decimal = Field(0, description="的中率")
    recovery_rate: Decimal = Field(0, description="回収率")

class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)

    catch_copy: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    body: Optional[str] = None

    logo_url: Optional[str] = Field(None, max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    banner_url: Optional[str] = Field(None, max_length=500)

    external_url: Optional[str] = Field(None, max_length=500)
    affiliate_url: Optional[str] = Field(None, max_length=500)

    rating: Optional[Decimal] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)

    sort_order: Optional[int] = None
    is_featured: Optional[bool] = None
    is_recommended: Optional[bool] = None
    is_public: Optional[bool] = None

    # 追加
    style_type: Optional[str] = Field(None, max_length=50)
    free_level: Optional[str] = Field(None, max_length=50)
    prediction_type: Optional[str] = Field(None, max_length=50)

    published_at: Optional[datetime] = None

    hit_amount: int | None = None
    hit_rate: Decimal | None = None
    recovery_rate: Decimal | None = None

class SiteOut(SiteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SitePublicToggle(BaseModel):
    is_public: bool