from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import get_dashboard_summary
from app.core.auth import get_current_admin  # 既存の認証

router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Admin Dashboard"],
)

@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def dashboard_summary(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return get_dashboard_summary(db)
