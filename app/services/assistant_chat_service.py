import json
import re
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.chat_faq import ChatFaq

from app.repositories import (
    chat_thread_repository,
    chat_message_repository,
    chat_question_log_repository,
    chat_faq_repository,
)




def normalize_question(text: str) -> str:
    text = text.strip().lower()

    # 記号除去
    text = re.sub(r"[！？?!.。、,，/／]", " ", text)

    # よくある助詞・語尾をざっくり空白化
    replace_words = [
        "です",
        "ます",
        "ください",
        "について",
        "とは",
        "って何",
        "ってなに",
        "なに",
        "何",
        "は",
        "が",
        "を",
        "に",
        "の",
        "で",
        "と",
        "も",
    ]

    for word in replace_words:
        text = text.replace(word, " ")

    # 空白整理
    text = re.sub(r"\s+", " ", text).strip()
    return text

def _safe_json_loads(value):
    if not value:
        return []

    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return parsed
        return []
    except Exception:
        return []


def _score_faq_match(message: str, normalized: str, faq: ChatFaq) -> int:
    score = 0

    raw_text = (message or "").strip().lower()
    normalized_text = (normalized or "").strip().lower()

    faq_normalized = (faq.normalized_question or "").strip().lower()
    question_pattern = (faq.question_pattern or "").strip().lower()

    # 1. 正規化質問の完全一致
    if faq_normalized and normalized_text == faq_normalized:
        score += 100

    # 2. 正規化質問の部分一致
    if faq_normalized and (
        faq_normalized in normalized_text or normalized_text in faq_normalized
    ):
        score += 70

    # 3. 質問パターンの部分一致
    if question_pattern and (
        question_pattern in raw_text or raw_text in question_pattern
    ):
        score += 50

    # 4. keywords_json の一致
    keywords = _safe_json_loads(faq.keywords_json)
    for keyword in keywords:
        kw = str(keyword).strip().lower()
        if not kw:
            continue

        normalized_kw = normalize_question(kw)

        if kw in raw_text:
            score += 25

        if normalized_kw and normalized_kw in normalized_text:
            score += 25

    # 5. 何かしら一致したFAQだけ、優先度を少し加点
    if score > 0:
        score += min(int(faq.priority or 0), 30)

    return score


def find_best_faq(db: Session, message: str, normalized: str, intent: str):
    faqs = (
        db.query(ChatFaq)
        .filter(ChatFaq.is_active.is_(True))
        .order_by(ChatFaq.priority.desc(), ChatFaq.id.desc())
        .all()
    )

    best_faq = None
    best_score = 0

    for faq in faqs:
        score = _score_faq_match(message, normalized, faq)

        # intent が一致していたら加点
        if faq.intent and faq.intent == intent:
            score += 30

        if score > best_score:
            best_score = score
            best_faq = faq

    # 低すぎるスコアは誤爆防止で不採用
    if best_score < 40:
        return None

    return best_faq



def detect_intent(message: str) -> str:
    text = message.lower()

    if "ニュース" in text or "最新情報" in text or "情報を教えて" in text:
        return "racing_news_request"
    if "ランキング" in text:
        return "ranking_question"
    if "無料予想" in text:
        return "free_prediction_question"
    if "枠順" in text or "ラッキー枠" in text:
        return "frame_trend_question"
    if (
        "騎手" in text
        or "ジョッキー" in text
        or "勝利騎手" in text
        or "好調な騎手" in text
        or "注目騎手" in text
    ):
        return "jockey_trend_question"
    
    if "記事" in text:
        return "article_question"    

    if "クチコミ" in text or "口コミ" in text:
        return "review_question"
    if "ipat" in text:
        return "ipat_request"
    if "spat4" in text:
        return "spat4_request"
    if "ライブ" in text or "映像" in text:
        return "live_view_request"
    if "日程" in text or "開催日程" in text:
        return "schedule_request"
    if "ログイン" in text:
        return "external_link_request"
    if "初心者" in text:
        return "beginner_question"
    if "おすすめサイト" in text or "サイト" in text:
        return "site_compare"

    return "general_racing_term"


def build_fallback_response(intent: str):
    if intent == "ranking_question":
        return {
            "assistant_message": "ランキングページで、的中金額・的中率・回収率の上位サイトを確認できます。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {"type": "open_page", "label": "ランキングを見る", "path": "/rankings"},
            ],
        }
    if intent == "frame_trend_question":
        return {
            "assistant_message": "枠順トレンドページで、その日のラッキー枠を確認できます。表示更新ボタンから最新表示に更新してください。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {"type": "open_page", "label": "枠順トレンドを見る", "path": "/frame-trends"},
            ],
        }
    
    if intent == "jockey_trend_question":
        return {
            "assistant_message": "騎手トレンドページで、本日の1〜6Rの勝利騎手や好調な騎手を確認できます。競馬場ごとの序盤レース結果から、注目騎手をチェックできます。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {"type": "open_page", "label": "騎手トレンドを見る", "path": "/jockey-trends"},
            ],
        }

    if intent == "article_question":
        return {
            "assistant_message": "検証結果や比較記事は記事一覧から確認できます。気になるテーマがあれば記事から見るのがおすすめです。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {"type": "open_page", "label": "記事を見る", "path": "/articles"},
            ],
        }
    if intent == "external_link_request":
        return {
            "assistant_message": "必要な公式ページへ直接移動できます。目的に合わせて選んでください。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {
                    "type": "open_url",
                    "label": "iPATを開く",
                    "url": "https://www.ipat.jra.go.jp/",
                },
                {
                    "type": "open_url",
                    "label": "SPAT4を開く",
                    "url": "https://www.spat4.jp/keiba/",
                },
                {
                    "type": "open_page",
                    "label": "便利リンクを見る",
                    "path": "/external-links",
                },
            ],
        }

    if intent == "ipat_request":
        return {
            "assistant_message": "iPAT のログインページを開けます。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {
                    "type": "open_url",
                    "label": "iPATを開く",
                    "url": "https://www.ipat.jra.go.jp/",
                }
            ],
        }

    if intent == "spat4_request":
        return {
            "assistant_message": "SPAT4 のページを開けます。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {
                    "type": "open_url",
                    "label": "SPAT4を開く",
                    "url": "https://www.spat4.jp/keiba/",
                }
            ],
        }

    if intent == "live_view_request":
        return {
            "assistant_message": "地方競馬ライブのページを開けます。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {
                    "type": "open_url",
                    "label": "地方競馬ライブを開く",
                    "url": "https://www.keiba.go.jp/live/",
                }
            ],
        }

    if intent == "schedule_request":
        return {
            "assistant_message": "JRA開催日程ページを開けます。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {
                    "type": "open_url",
                    "label": "JRA開催日程を開く",
                    "url": "https://www.jra.go.jp/keiba/calendar/",
                }
            ],
        }
    if intent == "racing_news_request":
        return {
            "assistant_message": "競馬に関するニュースや最新情報は、ニュース一覧ページから確認できます。気になる話題をまとめて見たいときに便利です。",
            "answered_by": "fallback",
            "source_summary": "assistant fallback",
            "suggested_actions": [
                {
                    "type": "open_url",
                    "label": "競馬ニュースを見る",
                    "url": "https://news.netkeiba.com/",
                }
            ],
        }

    return {
        "assistant_message": "ご質問ありがとうございます。必要ならランキング、無料予想、記事、枠順トレンドから案内できます。",
        "answered_by": "fallback",
        "source_summary": "assistant fallback",
        "suggested_actions": [
            {"type": "open_page", "label": "ランキングを見る", "path": "/rankings"},
            {"type": "open_page", "label": "無料予想を見る", "path": "/free-predictions"},
        ],
    }


def send_chat_message(db: Session, thread_id: int | None, message: str, user_id: int | None = None):
    if thread_id is None:
        thread = chat_thread_repository.create_thread(db, user_id=user_id)
    else:
        thread = chat_thread_repository.get_thread(db, thread_id)
        if not thread:
            thread = chat_thread_repository.create_thread(db, user_id=user_id)

    normalized = normalize_question(message)
    intent = detect_intent(message)

    user_message = chat_message_repository.create_message(
        db=db,
        thread_id=thread.id,
        role="user",
        content=message,
        intent=intent,
        normalized_question=normalized,
        user_id=user_id,
    )

    chat_thread_repository.update_thread_after_user_message(
        db=db,
        item=thread,
        last_user_message=message,
    )

    faq = find_best_faq(
        db=db,
        message=message,
        normalized=normalized,
        intent=intent,
    )

    if faq:
        suggested_actions = []
        if faq.suggested_actions_json:
            try:
                suggested_actions = json.loads(faq.suggested_actions_json)
            except Exception:
                suggested_actions = []

        faq.usage_count = (faq.usage_count or 0) + 1
        faq.last_used_at = datetime.now()
        db.add(faq)

        assistant_message_text = faq.answer_text
        answered_by = "faq"
        source_summary = f"faq #{faq.id}"
        faq_id = faq.id
        

    else:
        fallback = build_fallback_response(intent)
        assistant_message_text = fallback["assistant_message"]
        answered_by = fallback["answered_by"]
        source_summary = fallback["source_summary"]
        suggested_actions = fallback["suggested_actions"]
        faq_id = None

    assistant_message = chat_message_repository.create_message(
        db=db,
        thread_id=thread.id,
        role="assistant",
        content=assistant_message_text,
        intent=intent,
        normalized_question=normalized,
        answered_by=answered_by,
        source_summary=source_summary,
        suggested_actions_json=json.dumps(suggested_actions, ensure_ascii=False),
        model_name="faq_or_fallback",
        user_id=user_id,
    )

    chat_question_log_repository.create_question_log(
        db=db,
        thread_id=thread.id,
        message_id=user_message.id,
        user_id=user_id,
        raw_question=message,
        normalized_question=normalized,
        intent=intent,
        sub_intent=None,
        answered_by=answered_by,
        faq_id=faq_id,
        is_answered_successfully=True,
        needs_improvement=(answered_by == "fallback"),
    )

    return {
        "thread_id": thread.id,
        "assistant_message": assistant_message.content,
        "intent": intent,
        "answered_by": answered_by,
        "suggested_actions": suggested_actions,
        "source_summary": source_summary,
    }


def create_thread(db: Session, user_id: int | None = None):
    return chat_thread_repository.create_thread(db, user_id=user_id)


def get_thread_detail(db: Session, thread_id: int):
    thread = chat_thread_repository.get_thread(db, thread_id)
    if not thread:
        return None

    messages = chat_message_repository.list_messages_by_thread(db, thread_id)
    return {
        "thread": thread,
        "messages": messages,
    }