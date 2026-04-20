from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories import product_repository
from datetime import datetime, timezone

def _normalize_optional_datetime(value):
    if value is None:
        return None

    # epoch近辺を空扱いにする保険
    if isinstance(value, datetime):
        if value.year <= 1970:
            return None

    return value

def list_products(db: Session):
    return (
        db.query(Product)
        .order_by(Product.id.desc())
        .all()
    )


def list_public_products(db: Session):
    return product_repository.list_public_products(db)


def get_public_product(db: Session, product_id: int):
    return product_repository.get_public_product_by_id(db, product_id)


def create_product(db: Session, data: ProductCreate):
    payload = data.dict()
    payload["sold_out_at"] = _normalize_optional_datetime(payload.get("sold_out_at"))
    payload["publish_start_at"] = _normalize_optional_datetime(payload.get("publish_start_at"))
    payload["publish_end_at"] = _normalize_optional_datetime(payload.get("publish_end_at"))

    if not payload.get("sold_out"):
        payload["sold_out_at"] = None

    product = Product(**payload)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = db.query(Product).get(product_id)
    if not product:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).get(product_id)
    if product:
        db.delete(product)
        db.commit()