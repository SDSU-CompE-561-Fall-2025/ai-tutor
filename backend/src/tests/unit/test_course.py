"""Unit tests for course repository operations."""

import unittest

from app.core.auth import get_password_hash
from app.repository.course import CourseRepository
from app.repository.user import UserRepository
from app.schemas.course import CourseCreate
from app.schemas.user import UserCreate
from tests.base import BaseTestCase


class TestCourseRepository(BaseTestCase):
    """Tests for course repository operations."""

    def setUp(self) -> None:
        """Set up test fixtures with user and database session."""
        super().setUp()
        # Create a registered user for course tests
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)
        self.user = UserRepository.create(
            self.db_session,
            user_create,
            hashed_password,
        )

    def test_course_create(self) -> None:
        """Test creating a course via repository."""
        course_data = CourseCreate(**self.test_class_data)
        course = CourseRepository.create(self.db_session, course_data, self.user.id)

        assert course.id is not None
        assert course.name == self.test_class_data["name"]
        assert course.user_id == self.user.id

    def test_course_get_by_name(self) -> None:
        """Test retrieving a course by name via repository."""
        course_data = CourseCreate(**self.test_class_data)
        created_course = CourseRepository.create(
            self.db_session,
            course_data,
            self.user.id,
        )

        retrieved_course = CourseRepository.get_course_by_name(
            self.db_session,
            self.test_class_data["name"],
            self.user.id,
        )

        assert retrieved_course is not None
        assert retrieved_course.id == created_course.id
        assert retrieved_course.name == self.test_class_data["name"]

    def test_course_get_by_id(self) -> None:
        """Test retrieving a course by ID via repository."""
        course_data = CourseCreate(**self.test_class_data)
        created_course = CourseRepository.create(
            self.db_session,
            course_data,
            self.user.id,
        )

        retrieved_course = CourseRepository.get_course_by_id(
            self.db_session,
            created_course.id,
        )

        assert retrieved_course is not None
        assert retrieved_course.id == created_course.id
        assert retrieved_course.name == self.test_class_data["name"]

    def test_course_get_all(self) -> None:
        """Test retrieving all courses for a user via repository."""
        course_data1 = CourseCreate(**self.test_class_data)
        course_data2 = CourseCreate(
            name="Another Test Class",
            description="Another test class",
            semester="Spring 2026",
        )
        CourseRepository.create(self.db_session, course_data1, self.user.id)
        CourseRepository.create(self.db_session, course_data2, self.user.id)

        courses = CourseRepository.get_all(self.db_session, self.user.id)

        assert len(courses) == 2

    def test_course_delete(self) -> None:
        """Test deleting a course via repository."""
        course_data = CourseCreate(**self.test_class_data)
        created_course = CourseRepository.create(
            self.db_session,
            course_data,
            self.user.id,
        )

        CourseRepository.delete(self.db_session, created_course)

        retrieved_course = CourseRepository.get_course_by_id(
            self.db_session,
            created_course.id,
        )

        assert retrieved_course is None

    def test_course_get_by_name_not_found(self) -> None:
        """Test that get_course_by_name returns None for non-existent course."""
        retrieved_course = CourseRepository.get_course_by_name(
            self.db_session,
            "Nonexistent Course",
            self.user.id,
        )

        assert retrieved_course is None


if __name__ == "__main__":
    unittest.main()
