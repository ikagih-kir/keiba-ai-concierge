from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.product import Product

router = APIRouter()

@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .filter(Product.is_active == True)
        .all()
    )

    return [
        {
            "id": p.id,
            "name": p.name,
        }
        for p in products
    ]
