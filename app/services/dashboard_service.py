from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.hit_result import HitResult
from app.models.site import Site
from app.models.article import Article
from app.models.chat_faq import ChatFaq
from app.models.chat_question_log import ChatQuestionLog


def get_dashboard_summary(db: Session):
    product_count = db.query(Product).count()
    hit_result_count = db.query(HitResult).count()
    site_count = db.query(Site).count()
    article_count = db.query(Article).count()
    chat_faq_count = db.query(ChatFaq).count()
    chat_question_log_count = db.query(ChatQuestionLog).count()
    needs_improvement_question_count = (
        db.query(ChatQuestionLog)
        .filter(ChatQuestionLog.needs_improvement == True)
        .count()
    )

    return {
        "product_count": product_count,
        "hit_result_count": hit_result_count,
        "site_count": site_count,
        "article_count": article_count,
        "chat_faq_count": chat_faq_count,
        "chat_question_log_count": chat_question_log_count,
        "needs_improvement_question_count": needs_improvement_question_count,
    }