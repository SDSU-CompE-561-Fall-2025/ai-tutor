"""
Chat Message Model
This model defines a chat message within a Tutor Session
"""

import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChatMessageSenderType(enum.Enum):
    user = "user"
    assistant = "assistant"


class ChatMessage(Base):
    """
    SQLAlchemy model for chat messages in tutor sessions.

    Attributes:
        id (int): Primary key, unique identifier for the chat message.
        user_id (int): Foreign key reference to the user who sent/received the message.
        course_id (int): Foreign key reference to the course this message relates to.
        tutor_session_id (int): Foreign key reference to the tutoring session.
        role (ChatMessageSenderType): Enum indicating whether message is from user or AI tutor.
        message (str): The actual text content of the chat message.
        created_at (datetime): Timestamp.

    Relationships:
        tutor_session: Back reference to the TutorSession this message belongs to.
        course: Back reference to the Course this message is associated with.
        user: Back reference to the User who participated in this message exchange.

    Table:
        chat_messages: Database table storing all chat message records.
    """

    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    tutor_session_id = Column(Integer, ForeignKey("tutor_sessions.id"), nullable=False)
    role = Column(Enum(ChatMessageSenderType), nullable=False, name="chatrole")
    message = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    tutor_session = relationship("TutorSession", back_populates="chat_messages")
    user = relationship("User", back_populates="chat_messages")
