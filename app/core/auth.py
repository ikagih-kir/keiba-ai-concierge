from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.config import settings
from app.repositories.admin_repository import get_admin_by_id

# ✅ 正しい OAuth2 定義
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/auth/login")


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        admin_id: str | None = payload.get("sub")
        if admin_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admin = get_admin_by_id(db, int(admin_id))
    if admin is None:
        raise credentials_exception

    return admin
