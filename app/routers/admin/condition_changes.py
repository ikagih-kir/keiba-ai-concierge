from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.condition_change_horse import ConditionChangeHorse
from app.schemas.condition_change import RunBatchRequest, UpdateConditionChangeRequest
from app.services.condition_change_service import run_condition_change_batch

router = APIRouter(tags=["Admin Condition Changes"])


@router.post(
    "/condition-changes/run-batch",
    summary="条件変化馬バッチ実行",
)
def run_batch(payload: RunBatchRequest, db: Session = Depends(get_db)):
    result = run_condition_change_batch(db, payload.target_date)
    return {
        "message": "Condition change batch completed",
        "result": result,
    }


@router.patch(
    "/condition-changes/{item_id}",
    summary="条件変化馬の表示調整",
)
def update_condition_change(
    item_id: int,
    payload: UpdateConditionChangeRequest,
    db: Session = Depends(get_db),
):
    item = db.query(ConditionChangeHorse).filter(ConditionChangeHorse.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Condition change horse not found")

    if payload.is_featured is not None:
        item.is_featured = payload.is_featured

    if payload.display_order is not None:
        item.display_order = payload.display_order

    if payload.short_comment is not None:
        item.short_comment = payload.short_comment

    if payload.ai_comment is not None:
        item.ai_comment = payload.ai_comment

    db.commit()
    db.refresh(item)

    return {
        "message": "Condition change horse updated",
        "id": item.id,
    }