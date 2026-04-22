from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.frame_trend_snapshot import FrameTrendSnapshotOut
from app.services import frame_trend_snapshot_service
from app.schemas.frame_trend_monthly import FrameTrendMonthlyTopFrameResponse
from app.services import frame_trend_input_service


router = APIRouter(
    prefix="/frame-trends",
    tags=["Public Frame Trends"],
)


@router.get("", response_model=List[FrameTrendSnapshotOut])
def list_frame_trends(
    target_date: Optional[date] = Query(None, description="対象日"),
    db: Session = Depends(get_db),
):
    return frame_trend_snapshot_service.list_public_frame_trend_snapshots(
        db,
        target_date=target_date,
    )


@router.get("/{item_id}", response_model=FrameTrendSnapshotOut)
def get_frame_trend_detail(
    item_id: int,
    db: Session = Depends(get_db),
):
    return frame_trend_snapshot_service.get_public_frame_trend_snapshot(db, item_id)


@router.get("/monthly-top-frames", response_model=FrameTrendMonthlyTopFrameResponse)
def get_monthly_top_frames(
    meeting_type: str = Query("central", description="central / local / all"),
    months: int = Query(6, ge=1, le=24, description="何か月分返すか"),
    end_year: Optional[int] = Query(None, description="終了年"),
    end_month: Optional[int] = Query(None, ge=1, le=12, description="終了月"),
    db: Session = Depends(get_db),
):
    return frame_trend_input_service.get_monthly_top_frames(
        db,
        meeting_type=meeting_type,
        months=months,
        end_year=end_year,
        end_month=end_month,
    )