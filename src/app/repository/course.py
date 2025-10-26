"""
Course Repository 

This module provides data access layer for course operations.
"""

from sqlalchemy.orm import Session

from app.models.course import Course 
from app.schemas.course import CourseBase

class CourseRepository: 
    """Repository for Course data access"""
    
    @staticmethod
    def get_course_by_name(
        db: Session,
        course_name: str,
        user_id: int
    ) -> Course | None:
        """
        Get course by name

        Args: 
            db (Session): database session
            course_name (str): name of the course to retrieve
            user_id (int): ID of the user requesting the course
        """
        return db.query(Course).filter(Course.name == course_name, Course.user_id == user_id).first()
    
    @staticmethod
    def get_course_by_id(
        db: Session,
        course_id: int,
    ) -> Course | None:
        """
        Get course by ID

        Args: 
            db (Session): database session
            course_id (int): ID of the course to retrieve
            user_id (int): ID of the user requesting the course
        """
        return db.query(Course).filter(Course.id == course_id).first()
    
    @staticmethod
    def create(
        db: Session, 
        course: CourseBase,
        user_id: int
    ) -> Course: 
        """
        Create a new course. 
        
        Args: 
            db (Session): database session
            course (CourseBase): course data
            user_id (int): ID of the user creating the course
        """

        db_course = Course(
            name = course.name, 
            user_id = user_id,
        )

        db.add(db_course)
        db.commit() 
        db.refresh(db_course)
        return db_course
    
    @staticmethod
    def update(
        db: Session, 
        db_course: Course
    ) -> Course:
        """
        Update a course

        Args: 
            db (Session): database session
            db_course (Course): Course instance to update
        """
        db.commit() 
        db.refresh(db_course)
        return db_course

    @staticmethod
    def delete(
        db: Session, 
        db_course: Course
    ) -> None:
        """
        Delete a course

        Args: 
            db (Session): database session
            db_course (Course): Course instance to delete
        """
        db.delete(db_course)
        db.commit()

    @staticmethod
    def get_all(db: Session, user_id: int, course_id: int) -> list[Course]:
        """
        Get all courses for a user

        Args:
            db: database session
            user_id: ID of the user to retrieve courses for
        """
        return db.query(Course).filter(Course.id == course_id, Course.user_id == user_id).all()