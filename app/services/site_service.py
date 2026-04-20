from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import site_repository
from app.schemas.site import SiteCreate, SiteUpdate


def list_sites(db: Session):
    return site_repository.list_sites(db)


def list_public_sites(db: Session):
    return site_repository.list_public_sites(db)


def get_site(db: Session, site_id: int):
    site = site_repository.get_site_by_id(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="掲載サイトが見つかりません")
    return site


def get_public_site(db: Session, site_id: int):
    site = site_repository.get_public_site_by_id(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="掲載サイトが見つかりません")
    return site


def create_site(db: Session, data: SiteCreate):
    existing = site_repository.get_site_by_slug(db, data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="このslugはすでに使用されています")

    return site_repository.create_site(db, data)


def update_site(db: Session, site_id: int, data: SiteUpdate):
    site = site_repository.get_site_by_id(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="掲載サイトが見つかりません")

    if data.slug is not None:
        existing = site_repository.get_site_by_slug(db, data.slug)
        if existing and existing.id != site_id:
            raise HTTPException(status_code=400, detail="このslugはすでに使用されています")

    return site_repository.update_site(db, site, data)


def delete_site(db: Session, site_id: int):
    site = site_repository.get_site_by_id(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="掲載サイトが見つかりません")

    site_repository.delete_site(db, site)
    return {"message": "掲載サイトを削除しました"}


def toggle_site_public(db: Session, site_id: int, is_public: bool):
    site = site_repository.get_site_by_id(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="掲載サイトが見つかりません")

    return site_repository.toggle_site_public(db, site, is_public)


def refresh_site_review_stats(db: Session, site_id: int):
    site = site_repository.get_site_by_id(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="掲載サイトが見つかりません")

    return site_repository.refresh_site_review_stats(db, site_id)