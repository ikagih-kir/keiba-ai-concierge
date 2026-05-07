from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class ScheduledPushNotification(Base):
    __tablename__ = "scheduled_push_notifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    body = Column(String(255), nullable=False)
    target_path = Column(String(255), nullable=True)

    status = Column(String(20), nullable=False, default="scheduled", server_default="scheduled")
    scheduled_at = Column(DateTime, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)

    success_count = Column(Integer, nullable=False, default=0, server_default="0")
    failure_count = Column(Integer, nullable=False, default=0, server_default="0")
    total_count = Column(Integer, nullable=False, default=0, server_default="0")

    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)