"""
Tutor Session Model
This model defines a tutor message
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TutorSession(Base):
    __tablename__ = "tutor_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ended_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="tutor_sessions")
    course = relationship("Course", back_populates="tutor_sessions")
    chat_messages = relationship("ChatMessage", back_populates="tutor_session", cascade="all, delete-orphan")
