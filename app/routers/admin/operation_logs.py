from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.operation_log import OperationLog
from app.core.auth import get_current_admin

router = APIRouter(prefix="/operation-logs", tags=["OperationLogs"])


@router.get("")
def list_operation_logs(
    admin_email: str | None = Query(None),
    action: str | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),
):
    """
    管理者操作ログ一覧（閲覧専用）
    """

    q = db.query(OperationLog)

    # 🔍 フィルタ
    if admin_email:
        q = q.filter(OperationLog.admin_email == admin_email)

    if action:
        q = q.filter(OperationLog.action == action)

    # ✅ total件数（ページング用）
    total = q.count()

    # 📄 一覧取得
    items = (
        q.order_by(OperationLog.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
    )

    return {
        "total": total,
        "items": items,
    }
