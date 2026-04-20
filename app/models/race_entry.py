from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    DECIMAL,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class RaceEntry(Base):
    __tablename__ = "race_entries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    race_id = Column(BigInteger, ForeignKey("races.id"), nullable=False, index=True)

    horse_key = Column(String(64), nullable=False, index=True)
    horse_name = Column(String(255), nullable=False)

    frame_number = Column(Integer, nullable=True)
    horse_number = Column(Integer, nullable=True)

    sex = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)

    jockey_name = Column(String(100), nullable=True)
    trainer_name = Column(String(100), nullable=True)

    handicap_weight = Column(DECIMAL(4, 1), nullable=True)
    blinkers_now = Column(Boolean, nullable=False, default=False)

    odds = Column(DECIMAL(8, 2), nullable=True)
    popularity = Column(Integer, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    race = relationship("Race")

    __table_args__ = (
        UniqueConstraint("race_id", "horse_key", name="uq_race_entries_race_horse"),
    )