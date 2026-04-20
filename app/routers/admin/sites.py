
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_admin
from app.schemas.site import SiteCreate, SiteUpdate, SiteOut,  SitePublicToggle
from app.services import site_service

router = APIRouter(
    prefix="/sites",
    tags=["Admin Sites"],
)


@router.get("", response_model=List[SiteOut])
def list_sites(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_service.list_sites(db)


@router.get("/{site_id}", response_model=SiteOut)
def get_site(
    site_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_service.get_site(db, site_id)


@router.post("", response_model=SiteOut)
def create_site(
    data: SiteCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_service.create_site(db, data)


@router.put("/{site_id}", response_model=SiteOut)
def update_site(
    site_id: int,
    data: SiteUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_service.update_site(db, site_id, data)


@router.delete("/{site_id}")
def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_service.delete_site(db, site_id)


@router.post("/{site_id}/toggle_public", response_model=SiteOut)
def toggle_site_public(
    site_id: int,
    data: SitePublicToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return site_service.toggle_site_public(db, site_id, data.is_public)
