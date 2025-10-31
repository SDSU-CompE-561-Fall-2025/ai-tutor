"""
This model defines the Google OAuth2 token structure.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class AuthToken(Base):
    __tablename__ = "Google_Oauth2_Tokens"
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    expiry = Column(String)
    email = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="auth_token")
