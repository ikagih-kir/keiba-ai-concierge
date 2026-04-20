from sqlalchemy.orm import Session
from app.models.mail import Mail
from app.schemas.mail import MailCreate

def create_mail(db: Session, data: MailCreate):
    mail = Mail(**data.dict())
    db.add(mail)
    db.commit()
    db.refresh(mail)
    return mail

def list_mails(db: Session):
    return db.query(Mail).order_by(Mail.id.desc()).all()
