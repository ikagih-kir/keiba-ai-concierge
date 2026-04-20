from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.race_change_highlight import RaceChangeHighlightOut
from app.services import race_change_highlight_service

router = APIRouter(
    prefix="/race-change-highlights",
    tags=["Public Race Change Highlights"],
)


@router.get("", response_model=List[RaceChangeHighlightOut])
def list_race_change_highlights(
    target_date: Optional[date] = Query(None, description="対象日"),
    db: Session = Depends(get_db),
):
    return race_change_highlight_service.list_public_race_change_highlights(
        db,
        target_date=target_date,
    )


@router.get("/{item_id}", response_model=RaceChangeHighlightOut)
def get_race_change_highlight_detail(
    item_id: int,
    db: Session = Depends(get_db),
):
    return race_change_highlight_service.get_public_race_change_highlight(db, item_id)