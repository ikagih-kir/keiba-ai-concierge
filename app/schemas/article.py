from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ArticleBase(BaseModel):
    title: str = Field(..., max_length=255, description="記事タイトル")
    slug: str = Field(..., max_length=255, description="URL識別子")
    category: Optional[str] = Field(None, max_length=100, description="記事カテゴリ")

    excerpt: Optional[str] = Field(None, description="一覧用の短い説明文")
    body: Optional[str] = Field(None, description="記事本文")

    thumbnail_url: Optional[str] = Field(None, max_length=500, description="サムネイル画像URL")
    banner_url: Optional[str] = Field(None, max_length=500, description="記事メイン画像URL")

    is_featured: bool = Field(default=False, description="注目記事")
    is_public: bool = Field(default=True, description="公開フラグ")
    sort_order: int = Field(default=0, description="表示順")

    published_at: Optional[datetime] = Field(None, description="公開日時")


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)

    excerpt: Optional[str] = None
    body: Optional[str] = None

    thumbnail_url: Optional[str] = Field(None, max_length=500)
    banner_url: Optional[str] = Field(None, max_length=500)

    is_featured: Optional[bool] = None
    is_public: Optional[bool] = None
    sort_order: Optional[int] = None

    published_at: Optional[datetime] = None


class ArticleOut(BaseModel):
    id: int
    title: str
    category: Optional[str] = None
    excerpt: Optional[str] = None
    body: Optional[str] = None
    thumbnail_url: Optional[str] = None
    banner_url: Optional[str] = None
    published_at: Optional[datetime] = None
    is_public: bool

    model_config = ConfigDict(from_attributes=True)

class ArticlePublicToggle(BaseModel):
    is_public: bool