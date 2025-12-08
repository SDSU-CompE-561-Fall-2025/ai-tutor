"""Unit tests for file repository operations."""

import unittest

from app.core.auth import get_password_hash
from app.repository.course import CourseRepository
from app.repository.file import FileRepository
from app.repository.user import UserRepository
from app.schemas.course import CourseCreate
from app.schemas.file import FileCreate
from app.schemas.user import UserCreate
from tests.base import BaseTestCase


class TestFileRepository(BaseTestCase):
    """Tests for file repository operations."""

    def setUp(self) -> None:
        """Set up test fixtures with user, course and database session."""
        super().setUp()
        hashed_password = get_password_hash(self.test_user_data["password"])
        # Create a registered user for file tests
        user_create = UserCreate(**self.test_user_data)
        self.user = UserRepository.create(
            self.db_session,
            user_create,
            hashed_password,
        )
        # Create a course for file tests
        course_create = CourseCreate(**self.test_class_data)
        self.course = CourseRepository.create(
            self.db_session,
            course_create,
            self.user.id,
        )
        # Update test file data with course_id
        self.test_file_data["course_id"] = self.course.id

    def test_file_create(self) -> None:
        """Test creating a file via repository."""
        file_data = FileCreate(**self.test_file_data)
        file = FileRepository.create(self.db_session, file_data, self.user.id)

        assert file.id is not None
        assert file.name == self.test_file_data["name"]
        assert file.user_id == self.user.id

    def test_file_get_by_id(self) -> None:
        """Test retrieving a file by ID via repository."""
        file_data = FileCreate(**self.test_file_data)
        created_file = FileRepository.create(
            self.db_session,
            file_data,
            self.user.id,
        )

        retrieved_file = FileRepository.get_file_by_id(
            self.db_session,
            created_file.id,
            self.user.id,
        )

        assert retrieved_file is not None
        assert retrieved_file.id == created_file.id
        assert retrieved_file.name == self.test_file_data["name"]

    def test_file_get_all(self) -> None:
        """Test retrieving all files for a user via repository."""
        file_data1 = FileCreate(**self.test_file_data)
        file_data2 = FileCreate(
            name="another_document.pdf",
            google_drive_id="test_drive_id_456",
            course_id=self.course.id,
        )
        FileRepository.create(self.db_session, file_data1, self.user.id)
        FileRepository.create(self.db_session, file_data2, self.user.id)

        files = FileRepository.get_all(self.db_session, self.user.id)

        assert len(files) == 2

    def test_file_delete(self) -> None:
        """Test deleting a file via repository."""
        file_data = FileCreate(**self.test_file_data)
        created_file = FileRepository.create(
            self.db_session,
            file_data,
            self.user.id,
        )

        FileRepository.delete(self.db_session, created_file)

        retrieved_file = FileRepository.get_file_by_id(
            self.db_session,
            created_file.id,
            self.user.id,
        )

        assert retrieved_file is None

    def test_file_get_by_id_not_found(self) -> None:
        """Test that get_file_by_id returns None for non-existent file."""
        retrieved_file = FileRepository.get_file_by_id(
            self.db_session,
            9999,
            self.user.id,
        )

        assert retrieved_file is None

    def test_file_get_by_id_wrong_user(self) -> None:
        """Test that get_file_by_id returns None when user_id doesn't match."""
        file_data = FileCreate(**self.test_file_data)
        created_file = FileRepository.create(
            self.db_session,
            file_data,
            self.user.id,
        )

        # Try to retrieve with different user_id
        retrieved_file = FileRepository.get_file_by_id(
            self.db_session,
            created_file.id,
            9999,
        )

        assert retrieved_file is None


if __name__ == "__main__":
    unittest.main()
