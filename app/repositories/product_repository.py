from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product


JST = ZoneInfo("Asia/Tokyo")


def _now_jst_naive():
    """
    DBのDateTimeがtimezoneなしのため、
    日本時間のnaive datetimeで比較する。
    """
    return datetime.now(JST).replace(tzinfo=None)


class ProductRepository:
    def list(self, db: Session):
        return (
            db.query(Product)
            .order_by(Product.id.desc())
            .all()
        )

    def create(self, db: Session, data):
        product = Product(**data.dict())

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    def update(self, db: Session, product_id: int, data):
        product = db.query(Product).get(product_id)

        if not product:
            return None

        for k, v in data.dict(exclude_unset=True).items():
            setattr(product, k, v)

        db.commit()
        db.refresh(product)

        return product

    def delete(self, db: Session, product_id: int):
        product = db.query(Product).get(product_id)

        if product:
            db.delete(product)
            db.commit()


def list_public_products(db: Session):
    now = _now_jst_naive()

    return (
        db.query(Product)
        .filter(
            Product.status == "public",
            Product.is_active.is_(True),

            # 公開開始日時
            or_(
                Product.publish_start_at.is_(None),
                Product.publish_start_at <= now,
            ),

            # 公開終了日時
            or_(
                Product.publish_end_at.is_(None),
                Product.publish_end_at > now,
            ),
        )
        .order_by(
            Product.publish_start_at.desc(),
            Product.id.desc(),
        )
        .all()
    )


def get_public_product_by_id(
    db: Session,
    product_id: int,
):
    now = _now_jst_naive()

    return (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.status == "public",
            Product.is_active.is_(True),

            # 公開開始日時
            or_(
                Product.publish_start_at.is_(None),
                Product.publish_start_at <= now,
            ),

            # 公開終了日時
            or_(
                Product.publish_end_at.is_(None),
                Product.publish_end_at > now,
            ),
        )
        .first()
    )