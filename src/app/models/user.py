"""
User Model
Defines the User model with relationships to File and Course models.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    files = relationship("File", back_populates="user")
    courses = relationship("Course", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")
    tutor_sessions = relationship("TutorSession", back_populates="user")

    auth_token = relationship(
        "AuthToken",
        back_populates="user",
        uselist=False,
        lazy="joined",
    )
