from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.repositories.frame_trend_snapshot_repository as frame_trend_snapshot_repository
from app.schemas.frame_trend_snapshot import (
    FrameTrendSnapshotCreate,
    FrameTrendSnapshotUpdate,
)


def list_frame_trend_snapshots(db: Session):
    return frame_trend_snapshot_repository.list_frame_trend_snapshots(db)


def list_public_frame_trend_snapshots(db: Session, target_date: date | None = None):
    return frame_trend_snapshot_repository.list_public_frame_trend_snapshots(
        db,
        target_date=target_date,
    )


def get_frame_trend_snapshot(db: Session, item_id: int):
    item = frame_trend_snapshot_repository.get_frame_trend_snapshot_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="枠順トレンドデータが見つかりません")
    return item


def get_public_frame_trend_snapshot(db: Session, item_id: int):
    item = frame_trend_snapshot_repository.get_public_frame_trend_snapshot_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="枠順トレンドデータが見つかりません")
    return item


def create_frame_trend_snapshot(db: Session, data: FrameTrendSnapshotCreate):
    return frame_trend_snapshot_repository.create_frame_trend_snapshot(db, data)


def update_frame_trend_snapshot(
    db: Session,
    item_id: int,
    data: FrameTrendSnapshotUpdate,
):
    item = frame_trend_snapshot_repository.get_frame_trend_snapshot_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="枠順トレンドデータが見つかりません")

    return frame_trend_snapshot_repository.update_frame_trend_snapshot(db, item, data)


def delete_frame_trend_snapshot(db: Session, item_id: int):
    item = frame_trend_snapshot_repository.get_frame_trend_snapshot_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="枠順トレンドデータが見つかりません")

    frame_trend_snapshot_repository.delete_frame_trend_snapshot(db, item)
    return {"message": "枠順トレンドデータを削除しました"}


def toggle_frame_trend_snapshot_public(db: Session, item_id: int, is_public: bool):
    item = frame_trend_snapshot_repository.get_frame_trend_snapshot_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="枠順トレンドデータが見つかりません")

    return frame_trend_snapshot_repository.toggle_frame_trend_snapshot_public(
        db,
        item,
        is_public,
    )