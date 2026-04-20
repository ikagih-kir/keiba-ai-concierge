import json
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.repositories.frame_trend_input_repository as frame_trend_input_repository
import app.repositories.frame_trend_snapshot_repository as frame_trend_snapshot_repository
from app.schemas.frame_trend_input import FrameTrendInputBatchCreate


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

    trend_summary = None
    trend_note = None
    recommended_style = "balanced"
    ai_comment = None

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