from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.schemas.product import ProductOut


class HitResultBase(BaseModel):
    race_name: str
    hit_amount: int = Field(..., gt=0)  # 0より大きい制約
    image_url: Optional[str] = None


class HitResultCreate(HitResultBase):
    product_id: int  # ← 必須にする


class HitResultUpdate(BaseModel):
    product_id: Optional[int] = None
    race_name: Optional[str] = None
    hit_amount: Optional[int] = None
    image_url: Optional[str] = None


class HitResultOut(BaseModel):
    id: int
    race_name: str
    hit_amount: int
    image_url: Optional[str]
    created_at: datetime
    product: ProductOut

    model_config = ConfigDict(from_attributes=True)
