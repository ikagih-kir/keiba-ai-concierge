from sqlalchemy.orm import Session
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


def list_articles(db: Session):
    return (
        db.query(Article)
        .order_by(Article.sort_order.asc(), Article.id.desc())
        .all()
    )


def get_article_by_id(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def get_article_by_slug(db: Session, slug: str):
    return db.query(Article).filter(Article.slug == slug).first()


def create_article(db: Session, data: ArticleCreate):
    article = Article(
        title=data.title,
        slug=data.slug,
        category=data.category,
        excerpt=data.excerpt,
        body=data.body,
        thumbnail_url=data.thumbnail_url,
        banner_url=data.banner_url,
        is_featured=data.is_featured,
        is_public=data.is_public,
        sort_order=data.sort_order,
        published_at=data.published_at,
    )

    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def update_article(db: Session, article: Article, data: ArticleUpdate):
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article: Article):
    db.delete(article)
    db.commit()


def toggle_article_public(db: Session, article: Article, is_public: bool):
    article.is_public = is_public
    db.commit()
    db.refresh(article)
    return article


def list_public_articles(db: Session):
    return (
        db.query(Article)
        .filter(Article.is_public == True)
        .order_by(Article.published_at.desc(), Article.id.desc())
        .all()
    )


def get_public_article_by_id(db: Session, article_id: int):
    return (
        db.query(Article)
        .filter(
            Article.id == article_id,
            Article.is_public == True,
        )
        .first()
    )