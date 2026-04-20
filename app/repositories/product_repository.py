from sqlalchemy.orm import Session
from app.models.product import Product


class ProductRepository:
    def list(self, db: Session):
        return db.query(Product).order_by(Product.id.desc()).all()

    def create(self, db: Session, data):
        product = Product(**data.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(self, db: Session, product_id: int, data):
        product = db.query(Product).get(product_id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(product, k, v)
        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product_id: int):
        product = db.query(Product).get(product_id)
        db.delete(product)
        db.commit()


def list_public_products(db: Session):
    return (
        db.query(Product)
        .filter(
            Product.status == "public",
            Product.is_active == True,
        )
        .order_by(Product.publish_start_at.desc(), Product.id.desc())
        .all()
    )


def get_public_product_by_id(db: Session, product_id: int):
    return (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.status == "public",
            Product.is_active == True,
        )
        .first()
    )