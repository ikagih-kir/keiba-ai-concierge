from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class FrameTrendSnapshot(Base):
    __tablename__ = "frame_trend_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    target_date = Column(Date, nullable=False, index=True)

    title = Column(String(255), nullable=False)
    race_scope = Column(String(100), nullable=True)

    lucky_frame = Column(Integer, nullable=True)
    trend_summary = Column(String(255), nullable=True)
    trend_note = Column(Text, nullable=True)
    recommended_style = Column(String(20), nullable=True)  # stable / hole / balanced

    sample_size = Column(Integer, nullable=True)
    win_frame_data = Column(Text, nullable=True)
    place_frame_data = Column(Text, nullable=True)

    ai_comment = Column(Text, nullable=True)

    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    is_public = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())