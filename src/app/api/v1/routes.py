from fastapi import APIRouter

from app.routes import google_drive, user

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(user.api_router)
api_router.include_router(google_drive.api_router)
