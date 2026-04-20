from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.review import (
    PublicReviewCreate,
    PublicReviewListItemOut,
    MessageOut,
    ReviewHelpfulVoteIn,
)
from app.services import review_service

router = APIRouter(
    prefix="/public/reviews",
    tags=["Public Reviews"],
)


@router.get("", response_model=List[PublicReviewListItemOut])
def get_public_reviews(
    product_id: Optional[int] = None,
    site_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return review_service.list_public_reviews(
        db=db,
        product_id=product_id,
        site_id=site_id,
    )


@router.post(
    "",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
def create_public_review(
    data: PublicReviewCreate,
    db: Session = Depends(get_db),
):
    review_service.create_public_review(db, data)
    return MessageOut(
        message="クチコミを受け付けました。確認後に公開されます。"
    )


@router.post(
    "/{review_id}/vote_helpful",
    response_model=MessageOut,
    status_code=status.HTTP_200_OK,
)
def vote_helpful(
    review_id: int,
    data: ReviewHelpfulVoteIn,
    db: Session = Depends(get_db),
):
    review, result = review_service.vote_helpful(
        db=db,
        review_id=review_id,
        device_id=data.device_id,
        is_helpful=data.is_helpful,
    )

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="公開クチコミが見つかりませんでした",
        )

    if result == "already_voted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この端末からは既に評価済みです",
        )

    return MessageOut(message="評価を受け付けました。")