from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile, File
from app.schemas.hit_result import HitResultCreate
import uuid
import os



from app.db.session import get_db
from app.schemas.hit_result import (
    HitResultCreate,
    HitResultUpdate,
    HitResultOut,
)
from app.services import hit_result_service
from app.core.deps import get_current_admin

router = APIRouter(
    prefix="/hit-results",
    tags=["Admin HitResults"],
)


@router.get("", response_model=List[HitResultOut])
def list_hit_results(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return hit_result_service.list_hit_results(db)



from app.schemas.hit_result import HitResultCreate

@router.post("", response_model=HitResultOut)
def create_hit_result(
    data: HitResultCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return hit_result_service.create_hit_result(db, data)




@router.put("/{hit_result_id}", response_model=HitResultOut)
def update_hit_result(
    hit_result_id: int,
    data: HitResultUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return hit_result_service.update_hit_result(db, hit_result_id, data)


@router.delete("/{hit_result_id}")
def delete_hit_result(
    hit_result_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    hit_result_service.delete_hit_result(db, hit_result_id)
    return {"success": True}
