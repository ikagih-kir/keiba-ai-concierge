from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.site import Site
from app.models.review import Review
from app.schemas.site import SiteCreate, SiteUpdate


def list_sites(db: Session):
    return (
        db.query(Site)
        .order_by(Site.sort_order.asc(), Site.id.desc())
        .all()
    )


def list_public_sites(db: Session):
    return (
        db.query(Site)
        .filter(Site.is_public == True)
        .order_by(Site.sort_order.asc(), Site.id.desc())
        .all()
    )


def get_site_by_id(db: Session, site_id: int):
    return db.query(Site).filter(Site.id == site_id).first()


def get_public_site_by_id(db: Session, site_id: int):
    return (
        db.query(Site)
        .filter(
            Site.id == site_id,
            Site.is_public == True,
        )
        .first()
    )


def get_site_by_slug(db: Session, slug: str):
    return db.query(Site).filter(Site.slug == slug).first()


def create_site(db: Session, data: SiteCreate):
    site = Site(
        name=data.name,
        slug=data.slug,
        catch_copy=data.catch_copy,
        description=data.description,
        body=data.body,
        logo_url=data.logo_url,
        thumbnail_url=data.thumbnail_url,
        banner_url=data.banner_url,
        external_url=data.external_url,
        affiliate_url=data.affiliate_url,
        rating=data.rating,
        review_count=data.review_count,
        sort_order=data.sort_order,
        is_featured=data.is_featured,
        is_recommended=data.is_recommended,
        is_public=data.is_public,
        style_type=data.style_type,
        free_level=data.free_level,
        prediction_type=data.prediction_type,
        published_at=data.published_at,
        hit_amount=data.hit_amount,
        hit_rate=data.hit_rate,
        recovery_rate=data.recovery_rate,
    )

    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def update_site(db: Session, site: Site, data: SiteUpdate):
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(site, key, value)

    db.commit()
    db.refresh(site)
    return site


def delete_site(db: Session, site: Site):
    db.delete(site)
    db.commit()


def toggle_site_public(db: Session, site: Site, is_public: bool):
    site.is_public = is_public
    db.commit()
    db.refresh(site)
    return site


def refresh_site_review_stats(db: Session, site_id: int):
    site = get_site_by_id(db, site_id)
    if not site:
        return None

    result = (
        db.query(
            func.count(Review.id).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .filter(
            Review.site_id == site_id,
            Review.is_public == True,
        )
        .first()
    )

    review_count = int(result.review_count or 0)
    avg_rating = float(result.avg_rating or 0)

    site.review_count = review_count
    site.rating = round(avg_rating, 1)

    db.commit()
    db.refresh(site)
    return site