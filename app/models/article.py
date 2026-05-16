from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    # 対象サイト
    site_id = Column(
    BIGINT(unsigned=True),
    ForeignKey("sites.id", ondelete="SET NULL"),
    nullable=True,
    index=True,
)
    site = relationship("Site", lazy="joined")

    # 基本情報
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    category = Column(String(100), nullable=True)

    # 記事内容
    excerpt = Column(Text, nullable=True)
    body = Column(Text, nullable=True)

    # 画像
    thumbnail_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)

    # 表示制御
    is_featured = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # 公開日時
    published_at = Column(DateTime, nullable=True)

    # 作成更新日時
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @property
    def site_name(self):
        return self.site.name if self.site else None

    @property
    def site_external_url(self):
        return self.site.external_url if self.site else None

    @property
    def site_affiliate_url(self):
        return self.site.affiliate_url if self.site else None