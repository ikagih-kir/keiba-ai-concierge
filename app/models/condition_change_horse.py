from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class ConditionChangeHorse(Base):
    __tablename__ = "condition_change_horses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    race_id = Column(BigInteger, ForeignKey("races.id"), nullable=False, index=True)
    race_entry_id = Column(
        BigInteger,
        ForeignKey("race_entries.id"),
        nullable=False,
        index=True,
    )

    horse_key = Column(String(64), nullable=False, index=True)
    horse_name = Column(String(255), nullable=False)

    prev_race_date = Column(Date, nullable=True)
    prev_race_name = Column(String(255), nullable=True)
    prev_surface = Column(String(20), nullable=True)
    prev_distance = Column(Integer, nullable=True)
    prev_finish_position = Column(Integer, nullable=True)

    current_surface = Column(String(20), nullable=False)
    current_distance = Column(Integer, nullable=False)

    distance_diff = Column(Integer, nullable=False, default=0)
    surface_changed = Column(Boolean, nullable=False, default=False)

    blinkers_first_time = Column(Boolean, nullable=False, default=False)
    blinkers_reapplied = Column(Boolean, nullable=False, default=False)
    blinkers_removed = Column(Boolean, nullable=False, default=False)

    layoff_days = Column(Integer, nullable=True)

    change_flags = Column(JSON, nullable=False)
    change_score = Column(Integer, nullable=False, default=0)

    short_comment = Column(String(500), nullable=True)
    ai_comment = Column(Text, nullable=True)

    is_featured = Column(Boolean, nullable=False, default=False, index=True)
    display_order = Column(Integer, nullable=False, default=0)

    batch_date = Column(Date, nullable=False, index=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    race = relationship("Race")
    race_entry = relationship("RaceEntry")