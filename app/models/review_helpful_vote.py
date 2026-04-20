from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ReviewHelpfulVote(Base):
    __tablename__ = "review_helpful_votes"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False, index=True)

    # 端末識別子そのものは保存せず、ハッシュ化した値を保存
    device_id_hash = Column(String(64), nullable=False, index=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("review_id", "device_id_hash", name="uq_review_helpful_vote_review_device"),
    )

    review = relationship("Review")