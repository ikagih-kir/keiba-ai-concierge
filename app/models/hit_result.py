from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func  # ← 追加
from app.db.base import Base


class HitResult(Base):
    __tablename__ = "hit_results"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    race_name = Column(String(255), nullable=True)
    hit_amount = Column(Integer, nullable=True)
    image_url = Column(String(255), nullable=True)

    # 🔥 ここだけ修正
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    product = relationship(
        "Product",
        back_populates="hit_results",
    )
