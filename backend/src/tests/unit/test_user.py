"""Unit tests for user repository operations."""

import unittest

from app.core.auth import get_password_hash, verify_password
from app.repository.user import UserRepository
from app.schemas.user import UserCreate
from tests.base import BaseTestCase


class TestUserRepository(BaseTestCase):
    """Tests for user repository operations."""

    def setUp(self) -> None:
        """Set up test fixtures with database session."""
        super().setUp()

    def test_user_create(self) -> None:
        """Test creating a user via repository."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)

        user = UserRepository.create(self.db_session, user_create, hashed_password)

        assert user.id is not None
        assert user.email == self.test_user_data["email"]
        assert user.first_name == self.test_user_data["first_name"]
        assert user.last_name == self.test_user_data["last_name"]

    def test_user_get_by_email(self) -> None:
        """Test retrieving a user by email via repository."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)
        UserRepository.create(self.db_session, user_create, hashed_password)

        retrieved_user = UserRepository.get_by_email(
            self.db_session,
            self.test_user_data["email"],
        )

        assert retrieved_user is not None
        assert retrieved_user.email == self.test_user_data["email"]

    def test_user_get_by_id(self) -> None:
        """Test retrieving a user by ID via repository."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)

        created_user = UserRepository.create(
            self.db_session,
            user_create,
            hashed_password,
        )

        retrieved_user = UserRepository.get_by_id(self.db_session, created_user.id)

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == self.test_user_data["email"]

    def test_user_get_by_email_not_found(self) -> None:
        """Test that get_by_email returns None for non-existent user."""
        retrieved_user = UserRepository.get_by_email(
            self.db_session,
            "nonexistent@example.com",
        )

        assert retrieved_user is None

    def test_user_get_by_id_not_found(self) -> None:
        """Test that get_by_id returns None for non-existent user."""
        retrieved_user = UserRepository.get_by_id(self.db_session, 9999)

        assert retrieved_user is None


class TestUserSchema(BaseTestCase):
    """Tests for user schema validation."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        super().setUp()

    def test_user_create_schema_validation(self) -> None:
        """Test that user creation schema validates correctly."""
        user_create = UserCreate(**self.test_user_data)
        assert user_create.email == self.test_user_data["email"]
        assert user_create.password == self.test_user_data["password"]
        assert user_create.first_name == self.test_user_data["first_name"]
        assert user_create.last_name == self.test_user_data["last_name"]

class TestPasswordHandling(BaseTestCase):
    """Tests for password hashing and verification."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        super().setUp()

    def test_password_hashing(self) -> None:
        """Test that passwords are properly hashed."""
        hashed_password = get_password_hash(self.test_user_data["password"])

        assert hashed_password != self.test_user_data["password"]
        assert verify_password(
            self.test_user_data["password"],
            hashed_password,
        )

    def test_password_verification_failure(self) -> None:
        """Test that password verification fails with wrong password."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        assert not verify_password("wrongpassword", hashed_password)

if __name__ == "__main__":
    unittest.main()
