from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services import product_service
from app.core.deps import get_current_admin

router = APIRouter(
    prefix="/products",
    tags=["Admin Products"],
)


@router.get("", response_model=List[ProductOut])
def get_products(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return product_service.list_products(db)


@router.post("", response_model=ProductOut)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return product_service.create_product(db, data)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    product = product_service.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    product_service.delete_product(db, product_id)
    return {"success": True}
