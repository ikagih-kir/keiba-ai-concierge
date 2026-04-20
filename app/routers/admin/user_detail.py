from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["Admin User Detail"],
)

@router.get("/{user_id}/basic")
def get_user_basic(
    user_id: int,
    db: Session = Depends(get_db),
):
    repo = UserRepository()
    user = repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.get("/{user_id}/payment")
def get_user_payment(
    user_id: int,
    db: Session = Depends(get_db),
):
    repo = UserRepository()
    user = repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404)
    return {
        "payment_status": user.payment_status,
        "total_payment": user.total_payment,
    }


@router.get("/{user_id}/tags")
def get_user_tags(
    user_id: int,
    db: Session = Depends(get_db),
):
    repo = UserRepository()
    return {
        "tags": repo.get_user_tags(db, user_id)
    }
