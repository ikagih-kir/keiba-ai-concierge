from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.hit_result import HitResultOut
from app.services import hit_result_service

router = APIRouter(
    prefix="/hit-results",
    tags=["HitResults"],
)

@router.get("", response_model=List[HitResultOut])
def list_hit_results(db: Session = Depends(get_db)):
    return hit_result_service.list_hit_results(db)
