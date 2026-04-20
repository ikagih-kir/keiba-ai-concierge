from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.review import (
    ReviewOut,
    ReviewReply,
    ReviewCreate,
    ReviewUpdate,
    ReviewPublicToggle,
)
from app.services import review_service
from app.core.deps import get_current_admin

router = APIRouter(
    prefix="/reviews",
    tags=["Admin Reviews"],
)


@router.post("", response_model=ReviewOut)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return review_service.create_review(db, data)


@router.get("", response_model=List[ReviewOut])
def list_reviews(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return review_service.list_reviews(db)


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    review = review_service.update_review(db, review_id, data)
    if not review:
      raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/{review_id}/reply", response_model=ReviewOut)
def reply_review(
    review_id: int,
    data: ReviewReply,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return review_service.reply_review(db, review_id, data.admin_reply)


@router.post("/{review_id}/toggle_public", response_model=ReviewOut)
def toggle_review_public(
    review_id: int,
    data: ReviewPublicToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return review_service.toggle_review_public(db, review_id, data.is_public)