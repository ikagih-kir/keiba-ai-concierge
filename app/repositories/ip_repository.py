from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.ip_log import IpLog

class IpRepository:
    def get_latest_ips(self, db: Session, user_id: int):
        # 登録IP（最古のregister）
        reg_stmt = (
            select(IpLog.ip_address)
            .where(IpLog.user_id == user_id, IpLog.type == "register")
            .order_by(IpLog.created_at.asc())
            .limit(1)
        )
        register_ip = db.execute(reg_stmt).scalar_one_or_none()

        # 最終アクセスIP（最新のaccess）
        last_stmt = (
            select(IpLog.ip_address)
            .where(IpLog.user_id == user_id, IpLog.type == "access")
            .order_by(IpLog.created_at.desc())
            .limit(1)
        )
        last_ip = db.execute(last_stmt).scalar_one_or_none()

        return register_ip, last_ip

    def duplicate_ip_counts(self, db: Session, ip: str, threshold: int = 2):
        stmt = (
            select(IpLog.ip_address, func.count(func.distinct(IpLog.user_id)).label("user_count"))
            .where(IpLog.ip_address == ip)
            .group_by(IpLog.ip_address)
            .having(func.count(func.distinct(IpLog.user_id)) >= threshold)
        )
        row = db.execute(stmt).first()
        if not row:
            return None
        return {"ip": row[0], "user_count": int(row[1])}



    def get_user_ips(self, db: Session, user_id: int, limit: int = 20):
        return (
            db.query(IpLog)
            .filter(IpLog.user_id == user_id)
            .order_by(IpLog.created_at.desc())
            .limit(limit)
            .all()
        )