from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class HomeDialog(Base):
    __tablename__ = "home_dialogs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)

    primary_button_text = Column(String(50), nullable=True)
    primary_button_path = Column(String(255), nullable=True)
    secondary_button_text = Column(String(50), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    show_once_per_day = Column(Boolean, nullable=False, default=True, server_default="1")

    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)

    sort_order = Column(Integer, nullable=False, default=0, server_default="0")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)