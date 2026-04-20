from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ChatFaqBase(BaseModel):
    question_pattern: str = Field(..., max_length=255)
    normalized_question: str = Field(..., max_length=500)

    intent: str = Field(..., max_length=100)
    sub_intent: Optional[str] = Field(None, max_length=100)

    answer_title: Optional[str] = Field(None, max_length=255)
    answer_text: str

    suggested_actions_json: Optional[str] = None
    keywords_json: Optional[str] = None

    priority: int = 0
    is_active: bool = True


class ChatFaqCreate(ChatFaqBase):
    pass


class ChatFaqUpdate(BaseModel):
    question_pattern: Optional[str] = Field(None, max_length=255)
    normalized_question: Optional[str] = Field(None, max_length=500)

    intent: Optional[str] = Field(None, max_length=100)
    sub_intent: Optional[str] = Field(None, max_length=100)

    answer_title: Optional[str] = Field(None, max_length=255)
    answer_text: Optional[str] = None

    suggested_actions_json: Optional[str] = None
    keywords_json: Optional[str] = None

    priority: Optional[int] = None
    is_active: Optional[bool] = None


class ChatFaqOut(ChatFaqBase):
    id: int
    usage_count: int
    last_used_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)