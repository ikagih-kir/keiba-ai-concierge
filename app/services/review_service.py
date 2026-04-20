from sqlalchemy.orm import Session

from app.repositories import review_repository
from app.schemas.review import ReviewCreate, PublicReviewCreate, ReviewUpdate
from app.services import site_service


def create_review(db: Session, data: ReviewCreate):
    review = review_repository.create_review(db, data)

    if review.site_id:
        site_service.refresh_site_review_stats(db, review.site_id)

    return review_repository.get_review_by_id(db, review.id)


def update_review(db: Session, review_id: int, data: ReviewUpdate):
    review = review_repository.update_review(db, review_id, data)

    if review and review.site_id:
        site_service.refresh_site_review_stats(db, review.site_id)

    return review


def create_public_review(db: Session, data: PublicReviewCreate):
    review = review_repository.create_public_review(db, data)
    return review


def list_reviews(db: Session):
    return review_repository.list_reviews(db)


def reply_review(db: Session, review_id: int, reply: str):
    return review_repository.reply_review(db, review_id, reply)


def toggle_review_public(db: Session, review_id: int, is_public: bool):
    review = review_repository.toggle_review_public(db, review_id, is_public)

    if review and review.site_id:
        site_service.refresh_site_review_stats(db, review.site_id)

    return review


def vote_helpful(
    db: Session,
    review_id: int,
    device_id: str,
    is_helpful: bool = True,
):
    return review_repository.vote_helpful(
        db=db,
        review_id=review_id,
        device_id=device_id,
        is_helpful=is_helpful,
    )


def list_public_reviews(
    db: Session,
    product_id: int | None = None,
    site_id: int | None = None,
):
    return review_repository.list_public(db, product_id, site_id)


def list_public_reviews_by_site(db: Session, site_id: int):
    return review_repository.list_public_by_site(db, site_id)