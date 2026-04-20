import enum
from sqlalchemy import BigInteger, Enum, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base


class PaymentMethod(str, enum.Enum):
    credit = "credit"
    bank = "bank"
    amazonpay = "amazonpay"

class PaymentStatus(str, enum.Enum):
    success = "success"
    failed = "failed"
    pending = "pending"

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    method: Mapped[PaymentMethod | None] = mapped_column(Enum(PaymentMethod), nullable=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False)
    error_code: Mapped[str | None] = mapped_column(String(50), nullable=True)

    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_user_paid", "user_id", "paid_at"),
    )
