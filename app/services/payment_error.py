# app/services/payment_error_service.py

from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.operation_log import OperationLog
from datetime import datetime


def retry_payment_logic(db: Session, payment_id: int, admin_email: str):
    """
    再決済ロジック（仮）
    実際は Stripe / PayJP / GMO などに差し替える
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise ValueError("Payment not found")

    # 仮：成功したことにする
    payment.status = "paid"
    payment.updated_at = datetime.utcnow()

    # 操作ログ
    log = OperationLog(
        admin_email=admin_email,
        action="retry_payment",
        target_id=payment_id,
    )
    db.add(log)
    db.commit()

    return payment


def mark_resolved(db: Session, payment_id: int, admin_email: str):
    """
    決済エラーを対応済みにする
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise ValueError("Payment not found")

    payment.status = "resolved"
    payment.updated_at = datetime.utcnow()

    log = OperationLog(
        admin_email=admin_email,
        action="mark_payment_resolved",
        target_id=payment_id,
    )
    db.add(log)
    db.commit()

    return payment
