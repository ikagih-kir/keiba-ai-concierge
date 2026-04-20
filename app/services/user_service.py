from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.payment_repository import PaymentRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.payment_repo = PaymentRepository()

    def list_users(self, db: Session, q: str | None, register_status: str | None, payment_status: str | None, page: int, limit: int):
        total, users = self.user_repo.list_users(db, q, register_status, payment_status, page, limit)

        # status(警告)の簡易判定：課金済みなのに最終アクセスがない/古い 等は後で強化
        items = []
        for u in users:
            status = "warning" if (u.payment_status.value == "paid" and u.last_access_at is None) else "normal"
            items.append((u, status))

        return total, items

    def get_user_detail(self, db: Session, user_id: int):
        user = self.user_repo.get_user(db, user_id)
        if not user:
            return None
        tags = self.user_repo.get_user_tags(db, user_id)
        # groupsは今回省略（必要なら user_groups テーブル追加 or tagプレフィックスで運用）
        return user, tags
