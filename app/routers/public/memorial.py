from fastapi import APIRouter, HTTPException, Query

from app.schemas.memorial import MemorialResponseOut
from app.services.memorial_service import (
    get_jra_memorial,
    get_nankan_memorial,
)

router = APIRouter(
    prefix="/memorial",
    tags=["Memorial"],
)


@router.get("", response_model=MemorialResponseOut)
def get_memorial(
    source: str = Query(..., description="jra or nankan"),
):
    if source == "jra":
        return get_jra_memorial()

    if source == "nankan":
        return get_nankan_memorial()

    raise HTTPException(status_code=400, detail="source must be 'jra' or 'nankan'")