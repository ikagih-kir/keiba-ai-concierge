from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    label = Column(String(255))

    category_id = Column(Integer, nullable=True)

    hit_results = relationship(
        "HitResult",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    description = Column(Text, nullable=True)
    body = Column(Text, nullable=True)  # ← 追加

    status = Column(String(50), default="draft", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    publish_start_at = Column(DateTime, nullable=True)
    publish_end_at = Column(DateTime, nullable=True)

    sold_out = Column(Boolean, default=False)
    sold_out_at = Column(DateTime, nullable=True)

    race_count = Column(Integer, nullable=True)
    race_date = Column(String(50), nullable=True)
    ticket_type = Column(String(50), nullable=True)

    expected_return = Column(Integer, nullable=True)
    max_return = Column(Integer, nullable=True)

    recommended_amount = Column(String(100), nullable=True)
    recommended_race_count = Column(Integer, nullable=True)
    capacity = Column(Integer, nullable=True)

    price = Column(Integer, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )