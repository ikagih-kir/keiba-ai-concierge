from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.home_dialog import (
    HomeDialogCreate,
    HomeDialogOut,
    HomeDialogToggle,
    HomeDialogUpdate,
)
from app.services import home_dialog_service

router = APIRouter(
    prefix="/home-dialogs",
    tags=["Admin Home Dialogs"],
)


@router.get("", response_model=List[HomeDialogOut])
def list_home_dialogs(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return home_dialog_service.list_home_dialogs(db)


@router.post("", response_model=HomeDialogOut)
def create_home_dialog(
    data: HomeDialogCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return home_dialog_service.create_home_dialog(db, data)


@router.put("/{dialog_id}", response_model=HomeDialogOut)
def update_home_dialog(
    dialog_id: int,
    data: HomeDialogUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    dialog = home_dialog_service.update_home_dialog(db, dialog_id, data)
    if not dialog:
        raise HTTPException(status_code=404, detail="Home dialog not found")
    return dialog


@router.delete("/{dialog_id}")
def delete_home_dialog(
    dialog_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    ok = home_dialog_service.delete_home_dialog(db, dialog_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Home dialog not found")
    return {"message": "deleted"}


@router.post("/{dialog_id}/toggle", response_model=HomeDialogOut)
def toggle_home_dialog(
    dialog_id: int,
    data: HomeDialogToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    dialog = home_dialog_service.toggle_home_dialog(
        db,
        dialog_id,
        data.is_active,
    )
    if not dialog:
        raise HTTPException(status_code=404, detail="Home dialog not found")
    return dialog