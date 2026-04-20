from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChatQuestionLogOut(BaseModel):
    id: int
    thread_id: Optional[int] = None
    message_id: Optional[int] = None
    user_id: Optional[int] = None

    raw_question: str
    normalized_question: Optional[str] = None

    intent: Optional[str] = None
    sub_intent: Optional[str] = None
    answered_by: Optional[str] = None

    faq_id: Optional[int] = None

    is_answered_successfully: bool
    needs_improvement: bool

    feedback_score: Optional[int] = None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)