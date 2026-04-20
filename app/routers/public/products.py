from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.product import ProductOut
from app.services.product_service import (
    list_public_products,
    get_public_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Public Products"],
)


@router.get("", response_model=List[ProductOut])
def get_public_products(
    db: Session = Depends(get_db),
):
    return list_public_products(db)


@router.get("/{product_id}", response_model=ProductOut)
def get_public_product_detail(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_public_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product