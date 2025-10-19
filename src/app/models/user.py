"""
User Model
This model defines the user database URL
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    auth_token = relationship(
        "AuthToken",
        back_populates="user",
        uselist=False,
        lazy="joined",
    )
