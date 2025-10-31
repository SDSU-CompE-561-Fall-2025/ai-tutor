from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.tutor_session import TutorSession
from app.repository.course import CourseRepository
from app.repository.tutor_session import TutorSessionRepository
from app.schemas.course import CourseBase, CourseCreate


def create_course(db: Session, course: CourseBase, user_id: int) -> Course:
    """
    Create a new course

    Args:
        db: database session
        course: course creation data
        user_id: id of the user creating the course

    Returns:
        Course: Created course instance
    """
    existing_course = CourseRepository.get_course_by_name(db, course.name, user_id)
    if existing_course:
        msg = "Course with this name already exists."
        raise HTTPException(status_code=409, detail=msg)

    return CourseRepository.create(db, course, user_id)


def get_courses(
    db: Session,
    user_id: int,
) -> list[Course]:
    """
    Get all courses for a user.

    Args:
        db: database session
        user_id: id of the user
    """
    courses = CourseRepository.get_all(db, user_id)

    if courses is None:
        raise HTTPException(status_code=404, detail="No courses found for the user.")

    return courses

def delete_course(db: Session, course_id: int, user_id: int) -> None:
    """
    Delete a course by ID

    Args:
        db: database session
        course_id: id of the course to delete
        user_id: id of the user

    Returns:
        None
    """
    course = CourseRepository.get_course_by_id(db, course_id)
    if course is None or course.user_id != user_id:
        msg = "Course not found or access denied."
        raise HTTPException(status_code=404, detail=msg)

    CourseRepository.delete(db, course)


def update_course(
    db: Session,
    course_id: int,
    course_data: CourseCreate,
    user_id: int,
) -> Course:
    """
    Update a course by ID

    Args:
        db: database session
        course_id: id of the course to update
        course_data: new course data
        user_id: id of the user

    Returns:
        Course: Updated course instance
    """
    course = CourseRepository.get_course_by_id(db, course_id)
    if course is None or course.user_id != user_id:
        msg = "Course not found or access denied."
        raise HTTPException(status_code=404, detail=msg)

    existing_course = CourseRepository.get_course_by_name(db, course_data.name, user_id)
    if existing_course and existing_course.id != course_id:
        msg = "Course with this name already exists."
        raise HTTPException(status_code=409, detail=msg)

    course.name = course_data.name
    return CourseRepository.update(db, course)


def get_course_by_id(db: Session, course_id: int, user_id: int) -> Course:
    """
    Get a course by ID

    Args:
        db: database session
        course_id: id of the course to retrieve
        user_id: id of the user

    Returns:
        Course: Retrieved course instance
    """
    course = CourseRepository.get_course_by_id(db, course_id)
    if not course or course.user_id != user_id:
        msg = "Course not found or access denied."
        raise HTTPException(status_code=404, detail=msg)

    return course


def get_tutor_sessions_by_course(
    db: Session,
    course_id: int,
    user_id: int,
) -> list[TutorSession]:
    """
    Get all tutor sessions for a course

    Args:
        db: database session
        course_id: id of the course
        user_id: id of the user

    Returns:
        list: List of tutor sessions for the course
    """
    # Verify course exists and belongs to user
    course = CourseRepository.get_course_by_id(db, course_id)
    if not course or course.user_id != user_id:
        msg = "Course not found or access denied."
        raise HTTPException(status_code=404, detail=msg)

    return TutorSessionRepository.get_all_for_course(db, course_id)
