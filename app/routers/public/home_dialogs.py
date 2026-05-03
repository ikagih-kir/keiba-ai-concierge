from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.home_dialog import HomeDialogPublicOut
from app.services import home_dialog_service

router = APIRouter(
    prefix="/home-dialogs",
    tags=["Public Home Dialogs"],
)


@router.get("/active", response_model=HomeDialogPublicOut | None)
def get_active_home_dialog(
    db: Session = Depends(get_db),
):
    return home_dialog_service.get_active_home_dialog(db)