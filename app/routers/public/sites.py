from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.site import SiteOut
from app.schemas.review import PublicReviewOut
from app.services import site_service, review_service

router = APIRouter(
    prefix="/sites",
    tags=["Public Sites"],
)


@router.get("", response_model=List[SiteOut])
def list_sites(
    db: Session = Depends(get_db),
):
    return site_service.list_public_sites(db)


@router.get("/{site_id}", response_model=SiteOut)
def get_site_detail(
    site_id: int,
    db: Session = Depends(get_db),
):
    return site_service.get_public_site(db, site_id)


@router.get("/{site_id}/reviews", response_model=List[PublicReviewOut])
def list_site_reviews(
    site_id: int,
    db: Session = Depends(get_db),
):
    site_service.get_public_site(db, site_id)
    return review_service.list_public_reviews_by_site(db, site_id)