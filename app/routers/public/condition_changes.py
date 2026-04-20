from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.condition_change import (
    ConditionChangeHorseListResponse,
    ConditionChangeHorseResponse,
)
from app.services.condition_change_query_service import (
    get_condition_change_detail,
    get_condition_change_list,
)

router = APIRouter(tags=["Public Condition Changes"])


@router.get(
    "/condition-changes",
    response_model=ConditionChangeHorseListResponse,
    summary="条件が大きく変わる馬一覧",
)
def list_condition_changes(
    target_date: Optional[date] = Query(None, alias="date"),
    race_id: Optional[int] = Query(None),
    featured_only: bool = Query(False),
    min_score: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items = get_condition_change_list(
        db,
        target_date=target_date,
        race_id=race_id,
        featured_only=featured_only,
        min_score=min_score,
    )
    return {"items": items}


@router.get(
    "/condition-changes/{item_id}",
    response_model=ConditionChangeHorseResponse,
    summary="条件が大きく変わる馬詳細",
)
def get_condition_change(item_id: int, db: Session = Depends(get_db)):
    item = get_condition_change_detail(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Condition change horse not found")
    return item


@router.get(
    "/races/{race_id}/condition-changes",
    response_model=ConditionChangeHorseListResponse,
    summary="レース別の条件が大きく変わる馬一覧",
)
def list_condition_changes_by_race(
    race_id: int,
    min_score: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items = get_condition_change_list(
        db,
        race_id=race_id,
        featured_only=False,
        min_score=min_score,
    )
    return {"items": items}