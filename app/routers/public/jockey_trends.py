from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.jockey_trend import JockeyTrendPublicResponse
from app.services.jockey_trend_service import build_public_jockey_trend_response
from app.services import jockey_trend_service

router = APIRouter(prefix="/jockey-trends", tags=["jockey-trends"])

@router.get("/monthly-ranking")
def get_monthly_ranking(
    meeting_type: str = Query("central"),
    venue: Optional[str] = Query(None),
    months: int = Query(1),
    db: Session = Depends(get_db),
):
    return jockey_trend_service.get_monthly_ranking(
        db=db,
        meeting_type=meeting_type,
        venue=venue,
        months=months,
    )


@router.get("", response_model=JockeyTrendPublicResponse)
def get_jockey_trends(
    race_date: date = Query(...),
    meeting_type: str = Query("central"),
    venue: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return build_public_jockey_trend_response(
        db=db,
        race_date=race_date,
        meeting_type=meeting_type,
        venue=venue,
    )


@router.get("/today", response_model=JockeyTrendPublicResponse)
def get_today_jockey_trends(
    meeting_type: str = Query("central"),
    venue: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    today = date.today()

    return build_public_jockey_trend_response(
        db=db,
        race_date=today,
        meeting_type=meeting_type,
        venue=venue,
    )