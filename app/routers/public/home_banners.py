from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.home_banner import HomeBannerPublicOut
from app.services import home_banner_service

router = APIRouter(
    prefix="/home-banners",
    tags=["Public Home Banners"],
)


@router.get("/active", response_model=List[HomeBannerPublicOut])
def get_active_home_banners(
    db: Session = Depends(get_db),
):
    return home_banner_service.get_active_home_banners(db)