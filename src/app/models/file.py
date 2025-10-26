# ForeignKey - a column in one table that links to the primary key of another table (creates a relationship between the two)
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.core.database import Base

class File(Base): 
    __tablename__ = "files"
    # id: int, primary key, auto-increment
    # sqlalchemy will auto-increment primary keys by default
    id = Column(Integer, primary_key=True)
    # name: str, required, unique per course
    name = Column(String, nullable=False)
    # user_id: int, required, foreign key to users.id
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # course_id: int, required, foreign key to courses.id
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    # created_at: datetime, default to current time (server-side)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # A file is many to one with Course
    course = relationship("Course", back_populates="files")
    # A file is many to one with User
    user = relationship("User", back_populates="files")

    # Unique constraint: same file name allowed for different courses, but not within same course
    __table_args__ = (UniqueConstraint('name', 'course_id', name='unique_file_per_course'),)