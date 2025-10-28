from fastapi import APIRouter

from app.routes import chat_message, google_drive, tutor_session, user

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(user.api_router)
api_router.include_router(google_drive.api_router)
api_router.include_router(tutor_session.api_router)
api_router.include_router(chat_message.api_router)
