from sqlalchemy.orm import Session, joinedload
from app.models.hit_result import HitResult
from app.schemas.hit_result import HitResultCreate, HitResultUpdate



def list(db: Session):
    return (
        db.query(HitResult)
        .options(joinedload(HitResult.product))
        .order_by(HitResult.created_at.desc())
        .all()
    )


def get_by_id(db: Session, hit_result_id: int):
    return db.query(HitResult).filter(HitResult.id == hit_result_id).first()


def create(self, db, **kwargs):
    obj = HitResult(**kwargs)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj



def update(db: Session, obj: HitResult, data: HitResultUpdate):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: HitResult):
    db.delete(obj)
    db.commit()
