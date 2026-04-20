from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    # 既存: 無料予想(product)紐付け
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    # 新規: 掲載サイト(site)紐付け
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)

    # 投稿情報
    user_name = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)

    # 管理返信
    admin_reply = Column(Text, nullable=True)
    replied_at = Column(DateTime, nullable=True)

    # 公開設定
    is_public = Column(Boolean, default=True, nullable=False)

    # 画像
    image_url = Column(String(255), nullable=True)

    # 役立った数
    helpful_count = Column(Integer, nullable=False, default=0, server_default="0")

    # 作成日時
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # リレーション
    product = relationship("Product")
    site = relationship("Site")