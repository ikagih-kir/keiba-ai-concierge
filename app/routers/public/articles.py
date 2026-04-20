from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.article import ArticleOut
from app.services import article_service

router = APIRouter(
    prefix="/articles",
    tags=["Public Articles"],
)


@router.get("", response_model=List[ArticleOut])
def list_articles(
    db: Session = Depends(get_db),
):
    return article_service.list_public_articles(db)


@router.get("/{article_id}", response_model=ArticleOut)
def get_article_detail(
    article_id: int,
    db: Session = Depends(get_db),
):
    article = article_service.get_public_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article