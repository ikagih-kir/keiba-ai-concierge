from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories import product_repository
from datetime import datetime
from zoneinfo import ZoneInfo


JST = ZoneInfo("Asia/Tokyo")


def _now_jst_naive():
    """
    DBのDateTimeがtimezoneなしなので、
    日本時間をtimezoneなしdatetimeにして比較する。
    """
    return datetime.now(JST).replace(tzinfo=None)


def _normalize_optional_datetime(value):
    if value is None:
        return None

    # epoch近辺を空扱いにする保険
    if isinstance(value, datetime):
        if value.year <= 1970:
            return None

        # timezone付きで届いた場合もDB用にJSTのnaiveへ統一
        if value.tzinfo is not None:
            value = value.astimezone(JST).replace(tzinfo=None)

    return value

def _normalize_publish_end_at(value):
    """
    公開終了日は、その日の23:59:59まで有効にする。
    """
    value = _normalize_optional_datetime(value)

    if value is None:
        return None

    # 00:00:00で送られてきた日付指定の場合
    # その日の最後まで公開する
    if (
        value.hour == 0
        and value.minute == 0
        and value.second == 0
        and value.microsecond == 0
    ):
        return value.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )

    return value


def _expire_ended_products(db: Session):
    """
    公開終了日時を過ぎた無料予想を自動的に非公開にする。
    """
    now = _now_jst_naive()

    updated_count = (
        db.query(Product)
        .filter(
            Product.status == "public",
            Product.is_active.is_(True),
            Product.publish_end_at.isnot(None),
            Product.publish_end_at <= now,
        )
        .update(
            {
                Product.is_active: False,
            },
            synchronize_session=False,
        )
    )

    if updated_count > 0:
        db.commit()


def list_products(db: Session):
    # 管理画面を開いた時にも期限切れをOFFにする
    _expire_ended_products(db)

    return (
        db.query(Product)
        .order_by(Product.id.desc())
        .all()
    )


def list_public_products(db: Session):
    # Flutterから一覧取得された時にも期限切れをOFFにする
    _expire_ended_products(db)

    return product_repository.list_public_products(db)


def get_public_product(db: Session, product_id: int):
    # Flutterから詳細取得された時にも期限切れをOFFにする
    _expire_ended_products(db)

    return product_repository.get_public_product_by_id(db, product_id)


def create_product(db: Session, data: ProductCreate):
    payload = data.dict()

    payload["sold_out_at"] = _normalize_optional_datetime(
        payload.get("sold_out_at")
    )
    payload["publish_start_at"] = _normalize_optional_datetime(
        payload.get("publish_start_at")
    )
    payload["publish_end_at"] = _normalize_publish_end_at(
        payload.get("publish_end_at")
    )

    if not payload.get("sold_out"):
        payload["sold_out_at"] = None

    # 作成時点ですでに終了日時を過ぎていた場合は非公開
    publish_end_at = payload.get("publish_end_at")

    if (
        publish_end_at is not None
        and publish_end_at <= _now_jst_naive()
    ):
        payload["is_active"] = False

    product = Product(**payload)

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product(
    db: Session,
    product_id: int,
    data: ProductUpdate,
):
    product = db.query(Product).get(product_id)

    if not product:
        return None

    payload = data.dict(exclude_unset=True)

    # 日時系を正規化
    for key in [
        "sold_out_at",
        "publish_start_at",
    ]:
        if key in payload:
            payload[key] = _normalize_optional_datetime(payload[key])

    if "publish_end_at" in payload:
        payload["publish_end_at"] = _normalize_publish_end_at(
            payload["publish_end_at"]
        )

    for key, value in payload.items():
        setattr(product, key, value)

    # 売り切れOFFなら日時も消す
    if not product.sold_out:
        product.sold_out_at = None

    # 終了日時を過ぎていたら強制的に公開OFF
    if (
        product.publish_end_at is not None
        and product.publish_end_at <= _now_jst_naive()
    ):
        product.is_active = False

    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).get(product_id)

    if product:
        db.delete(product)
        db.commit()