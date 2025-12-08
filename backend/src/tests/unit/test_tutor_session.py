"""Unit tests for tutor session repository operations."""

import unittest

from app.core.auth import get_password_hash
from app.repository.course import CourseRepository
from app.repository.tutor_session import TutorSessionRepository
from app.repository.user import UserRepository
from app.schemas.course import CourseCreate
from app.schemas.tutor_session import TutorSessionCreate
from app.schemas.user import UserCreate
from tests.base import BaseTestCase


class TestTutorSessionRepository(BaseTestCase):
    """Tests for tutor session repository operations."""

    def setUp(self) -> None:
        """Set up test fixtures with user, course, and database session."""
        super().setUp()
        hashed_password = get_password_hash(self.test_user_data["password"])
        # Create a registered user for tutor session tests
        user_create = UserCreate(**self.test_user_data)
        self.user = UserRepository.create(
            self.db_session,
            user_create,
            hashed_password,
        )
        # Create a course for the user
        course_data = CourseCreate(**self.test_class_data)
        self.course = CourseRepository.create(
            self.db_session,
            course_data,
            self.user.id,
        )

    def test_tutor_session_create(self) -> None:
        """Test creating a tutor session via repository."""
        session_data = TutorSessionCreate(
            title="Test Session",
            course_id=self.course.id,
        )
        session = TutorSessionRepository.create(
            self.db_session,
            session_data,
            self.user.id,
        )

        assert session.id is not None
        assert session.title == "Test Session"
        assert session.course_id == self.course.id
        assert session.user_id == self.user.id

    def test_tutor_session_get_by_id(self) -> None:
        """Test retrieving a tutor session by ID via repository."""
        session_data = TutorSessionCreate(
            title="Test Session",
            course_id=self.course.id,
        )
        created_session = TutorSessionRepository.create(
            self.db_session,
            session_data,
            self.user.id,
        )

        retrieved_session = TutorSessionRepository.get_by_id(
            self.db_session,
            created_session.id,
        )

        assert retrieved_session is not None
        assert retrieved_session.id == created_session.id
        assert retrieved_session.title == "Test Session"

    def test_tutor_session_get_by_course(self) -> None:
        """Test retrieving a tutor session by course via repository."""
        session_data = TutorSessionCreate(
            title="Test Session",
            course_id=self.course.id,
        )
        created_session = TutorSessionRepository.create(
            self.db_session,
            session_data,
            self.user.id,
        )

        retrieved_session = TutorSessionRepository.get_by_course(
            self.db_session,
            self.course.id,
        )

        assert retrieved_session is not None
        assert retrieved_session.id == created_session.id
        assert retrieved_session.course_id == self.course.id

    def test_tutor_session_get_by_user(self) -> None:
        """Test retrieving a tutor session by user via repository."""
        session_data = TutorSessionCreate(
            title="Test Session",
            course_id=self.course.id,
        )
        created_session = TutorSessionRepository.create(
            self.db_session,
            session_data,
            self.user.id,
        )

        retrieved_session = TutorSessionRepository.get_by_user(
            self.db_session,
            self.user.id,
        )

        assert retrieved_session is not None
        assert retrieved_session.id == created_session.id
        assert retrieved_session.user_id == self.user.id

    def test_tutor_session_delete(self) -> None:
        """Test deleting a tutor session via repository."""
        session_data = TutorSessionCreate(
            title="Test Session",
            course_id=self.course.id,
        )
        created_session = TutorSessionRepository.create(
            self.db_session,
            session_data,
            self.user.id,
        )

        TutorSessionRepository.delete(self.db_session, created_session)

        retrieved_session = TutorSessionRepository.get_by_id(
            self.db_session,
            created_session.id,
        )

        assert retrieved_session is None

    def test_tutor_session_get_by_id_not_found(self) -> None:
        """Test that get_by_id returns None for non-existent session."""
        retrieved_session = TutorSessionRepository.get_by_id(
            self.db_session,
            9999,
        )

        assert retrieved_session is None


if __name__ == "__main__":
    unittest.main()
