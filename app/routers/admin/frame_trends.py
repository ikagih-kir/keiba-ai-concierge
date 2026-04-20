from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.frame_trend_input import (
    FrameTrendInputBatchCreate,
    FrameTrendInputOut,
)
from app.schemas.frame_trend_snapshot import (
    FrameTrendSnapshotCreate,
    FrameTrendSnapshotOut,
    FrameTrendSnapshotPublicToggle,
    FrameTrendSnapshotUpdate,
)
import app.services.frame_trend_input_service as frame_trend_input_service
import app.services.frame_trend_snapshot_service as frame_trend_snapshot_service

router = APIRouter(
    prefix="/frame-trends",
    tags=["Admin Frame Trends"],
)


@router.get("", response_model=List[FrameTrendSnapshotOut])
def list_frame_trends(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_snapshot_service.list_frame_trend_snapshots(db)


@router.get("/{item_id}", response_model=FrameTrendSnapshotOut)
def get_frame_trend(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_snapshot_service.get_frame_trend_snapshot(db, item_id)


@router.post("", response_model=FrameTrendSnapshotOut)
def create_frame_trend(
    data: FrameTrendSnapshotCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_snapshot_service.create_frame_trend_snapshot(db, data)


@router.put("/{item_id}", response_model=FrameTrendSnapshotOut)
def update_frame_trend(
    item_id: int,
    data: FrameTrendSnapshotUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_snapshot_service.update_frame_trend_snapshot(db, item_id, data)


@router.delete("/{item_id}")
def delete_frame_trend(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_snapshot_service.delete_frame_trend_snapshot(db, item_id)


@router.post("/{item_id}/toggle_public", response_model=FrameTrendSnapshotOut)
def toggle_frame_trend_public(
    item_id: int,
    data: FrameTrendSnapshotPublicToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_snapshot_service.toggle_frame_trend_snapshot_public(
        db,
        item_id,
        data.is_public,
    )


@router.get("/inputs/list", response_model=List[FrameTrendInputOut])
def list_frame_trend_inputs(
    target_date: Optional[date] = Query(None),
    venue: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_input_service.list_frame_trend_inputs(
        db,
        target_date=target_date,
        venue=venue,
    )


@router.post("/inputs/batch", response_model=List[FrameTrendInputOut])
def create_frame_trend_inputs_batch(
    data: FrameTrendInputBatchCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return frame_trend_input_service.create_or_update_frame_trend_inputs_batch(
        db,
        data,
    )