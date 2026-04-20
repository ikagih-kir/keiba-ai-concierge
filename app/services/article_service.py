from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import article_repository
from app.schemas.article import ArticleCreate, ArticleUpdate


def list_articles(db: Session):
    return article_repository.list_articles(db)


def get_article(db: Session, article_id: int):
    article = article_repository.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="記事が見つかりません")
    return article


def create_article(db: Session, data: ArticleCreate):
    existing = article_repository.get_article_by_slug(db, data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="このslugはすでに使用されています")

    return article_repository.create_article(db, data)


def update_article(db: Session, article_id: int, data: ArticleUpdate):
    article = article_repository.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="記事が見つかりません")

    if data.slug is not None:
        existing = article_repository.get_article_by_slug(db, data.slug)
        if existing and existing.id != article_id:
            raise HTTPException(status_code=400, detail="このslugはすでに使用されています")

    return article_repository.update_article(db, article, data)


def delete_article(db: Session, article_id: int):
    article = article_repository.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="記事が見つかりません")

    article_repository.delete_article(db, article)
    return {"message": "記事を削除しました"}


def toggle_article_public(db: Session, article_id: int, is_public: bool):
    article = article_repository.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="記事が見つかりません")

    return article_repository.toggle_article_public(db, article, is_public)


def list_public_articles(db: Session):
    return article_repository.list_public_articles(db)


def get_public_article(db: Session, article_id: int):
    return article_repository.get_public_article_by_id(db, article_id)