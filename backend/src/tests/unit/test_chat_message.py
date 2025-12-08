"""Unit tests for chat message repository operations."""

import unittest

from app.core.auth import get_password_hash
from app.models.chat_message import ChatMessageSenderType
from app.repository.chat_message import ChatMessageRepository
from app.repository.course import CourseRepository
from app.repository.tutor_session import TutorSessionRepository
from app.repository.user import UserRepository
from app.schemas.chat_message import ChatMessageCreate
from app.schemas.course import CourseCreate
from app.schemas.tutor_session import TutorSessionCreate
from app.schemas.user import UserCreate
from tests.base import BaseTestCase


class TestChatMessageRepository(BaseTestCase):
    """Tests for chat message repository operations."""

    def setUp(self) -> None:
        """Set up test fixtures with user, course, session, and database session."""
        super().setUp()
        hashed_password = get_password_hash(self.test_user_data["password"])
        # Create a registered user for chat message tests
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
        # Create a tutor session for the course
        session_data = TutorSessionCreate(
            title="Test Session",
            course_id=self.course.id,
        )
        self.session = TutorSessionRepository.create(
            self.db_session,
            session_data,
            self.user.id,
        )

    def test_chat_message_create_user_message(self) -> None:
        """Test creating a user chat message via repository."""
        message_data = ChatMessageCreate(
            role=ChatMessageSenderType.user,
            message="Hello, tutor!",
            tutor_session_id=self.session.id,
        )
        message = ChatMessageRepository.create(
            self.db_session,
            message_data,
            self.user.id,
        )

        assert message.id is not None
        assert message.role == ChatMessageSenderType.user
        assert message.message == "Hello, tutor!"
        assert message.tutor_session_id == self.session.id
        assert message.user_id == self.user.id

    def test_chat_message_create_assistant_message(self) -> None:
        """Test creating an assistant chat message via repository."""
        message_data = ChatMessageCreate(
            role=ChatMessageSenderType.assistant,
            message="Hello! How can I help?",
            tutor_session_id=self.session.id,
        )
        message = ChatMessageRepository.create(
            self.db_session,
            message_data,
            self.user.id,
        )

        assert message.id is not None
        assert message.role == ChatMessageSenderType.assistant
        assert message.message == "Hello! How can I help?"

    def test_chat_message_get_by_id(self) -> None:
        """Test retrieving a chat message by ID via repository."""
        message_data = ChatMessageCreate(
            role=ChatMessageSenderType.user,
            message="Test message",
            tutor_session_id=self.session.id,
        )
        created_message = ChatMessageRepository.create(
            self.db_session,
            message_data,
            self.user.id,
        )

        retrieved_message = ChatMessageRepository.get_message_by_id(
            self.db_session,
            created_message.id,
        )

        assert retrieved_message is not None
        assert retrieved_message.id == created_message.id
        assert retrieved_message.message == "Test message"

    def test_chat_message_get_all_by_session(self) -> None:
        """Test retrieving all messages for a session via repository."""
        msg1_data = ChatMessageCreate(
            role=ChatMessageSenderType.user,
            message="First message",
            tutor_session_id=self.session.id,
        )
        msg2_data = ChatMessageCreate(
            role=ChatMessageSenderType.assistant,
            message="Assistant response",
            tutor_session_id=self.session.id,
        )
        ChatMessageRepository.create(self.db_session, msg1_data, self.user.id)
        ChatMessageRepository.create(self.db_session, msg2_data, self.user.id)

        messages = ChatMessageRepository.get_all_messages_by_tutor_session_id(
            self.db_session,
            self.session.id,
        )

        assert len(messages) == 2
        assert messages[0].role == ChatMessageSenderType.user
        assert messages[1].role == ChatMessageSenderType.assistant

    def test_chat_message_delete(self) -> None:
        """Test deleting a chat message via repository."""
        message_data = ChatMessageCreate(
            role=ChatMessageSenderType.user,
            message="Test message",
            tutor_session_id=self.session.id,
        )
        created_message = ChatMessageRepository.create(
            self.db_session,
            message_data,
            self.user.id,
        )

        ChatMessageRepository.delete(self.db_session, created_message)

        retrieved_message = ChatMessageRepository.get_message_by_id(
            self.db_session,
            created_message.id,
        )

        assert retrieved_message is None

    def test_chat_message_get_by_id_not_found(self) -> None:
        """Test that get_message_by_id returns None for non-existent message."""
        retrieved_message = ChatMessageRepository.get_message_by_id(
            self.db_session,
            9999,
        )

        assert retrieved_message is None


if __name__ == "__main__":
    unittest.main()
