import enum
from sqlalchemy import BigInteger, Enum, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base


class PointType(str, enum.Enum):
    free = "free"
    paid = "paid"

class Point(Base):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    type: Mapped[PointType] = mapped_column(Enum(PointType), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_user_point", "user_id"),
    )
