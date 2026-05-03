from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session, joinedload
import hashlib

from app.models.review import Review
from app.models.review_helpful_vote import ReviewHelpfulVote
from app.schemas.review import ReviewCreate, PublicReviewCreate, ReviewUpdate


def create_review(db: Session, data: ReviewCreate):
    review = Review(
        product_id=data.product_id,
        site_id=data.site_id,
        user_name=data.user_name,
        rating=data.rating,
        comment=data.comment,
        image_url=data.image_url,
        is_public=data.is_public,
        helpful_count=data.helpful_count,
        created_at=data.created_at or datetime.utcnow(),
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return get_review_by_id(db, review.id)


def update_review(db: Session, review_id: int, data: ReviewUpdate):
    review = db.get(Review, review_id)
    if not review:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)

    return get_review_by_id(db, review.id)


def create_public_review(db: Session, data: PublicReviewCreate):
    review = Review(
        product_id=None,
        site_id=data.site_id,
        user_name=data.user_name,
        rating=data.rating,
        comment=data.comment,
        image_url=data.image_url,
        is_public=False,  # Flutter投稿は必ず審査待ち
        helpful_count=0,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return get_review_by_id(db, review.id)


def get_review_by_id(db: Session, review_id: int):
    return (
        db.query(Review)
        .options(
            joinedload(Review.product),
            joinedload(Review.site),
        )
        .filter(Review.id == review_id)
        .first()
    )


def list_reviews(db: Session):
    return (
        db.query(Review)
        .options(
            joinedload(Review.product),
            joinedload(Review.site),
        )
        .order_by(Review.id.desc())
        .all()
    )


def reply_review(db: Session, review_id: int, reply: str):
    review = db.get(Review, review_id)
    if not review:
        return None

    review.admin_reply = reply
    review.replied_at = datetime.utcnow()
    db.commit()
    db.refresh(review)

    return get_review_by_id(db, review.id)


def toggle_review_public(db: Session, review_id: int, is_public: bool):
    review = db.get(Review, review_id)
    if not review:
        return None

    review.is_public = is_public
    db.commit()
    db.refresh(review)

    return get_review_by_id(db, review.id)


def _hash_device_id(device_id: str) -> str:
    return hashlib.sha256(device_id.strip().encode("utf-8")).hexdigest()


def vote_helpful(
    db: Session,
    review_id: int,
    device_id: str,
    is_helpful: bool = True,
):
    review = db.get(Review, review_id)
    if not review:
        return None, "not_found"

    if not review.is_public:
        return None, "not_found"

    device_id_hash = _hash_device_id(device_id)

    existing_vote = (
        db.query(ReviewHelpfulVote)
        .filter(
            ReviewHelpfulVote.review_id == review_id,
            ReviewHelpfulVote.device_id_hash == device_id_hash,
        )
        .first()
    )

    if existing_vote:
        return get_review_by_id(db, review.id), "already_voted"

    vote = ReviewHelpfulVote(
        review_id=review_id,
        device_id_hash=device_id_hash,
    )
    db.add(vote)

    if is_helpful:
        review.helpful_count = (review.helpful_count or 0) + 1

    db.commit()
    db.refresh(review)

    return get_review_by_id(db, review.id), "created"


def list_public(
    db: Session,
    product_id: Optional[int] = None,
    site_id: Optional[int] = None,
):
    query = (
        db.query(Review)
        .options(
            joinedload(Review.product),
            joinedload(Review.site),
        )
        .filter(Review.is_public.is_(True))
    )

    if product_id is not None:
        query = query.filter(Review.product_id == product_id)

    if site_id is not None:
        query = query.filter(Review.site_id == site_id)

    return query.order_by(Review.created_at.desc(), Review.id.desc()).all()


def list_public_by_site(db: Session, site_id: int):
    return (
        db.query(Review)
        .options(
            joinedload(Review.product),
            joinedload(Review.site),
        )
        .filter(
            Review.site_id == site_id,
            Review.is_public.is_(True),
        )
        .order_by(Review.created_at.desc(), Review.id.desc())
        .all()
    )