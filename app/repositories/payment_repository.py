from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.payment import Payment

class PaymentRepository:
    def list_by_user(self, db: Session, user_id: int, limit: int = 50):
        stmt = (
            select(Payment)
            .where(Payment.user_id == user_id)
            .order_by(Payment.paid_at.desc().nullslast(), Payment.id.desc())
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def sum_success_amount(self, db: Session, user_id: int) -> int:
        stmt = select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.user_id == user_id,
            Payment.status == "success",
        )
        return int(db.execute(stmt).scalar_one())
