"""Unit tests for class and course management."""

import unittest

from app.models.course import Course
from app.schemas.course import CourseCreate
from tests.base import BaseTestCase


class TestCourseCreation(BaseTestCase):
    """Tests for course creation."""

    def test_course_creation(self) -> None:
        """Test creating a course."""
        user = self.create_registered_user()
        course = Course(
            name=self.test_class_data["name"],
            description=self.test_class_data["description"],
            semester=self.test_class_data["semester"],
            user_id=user.id,
        )
        self.db_session.add(course)
        self.db_session.commit()
        self.db_session.refresh(course)

        assert course.id is not None
        assert course.name == self.test_class_data["name"]
        assert course.description == self.test_class_data["description"]
        assert course.semester == self.test_class_data["semester"]
        assert course.user_id == user.id

    def test_course_model_fields(self) -> None:
        """Test that all required course model fields are present."""
        user = self.create_registered_user()
        course = Course(
            name=self.test_class_data["name"],
            description=self.test_class_data["description"],
            semester=self.test_class_data["semester"],
            user_id=user.id,
        )
        self.db_session.add(course)
        self.db_session.commit()
        self.db_session.refresh(course)

        assert hasattr(course, "id")
        assert hasattr(course, "name")
        assert hasattr(course, "description")
        assert hasattr(course, "semester")
        assert hasattr(course, "user_id")
        assert hasattr(course, "created_at")

    def test_multiple_courses_same_user(self) -> None:
        """Test creating multiple courses for the same user."""
        user = self.create_registered_user()
        course1 = Course(
            name="Course 1",
            description="First course",
            semester="Fall 2025",
            user_id=user.id,
        )
        course2 = Course(
            name="Course 2",
            description="Second course",
            semester="Spring 2026",
            user_id=user.id,
        )
        self.db_session.add(course1)
        self.db_session.add(course2)
        self.db_session.commit()

        courses = self.db_session.query(Course).filter_by(user_id=user.id).all()
        assert len(courses) == 2

    def test_course_schema_validation(self) -> None:
        """Test course schema validation."""
        course_data = {
            "name": "Test Course",
            "description": "A test course",
            "semester": "Fall 2025",
        }
        course_create = CourseCreate(**course_data)
        assert course_create.name == course_data["name"]
        assert course_create.description == course_data["description"]
        assert course_create.semester == course_data["semester"]

    def test_course_relationships(self) -> None:
        """Test course relationships with user."""
        user = self.create_registered_user()
        course = Course(
            name="Test Course",
            description="Test",
            semester="Fall 2025",
            user_id=user.id,
        )
        self.db_session.add(course)
        self.db_session.commit()

        assert course.user_id == user.id


if __name__ == "__main__":
    unittest.main()
