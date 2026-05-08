from collections import Counter
from datetime import date
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from datetime import date, timedelta

from app.models.jockey_trend import JockeyTrend
from app.schemas.jockey_trend import (
    JockeyTrendCreate,
    JockeyTrendPublicItem,
    JockeyTrendPublicResponse,
    JockeyTrendRankingItem,
    JockeyTrendTopJockey,
    JockeyTrendUpdate,
)


def create_jockey_trend(db: Session, data: JockeyTrendCreate) -> JockeyTrend:
    item = JockeyTrend(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_admin_jockey_trends(
    db: Session,
    race_date: Optional[date] = None,
    meeting_type: Optional[str] = None,
    venue: Optional[str] = None,
) -> list[JockeyTrend]:
    q = db.query(JockeyTrend)

    if race_date is not None:
        q = q.filter(JockeyTrend.race_date == race_date)

    if meeting_type:
        q = q.filter(JockeyTrend.meeting_type == meeting_type)

    if venue:
        q = q.filter(JockeyTrend.venue == venue)

    return q.order_by(
        JockeyTrend.race_date.desc(),
        JockeyTrend.meeting_type.asc(),
        JockeyTrend.venue.asc(),
        JockeyTrend.race_no.asc(),
    ).all()


def get_jockey_trend(db: Session, item_id: int) -> JockeyTrend | None:
    return db.query(JockeyTrend).filter(JockeyTrend.id == item_id).first()


def update_jockey_trend(
    db: Session,
    item: JockeyTrend,
    data: JockeyTrendUpdate,
) -> JockeyTrend:
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_jockey_trend(db: Session, item: JockeyTrend) -> None:
    db.delete(item)
    db.commit()


def build_public_jockey_trend_response(
    db: Session,
    race_date: date,
    meeting_type: str = "central",
    venue: Optional[str] = None,
) -> JockeyTrendPublicResponse:
    q = db.query(JockeyTrend).filter(
        JockeyTrend.race_date == race_date,
        JockeyTrend.meeting_type == meeting_type,
        JockeyTrend.is_published.is_(True),
    )

    if venue:
        q = q.filter(JockeyTrend.venue == venue)

    items = q.order_by(JockeyTrend.race_no.asc()).all()

    counter = Counter()
    for item in items:
        name = (item.jockey_name or "").strip()
        if name:
            counter[name] += 1

    ranking = []
    for index, entry in enumerate(counter.most_common(), start=1):
        jockey_name, win_count = entry
        ranking.append(
            JockeyTrendRankingItem(
                rank=index,
                jockey_name=jockey_name,
                win_count=win_count,
            )
        )

    top_jockey = None
    if ranking:
        top_jockey = JockeyTrendTopJockey(
            jockey_name=ranking[0].jockey_name,
            win_count=ranking[0].win_count,
        )

    return JockeyTrendPublicResponse(
        race_date=race_date,
        meeting_type=meeting_type,
        venue=venue,
        items=[
            JockeyTrendPublicItem(
                id=item.id,
                race_no=item.race_no,
                race_name=item.race_name,
                jockey_name=item.jockey_name,
                horse_name=item.horse_name,
                venue=item.venue,
            )
            for item in items
        ],
        ranking=ranking,
        top_jockey=top_jockey,
    )

def get_monthly_ranking(db, meeting_type: str, venue: str | None, months: int):
    """
    月間勝利数ランキング

    months=1 の場合:
        今月1日〜翌月1日未満

    months=2 の場合:
        先月1日〜翌月1日未満

    ※ 直近30日ではなく、カレンダー月単位で集計する
    """
    today = date.today()

    # 今月の1日
    current_month_start = date(today.year, today.month, 1)

    # months分さかのぼった開始月
    start_month_index = today.month - months + 1
    start_year = today.year

    while start_month_index <= 0:
        start_month_index += 12
        start_year -= 1

    from_date = date(start_year, start_month_index, 1)

    # 翌月1日
    if today.month == 12:
        to_date = date(today.year + 1, 1, 1)
    else:
        to_date = date(today.year, today.month + 1, 1)

    query = db.query(
        JockeyTrend.jockey_name,
        func.count(JockeyTrend.id).label("win_count"),
    ).filter(
        JockeyTrend.race_date >= from_date,
        JockeyTrend.race_date < to_date,
        JockeyTrend.meeting_type == meeting_type,
        JockeyTrend.is_published.is_(True),
    )

    if venue:
        query = query.filter(JockeyTrend.venue == venue)

    results = query.group_by(
        JockeyTrend.jockey_name,
    ).order_by(
        func.count(JockeyTrend.id).desc(),
        JockeyTrend.jockey_name.asc(),
    ).all()

    items = [
        {
            "rank": i + 1,
            "jockey_name": r.jockey_name,
            "win_count": int(r.win_count),
        }
        for i, r in enumerate(results)
    ]

    return {
        "meeting_type": meeting_type,
        "venue": venue,
        "months": months,
        "from_date": from_date.isoformat(),
        "to_date": to_date.isoformat(),
        "items": items,
    }

def get_yearly_monthly_champions(
    db: Session,
    *,
    year: int | None = None,
    meeting_type: str = "central",
):
    today = date.today()
    target_year = year or today.year

    query = db.query(
        extract("month", JockeyTrend.race_date).label("month"),
        JockeyTrend.jockey_name.label("jockey_name"),
        func.count(JockeyTrend.id).label("win_count"),
    ).filter(
        extract("year", JockeyTrend.race_date) == target_year,
        JockeyTrend.is_published == True,
    )

    if meeting_type != "all":
        query = query.filter(JockeyTrend.meeting_type == meeting_type)

    rows = (
        query
        .group_by(
            extract("month", JockeyTrend.race_date),
            JockeyTrend.jockey_name,
        )
        .order_by(
            extract("month", JockeyTrend.race_date).asc(),
            func.count(JockeyTrend.id).desc(),
            JockeyTrend.jockey_name.asc(),
        )
        .all()
    )

    champions_by_month = {}

    for row in rows:
        month = int(row.month)

        # その月の1位だけ採用
        if month not in champions_by_month:
            champions_by_month[month] = {
                "month": month,
                "jockey_name": row.jockey_name,
                "win_count": int(row.win_count),
            }

    return {
        "year": target_year,
        "meeting_type": meeting_type,
        "items": list(champions_by_month.values()),
    }