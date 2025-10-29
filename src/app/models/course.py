from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # A course is one to many with File
    # If a course is deleted, all associated files should also be deleted
    files = relationship("File", back_populates="course", cascade="all, delete-orphan")
    # A course is many to one with User
    user = relationship("User", back_populates="courses")
    # A course is one to many with TutorSession
    # If a course is deleted, all associated tutor sessions should also be deleted
    tutor_sessions = relationship(
        "TutorSession",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    # Unique constraint: same course name allowed for different users, but not within same user
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="unique_course_per_user"),
    )
