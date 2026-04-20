from app.routers import admin_hit_results
from fastapi import APIRouter

router = APIRouter()
router.include_router(admin_hit_results.router)