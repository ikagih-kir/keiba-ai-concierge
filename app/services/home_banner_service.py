from sqlalchemy.orm import Session

from app.repositories import home_banner_repository
from app.schemas.home_banner import HomeBannerCreate, HomeBannerUpdate


def list_home_banners(db: Session):
    return home_banner_repository.list_home_banners(db)

def get_home_banner(db: Session, banner_id: int):
    return home_banner_repository.get_home_banner(db, banner_id)


def get_active_home_banners(db: Session):
    return home_banner_repository.get_active_home_banners(db)


def create_home_banner(db: Session, data: HomeBannerCreate):
    return home_banner_repository.create_home_banner(db, data)


def update_home_banner(db: Session, banner_id: int, data: HomeBannerUpdate):
    return home_banner_repository.update_home_banner(db, banner_id, data)


def delete_home_banner(db: Session, banner_id: int):
    return home_banner_repository.delete_home_banner(db, banner_id)


def toggle_home_banner(db: Session, banner_id: int, is_active: bool):
    return home_banner_repository.toggle_home_banner(db, banner_id, is_active)