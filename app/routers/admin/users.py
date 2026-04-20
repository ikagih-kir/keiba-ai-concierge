from fastapi import APIRouter, Depends
from app.core.deps import require_role

router = APIRouter(prefix="/users")

@router.get(
    "",
    dependencies=[Depends(require_role(["super_admin", "operator", "viewer"]))],
)
def list_users():
    return {"msg": "ユーザー一覧"}

@router.post(
    "",
    dependencies=[Depends(require_role(["super_admin"]))],
)
def create_user():
    return {"msg": "ユーザー作成"}
