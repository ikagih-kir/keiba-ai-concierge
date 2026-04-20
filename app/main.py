from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.models import *  # noqa
from app.core.config import settings
from app.routers.admin.router import router as admin_router
from app.routers.admin.chat_ws import chat_ws

from app.routers.admin import mails as admin_mails
from app.routers.admin import dashboard
from app.routers.admin import sites as admin_sites
from app.routers.admin import articles as admin_articles

from app.routers.public import products as public_products
from app.routers.public import mails as public_mails
from app.routers.public import reviews as public_reviews
from app.routers.public import hit_results as public_hit_results
from app.routers.public import sites as public_sites
from app.routers.public import articles as public_articles
from app.routers.public.assistant_messages import router as assistant_messages_router
from app.routers.public.race_change_highlights import router as race_change_highlights_router
from app.routers.public.frame_trends import router as frame_trends_router

from app.routers.admin.assistant_messages import router as admin_assistant_messages_router
from app.routers.admin.race_change_highlights import router as admin_race_change_highlights_router
from app.routers.admin.frame_trends import router as admin_frame_trends_router

from app.routers.public import condition_changes as public_condition_changes
from app.routers.admin import condition_changes as admin_condition_changes
from app.routers.public import memorial as public_memorial
from app.routers.public.rankings import router as rankings_router

from app.routers.public.assistant_chat import router as assistant_chat_router
from app.routers.admin.chat_faqs import router as admin_chat_faqs_router
from app.routers.admin.chat_question_logs import router as admin_chat_question_logs_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await chat_ws(websocket, user_id)


# ----------------------------
# Admin
# ----------------------------
app.include_router(admin_router)
app.include_router(dashboard.router)
app.include_router(admin_sites.router, prefix="/admin")
app.include_router(admin_articles.router, prefix="/admin")
app.include_router(admin_assistant_messages_router, prefix="/admin")
app.include_router(admin_race_change_highlights_router, prefix="/admin")
app.include_router(admin_frame_trends_router, prefix="/admin")
app.include_router(admin_condition_changes.router, prefix="/admin")
app.include_router(admin_chat_faqs_router, prefix="/admin")
app.include_router(admin_chat_question_logs_router, prefix="/admin")

# ----------------------------
# Public
# ----------------------------
app.include_router(public_products.router)
app.include_router(public_mails.router)
app.include_router(public_reviews.router)
app.include_router(public_hit_results.router)
app.include_router(public_sites.router)
app.include_router(public_articles.router)
app.include_router(assistant_messages_router)
app.include_router(race_change_highlights_router)
app.include_router(frame_trends_router)
app.include_router(public_condition_changes.router)
app.include_router(public_memorial.router)
app.include_router(rankings_router)
app.include_router(assistant_chat_router)