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
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    tutor_session_id = Column(Integer, ForeignKey("tutor_sessions.id"), nullable=False)
    role = Column(Enum(ChatMessageSenderType), nullable=False, name="chatrole")
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tutor_session = relationship("TutorSession", back_populates="chat_messages")
    course = relationship("Course", back_populates="chat_messages")
    user = relationship("User", back_populates="chat_messages")
