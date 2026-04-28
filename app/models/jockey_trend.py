from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, func

from app.db.base import Base


class JockeyTrend(Base):
    __tablename__ = "jockey_trends"

    id = Column(Integer, primary_key=True, index=True)

    race_date = Column(Date, nullable=False, index=True)
    venue = Column(String(50), nullable=True, index=True)
    meeting_type = Column(String(20), nullable=False, default="central", index=True)
    # central / local

    race_no = Column(Integer, nullable=False)
    race_name = Column(String(100), nullable=True)

    jockey_name = Column(String(100), nullable=False, index=True)
    horse_name = Column(String(100), nullable=True)

    memo = Column(Text, nullable=True)
    is_published = Column(Boolean, nullable=False, default=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )