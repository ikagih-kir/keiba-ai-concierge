from sqlalchemy.orm import Session

from app.models.site import Site


def list_site_rankings(
    db: Session,
    sort: str = "hit_amount",
    limit: int = 50,
):
    sort_map = {
        "hit_amount": Site.hit_amount,
        "hit_rate": Site.hit_rate,
        "recovery_rate": Site.recovery_rate,
    }

    sort_column = sort_map.get(sort, Site.hit_amount)

    items = (
        db.query(Site)
        .filter(Site.is_public == True)
        .order_by(sort_column.desc(), Site.rating.desc(), Site.id.asc())
        .limit(limit)
        .all()
    )

    results = []
    for index, item in enumerate(items, start=1):
        results.append(
            {
                "site_id": item.id,
                "site_name": item.name,
                "logo_url": item.logo_url or item.thumbnail_url,
                "hit_amount": int(item.hit_amount or 0),
                "hit_rate": float(item.hit_rate or 0),
                "recovery_rate": float(item.recovery_rate or 0),
                "rank": index,
            }
        )

    return {"items": results}