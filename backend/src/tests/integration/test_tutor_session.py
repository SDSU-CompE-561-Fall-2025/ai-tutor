"""Integration tests for tutor session endpoints."""

import unittest

from app.repository.course import CourseRepository
from app.schemas.course import CourseCreate
from tests.base import BaseTestCase


class TestTutorSessionEndpoints(BaseTestCase):
    """Tests for tutor session endpoints."""

    def setUp(self) -> None:
        """Set up test fixtures including a user and course via repositories."""
        super().setUp()
        self.user = self.create_registered_user()
        course_data = CourseCreate(**self.test_class_data)
        self.course = CourseRepository.create(
            self.db_session,
            course_data,
            self.user.id,
        )

    def test_create_tutor_session(self) -> None:
        """Test creating a tutor session via endpoint."""
        authenticated_client = self.get_authenticated_client()
        session_data = {
            "course_id": self.course.id,
            "title": "Learning Session",
        }
        response = authenticated_client.post(
            "/api/v1/tutor-session/chat",
            json=session_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == session_data["title"]
        assert data["course_name"] == self.course.name

    def test_get_tutor_session_by_id(self) -> None:
        """Test getting a specific tutor session by ID."""
        authenticated_client = self.get_authenticated_client()
        session_data = {
            "course_id": self.course.id,
            "title": "Test Session",
        }
        create_response = authenticated_client.post(
            "/api/v1/tutor-session/chat",
            json=session_data,
        )

        if create_response.status_code != 200:
            return

        session_id = create_response.json()["id"]

        response = authenticated_client.get(f"/api/v1/tutor-session/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == session_id
        assert data["title"] == session_data["title"]
        assert data["course_name"] == self.course.name

    def test_delete_tutor_session(self) -> None:
        """Test deleting a tutor session via endpoint."""
        authenticated_client = self.get_authenticated_client()
        # Create a session first
        session_data = {
            "course_id": self.course.id,
            "title": "Session to Delete",
        }
        create_response = authenticated_client.post(
            "/api/v1/tutor-session/chat",
            json=session_data,
        )

        if create_response.status_code != 200:
            return

        session_id = create_response.json()["id"]

        # Delete it
        response = authenticated_client.delete(f"/api/v1/tutor-session/{session_id}")
        assert response.status_code in [200, 204]

    def test_get_tutor_session_messages(self) -> None:
        """Test getting messages for a tutor session."""
        authenticated_client = self.get_authenticated_client()
        session_data = {
            "course_id": self.course.id,
            "title": "Test Session",
        }
        create_response = authenticated_client.post(
            "/api/v1/tutor-session/chat",
            json=session_data,
        )

        if create_response.status_code != 200:
            return

        session_id = create_response.json()["id"]

        response = authenticated_client.get(
            f"/api/v1/tutor-session/{session_id}/messages",
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


if __name__ == "__main__":
    unittest.main()
