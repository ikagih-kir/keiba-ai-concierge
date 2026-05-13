from datetime import date
from sqlalchemy.orm import Session
from app.models.frame_trend_snapshot import FrameTrendSnapshot

from app.models.frame_trend_snapshot import FrameTrendSnapshot
from app.schemas.frame_trend_snapshot import (
    FrameTrendSnapshotCreate,
    FrameTrendSnapshotUpdate,
)


def list_frame_trend_snapshots(db: Session):
    return (
        db.query(FrameTrendSnapshot)
        .order_by(
            FrameTrendSnapshot.target_date.desc(),
            FrameTrendSnapshot.sort_order.asc(),
            FrameTrendSnapshot.id.desc(),
        )
        .all()
    )


def list_public_frame_trend_snapshots(db: Session, target_date: date | None = None):
    query = db.query(FrameTrendSnapshot).filter(FrameTrendSnapshot.is_public == True)

    if target_date is not None:
        query = query.filter(FrameTrendSnapshot.target_date == target_date)

    return (
        query.order_by(
            FrameTrendSnapshot.sort_order.asc(),
            FrameTrendSnapshot.id.desc(),
        )
        .all()
    )


def get_frame_trend_snapshot_by_id(db: Session, item_id: int):
    return (
        db.query(FrameTrendSnapshot)
        .filter(FrameTrendSnapshot.id == item_id)
        .first()
    )


def get_public_frame_trend_snapshot_by_id(db: Session, item_id: int):
    return (
        db.query(FrameTrendSnapshot)
        .filter(
            FrameTrendSnapshot.id == item_id,
            FrameTrendSnapshot.is_public == True,
        )
        .first()
    )


def create_frame_trend_snapshot(db: Session, data: FrameTrendSnapshotCreate):
    item = FrameTrendSnapshot(
        target_date=data.target_date,
        title=data.title,
        race_scope=data.race_scope,
        lucky_frame=data.lucky_frame,
        trend_summary=data.trend_summary,
        trend_note=data.trend_note,
        recommended_style=data.recommended_style,
        sample_size=data.sample_size,
        win_frame_data=data.win_frame_data,
        place_frame_data=data.place_frame_data,
        ai_comment=data.ai_comment,
        is_featured=data.is_featured,
        sort_order=data.sort_order,
        is_public=data.is_public,
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_frame_trend_snapshot(
    db: Session,
    item: FrameTrendSnapshot,
    data: FrameTrendSnapshotUpdate,
):
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_frame_trend_snapshot(db: Session, item: FrameTrendSnapshot):
    db.delete(item)
    db.commit()


def toggle_frame_trend_snapshot_public(
    db: Session,
    item: FrameTrendSnapshot,
    is_public: bool,
):
    item.is_public = is_public
    db.commit()
    db.refresh(item)
    return item

def get_frame_trend_snapshot_by_date_and_scope(
    db: Session,
    *,
    target_date: date,
    race_scope: str,
):
    return (
        db.query(FrameTrendSnapshot)
        .filter(
            FrameTrendSnapshot.target_date == target_date,
            FrameTrendSnapshot.race_scope == race_scope,
        )
        .first()
    )


def upsert_frame_trend_snapshot_by_date_and_scope(
    db: Session,
    *,
    target_date: date,
    title: str,
    race_scope: str,
    lucky_frame: int | None,
    trend_summary: str | None,
    trend_note: str | None,
    recommended_style: str | None,
    sample_size: int | None,
    win_frame_data: str | None,
    place_frame_data: str | None,
    ai_comment: str | None,
    is_featured: bool,
    sort_order: int,
    is_public: bool,
):
    item = get_frame_trend_snapshot_by_date_and_scope(
        db,
        target_date=target_date,
        race_scope=race_scope,
    )

    if item is None:
        item = FrameTrendSnapshot(
            target_date=target_date,
            title=title,
            race_scope=race_scope,
            lucky_frame=lucky_frame,
            trend_summary=trend_summary,
            trend_note=trend_note,
            recommended_style=recommended_style,
            sample_size=sample_size,
            win_frame_data=win_frame_data,
            place_frame_data=place_frame_data,
            ai_comment=ai_comment,
            is_featured=is_featured,
            sort_order=sort_order,
            is_public=is_public,
        )
        db.add(item)
    else:
        item.title = title
        item.lucky_frame = lucky_frame
        item.trend_summary = trend_summary
        item.trend_note = trend_note
        item.recommended_style = recommended_style
        item.sample_size = sample_size
        item.win_frame_data = win_frame_data
        item.place_frame_data = place_frame_data
        item.ai_comment = ai_comment
        item.is_featured = is_featured
        item.sort_order = sort_order
        item.is_public = is_public

    db.flush()
    return item


def delete_frame_trend_snapshot_by_date_and_scope(
    db: Session,
    *,
    target_date: date,
    race_scope: str,
) -> int:
    deleted_count = (
        db.query(FrameTrendSnapshot)
        .filter(
            FrameTrendSnapshot.target_date == target_date,
            FrameTrendSnapshot.race_scope == race_scope,
        )
        .delete(synchronize_session=False)
    )

    return deleted_count