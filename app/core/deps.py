# app/core/deps.py
from fastapi import Depends, HTTPException, status
from app.core.auth import get_current_admin as _get_current_admin

# ルーター用の入口として再エクスポート
def get_current_admin(admin = Depends(_get_current_admin)):
    return admin


def require_role(role: str):
    def _require(admin = Depends(_get_current_admin)):
        if admin.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )
        return admin
    return _require
