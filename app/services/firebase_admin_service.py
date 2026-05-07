import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials, messaging


_FIREBASE_APP_INITIALIZED = False


def init_firebase_admin():
    global _FIREBASE_APP_INITIALIZED

    if _FIREBASE_APP_INITIALIZED:
        return

    if firebase_admin._apps:
        _FIREBASE_APP_INITIALIZED = True
        return

    cred_path = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH",
        "/etc/keiba-ai-concierge/firebase/service-account.json",
    )

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

    _FIREBASE_APP_INITIALIZED = True


def send_push_to_token(
    *,
    token: str,
    title: str,
    body: str,
    target_path: Optional[str] = None,
):
    init_firebase_admin()

    data = {}
    if target_path:
        data["target_path"] = target_path

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        token=token,
    )

    return messaging.send(message)


def send_push_to_tokens(
    *,
    tokens: list[str],
    title: str,
    body: str,
    target_path: Optional[str] = None,
):
    init_firebase_admin()

    if not tokens:
        return {
            "success_count": 0,
            "failure_count": 0,
            "responses": [],
        }

    data = {}
    if target_path:
        data["target_path"] = target_path

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        tokens=tokens,
    )

    response = messaging.send_each_for_multicast(message)

    return {
        "success_count": response.success_count,
        "failure_count": response.failure_count,
        "responses": [
            {
                "success": r.success,
                "exception": str(r.exception) if r.exception else None,
            }
            for r in response.responses
        ],
    }