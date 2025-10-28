from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.repository.chat_message import ChatMessageRepository
from app.schemas.chat_message import ChatMessageCreate, ChatMessageResponse


def create_chat_message(
        db: Session,
        chat_message: ChatMessageCreate,
        user_id: int,
) -> ChatMessageResponse:
    """
    Create a new chat message.

    Args:
        db: Database session
        chat_message: ChatMessage creation data
        user_id: ID of the user creating the category

    Returns:
        chat_message: Created chat message
    """
    chat_message = ChatMessageRepository.create(db, chat_message, user_id)

    tutor_session_title = chat_message.tutor_session.title
    course_name = chat_message.tutor_session.course.name

    return ChatMessageResponse(
        id=chat_message.id,
        role=chat_message.role,
        message=chat_message.message,
        tutor_session_title=tutor_session_title,
        course_name=course_name,
        created_at=chat_message.created_at,
    )

def get_chat_messages_by_tutor_session(db: Session, tutor_session_id: int, user_id: int) -> list[ChatMessage]:
    """
    Get all chat messages for a tutor session.

    Args:
        db: Database session
        tutor_session_id: ID of the tutor session
        user_id: ID of the user
    Returns:
        list[ChatMessage]: List of chat messages
    """
    chat_messages = ChatMessageRepository.get_all_messages_by_tutor_session_id(db, tutor_session_id)
    for message in chat_messages:
        if message is None or message.user_id != user_id:  # type: ignore[union-attr]
            msg = "Access denied to chat messages."
            raise ValueError(msg)

    return chat_messages

def get_chat_messages_by_course(db: Session, course_id: int, user_id: int) -> list[ChatMessage]:
    """
    Get all chat messages for a course.

    Args:
        db: Database session
        course_id: ID of the course
        user_id: ID of the user
    Returns:
        list[ChatMessage]: List of chat messages
    """
    chat_messages = ChatMessageRepository.get_all_messages_by_course_id(db, course_id)
    for message in chat_messages:
        if message is None or message.user_id != user_id:  # type: ignore[union-attr]
            msg = "Access denied to chat messages."
            raise ValueError(msg)

    return chat_messages

def get_all_chat_messages(db: Session, user_id: int) -> list[ChatMessage]:
    """
    Get all chat messages for a user.

    Args:
        db: Database session
        user_id: ID of the user
    Returns:
        list[ChatMessage]: List of chat messages
    """
    chat_messages = ChatMessageRepository.get_all_messages(db, user_id)
    for message in chat_messages:
        if message is None or message.user_id != user_id:  # type: ignore[union-attr]
            msg = "Access denied to chat messages."
            raise ValueError(msg)

    return chat_messages


def delete_chat_message(db: Session, message_id: int, user_id: int) -> None:
    """
    Delete a chat message by ID.

    Args:
        db: Database session
        message_id: ID of the chat message to delete
        user_id: ID of the user
    Returns:
        None
    """
    chat_message = ChatMessageRepository.get_by_id(db, message_id)
    if not chat_message or chat_message.user_id != user_id:  # type: ignore[union-attr]
        msg = "Chat Message not found or access denied."
        raise ValueError(msg)

    ChatMessageRepository.delete(db, chat_message)

def update_chat_message(
    db: Session,
    message_id: int,
    message_data: ChatMessageCreate,
    user_id: int,
) -> ChatMessage:
    """
    Update a chat message by ID.

    Args:
        db: Database session
        message_id: ID of the category to update
        message_data: New category data
        user_id: ID of the user
    Returns:
        ChatMessage: Updated chat message
    """
    chat_message = ChatMessageRepository.get_by_id(db, message_id)
    if not chat_message or chat_message.user_id != user_id:  # type: ignore[union-attr]
        msg = "ChatMessage not found or access denied."
        raise ValueError(msg)

    chat_message.role = message_data.role
    chat_message.message = message_data.message
    chat_message.tutor_session_id = message_data.tutor_session_id

    return ChatMessageRepository.update(db, chat_message)


def get_chat_message(db: Session, chat_message_id: int, user_id: int) -> ChatMessage:
    """
    Get a chat message by ID.

    Args:
        db: Database session
        chat_message_id: ID of the chat message to retrieve
        user_id: ID of the user
    Returns:
        ChatMessage: Retrieved chat message
    """
    chat_message = ChatMessageRepository.get_by_id(db, chat_message_id)
    if not chat_message or chat_message.user_id != user_id:  # type: ignore[union-attr]
        msg = "ChatMessage not found or access denied."
        raise ValueError(msg)

    return chat_message


