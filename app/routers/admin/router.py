from fastapi import APIRouter
from app.routers.admin import auth, products, hit_results, chat_logs, mails, reviews


# app/routers/admin/router.py
router = APIRouter(
    prefix="/admin",
)


router.include_router(auth.router)
router.include_router(products.router)
router.include_router(hit_results.router)
router.include_router(chat_logs.router)
router.include_router(mails.router)   # ← 追加
router.include_router(reviews.router) # ← 追加