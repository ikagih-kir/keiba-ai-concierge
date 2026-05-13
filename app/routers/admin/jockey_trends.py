from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.jockey_trend import (
    JockeyTrendCreate,
    JockeyTrendItem,
    JockeyTrendUpdate,
)
from app.services.jockey_trend_service import (
    create_jockey_trend,
    delete_jockey_trend,
    delete_jockey_trends_by_date_venue,
    get_jockey_trend,
    list_admin_jockey_trends,
    update_jockey_trend,
)

router = APIRouter(prefix="/admin/jockey-trends", tags=["admin-jockey-trends"])


@router.get("", response_model=list[JockeyTrendItem])
def list_jockey_trends(
    race_date: Optional[date] = Query(None),
    meeting_type: Optional[str] = Query(None),
    venue: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return list_admin_jockey_trends(
        db=db,
        race_date=race_date,
        meeting_type=meeting_type,
        venue=venue,
    )


@router.post("", response_model=JockeyTrendItem)
def create_item(
    data: JockeyTrendCreate,
    db: Session = Depends(get_db),
):
    return create_jockey_trend(db=db, data=data)

@router.delete("/by-date-venue")
def delete_items_by_date_venue(
    race_date: date = Query(...),
    meeting_type: str = Query(...),
    venue: str = Query(...),
    db: Session = Depends(get_db),
):
    return delete_jockey_trends_by_date_venue(
        db=db,
        race_date=race_date,
        meeting_type=meeting_type,
        venue=venue,
    )


@router.put("/{item_id}", response_model=JockeyTrendItem)
def update_item(
    item_id: int,
    data: JockeyTrendUpdate,
    db: Session = Depends(get_db),
):
    item = get_jockey_trend(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Jockey trend not found")

    return update_jockey_trend(db=db, item=item, data=data)


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = get_jockey_trend(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Jockey trend not found")

    delete_jockey_trend(db=db, item=item)
    return {"ok": True}