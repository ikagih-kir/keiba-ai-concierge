from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import race_change_highlight_repository
from app.schemas.race_change_highlight import (
    RaceChangeHighlightCreate,
    RaceChangeHighlightUpdate,
)


def list_race_change_highlights(db: Session):
    return race_change_highlight_repository.list_race_change_highlights(db)


def list_public_race_change_highlights(db: Session, target_date: date | None = None):
    return race_change_highlight_repository.list_public_race_change_highlights(
        db,
        target_date=target_date,
    )


def get_race_change_highlight(db: Session, item_id: int):
    item = race_change_highlight_repository.get_race_change_highlight_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="条件変わり馬データが見つかりません")
    return item


def get_public_race_change_highlight(db: Session, item_id: int):
    item = race_change_highlight_repository.get_public_race_change_highlight_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="条件変わり馬データが見つかりません")
    return item


def create_race_change_highlight(db: Session, data: RaceChangeHighlightCreate):
    return race_change_highlight_repository.create_race_change_highlight(db, data)


def update_race_change_highlight(
    db: Session,
    item_id: int,
    data: RaceChangeHighlightUpdate,
):
    item = race_change_highlight_repository.get_race_change_highlight_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="条件変わり馬データが見つかりません")

    return race_change_highlight_repository.update_race_change_highlight(db, item, data)


def delete_race_change_highlight(db: Session, item_id: int):
    item = race_change_highlight_repository.get_race_change_highlight_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="条件変わり馬データが見つかりません")

    race_change_highlight_repository.delete_race_change_highlight(db, item)
    return {"message": "条件変わり馬データを削除しました"}


def toggle_race_change_highlight_public(db: Session, item_id: int, is_public: bool):
    item = race_change_highlight_repository.get_race_change_highlight_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="条件変わり馬データが見つかりません")

    return race_change_highlight_repository.toggle_race_change_highlight_public(
        db,
        item,
        is_public,
    )