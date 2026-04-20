from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assistant_message import AssistantMessageOut
from app.services import assistant_message_service

router = APIRouter(
    prefix="/assistant-messages",
    tags=["Public Assistant Messages"],
)


@router.get("", response_model=List[AssistantMessageOut])
def list_assistant_messages(
    target_date: Optional[date] = Query(None, description="対象日"),
    target_segment: Optional[str] = Query(None, description="対象セグメント"),
    db: Session = Depends(get_db),
):
    return assistant_message_service.list_public_assistant_messages(
        db,
        target_date=target_date,
        target_segment=target_segment,
    )


@router.get("/today", response_model=List[AssistantMessageOut])
def list_today_assistant_messages(
    target_segment: Optional[str] = Query(None, description="対象セグメント"),
    db: Session = Depends(get_db),
):
    today = date.today()
    return assistant_message_service.list_public_assistant_messages(
        db,
        target_date=today,
        target_segment=target_segment,
    )


@router.get("/{item_id}", response_model=AssistantMessageOut)
def get_assistant_message_detail(
    item_id: int,
    db: Session = Depends(get_db),
):
    return assistant_message_service.get_public_assistant_message(db, item_id)