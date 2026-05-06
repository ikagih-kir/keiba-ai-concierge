from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func

from app.db.base import Base


class PushToken(Base):
    __tablename__ = "push_tokens"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(String(255), nullable=True, index=True)
    fcm_token = Column(Text, nullable=False)

    platform = Column(String(20), nullable=True)  # android / ios
    app_version = Column(String(50), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, server_default="1")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )