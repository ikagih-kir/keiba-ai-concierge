from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.home_banner import (
    HomeBannerCreate,
    HomeBannerOut,
    HomeBannerToggle,
    HomeBannerUpdate,
)
from app.services import home_banner_service

router = APIRouter(
    prefix="/home-banners",
    tags=["Admin Home Banners"],
)


@router.get("", response_model=List[HomeBannerOut])
def list_home_banners(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return home_banner_service.list_home_banners(db)


@router.get("/{banner_id}", response_model=HomeBannerOut)
def get_home_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    banner = home_banner_service.get_home_banner(db, banner_id)
    if not banner:
        raise HTTPException(status_code=404, detail="Home banner not found")
    return banner


@router.post("", response_model=HomeBannerOut)
def create_home_banner(
    data: HomeBannerCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return home_banner_service.create_home_banner(db, data)


@router.put("/{banner_id}", response_model=HomeBannerOut)
def update_home_banner(
    banner_id: int,
    data: HomeBannerUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    banner = home_banner_service.update_home_banner(db, banner_id, data)
    if not banner:
        raise HTTPException(status_code=404, detail="Home banner not found")
    return banner


@router.delete("/{banner_id}")
def delete_home_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    ok = home_banner_service.delete_home_banner(db, banner_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Home banner not found")
    return {"message": "deleted"}


@router.post("/{banner_id}/toggle", response_model=HomeBannerOut)
def toggle_home_banner(
    banner_id: int,
    data: HomeBannerToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    banner = home_banner_service.toggle_home_banner(
        db,
        banner_id,
        data.is_active,
    )
    if not banner:
        raise HTTPException(status_code=404, detail="Home banner not found")
    return banner