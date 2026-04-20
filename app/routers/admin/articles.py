from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_admin
from app.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleOut,
    ArticlePublicToggle,
)
from app.services import article_service

router = APIRouter(
    prefix="/articles",
    tags=["Admin Articles"],
)


@router.get("", response_model=List[ArticleOut])
def list_articles(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return article_service.list_articles(db)


@router.get("/{article_id}", response_model=ArticleOut)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return article_service.get_article(db, article_id)


@router.post("", response_model=ArticleOut)
def create_article(
    data: ArticleCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return article_service.create_article(db, data)


@router.put("/{article_id}", response_model=ArticleOut)
def update_article(
    article_id: int,
    data: ArticleUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return article_service.update_article(db, article_id, data)


@router.post("/{article_id}/toggle_public", response_model=ArticleOut)
def toggle_article_public(
    article_id: int,
    data: ArticlePublicToggle,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return article_service.toggle_article_public(db, article_id, data.is_public)


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return article_service.delete_article(db, article_id)