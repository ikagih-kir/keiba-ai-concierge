# app/db/base.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# 🔥 ここで全モデルを登録
from app.models.product import Product  # noqa
from app.models.review import Review    # noqa
from app.models.hit_result import HitResult  # noqa
from app.models.user import User        # noqa
from app.models.admin import Admin      # noqa
from app.models.site import Site
from app.models.article import Article
from app.models.home_dialog import HomeDialog  # noqa
from app.models.push_token import PushToken  # noqa