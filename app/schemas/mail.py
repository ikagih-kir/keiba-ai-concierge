from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MailCreate(BaseModel):
    title: str
    body: str
    product_id: int | None = None


class MailOut(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
