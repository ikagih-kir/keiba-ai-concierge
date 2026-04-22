from datetime import date

from sqlalchemy.orm import Session

from app.models.frame_trend_input import FrameTrendInput


def list_frame_trend_inputs(
    db: Session,
    target_date: date | None = None,
    venue: str | None = None,
):
    query = db.query(FrameTrendInput)

    if target_date is not None:
        query = query.filter(FrameTrendInput.target_date == target_date)

    if venue is not None:
        query = query.filter(FrameTrendInput.venue == venue)

    return (
        query.order_by(
            FrameTrendInput.target_date.desc(),
            FrameTrendInput.venue.asc(),
            FrameTrendInput.race_number.asc(),
        )
        .all()
    )

def list_frame_trend_inputs_by_date_range(
    db: Session,
    *,
    start_date: date,
    end_date: date,
):
    return (
        db.query(FrameTrendInput)
        .filter(
            FrameTrendInput.target_date >= start_date,
            FrameTrendInput.target_date <= end_date,
        )
        .order_by(
            FrameTrendInput.target_date.asc(),
            FrameTrendInput.venue.asc(),
            FrameTrendInput.race_number.asc(),
        )
        .all()
    )


def get_frame_trend_input_by_unique_key(
    db: Session,
    *,
    target_date: date,
    venue: str,
    race_number: int,
):
    return (
        db.query(FrameTrendInput)
        .filter(
            FrameTrendInput.target_date == target_date,
            FrameTrendInput.venue == venue,
            FrameTrendInput.race_number == race_number,
        )
        .first()
    )


def upsert_frame_trend_input(
    db: Session,
    *,
    target_date: date,
    venue: str,
    race_number: int,
    winning_frame: int,
):
    item = get_frame_trend_input_by_unique_key(
        db,
        target_date=target_date,
        venue=venue,
        race_number=race_number,
    )

    if item is None:
        item = FrameTrendInput(
            target_date=target_date,
            venue=venue,
            race_number=race_number,
            winning_frame=winning_frame,
        )
        db.add(item)
    else:
        item.winning_frame = winning_frame

    db.flush()
    return item


def delete_inputs_by_date_and_venue(
    db: Session,
    *,
    target_date: date,
    venue: str,
):
    (
        db.query(FrameTrendInput)
        .filter(
            FrameTrendInput.target_date == target_date,
            FrameTrendInput.venue == venue,
        )
        .delete(synchronize_session=False)
    )
    db.flush()