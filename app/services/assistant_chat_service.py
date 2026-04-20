import json
import re
from sqlalchemy.orm import Session

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
        },

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

    faq = chat_faq_repository.find_active_faq_by_normalized_question(db, normalized)

    if faq:
        suggested_actions = []
        if faq.suggested_actions_json:
            try:
                suggested_actions = json.loads(faq.suggested_actions_json)
            except Exception:
                suggested_actions = []

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