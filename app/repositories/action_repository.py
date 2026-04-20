from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.action_log import ActionLog

class ActionRepository:
    def count_by_type(self, db: Session, user_id: int):
        stmt = (
            select(ActionLog.action_type, func.count())
            .where(ActionLog.user_id == user_id)
            .group_by(ActionLog.action_type)
        )
        rows = db.execute(stmt).all()
        return {action_type.value: int(cnt) for action_type, cnt in rows}

def get_user_actions(self, db: Session, user_id: int, limit: int = 20):
    return (
        db.query(ActionLog)
        .filter(ActionLog.user_id == user_id)
        .order_by(ActionLog.created_at.desc())
        .limit(limit)
        .all()
    )