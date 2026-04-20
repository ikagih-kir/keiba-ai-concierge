from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class PaymentItem(BaseModel):
    method: Literal["credit","bank","amazonpay"] | None = None
    amount: int
    status: Literal["success","failed","pending"]
    error_code: str | None = None
    paid_at: datetime | None = None

class UserPaymentsResponse(BaseModel):
    total_amount: int
    count: int
    items: list[PaymentItem]
