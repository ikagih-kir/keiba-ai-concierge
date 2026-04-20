from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from app.models.user import User
from app.models.user_tag import UserTag


class UserRepository:
    def list_users(
        self,
        db: Session,
        q: str | None = None,
        register_status: str | None = None,
        payment_status: str | None = None,
        page: int = 1,
        limit: int = 20,
    ):
        stmt = select(User)

        if q:
            like = f"%{q}%"
            stmt = stmt.where(
                or_(
                    func.cast(User.id, func.char).like(like),
                    User.nickname.like(like),
                    User.email.like(like),
                )
            )

        if register_status:
            stmt = stmt.where(User.register_status == register_status)

        if payment_status:
            stmt = stmt.where(User.payment_status == payment_status)

        # total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.execute(count_stmt).scalar_one()

        stmt = stmt.order_by(User.id.desc()).offset((page - 1) * limit).limit(limit)
        items = db.execute(stmt).scalars().all()

        return total, items

    def get_user_tags(self, db: Session, user_id: int) -> list[str]:
        stmt = (
            select(UserTag.tag)
            .where(UserTag.user_id == user_id)
            .order_by(UserTag.tag.asc())
        )
        return [r[0] for r in db.execute(stmt).all()]
    

    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

