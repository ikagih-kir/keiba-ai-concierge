from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class ProductStatus(str, Enum):
    draft = "draft"
    public = "public"
    private = "private"


class ProductBase(BaseModel):
    category_id: Optional[int] = None

    name: str = Field(..., example="フェブラリーS攻略")
    label: Optional[str] = Field(None, example="今週限定・重賞特化")
    description: Optional[str] = None
    body: Optional[str] = None

    status: ProductStatus = ProductStatus.draft
    is_active: bool = True

    publish_start_at: Optional[datetime] = None
    publish_end_at: Optional[datetime] = None

    sold_out: bool = False
    sold_out_at: Optional[datetime] = None

    race_count: Optional[int] = Field(None, example=3)
    race_date: Optional[str] = Field(None, example="2026/02/15")
    ticket_type: Optional[str] = Field(None, example="3連単")

    expected_return: Optional[int] = Field(None, example=120)
    max_return: Optional[int] = Field(None, example=980)

    recommended_amount: Optional[str] = Field(None, example="10,000円")
    recommended_race_count: Optional[int] = Field(None, example=3)
    capacity: Optional[int] = Field(None, example=50)

    price: int = Field(..., example=9800)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None

    status: Optional[ProductStatus] = None
    is_active: Optional[bool] = None

    publish_start_at: Optional[datetime] = None
    publish_end_at: Optional[datetime] = None

    sold_out: Optional[bool] = None
    sold_out_at: Optional[datetime] = None

    race_count: Optional[int] = None
    race_date: Optional[str] = None
    ticket_type: Optional[str] = None

    expected_return: Optional[int] = None
    max_return: Optional[int] = None

    recommended_amount: Optional[str] = None
    recommended_race_count: Optional[int] = None
    capacity: Optional[int] = None

    price: Optional[int] = None


class ProductOut(BaseModel):
    id: int
    category_id: Optional[int] = None

    name: str
    label: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None

    status: ProductStatus
    is_active: bool

    publish_start_at: Optional[datetime] = None
    publish_end_at: Optional[datetime] = None

    sold_out: bool
    sold_out_at: Optional[datetime] = None

    race_count: Optional[int] = None
    race_date: Optional[str] = None
    ticket_type: Optional[str] = None

    expected_return: Optional[int] = None
    max_return: Optional[int] = None

    recommended_amount: Optional[str] = None
    recommended_race_count: Optional[int] = None
    capacity: Optional[int] = None

    price: int

    model_config = ConfigDict(from_attributes=True)