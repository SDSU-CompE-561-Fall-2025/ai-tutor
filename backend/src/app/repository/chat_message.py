"""tutor message repository.

This module provides data access layer for tutor message operations.
"""

from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.schemas.chat_message import (
    ChatMessageCreate,
)


class ChatMessageRepository:
    """Repository for ChatMessage data access."""

    @staticmethod
    def get_message_by_id(db: Session, chat_message_id: int) -> ChatMessage | None:
        """
        Get a chat message by ID.

        Args:
            db: Database session
            chat_message_id: ChatMessage ID

        Returns:
            ChatMessage | None: ChatMessage if found, None otherwise
        """
        return db.query(ChatMessage).filter(ChatMessage.id == chat_message_id).first()

    @staticmethod
    def get_all_messages_by_tutor_session_id(
        db: Session,
        tutor_session_id: int,
    ) -> list[ChatMessage]:
        """
        Get all chat messages from Tutor Session.

        Args:
            db: Database session
            tutor_session_id: TutorSession ID

        Returns:
            list[ChatMessage]: List of ChatMessages
        """
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.tutor_session_id == tutor_session_id)
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        chat_message: ChatMessageCreate,
        user_id: int,
    ) -> ChatMessage:
        """
        Create a new chat message.

        Args:
            db: Database session
            chat_message: ChatMessage creation data

        Returns:
            ChatMessage: Created chat message
        """
        db_message = ChatMessage(
            role=chat_message.role,
            message=chat_message.message,
            tutor_session_id=chat_message.tutor_session_id,
            user_id=user_id,
        )

        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def update(db: Session, db_message: ChatMessage) -> ChatMessage:
        """
        Update chat message.

        Args:
            db: Database session
            db_message: ChatMessage instance to update

        Returns:
            ChatMessage: Updated chat message
        """
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def delete(db: Session, db_message: ChatMessage) -> None:
        """
        Delete chat message.

        Args:
            db: Database session
            db_message: ChatMessage instance to delete
        """
        db.delete(db_message)
        db.commit()

    @staticmethod
    def get_all_messages(db: Session, user_id: int) -> list[ChatMessage]:
        """
        Get all chat messages for a user.

        Args:
            db: Database session
            user_id: ID of the user
        Returns:
            list[ChatMessage]: List of chat messages
        """
        return db.query(ChatMessage).filter(ChatMessage.user_id == user_id).all()
