from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.models.condition_change_horse import ConditionChangeHorse
from app.models.race import Race


def get_condition_change_list(
    db: Session,
    *,
    target_date: Optional[date] = None,
    race_id: Optional[int] = None,
    featured_only: bool = False,
    min_score: int = 0,
):
    query = (
        db.query(ConditionChangeHorse, Race)
        .join(Race, ConditionChangeHorse.race_id == Race.id)
    )

    if target_date is not None:
        query = query.filter(Race.race_date == target_date)

    if race_id is not None:
        query = query.filter(ConditionChangeHorse.race_id == race_id)

    if featured_only:
        query = query.filter(ConditionChangeHorse.is_featured.is_(True))

    query = query.filter(ConditionChangeHorse.change_score >= min_score)

    query = query.order_by(
        ConditionChangeHorse.is_featured.desc(),
        ConditionChangeHorse.display_order.asc(),
        ConditionChangeHorse.change_score.desc(),
        ConditionChangeHorse.id.desc(),
    )

    rows = query.all()

    items = []
    for item, race in rows:
        items.append(
            {
                "id": item.id,
                "horse_name": item.horse_name,
                "race_name": race.race_name,
                "race_date": race.race_date,
                "venue": race.venue,
                "race_number": race.race_number,
                "prev_race_date": item.prev_race_date,
                "prev_race_name": item.prev_race_name,
                "prev_surface": item.prev_surface,
                "prev_distance": item.prev_distance,
                "prev_finish_position": item.prev_finish_position,
                "current_surface": item.current_surface,
                "current_distance": item.current_distance,
                "distance_diff": item.distance_diff,
                "surface_changed": item.surface_changed,
                "blinkers_first_time": item.blinkers_first_time,
                "blinkers_reapplied": item.blinkers_reapplied,
                "blinkers_removed": item.blinkers_removed,
                "layoff_days": item.layoff_days,
                "change_flags": item.change_flags or [],
                "change_score": item.change_score,
                "short_comment": item.short_comment,
                "ai_comment": item.ai_comment,
                "is_featured": item.is_featured,
                "display_order": item.display_order,
                "created_at": item.created_at,
            }
        )

    return items


def get_condition_change_detail(db: Session, item_id: int):
    row = (
        db.query(ConditionChangeHorse, Race)
        .join(Race, ConditionChangeHorse.race_id == Race.id)
        .filter(ConditionChangeHorse.id == item_id)
        .first()
    )
    if row is None:
        return None

    item, race = row

    return {
        "id": item.id,
        "horse_name": item.horse_name,
        "race_name": race.race_name,
        "race_date": race.race_date,
        "venue": race.venue,
        "race_number": race.race_number,
        "prev_race_date": item.prev_race_date,
        "prev_race_name": item.prev_race_name,
        "prev_surface": item.prev_surface,
        "prev_distance": item.prev_distance,
        "prev_finish_position": item.prev_finish_position,
        "current_surface": item.current_surface,
        "current_distance": item.current_distance,
        "distance_diff": item.distance_diff,
        "surface_changed": item.surface_changed,
        "blinkers_first_time": item.blinkers_first_time,
        "blinkers_reapplied": item.blinkers_reapplied,
        "blinkers_removed": item.blinkers_removed,
        "layoff_days": item.layoff_days,
        "change_flags": item.change_flags or [],
        "change_score": item.change_score,
        "short_comment": item.short_comment,
        "ai_comment": item.ai_comment,
        "is_featured": item.is_featured,
        "display_order": item.display_order,
        "created_at": item.created_at,
    }