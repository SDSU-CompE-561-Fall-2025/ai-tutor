from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 

import app.services.course as course_service
from app.core.auth import oauth2_scheme
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.course import CourseCreate, CourseResponse

api_router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@api_router.post("/")
async def create_category(
    course: CourseCreate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CourseResponse:
    """Create a new course"""
    user = get_current_user(token, db)
    return course_service.create_course(db, course, user.id)

@api_router.get("/")
async def get_courses(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> list[CourseResponse]:
    """Get all courses for the current user"""
    user = get_current_user(token, db)
    return course_service.get_courses(db, user.id)

@api_router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    """Delete a course by ID"""
    user = get_current_user(token, db)
    return course_service.delete_course(db, course_id, user.id)

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
async def get_course(
    course_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CourseResponse:
    """Get a course by ID"""
    user = get_current_user(token, db)
    return course_service.get_course_by_id(db, course_id, user.id)