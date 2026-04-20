from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_admin
from app.services.payment_error import retry_payment_logic, mark_resolved
from app.services.operation_log_service import record_operation_log

router = APIRouter(prefix="/payment-errors", tags=["PaymentErrors"])


@router.post("/{id}/retry")
def retry_payment_error(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),  # ✅ callable
):
    result = retry_payment_logic(id)

    record_operation_log(
        db,
        admin=admin,
        action="retry_payment",
        target_type="payment_error",
        target_id=id,
        detail=result.get("message"),
    )

    return result


@router.post("/{id}/resolve")
def resolve_payment_error(
    id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin),  # ✅ callable
):
    mark_resolved(id)

    record_operation_log(
        db,
        admin=admin,
        action="resolve_payment",
        target_type="payment_error",
        target_id=id,
        detail="管理画面から対応済みに変更",
    )

    return {"success": True}
