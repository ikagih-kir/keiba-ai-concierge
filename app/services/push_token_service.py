from sqlalchemy.orm import Session

from app.repositories import push_token_repository
from app.schemas.push_token import PushTokenCreate


def register_push_token(db: Session, data: PushTokenCreate):
    return push_token_repository.upsert_push_token(db, data)


def list_active_tokens(db: Session):
    return push_token_repository.list_active_tokens(db)