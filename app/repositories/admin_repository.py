from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.core.security import verify_password


def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()


def get_admin_by_id(db: Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()

def authenticate_admin(db: Session, email: str, password: str):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        return None

    # ★ password_hash を使う
    if not verify_password(password, admin.password_hash):
        return None

    return admin

