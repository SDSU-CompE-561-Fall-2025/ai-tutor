"""Unit tests for user authentication and management."""

import unittest

from app.core.auth import get_password_hash, verify_password
from app.repository.user import UserRepository
from app.schemas.user import UserCreate
from app.services.user import UserService
from tests.base import BaseTestCase


class TestUserRegistration(BaseTestCase):
    """Tests for user registration and validation."""

    def test_user_registration_validation(self) -> None:
        """Test that user data validation works correctly."""
        user_create = UserCreate(**self.test_user_data)
        assert user_create.email == self.test_user_data["email"]
        assert user_create.password == self.test_user_data["password"]
        assert user_create.first_name == self.test_user_data["first_name"]
        assert user_create.last_name == self.test_user_data["last_name"]


class TestUserRepository(BaseTestCase):
    """Tests for user repository operations."""

    def test_user_repository_create(self) -> None:
        """Test creating a user in the repository."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)

        user = UserRepository.create(
            self.db_session,
            user_create,
            hashed_password,
        )

        assert user.id is not None
        assert user.email == self.test_user_data["email"]
        assert user.first_name == self.test_user_data["first_name"]
        assert user.last_name == self.test_user_data["last_name"]

    def test_user_repository_get_by_email(self) -> None:
        """Test retrieving a user by email."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)
        UserRepository.create(
            self.db_session,
            user_create,
            hashed_password,
        )

        retrieved_user = UserRepository.get_by_email(
            self.db_session,
            self.test_user_data["email"],
        )

        assert retrieved_user is not None
        assert retrieved_user.email == self.test_user_data["email"]

    def test_user_repository_get_by_id(self) -> None:
        """Test retrieving a user by ID."""
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


class TestPasswordHandling(BaseTestCase):
    """Tests for password hashing and verification."""

    def test_user_password_hashing(self) -> None:
        """Test that passwords are properly hashed."""
        hashed_password = get_password_hash(self.test_user_data["password"])

        assert hashed_password != self.test_user_data["password"]
        assert verify_password(
            self.test_user_data["password"],
            hashed_password,
        )
        assert not verify_password("wrongpassword", hashed_password)


class TestUserAuthentication(BaseTestCase):
    """Tests for user authentication logic."""

    def test_user_authentication_success(self) -> None:
        """Test successful user authentication."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)
        UserRepository.create(self.db_session, user_create, hashed_password)

        authenticated_user = UserService.authenticate(
            self.db_session,
            self.test_user_data["email"],
            self.test_user_data["password"],
        )

        assert authenticated_user is not None
        assert authenticated_user.email == self.test_user_data["email"]

    def test_user_authentication_failure_wrong_password(self) -> None:
        """Test authentication fails with incorrect password."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user_create = UserCreate(**self.test_user_data)
        UserRepository.create(self.db_session, user_create, hashed_password)

        unauthenticated_user = UserService.authenticate(
            self.db_session,
            self.test_user_data["email"],
            "wrongpassword",
        )

        assert unauthenticated_user is None


if __name__ == "__main__":
    unittest.main()
