from datetime import datetime

from sqlalchemy.orm import Session

from app.models.home_banner import HomeBanner
from app.schemas.home_banner import HomeBannerCreate, HomeBannerUpdate


def list_home_banners(db: Session):
    return (
        db.query(HomeBanner)
        .order_by(HomeBanner.sort_order.asc(), HomeBanner.id.desc())
        .all()
    )

def get_home_banner(db: Session, banner_id: int):
    return db.query(HomeBanner).filter(HomeBanner.id == banner_id).first()


def get_active_home_banners(db: Session):
    now = datetime.now()

    return (
        db.query(HomeBanner)
        .filter(HomeBanner.is_active.is_(True))
        .filter((HomeBanner.start_at.is_(None)) | (HomeBanner.start_at <= now))
        .filter((HomeBanner.end_at.is_(None)) | (HomeBanner.end_at >= now))
        .order_by(HomeBanner.sort_order.asc(), HomeBanner.id.desc())
        .all()
    )


def create_home_banner(db: Session, data: HomeBannerCreate):
    banner = HomeBanner(**data.model_dump())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner


def update_home_banner(db: Session, banner_id: int, data: HomeBannerUpdate):
    banner = db.query(HomeBanner).filter(HomeBanner.id == banner_id).first()
    if not banner:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(banner, key, value)

    db.commit()
    db.refresh(banner)
    return banner


def delete_home_banner(db: Session, banner_id: int):
    banner = db.query(HomeBanner).filter(HomeBanner.id == banner_id).first()
    if not banner:
        return False

    db.delete(banner)
    db.commit()
    return True


def toggle_home_banner(db: Session, banner_id: int, is_active: bool):
    banner = db.query(HomeBanner).filter(HomeBanner.id == banner_id).first()
    if not banner:
        return None

    banner.is_active = is_active
    db.commit()
    db.refresh(banner)
    return banner