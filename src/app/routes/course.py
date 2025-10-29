from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.course as course_service
from app.core.auth import oauth2_scheme
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.course import CourseCreate, CourseResponse
from app.schemas.tutor_session import TutorSessionResponse

api_router = APIRouter(prefix="/courses", tags=["courses"])


@api_router.post("/")
async def create_course(
    course: CourseCreate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CourseResponse:
    """Create a new course"""
    user = get_current_user(token, db)
    return course_service.create_course(db, course, user.id)  # pyright: ignore[reportArgumentType]


@api_router.get("/")
async def get_all_courses(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> list[CourseResponse]:
    """Get all courses for the current user"""
    user = get_current_user(token, db)
    return course_service.get_courses(db, user.id)  # pyright: ignore[reportReturnType, reportArgumentType]


@api_router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    """Delete a course by ID"""
    user = get_current_user(token, db)
    return course_service.delete_course(db, course_id, user.id)  # pyright: ignore[reportArgumentType]


@api_router.put("/{course_id}")
async def update_course(
    course_id: int,
    course: CourseCreate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CourseResponse:
    """Update a course by ID"""
    user = get_current_user(token, db)
    return course_service.update_course(db, course_id, course, user.id)


@api_router.get("/{course_id}")
async def get_course_by_id(
    course_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CourseResponse:
    """Get a course by ID"""
    user = get_current_user(token, db)
    return course_service.get_course_by_id(db, course_id, user.id)


@api_router.get("/{course_id}/tutor-sessions")
async def get_tutor_sessions_by_course(
    course_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> list[TutorSessionResponse]:
    """Get all tutor sessions for a course"""
    user = get_current_user(token, db)
    tutor_sessions = course_service.get_tutor_sessions_by_course(
        db,
        course_id,
        user.id,
    )
    return [
        TutorSessionResponse(
            id=tutor_session.id,  # pyright: ignore[reportArgumentType]
            title=tutor_session.title,  # pyright: ignore[reportArgumentType]
            course_name=tutor_session.course.name,
            chat_messages=tutor_session.chat_messages,
            created_at=tutor_session.created_at,  # pyright: ignore[reportArgumentType]
        )
        for tutor_session in tutor_sessions
    ]
