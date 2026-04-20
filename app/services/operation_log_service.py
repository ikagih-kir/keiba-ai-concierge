from sqlalchemy.orm import Session
from app.models.operation_log import OperationLog

def record_operation_log(
    db: Session,
    *,
    admin_id: int,
    admin_email: str,
    action: str,
    target_type: str,
    target_id: int,
    detail: str | None = None,
):
    log = OperationLog(
        admin_id=admin_id,
        admin_email=admin_email,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
    )
    db.add(log)
    db.commit()
