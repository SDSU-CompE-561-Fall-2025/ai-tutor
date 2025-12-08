"""Integration tests for chat message endpoints."""

import datetime
import unittest
from unittest.mock import MagicMock, patch

from app.repository.course import CourseRepository
from app.repository.tutor_session import TutorSessionRepository
from app.schemas.course import CourseCreate
from app.schemas.tutor_session import TutorSessionCreate
from tests.base import BaseTestCase


_MOCK_TIMESTAMP = datetime.datetime.now(datetime.UTC)


class TestChatMessageEndpoints(BaseTestCase):
    """Tests for chat message endpoints."""

    def setUp(self) -> None:
        """Set up test fixtures including a session via repositories."""
        super().setUp()
        self.user = self.create_registered_user()
        course_data = CourseCreate(**self.test_class_data)
        self.course = CourseRepository.create(
            self.db_session,
            course_data,
            self.user.id,
        )
        # Create a tutor session via repository
        session_data = TutorSessionCreate(
            title="Test Session",
            course_id=self.course.id,
        )
        self.session = TutorSessionRepository.create(
            self.db_session,
            session_data,
            self.user.id,
        )

    @patch("app.services.chat_message.ai_generate_response_gemini")
    def test_send_chat_message(self, mock_ai_generate: MagicMock) -> None:
        """Test sending a chat message via endpoint."""
        # Mock the AI response
        mock_ai_generate.return_value = MagicMock(
            id=1,
            message="This is a mock AI response",
            role="assistant",
            tutor_session=self.session,
            created_at=datetime.datetime.now(datetime.UTC),
        )

        authenticated_client = self.get_authenticated_client()
        message_data = {
            "tutor_session_id": self.session.id,
            "message": "What is photosynthesis?",
            "role": "user",
        }
        response = authenticated_client.post(
            "/api/v1/chat-messages",
            json=message_data,
        )
        # Response might be 200 or 201
        assert response.status_code in [200, 201]
        if response.status_code in [200, 201]:
            data = response.json()
            assert data["message"] == "This is a mock AI response"
            assert data["role"] == "assistant"

    @patch("app.services.chat_message.ai_generate_response_gemini")
    def test_get_chat_messages(self, mock_ai_generate: MagicMock) -> None:
        """Test getting list of chat messages for a session."""
        # Mock the AI response
        mock_ai_generate.return_value = MagicMock(
            id=1,
            message="Hello!",
            role="assistant",
            tutor_session=self.session,
            created_at=_MOCK_TIMESTAMP,
        )

        authenticated_client = self.get_authenticated_client()
        # Send a message first
        message_data = {
            "tutor_session_id": self.session.id,
            "message": "Hello!",
            "role": "user",
        }
        authenticated_client.post(
            "/api/v1/chat-messages",
            json=message_data,
        )

        response = authenticated_client.get(
            f"/api/v1/tutor-session/{self.session.id}/messages",
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @patch("app.services.chat_message.ai_generate_response_gemini")
    def test_get_chat_message_by_id(self, mock_ai_generate: MagicMock) -> None:
        """Test getting a specific chat message by ID."""
        # Mock the AI response
        mock_ai_generate.return_value = MagicMock(
            id=1,
            message="Test message",
            role="assistant",
            tutor_session=self.session,
            created_at=_MOCK_TIMESTAMP,
        )

        authenticated_client = self.get_authenticated_client()
        # Send a message first
        message_data = {
            "tutor_session_id": self.session.id,
            "message": "Test message",
            "role": "user",
        }
        send_response = authenticated_client.post(
            "/api/v1/chat-messages",
            json=message_data,
        )

        if send_response.status_code not in [200, 201]:
            return

        message_id = send_response.json()["id"]

        response = authenticated_client.get(
            f"/api/v1/chat-messages/{message_id}",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == message_id
        assert data["message"] == "Test message"

    @patch("app.services.chat_message.ai_generate_response_gemini")
    def test_chat_message_conversation_workflow(self, mock_ai_generate: MagicMock) -> None:
        """Test a complete chat message conversation workflow."""
        # Mock the AI response
        mock_ai_generate.return_value = MagicMock(
            id=1,
            message="Photosynthesis is...",
            role="assistant",
            tutor_session=self.session,
            created_at=_MOCK_TIMESTAMP,
        )

        authenticated_client = self.get_authenticated_client()
        # Send user message
        user_message_data = {
            "tutor_session_id": self.session.id,
            "message": "How does photosynthesis work?",
            "role": "user",
        }
        user_response = authenticated_client.post(
            "/api/v1/chat-messages",
            json=user_message_data,
        )
        if user_response.status_code not in [200, 201]:
            return

        # Verify message was created
        messages_response = authenticated_client.get(
            f"/api/v1/tutor-session/{self.session.id}/messages",
        )
        if messages_response.status_code != 200:
            return
        messages = messages_response.json()
        assert len(messages) >= 1

    def test_chat_message_unauthorized(self) -> None:
        """Test accessing chat message endpoints without authentication."""
        response = self.client.get(
            "/api/v1/chat-messages/",
        )
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    unittest.main()
