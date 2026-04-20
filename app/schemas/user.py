from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

RegisterStatus = Literal["temp","active","suspended","withdrawn"]
PaymentStatus = Literal["unpaid","paid"]
Gender = Literal["male","female","other"]

class UserListItem(BaseModel):
    id: int
    nickname: str | None = None
    register_status: RegisterStatus
    payment_status: PaymentStatus
    total_payment: int = 0
    last_access_at: datetime | None = None
    status: Literal["normal","warning"] = "normal"  # UI用

class UserDetail(BaseModel):
    id: int
    nickname: str | None = None
    email: str | None = None
    gender: Gender | None = None
    age: int | None = None
    register_status: RegisterStatus
    payment_status: PaymentStatus
    total_payment: int = 0
    last_access_at: datetime | None = None
    tags: list[str] = []
    groups: list[str] = []  # 今回は将来拡張枠（タグで代替でもOK）
    created_at: datetime

class UserListResponse(BaseModel):
    id: int
    nickname: str | None
    register_status: str
    payment_status: str
    total_payment: int

    class Config:
        from_attributes = True

class PointGrantRequest(BaseModel):
    type: Literal["free","paid"]
    amount: int = Field(gt=0)
    reason: str | None = None

class StatusChangeRequest(BaseModel):
    status: Literal["temp","active","suspended","withdrawn"]
    reason: str | None = None

class UserBasicResponse(BaseModel):
    id: int
    nickname: str | None
    email: str | None
    register_status: str
    payment_status: str
    total_payment: int
    last_access_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True