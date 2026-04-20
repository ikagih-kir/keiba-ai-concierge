from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, DECIMAL,BigInteger, Numeric
from sqlalchemy.sql import func
from app.db.base import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)

    catch_copy = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    body = Column(Text, nullable=True)

    logo_url = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)

    external_url = Column(String(500), nullable=False)
    affiliate_url = Column(String(500), nullable=True)

    rating = Column(DECIMAL(2, 1), default=0.0)
    review_count = Column(Integer, default=0)

    hit_amount = Column(BigInteger, nullable=False, default=0)
    hit_rate = Column(Numeric(5, 2), nullable=False, default=0)
    recovery_rate = Column(Numeric(6, 2), nullable=False, default=0)

    sort_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_recommended = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)

    # 追加
    style_type = Column(String(50), nullable=True)
    free_level = Column(String(50), nullable=True)
    prediction_type = Column(String(50), nullable=True)

    published_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
