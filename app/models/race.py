from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Integer, Date, DateTime

from app.db.base import Base


class Race(Base):
    __tablename__ = "races"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    race_key = Column(String(64), nullable=False, unique=True, index=True)

    race_date = Column(Date, nullable=False, index=True)
    venue = Column(String(50), nullable=False)
    race_number = Column(Integer, nullable=False)
    race_name = Column(String(255), nullable=False)

    grade = Column(String(20), nullable=True)
    surface = Column(String(20), nullable=False)   # turf / dirt
    distance = Column(Integer, nullable=False)
    direction = Column(String(20), nullable=True)  # left / right / straight
    course_class = Column(String(50), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )