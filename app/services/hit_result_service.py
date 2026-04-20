from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import hit_result_repository as repo
from app.schemas.hit_result import HitResultCreate, HitResultUpdate
from app.models.hit_result import HitResult


def list_hit_results(db):
    return repo.list(db)


def create_hit_result(db: Session, data: HitResultCreate):
    hit = HitResult(
        product_id=data.product_id,
        race_name=data.race_name,
        hit_amount=data.hit_amount,
        image_url=data.image_url,
    )
    db.add(hit)
    db.commit()
    db.refresh(hit)
    return hit




def update_hit_result(db: Session, hit_result_id: int, data: HitResultUpdate):
    obj = repo.get_by_id(db, hit_result_id)
    if not obj:
        raise HTTPException(status_code=404, detail="HitResult not found")
    return repo.update(db, obj, data)


def delete_hit_result(db: Session, hit_result_id: int):
    obj = repo.get_by_id(db, hit_result_id)
    if not obj:
        raise HTTPException(status_code=404, detail="HitResult not found")
    repo.delete(db, obj)
