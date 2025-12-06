"""Base test class setup and shared test utilities for unittest."""

import os
import tempfile
import unittest
from collections.abc import Generator
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.auth import get_password_hash
from app.core.database import Base
from app.core.dependencies import get_db
from app.main import app
from app.models.user import User


class BaseTestCase(unittest.TestCase):
    """Base test case class with database and client setup."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test database for all tests in the class."""
        # Create temporary database
        fd, cls.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        cls.test_db_url = f"sqlite:///{cls.db_path}"

        # Create engine and tables
        cls.engine = create_engine(
            cls.test_db_url,
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(bind=cls.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up test database after all tests."""
        Base.metadata.drop_all(bind=cls.engine)
        cls.engine.dispose()
        Path(cls.db_path).unlink(missing_ok=True)

    def setUp(self) -> None:
        """Set up for each test."""
        # Create new session for each test
        testing_session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        self.db_session = testing_session_local()

        # Set up test client with overridden database
        def override_get_db() -> Generator[Session, None, None]:
            yield self.db_session

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

        # Create test data
        self.test_user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
        }

        self.test_class_data = {
            "name": "Test Class",
            "description": "A test class for testing",
            "semester": "Fall 2025",
        }

        self.test_file_data = {
            "filename": "test_document.pdf",
            "file_type": "pdf",
        }

    def tearDown(self) -> None:
        """Clean up after each test."""
        self.db_session.close()
        app.dependency_overrides.clear()

    def create_registered_user(self) -> User:
        """Helper to create a registered test user."""
        hashed_password = get_password_hash(self.test_user_data["password"])
        user = User(
            email=self.test_user_data["email"],
            hashed_password=hashed_password,
            first_name=self.test_user_data["first_name"],
            last_name=self.test_user_data["last_name"],
        )
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_auth_token(self) -> str:
        """Helper to get JWT token for authenticated user."""
        response = self.client.post(
            "/api/v1/user/login",
            data={
                "username": self.test_user_data["email"],
                "password": self.test_user_data["password"],
            },
        )
        return response.json()["access_token"]

    def get_authenticated_client(self) -> TestClient:
        """Helper to get test client with authentication headers."""
        token = self.get_auth_token()
        self.client.headers = {"Authorization": f"Bearer {token}"}
        return self.client
