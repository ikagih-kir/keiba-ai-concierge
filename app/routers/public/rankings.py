from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ranking import SiteRankingListResponse
from app.services import ranking_service

router = APIRouter(
    prefix="/rankings",
    tags=["Public Rankings"],
)


@router.get("/sites", response_model=SiteRankingListResponse)
def list_site_rankings(
    sort: str = Query("hit_amount", pattern="^(hit_amount|hit_rate|recovery_rate)$"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return ranking_service.list_site_rankings(
        db,
        sort=sort,
        limit=limit,
    )