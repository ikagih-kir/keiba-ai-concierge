from app.db.base import Base

# 🔽 必ずこの順で
from app.models.user import User
from app.models.admin import Admin
from app.models.product import Product   # ← 必須・最優先
from app.models.review import Review
from app.models.hit_result import HitResult
from app.models.review_helpful_vote import ReviewHelpfulVote
from app.models.race import Race
from app.models.race_entry import RaceEntry
from app.models.condition_change_horse import ConditionChangeHorse
from app.models.frame_trend_input import FrameTrendInput
from app.models.chat_thread import ChatThread
from app.models.chat_message import ChatMessage
from app.models.chat_question_log import ChatQuestionLog
from app.models.chat_faq import ChatFaq