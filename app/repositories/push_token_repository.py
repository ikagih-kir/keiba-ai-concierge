from sqlalchemy.orm import Session

from app.models.push_token import PushToken
from app.schemas.push_token import PushTokenCreate


def upsert_push_token(db: Session, data: PushTokenCreate):
    token = (
        db.query(PushToken)
        .filter(PushToken.fcm_token == data.fcm_token)
        .first()
    )

    if token:
        token.device_id = data.device_id
        token.platform = data.platform
        token.app_version = data.app_version
        token.is_active = True
    else:
        token = PushToken(
            device_id=data.device_id,
            fcm_token=data.fcm_token,
            platform=data.platform,
            app_version=data.app_version,
            is_active=True,
        )
        db.add(token)

    db.commit()
    db.refresh(token)
    return token


def list_active_tokens(db: Session):
    return db.query(PushToken).filter(PushToken.is_active == True).all()