from fastapi import APIRouter

from app.routes import user

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(user.api_router)
