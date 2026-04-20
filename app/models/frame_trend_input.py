from sqlalchemy import Column, Integer, String, Date, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.db.base import Base


class FrameTrendInput(Base):
    __tablename__ = "frame_trend_inputs"

    id = Column(Integer, primary_key=True, index=True)

    target_date = Column(Date, nullable=False, index=True)
    venue = Column(String(50), nullable=False, index=True)
    race_number = Column(Integer, nullable=False)
    winning_frame = Column(Integer, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(
            "target_date",
            "venue",
            "race_number",
            name="uq_frame_trend_input_target_date_venue_race_number",
        ),
    )