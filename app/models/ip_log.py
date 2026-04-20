import enum
from sqlalchemy import BigInteger, Enum, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base


class IpType(str, enum.Enum):
    register = "register"
    access = "access"

class IpLog(Base):
    __tablename__ = "ip_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)  # IPv6対応
    type: Mapped[IpType] = mapped_column(Enum(IpType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_ip", "ip_address"),
        Index("idx_user_ip", "user_id"),
    )
