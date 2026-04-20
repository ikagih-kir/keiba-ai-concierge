from sqlalchemy.orm import Session
from app.models.point import Point, PointType
from datetime import datetime

class PointService:
    def grant(self, db: Session, user_id: int, point_type: str, amount: int, reason: str | None):
        p = Point(
            user_id=user_id,
            type=PointType(point_type),
            amount=amount,
            reason=reason,
            created_at=datetime.utcnow(),
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
