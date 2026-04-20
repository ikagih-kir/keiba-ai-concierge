from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class AssistantMessage(Base):
    __tablename__ = "assistant_messages"

    id = Column(Integer, primary_key=True, index=True)

    target_date = Column(Date, nullable=False, index=True)

    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    message_type = Column(String(50), nullable=True)  # daily / condition / frame_trend / site_guide ...
    priority = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)

    is_featured = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)

    action_type = Column(String(20), nullable=True)   # internal / external / none
    action_label = Column(String(100), nullable=True)
    action_path = Column(String(255), nullable=True)

    target_segment = Column(String(50), nullable=True)  # all / beginner / stable / hole ...
    related_content_type = Column(String(50), nullable=True)
    related_content_id = Column(Integer, nullable=True)

    note = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())