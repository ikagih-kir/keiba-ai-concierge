from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.race import Race
from app.models.race_entry import RaceEntry
from app.models.condition_change_horse import ConditionChangeHorse


SCORE_RULES = {
    "surface_change_turf_to_dirt": 30,
    "surface_change_dirt_to_turf": 30,
    "distance_shortening_medium": 15,
    "distance_shortening_large": 25,
    "distance_extension_medium": 15,
    "distance_extension_large": 25,
    "first_blinkers": 20,
    "blinkers_reapplied": 12,
    "blinkers_removed": 10,
    "layoff_over_90": 8,
    "layoff_over_180": 15,
    "surface_and_distance_changed": 10,
    "first_time_mile": 12,
    "first_time_sprint": 12,
    "first_time_middle_distance": 12,
}


def calc_layoff_days(prev_race_date: Optional[date], current_race_date: date) -> Optional[int]:
    if not prev_race_date:
        return None
    return (current_race_date - prev_race_date).days


def detect_special_distance_flag(current_distance: int, prev_distance: Optional[int]) -> List[str]:
    if prev_distance is None:
        return []

    flags: List[str] = []

    if current_distance == 1600 and prev_distance != 1600:
        flags.append("first_time_mile")
    elif current_distance <= 1400 and prev_distance > 1400:
        flags.append("first_time_sprint")
    elif 1800 <= current_distance <= 2200 and not (1800 <= prev_distance <= 2200):
        flags.append("first_time_middle_distance")

    return flags


def detect_condition_changes(
    prev_surface: Optional[str],
    prev_distance: Optional[int],
    current_surface: str,
    current_distance: int,
    prev_blinkers: Optional[List[bool]],
    blinkers_now: bool,
    layoff_days: Optional[int],
) -> Dict[str, Any]:
    flags: List[str] = []
    score = 0

    distance_diff = 0
    if prev_distance is not None:
        distance_diff = current_distance - prev_distance

    if prev_surface and prev_surface != current_surface:
        if prev_surface == "turf" and current_surface == "dirt":
            flags.append("surface_change_turf_to_dirt")
        elif prev_surface == "dirt" and current_surface == "turf":
            flags.append("surface_change_dirt_to_turf")

    if prev_distance is not None:
        if distance_diff <= -800:
            flags.append("distance_shortening_large")
        elif distance_diff <= -400:
            flags.append("distance_shortening_medium")
        elif distance_diff >= 800:
            flags.append("distance_extension_large")
        elif distance_diff >= 400:
            flags.append("distance_extension_medium")

    blinkers_first_time = False
    blinkers_reapplied = False
    blinkers_removed = False

    if prev_blinkers:
        last_blinkers = prev_blinkers[0]

        if blinkers_now and all(not x for x in prev_blinkers):
            flags.append("first_blinkers")
            blinkers_first_time = True
        elif blinkers_now and (not last_blinkers) and any(prev_blinkers[1:]):
            flags.append("blinkers_reapplied")
            blinkers_reapplied = True
        elif (not blinkers_now) and last_blinkers:
            flags.append("blinkers_removed")
            blinkers_removed = True

    if layoff_days is not None:
        if layoff_days >= 180:
            flags.append("layoff_over_180")
        elif layoff_days >= 90:
            flags.append("layoff_over_90")

    flags.extend(detect_special_distance_flag(current_distance, prev_distance))

    if any(flag.startswith("surface_change_") for flag in flags) and abs(distance_diff) >= 400:
        flags.append("surface_and_distance_changed")

    for flag in flags:
        score += SCORE_RULES.get(flag, 0)

    return {
        "flags": flags,
        "score": score,
        "distance_diff": distance_diff,
        "surface_changed": prev_surface != current_surface if prev_surface else False,
        "blinkers_first_time": blinkers_first_time,
        "blinkers_reapplied": blinkers_reapplied,
        "blinkers_removed": blinkers_removed,
    }


def build_short_comment(
    flags: List[str],
    prev_surface: Optional[str],
    prev_distance: Optional[int],
    current_surface: str,
    current_distance: int,
) -> Optional[str]:
    parts: List[str] = []

    if prev_surface and prev_surface != current_surface:
        jp_prev = "芝" if prev_surface == "turf" else "ダート"
        jp_curr = "芝" if current_surface == "turf" else "ダート"
        parts.append(f"{jp_prev}から{jp_curr}替わり")

    if prev_distance is not None:
        diff = current_distance - prev_distance
        if diff <= -800:
            parts.append(f"{abs(diff)}mの大幅短縮")
        elif diff <= -400:
            parts.append(f"{abs(diff)}m短縮")
        elif diff >= 800:
            parts.append(f"{diff}mの大幅延長")
        elif diff >= 400:
            parts.append(f"{diff}m延長")

    if "first_blinkers" in flags:
        parts.append("初ブリンカー")
    elif "blinkers_reapplied" in flags:
        parts.append("ブリンカー再装着")
    elif "blinkers_removed" in flags:
        parts.append("ブリンカー解除")

    if "first_time_mile" in flags:
        parts.append("初マイル")
    elif "first_time_sprint" in flags:
        parts.append("短距離替わり")
    elif "first_time_middle_distance" in flags:
        parts.append("中距離替わり")

    if not parts:
        return None

    return " / ".join(parts)


def upsert_race(db: Session, race_data: Dict[str, Any]) -> Race:
    race = db.query(Race).filter(Race.race_key == race_data["race_key"]).first()

    if race is None:
        race = Race(race_key=race_data["race_key"])
        db.add(race)

    race.race_date = race_data["race_date"]
    race.venue = race_data["venue"]
    race.race_number = race_data["race_number"]
    race.race_name = race_data["race_name"]
    race.grade = race_data.get("grade")
    race.surface = race_data["surface"]
    race.distance = race_data["distance"]
    race.direction = race_data.get("direction")
    race.course_class = race_data.get("course_class")

    db.flush()
    return race


def upsert_race_entry(db: Session, race: Race, entry_data: Dict[str, Any]) -> RaceEntry:
    entry = (
        db.query(RaceEntry)
        .filter(RaceEntry.race_id == race.id, RaceEntry.horse_key == entry_data["horse_key"])
        .first()
    )

    if entry is None:
        entry = RaceEntry(race_id=race.id, horse_key=entry_data["horse_key"])
        db.add(entry)

    entry.horse_name = entry_data["horse_name"]
    entry.frame_number = entry_data.get("frame_number")
    entry.horse_number = entry_data.get("horse_number")
    entry.sex = entry_data.get("sex")
    entry.age = entry_data.get("age")
    entry.jockey_name = entry_data.get("jockey_name")
    entry.trainer_name = entry_data.get("trainer_name")
    entry.handicap_weight = entry_data.get("handicap_weight")
    entry.blinkers_now = entry_data.get("blinkers_now", False)
    entry.odds = entry_data.get("odds")
    entry.popularity = entry_data.get("popularity")

    db.flush()
    return entry


def upsert_condition_change_result(
    db: Session,
    *,
    race: Race,
    race_entry: RaceEntry,
    prev_run: Optional[Dict[str, Any]],
    detection_result: Dict[str, Any],
    short_comment: Optional[str],
    batch_date: date,
) -> ConditionChangeHorse:
    existing = (
        db.query(ConditionChangeHorse)
        .filter(
            ConditionChangeHorse.race_id == race.id,
            ConditionChangeHorse.race_entry_id == race_entry.id,
            ConditionChangeHorse.batch_date == batch_date,
        )
        .first()
    )

    if existing is None:
        existing = ConditionChangeHorse(
            race_id=race.id,
            race_entry_id=race_entry.id,
            horse_key=race_entry.horse_key,
            horse_name=race_entry.horse_name,
            batch_date=batch_date,
            change_flags=[],
        )
        db.add(existing)

    existing.horse_key = race_entry.horse_key
    existing.horse_name = race_entry.horse_name

    if prev_run:
        existing.prev_race_date = prev_run.get("race_date")
        existing.prev_race_name = prev_run.get("race_name")
        existing.prev_surface = prev_run.get("surface")
        existing.prev_distance = prev_run.get("distance")
        existing.prev_finish_position = prev_run.get("finish_position")
        existing.layoff_days = prev_run.get("layoff_days")
    else:
        existing.prev_race_date = None
        existing.prev_race_name = None
        existing.prev_surface = None
        existing.prev_distance = None
        existing.prev_finish_position = None
        existing.layoff_days = None

    existing.current_surface = race.surface
    existing.current_distance = race.distance

    existing.distance_diff = detection_result["distance_diff"]
    existing.surface_changed = detection_result["surface_changed"]
    existing.blinkers_first_time = detection_result["blinkers_first_time"]
    existing.blinkers_reapplied = detection_result["blinkers_reapplied"]
    existing.blinkers_removed = detection_result["blinkers_removed"]

    existing.change_flags = detection_result["flags"]
    existing.change_score = detection_result["score"]
    existing.short_comment = short_comment

    existing.is_featured = False
    existing.display_order = 0

    db.flush()
    return existing


def mark_featured_horses(
    db: Session,
    batch_date: date,
    featured_count: int = 10,
    min_score: int = 20,
) -> None:
    rows = (
        db.query(ConditionChangeHorse)
        .filter(
            ConditionChangeHorse.batch_date == batch_date,
            ConditionChangeHorse.change_score >= min_score,
        )
        .order_by(
            ConditionChangeHorse.change_score.desc(),
            ConditionChangeHorse.id.asc(),
        )
        .all()
    )

    for idx, row in enumerate(rows):
        row.is_featured = idx < featured_count
        row.display_order = idx + 1 if idx < featured_count else 9999 + idx


# ----------------------------
# テスト用ダミーデータ
# ----------------------------

DUMMY_RACES: List[Dict[str, Any]] = [
    {
        "race_key": "2026-03-31_nakayama_11r",
        "race_date": date(2026, 3, 31),
        "venue": "中山",
        "race_number": 11,
        "race_name": "ダミー杯",
        "grade": "G3",
        "surface": "turf",
        "distance": 1600,
        "direction": "right",
        "course_class": "重賞",
    },
    {
        "race_key": "2026-03-31_hanshin_10r",
        "race_date": date(2026, 3, 31),
        "venue": "阪神",
        "race_number": 10,
        "race_name": "ダミーダート特別",
        "grade": None,
        "surface": "dirt",
        "distance": 1400,
        "direction": "right",
        "course_class": "3勝クラス",
    },
]

DUMMY_RACE_ENTRIES: Dict[str, List[Dict[str, Any]]] = {
    "2026-03-31_nakayama_11r": [
        {
            "horse_key": "horse_001",
            "horse_name": "サンプルマイラー",
            "frame_number": 1,
            "horse_number": 1,
            "sex": "牡",
            "age": 4,
            "jockey_name": "田中太郎",
            "trainer_name": "佐藤厩舎",
            "handicap_weight": 56.0,
            "blinkers_now": False,
            "odds": 4.8,
            "popularity": 2,
        },
        {
            "horse_key": "horse_002",
            "horse_name": "ブリンカーエース",
            "frame_number": 2,
            "horse_number": 3,
            "sex": "牡",
            "age": 5,
            "jockey_name": "山田次郎",
            "trainer_name": "高橋厩舎",
            "handicap_weight": 57.0,
            "blinkers_now": True,
            "odds": 8.6,
            "popularity": 5,
        },
        {
            "horse_key": "horse_003",
            "horse_name": "ロングランスター",
            "frame_number": 4,
            "horse_number": 7,
            "sex": "牝",
            "age": 4,
            "jockey_name": "鈴木花子",
            "trainer_name": "伊藤厩舎",
            "handicap_weight": 54.0,
            "blinkers_now": False,
            "odds": 12.4,
            "popularity": 7,
        },
    ],
    "2026-03-31_hanshin_10r": [
        {
            "horse_key": "horse_004",
            "horse_name": "ダートチェンジャー",
            "frame_number": 3,
            "horse_number": 5,
            "sex": "牡",
            "age": 4,
            "jockey_name": "川村一樹",
            "trainer_name": "森厩舎",
            "handicap_weight": 56.0,
            "blinkers_now": True,
            "odds": 6.2,
            "popularity": 3,
        },
        {
            "horse_key": "horse_005",
            "horse_name": "スプリントクイーン",
            "frame_number": 5,
            "horse_number": 9,
            "sex": "牝",
            "age": 5,
            "jockey_name": "井上美咲",
            "trainer_name": "西園厩舎",
            "handicap_weight": 55.0,
            "blinkers_now": False,
            "odds": 15.8,
            "popularity": 8,
        },
    ],
}

DUMMY_PREVIOUS_RUNS: Dict[str, Dict[str, Any]] = {
    "horse_001": {
        "race_date": date(2026, 2, 15),
        "race_name": "東京新聞杯",
        "surface": "turf",
        "distance": 2000,
        "finish_position": 6,
    },
    "horse_002": {
        "race_date": date(2025, 11, 30),
        "race_name": "チャレンジC",
        "surface": "turf",
        "distance": 1800,
        "finish_position": 8,
    },
    "horse_003": {
        "race_date": date(2026, 2, 22),
        "race_name": "ダイヤモンドS",
        "surface": "turf",
        "distance": 3400,
        "finish_position": 4,
    },
    "horse_004": {
        "race_date": date(2026, 3, 1),
        "race_name": "洛陽S",
        "surface": "turf",
        "distance": 1600,
        "finish_position": 10,
    },
    "horse_005": {
        "race_date": date(2026, 3, 8),
        "race_name": "オーシャンS",
        "surface": "turf",
        "distance": 1200,
        "finish_position": 3,
    },
}

DUMMY_PREVIOUS_BLINKERS: Dict[str, List[bool]] = {
    "horse_001": [False, False, False],
    "horse_002": [False, False, False],
    "horse_003": [False, False, False],
    "horse_004": [False, True, True],
    "horse_005": [True, True, False],
}


# ----------------------------
# 外部データ取得部（今はダミー）
# 後で実データ取得に差し替え
# ----------------------------

def fetch_target_races(target_date: date) -> List[Dict[str, Any]]:
    return [race for race in DUMMY_RACES if race["race_date"] == target_date]


def fetch_race_entries(race_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return DUMMY_RACE_ENTRIES.get(race_data["race_key"], [])


def fetch_previous_run(horse_key: str) -> Optional[Dict[str, Any]]:
    return DUMMY_PREVIOUS_RUNS.get(horse_key)


def fetch_previous_blinkers(horse_key: str, limit: int = 3) -> List[bool]:
    return DUMMY_PREVIOUS_BLINKERS.get(horse_key, [])[:limit]


def run_condition_change_batch(db: Session, target_date: date) -> Dict[str, Any]:
    races = fetch_target_races(target_date)

    processed_races = 0
    processed_entries = 0
    saved_results = 0

    for race_data in races:
        race = upsert_race(db, race_data)
        processed_races += 1

        entries = fetch_race_entries(race_data)

        for entry_data in entries:
            race_entry = upsert_race_entry(db, race, entry_data)
            processed_entries += 1

            prev_run = fetch_previous_run(entry_data["horse_key"])
            prev_blinkers = fetch_previous_blinkers(entry_data["horse_key"], limit=3)

            layoff_days = calc_layoff_days(
                prev_run.get("race_date") if prev_run else None,
                race.race_date,
            )

            detection_result = detect_condition_changes(
                prev_surface=prev_run.get("surface") if prev_run else None,
                prev_distance=prev_run.get("distance") if prev_run else None,
                current_surface=race.surface,
                current_distance=race.distance,
                prev_blinkers=prev_blinkers,
                blinkers_now=entry_data.get("blinkers_now", False),
                layoff_days=layoff_days,
            )

            if prev_run is not None:
                prev_run["layoff_days"] = layoff_days

            short_comment = build_short_comment(
                detection_result["flags"],
                prev_run.get("surface") if prev_run else None,
                prev_run.get("distance") if prev_run else None,
                race.surface,
                race.distance,
            )

            upsert_condition_change_result(
                db,
                race=race,
                race_entry=race_entry,
                prev_run=prev_run,
                detection_result=detection_result,
                short_comment=short_comment,
                batch_date=target_date,
            )
            saved_results += 1

    mark_featured_horses(db, batch_date=target_date)

    db.commit()

    return {
        "target_date": str(target_date),
        "processed_races": processed_races,
        "processed_entries": processed_entries,
        "saved_results": saved_results,
    }