from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.push_token import PushTokenCreate, PushTokenOut
from app.services import push_token_service

router = APIRouter(
    prefix="/push-tokens",
    tags=["Public Push Tokens"],
)


@router.post("", response_model=PushTokenOut)
def register_push_token(
    data: PushTokenCreate,
    db: Session = Depends(get_db),
):
    return push_token_service.register_push_token(db, data)