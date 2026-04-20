from datetime import date
from sqlalchemy.orm import Session

from app.models.race_change_highlight import RaceChangeHighlight
from app.schemas.race_change_highlight import (
    RaceChangeHighlightCreate,
    RaceChangeHighlightUpdate,
)


def list_race_change_highlights(db: Session):
    return (
        db.query(RaceChangeHighlight)
        .order_by(
            RaceChangeHighlight.target_date.desc(),
            RaceChangeHighlight.sort_order.asc(),
            RaceChangeHighlight.id.desc(),
        )
        .all()
    )


def list_public_race_change_highlights(db: Session, target_date: date | None = None):
    query = db.query(RaceChangeHighlight).filter(RaceChangeHighlight.is_public == True)

    if target_date is not None:
        query = query.filter(RaceChangeHighlight.target_date == target_date)

    return (
        query.order_by(
            RaceChangeHighlight.sort_order.asc(),
            RaceChangeHighlight.id.desc(),
        )
        .all()
    )


def get_race_change_highlight_by_id(db: Session, item_id: int):
    return (
        db.query(RaceChangeHighlight)
        .filter(RaceChangeHighlight.id == item_id)
        .first()
    )


def get_public_race_change_highlight_by_id(db: Session, item_id: int):
    return (
        db.query(RaceChangeHighlight)
        .filter(
            RaceChangeHighlight.id == item_id,
            RaceChangeHighlight.is_public == True,
        )
        .first()
    )


def create_race_change_highlight(db: Session, data: RaceChangeHighlightCreate):
    item = RaceChangeHighlight(
        target_date=data.target_date,
        race_name=data.race_name,
        race_course=data.race_course,
        horse_name=data.horse_name,
        previous_surface=data.previous_surface,
        current_surface=data.current_surface,
        previous_distance=data.previous_distance,
        current_distance=data.current_distance,
        previous_jockey=data.previous_jockey,
        current_jockey=data.current_jockey,
        surface_changed=data.surface_changed,
        distance_changed=data.distance_changed,
        distance_direction=data.distance_direction,
        gear_changed=data.gear_changed,
        jockey_changed=data.jockey_changed,
        class_changed=data.class_changed,
        change_summary=data.change_summary,
        ai_comment=data.ai_comment,
        note=data.note,
        impact_level=data.impact_level,
        is_featured=data.is_featured,
        sort_order=data.sort_order,
        is_public=data.is_public,
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_race_change_highlight(
    db: Session,
    item: RaceChangeHighlight,
    data: RaceChangeHighlightUpdate,
):
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_race_change_highlight(db: Session, item: RaceChangeHighlight):
    db.delete(item)
    db.commit()


def toggle_race_change_highlight_public(
    db: Session,
    item: RaceChangeHighlight,
    is_public: bool,
):
    item.is_public = is_public
    db.commit()
    db.refresh(item)
    return item