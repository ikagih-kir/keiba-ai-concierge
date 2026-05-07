from sqlalchemy.orm import Session

from app.services import firebase_admin_service
from app.services import push_token_service


def send_push_notification(
    db: Session,
    *,
    title: str,
    body: str,
    target_path: str | None = None,
):
    tokens = push_token_service.list_active_tokens(db)

    fcm_tokens = [
        item.fcm_token
        for item in tokens
        if item.fcm_token
    ]

    result = firebase_admin_service.send_push_to_tokens(
        tokens=fcm_tokens,
        title=title,
        body=body,
        target_path=target_path,
    )

    return {
        "success_count": result["success_count"],
        "failure_count": result["failure_count"],
        "total_count": len(fcm_tokens),
    }