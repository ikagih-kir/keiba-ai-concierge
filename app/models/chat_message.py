from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(
        Integer,
        ForeignKey("chat_threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role = Column(String(20), nullable=False)  # user / assistant / system
    content = Column(Text, nullable=False)

    intent = Column(String(100), nullable=True, index=True)
    normalized_question = Column(String(500), nullable=True)
    answered_by = Column(String(50), nullable=True, index=True)
    source_summary = Column(String(255), nullable=True)
    suggested_actions_json = Column(Text, nullable=True)

    model_name = Column(String(100), nullable=True)
    response_ms = Column(Integer, nullable=True)

    user_id = Column(BigInteger, nullable=True, index=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)