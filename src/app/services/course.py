from  sqlalchemy.orm import Session

from app.models.course import Course
from app.models.file import File
from app.repository.course import CourseRepository
from app.schemas.course import CourseBase, CourseCreate

def create_course(
    db: Session, 
    course: CourseBase, 
    user_id: int
) -> Course:
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
        return {"error": msg}

    return CourseRepository.create(db, course, user_id)

def get_courses(
    db: Session, 
    user_id: int,
    course_id: int
) -> list[Course]:
    """
    Get all courses for a user. 

    Args: 
        db: database session
        user_id: id of the user
    """
    return CourseRepository.get_all(db, user_id, course_id)

def delete_course(
    db: Session, 
    course_id: int, 
    user_id: int
) -> None:
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
        raise ValueError(msg)

    # Check if course has associated files
    associated_files = db.query(File).filter(File.course_id == course_id).count()
    if associated_files > 0:
        msg = "Cannot delete course with associated files. Delete the files first."
        raise ValueError(msg)

    CourseRepository.delete(db, course)

def update_course(
    db: Session, 
    course_id: int, 
    course_data: CourseCreate, 
    user_id: int
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
        raise ValueError(msg)
    
    existing_course = CourseRepository.get_course_by_name(db, course_data.name, user_id)
    if existing_course and existing_course.id != course_id:
        msg = "Course with this name already exists."
        raise ValueError(msg)

    course.name = course_data.name
    return CourseRepository.update(db, course)

def get_course_by_id(
    db: Session, 
    course_id: int, 
    user_id: int
) -> Course:
    """
    Get a course by ID

    Args: 
        db: database session
        course_id: id of the course to retrieve
        user_id: id of the user

    Returns:
        Course: Retrieved course instance
    """
    category = CourseRepository.get_course_by_id(db, course_id)
    if not category or category.user_id != user_id:
        msg = "Course not found or access denied."
        raise ValueError(msg)

    return category