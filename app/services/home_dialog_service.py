from sqlalchemy.orm import Session

from app.repositories import home_dialog_repository
from app.schemas.home_dialog import HomeDialogCreate, HomeDialogUpdate


def list_home_dialogs(db: Session):
    return home_dialog_repository.list_home_dialogs(db)


def get_active_home_dialog(db: Session):
    return home_dialog_repository.get_active_home_dialog(db)


def create_home_dialog(db: Session, data: HomeDialogCreate):
    return home_dialog_repository.create_home_dialog(db, data)


def update_home_dialog(db: Session, dialog_id: int, data: HomeDialogUpdate):
    return home_dialog_repository.update_home_dialog(db, dialog_id, data)


def delete_home_dialog(db: Session, dialog_id: int):
    return home_dialog_repository.delete_home_dialog(db, dialog_id)


def toggle_home_dialog(db: Session, dialog_id: int, is_active: bool):
    return home_dialog_repository.toggle_home_dialog(db, dialog_id, is_active)