import json
from collections import defaultdict
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.repositories.frame_trend_input_repository as frame_trend_input_repository
import app.repositories.frame_trend_snapshot_repository as frame_trend_snapshot_repository
from app.schemas.frame_trend_input import FrameTrendInputBatchCreate
from app.schemas.frame_trend_monthly import (
    FrameTrendVenueMonthlyTopFrameItem,
    FrameTrendVenueMonthlyTopFrameResponse,
)

LOCAL_VENUES = {
    "大井",
    "船橋",
    "川崎",
    "浦和",
    "門別",
    "名古屋",
    "笠松",
    "園田",
    "姫路",
    "高知",
    "佐賀",
    "金沢",
    "盛岡",
    "水沢",
}


def _detect_meeting_type_by_venue(venue: str) -> str:
    return "local" if venue in LOCAL_VENUES else "central"


def _month_range_from_end(year: int, month: int, months: int):
    start_year = year
    start_month = month - (months - 1)

    while start_month <= 0:
        start_month += 12
        start_year -= 1

    start_date = date(start_year, start_month, 1)

    if month == 12:
        next_month_date = date(year + 1, 1, 1)
    else:
        next_month_date = date(year, month + 1, 1)

    end_date = next_month_date.fromordinal(next_month_date.toordinal() - 1)
    return start_date, end_date


def get_monthly_top_frames_by_venue(
    db: Session,
    *,
    meeting_type: str = "central",
    months: int = 6,
    end_year: int | None = None,
    end_month: int | None = None,
):
    today = date.today()
    target_year = end_year or today.year
    target_month = end_month or today.month

    start_date, end_date = _month_range_from_end(
        target_year,
        target_month,
        months,
    )

    rows = frame_trend_input_repository.list_frame_trend_inputs_by_date_range(
        db,
        start_date=start_date,
        end_date=end_date,
    )

    venue_monthly_counts = defaultdict(
        lambda: {
            "frame_counts": {i: 0 for i in range(1, 9)},
            "sample_size": 0,
        }
    )

    for row in rows:
        row_meeting_type = _detect_meeting_type_by_venue(row.venue)

        if meeting_type != "all" and row_meeting_type != meeting_type:
            continue

        key = (row.venue, row.target_date.year, row.target_date.month)
        venue_monthly_counts[key]["frame_counts"][row.winning_frame] += 1
        venue_monthly_counts[key]["sample_size"] += 1

    items = []
    sorted_keys = sorted(
        venue_monthly_counts.keys(),
        key=lambda x: (x[1], x[2], x[0]),
    )

    for venue, year, month in sorted_keys:
        frame_counts = venue_monthly_counts[(venue, year, month)]["frame_counts"]
        sample_size = venue_monthly_counts[(venue, year, month)]["sample_size"]

        top_frame = None
        top_win_count = 0

        for frame in range(1, 9):
            count = frame_counts[frame]
            if count > top_win_count:
                top_frame = frame
                top_win_count = count

        items.append(
            FrameTrendVenueMonthlyTopFrameItem(
                venue=venue,
                year=year,
                month=month,
                top_frame=top_frame,
                top_win_count=top_win_count,
                frame_win_counts={str(k): v for k, v in frame_counts.items()},
                sample_size=sample_size,
            )
        )

    return FrameTrendVenueMonthlyTopFrameResponse(
        meeting_type=meeting_type,
        items=items,
    )


def list_frame_trend_inputs(
    db: Session,
    target_date: date | None = None,
    venue: str | None = None,
):
    return frame_trend_input_repository.list_frame_trend_inputs(
        db,
        target_date=target_date,
        venue=venue,
    )


def create_or_update_frame_trend_inputs_batch(
    db: Session,
    data: FrameTrendInputBatchCreate,
):
    race_numbers = [item.race_number for item in data.results]

    if len(set(race_numbers)) != len(race_numbers):
        raise HTTPException(status_code=400, detail="同じレース番号が重複しています")

    for race_number in race_numbers:
        if race_number < 1 or race_number > 6:
            raise HTTPException(status_code=400, detail="入力できるのは1〜6Rのみです")

    saved_items = []
    for item in data.results:
        saved = frame_trend_input_repository.upsert_frame_trend_input(
            db,
            target_date=data.target_date,
            venue=data.venue,
            race_number=item.race_number,
            winning_frame=item.winning_frame,
        )
        saved_items.append(saved)

    generate_frame_trend_snapshot(
        db,
        target_date=data.target_date,
        venue=data.venue,
    )

    db.commit()
    return saved_items


def generate_frame_trend_snapshot(
    db: Session,
    *,
    target_date: date,
    venue: str,
):
    inputs = frame_trend_input_repository.list_frame_trend_inputs(
        db,
        target_date=target_date,
        venue=venue,
    )

    target_inputs = [x for x in inputs if 1 <= x.race_number <= 6]

    counts = {i: 0 for i in range(1, 9)}
    for row in target_inputs:
        counts[row.winning_frame] += 1

    total_races = len(target_inputs)
    max_count = max(counts.values()) if total_races > 0 else 0

    lucky_frame = None
    if max_count > 0:
        top_frames = [frame for frame, cnt in counts.items() if cnt == max_count]
        lucky_frame = min(top_frames)

    recommended_style = "balanced"

    if lucky_frame is not None:
        trend_summary = f"1〜6Rで{lucky_frame}枠が最多{max_count}勝"
        trend_note = f"今日の{venue}は{lucky_frame}枠が好調です。"
        ai_comment = f"{venue}の1〜6Rでは{lucky_frame}枠が{max_count}勝でトップです。"
    else:
        trend_summary = "まだデータが不足しています"
        trend_note = "1〜6Rの結果入力後に自動集計されます。"
        ai_comment = "現時点ではラッキー枠を判定できるだけのデータがありません。"

    race_scope = f"{venue}_1to6"
    title = f"{venue}のラッキー枠"

    win_frame_data = json.dumps(counts, ensure_ascii=False)
    place_frame_data = json.dumps({}, ensure_ascii=False)

    return frame_trend_snapshot_repository.upsert_frame_trend_snapshot_by_date_and_scope(
        db,
        target_date=target_date,
        title=title,
        race_scope=race_scope,
        lucky_frame=lucky_frame,
        trend_summary=trend_summary,
        trend_note=trend_note,
        recommended_style=recommended_style,
        sample_size=total_races,
        win_frame_data=win_frame_data,
        place_frame_data=place_frame_data,
        ai_comment=ai_comment,
        is_featured=True,
        sort_order=0,
        is_public=True,
    )


def delete_frame_trend_inputs_for_venue_day(
    db: Session,
    *,
    target_date: date,
    venue: str,
):
    race_scope = f"{venue}_1to6"

    deleted_inputs_count = (
        frame_trend_input_repository.delete_frame_trend_inputs_by_date_and_venue(
            db,
            target_date=target_date,
            venue=venue,
        )
    )

    deleted_snapshots_count = (
        frame_trend_snapshot_repository.delete_frame_trend_snapshot_by_date_and_scope(
            db,
            target_date=target_date,
            race_scope=race_scope,
        )
    )

    db.commit()

    return {
        "message": "枠順トレンド入力データを削除しました",
        "target_date": str(target_date),
        "venue": venue,
        "deleted_inputs_count": deleted_inputs_count,
        "deleted_snapshots_count": deleted_snapshots_count,
    }