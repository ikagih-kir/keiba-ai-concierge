import enum
from sqlalchemy import BigInteger, Enum, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base


class ActionType(str, enum.Enum):
    login = "login"
    view_free = "view_free"
    view_paid = "view_paid"
    click = "click"

class ActionLog(Base):
    __tablename__ = "action_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_user_action", "user_id", "created_at"),
    )
