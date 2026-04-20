from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class ChatQuestionLog(Base):
    __tablename__ = "chat_question_logs"

    id = Column(Integer, primary_key=True, index=True)

    thread_id = Column(
        Integer,
        ForeignKey("chat_threads.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    message_id = Column(
        Integer,
        ForeignKey("chat_messages.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_id = Column(BigInteger, nullable=True, index=True)

    raw_question = Column(Text, nullable=False)
    normalized_question = Column(String(500), nullable=True, index=True)

    intent = Column(String(100), nullable=True, index=True)
    sub_intent = Column(String(100), nullable=True, index=True)
    answered_by = Column(String(50), nullable=True, index=True)

    faq_id = Column(
        Integer,
        ForeignKey("chat_faqs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    is_answered_successfully = Column(Boolean, nullable=False, default=True)
    needs_improvement = Column(Boolean, nullable=False, default=False)

    feedback_score = Column(Integer, nullable=True)  # -1 / 0 / 1 など

    created_at = Column(DateTime, server_default=func.now(), nullable=False)