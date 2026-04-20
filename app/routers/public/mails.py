from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.mail import Mail

router = APIRouter(prefix="/mails", tags=["Public Mails"])

@router.get("")
def list_mails(db: Session = Depends(get_db)):
    return (
        db.query(Mail)
        .order_by(Mail.id.desc())
        .all()
    )
