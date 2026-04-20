from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.race_change_highlight import (
    RaceChangeHighlightCreate,
    RaceChangeHighlightOut,
    RaceChangeHighlightPublicToggle,
    RaceChangeHighlightUpdate,
)
from app.services import race_change_highlight_service

router = APIRouter(
    prefix="/race-change-highlights",
    tags=["Admin Race Change Highlights"],
)


@router.get("", response_model=List[RaceChangeHighlightOut])
def list_race_change_highlights(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return race_change_highlight_service.list_race_change_highlights(db)


@router.get("/{item_id}", response_model=RaceChangeHighlightOut)
def get_race_change_highlight(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return race_change_highlight_service.get_race_change_highlight(db, item_id)


@router.post("", response_model=RaceChangeHighlightOut)
def create_race_change_highlight(
    data: RaceChangeHighlightCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return race_change_highlight_service.create_race_change_highlight(db, data)


@router.put("/{item_id}", response_model=RaceChangeHighlightOut)
def update_race_change_highlight(
    item_id: int,
    data: RaceChangeHighlightUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return race_change_highlight_service.update_race_change_highlight(db, item_id, data)


@router.delete("/{item_id}")
def delete_race_change_highlight(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return race_change_highlight_service.delete_race_change_highlight(db, item_id)


@router.post("/{item_id}/toggle_public", response_model=RaceChangeHighlightOut)
def toggle_race_change_highlight_public(
    item_id: int,
    data: RaceChangeHighlightPublicToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return race_change_highlight_service.toggle_race_change_highlight_public(
        db,
        item_id,
        data.is_public,
    )