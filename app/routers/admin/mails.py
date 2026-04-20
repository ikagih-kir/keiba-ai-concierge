from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.mail import MailCreate, MailOut
from app.services import mail_service
from app.core.deps import get_current_admin

router = APIRouter(
    prefix="/mails",
    tags=["Admin Mails"],
)

@router.post("", response_model=MailOut)
def create_mail(
    data: MailCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return mail_service.create_mail(db, data)

@router.get("", response_model=List[MailOut])
def list_mails(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return mail_service.list_mails(db)
