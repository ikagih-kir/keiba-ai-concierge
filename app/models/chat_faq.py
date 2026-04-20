from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class ChatFaq(Base):
    __tablename__ = "chat_faqs"

    id = Column(Integer, primary_key=True, index=True)

    question_pattern = Column(String(255), nullable=False)
    normalized_question = Column(String(500), nullable=False, index=True)

    intent = Column(String(100), nullable=False, index=True)
    sub_intent = Column(String(100), nullable=True, index=True)

    answer_title = Column(String(255), nullable=True)
    answer_text = Column(Text, nullable=False)

    suggested_actions_json = Column(Text, nullable=True)
    keywords_json = Column(Text, nullable=True)

    priority = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    usage_count = Column(Integer, nullable=False, default=0)
    last_used_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )