from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.repositories.admin_repository import authenticate_admin
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Admin Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    admin = authenticate_admin(db, data.email, data.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(admin.id), "email": admin.email, "role": admin.role}
    )

    return {"access_token": token, "token_type": "bearer"}
