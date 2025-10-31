"""
Tutor Session Model
This model defines a tutor message
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TutorSession(Base):
    """
    SQLAlchemy model representing a tutoring session between a user and a course.

    Attributes:
        id (int): Primary key identifier for the tutor session.
        user_id (int): Foreign key reference to the user participating in the session.
        course_id (int): Foreign key reference to the course being studied.
        title (str): Optional title or description of the tutoring session.
        created_at (datetime): timestamp.

    Relationships:
        user (User): The user who owns this tutoring session.
        course (Course): The course associated with this tutoring session.
        chat_messages (List[ChatMessage]): All chat messages within this session,
    """

    __tablename__ = "tutor_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="tutor_sessions")
    course = relationship("Course", back_populates="tutor_sessions")
    chat_messages = relationship(
        "ChatMessage",
        back_populates="tutor_session",
        cascade="all, delete-orphan",
    )
