from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel, Field, ConfigDict


class SuggestedAction(BaseModel):
    type: str
    label: str
    path: Optional[str] = None
    url: Optional[str] = None


class ChatSendRequest(BaseModel):
    thread_id: Optional[int] = None
    message: str = Field(..., min_length=1, max_length=3000)
    user_id: Optional[int] = None


class ChatThreadCreateResponse(BaseModel):
    thread_id: int


class ChatMessageOut(BaseModel):
    id: int
    thread_id: int
    role: str
    content: str
    intent: Optional[str] = None
    normalized_question: Optional[str] = None
    answered_by: Optional[str] = None
    source_summary: Optional[str] = None
    suggested_actions_json: Optional[str] = None
    llm_model_name: Optional[str] = None
    response_ms: Optional[int] = None
    user_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatSendResponse(BaseModel):
    thread_id: int
    assistant_message: str
    intent: Optional[str] = None
    answered_by: Optional[str] = None
    suggested_actions: List[SuggestedAction] = []
    source_summary: Optional[str] = None


class ChatThreadOut(BaseModel):
    id: int
    user_id: Optional[int] = None
    title: Optional[str] = None
    last_user_message: Optional[str] = None
    message_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatThreadDetailResponse(BaseModel):
    thread: ChatThreadOut
    messages: List[ChatMessageOut]