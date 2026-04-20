from pydantic import BaseModel


class DashboardSummary(BaseModel):
    product_count: int
    hit_result_count: int
    site_count: int
    article_count: int
    chat_faq_count: int
    chat_question_log_count: int
    needs_improvement_question_count: int