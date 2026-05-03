from datetime import datetime

from sqlalchemy.orm import Session

from app.models.home_dialog import HomeDialog
from app.schemas.home_dialog import HomeDialogCreate, HomeDialogUpdate


def list_home_dialogs(db: Session):
    return (
        db.query(HomeDialog)
        .order_by(HomeDialog.sort_order.asc(), HomeDialog.id.desc())
        .all()
    )


def get_home_dialog_by_id(db: Session, dialog_id: int):
    return db.query(HomeDialog).filter(HomeDialog.id == dialog_id).first()


def get_active_home_dialog(db: Session):
    now = datetime.now()

    query = db.query(HomeDialog).filter(HomeDialog.is_active == True)

    query = query.filter(
        (HomeDialog.start_at == None) | (HomeDialog.start_at <= now)
    )
    query = query.filter(
        (HomeDialog.end_at == None) | (HomeDialog.end_at >= now)
    )

    return (
        query
        .order_by(HomeDialog.sort_order.asc(), HomeDialog.id.desc())
        .first()
    )


def create_home_dialog(db: Session, data: HomeDialogCreate):
    obj = HomeDialog(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_home_dialog(db: Session, dialog_id: int, data: HomeDialogUpdate):
    obj = get_home_dialog_by_id(db, dialog_id)
    if not obj:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_home_dialog(db: Session, dialog_id: int):
    obj = get_home_dialog_by_id(db, dialog_id)
    if not obj:
        return False

    db.delete(obj)
    db.commit()
    return True


def toggle_home_dialog(db: Session, dialog_id: int, is_active: bool):
    obj = get_home_dialog_by_id(db, dialog_id)
    if not obj:
        return None

    obj.is_active = is_active
    db.commit()
    db.refresh(obj)
    return obj