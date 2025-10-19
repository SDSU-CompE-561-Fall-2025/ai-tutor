from fastapi import APIRouter

from app.routes import user, file, course

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(user.api_router)
api_router.include_router(file.api_router)
api_router.include_router(course.api_router)
