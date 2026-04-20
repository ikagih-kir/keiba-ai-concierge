from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class RaceChangeHighlight(Base):
    __tablename__ = "race_change_highlights"

    id = Column(Integer, primary_key=True, index=True)

    target_date = Column(Date, nullable=False, index=True)

    race_name = Column(String(255), nullable=False)
    race_course = Column(String(100), nullable=True)
    horse_name = Column(String(255), nullable=False)

    previous_surface = Column(String(20), nullable=True)   # turf / dirt
    current_surface = Column(String(20), nullable=True)

    previous_distance = Column(Integer, nullable=True)
    current_distance = Column(Integer, nullable=True)

    previous_jockey = Column(String(100), nullable=True)
    current_jockey = Column(String(100), nullable=True)

    surface_changed = Column(Boolean, default=False)
    distance_changed = Column(Boolean, default=False)
    distance_direction = Column(String(20), nullable=True)  # up / down / same
    gear_changed = Column(Boolean, default=False)
    jockey_changed = Column(Boolean, default=False)
    class_changed = Column(Boolean, default=False)

    change_summary = Column(String(255), nullable=True)
    ai_comment = Column(Text, nullable=True)
    note = Column(Text, nullable=True)

    impact_level = Column(String(20), nullable=True)  # high / medium / low
    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    is_public = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())