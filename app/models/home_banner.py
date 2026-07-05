from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.base import Base


class HomeBanner(Base):
    __tablename__ = "home_banners"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=False)
    link_url = Column(String(500), nullable=True)
    placement = Column(String(50), nullable=False, default="home_middle", server_default="home_middle")

    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)

    sort_order = Column(Integer, nullable=False, default=0, server_default="0")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)