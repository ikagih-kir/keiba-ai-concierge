from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class ChatThread(Base):
    __tablename__ = "chat_threads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=True, index=True)
    title = Column(String(255), nullable=True)
    last_user_message = Column(String(1000), nullable=True)
    message_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )