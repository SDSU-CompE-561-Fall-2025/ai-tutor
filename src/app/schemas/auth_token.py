"""
Schema for Google OAuth2 authentication token.
"""

from datetime import datetime

from pydantic import BaseModel


class AuthTokenBase(BaseModel):
    access_token: str
    refresh_token: str
    expiry: datetime


class AuthTokenCreate(AuthTokenBase):
    email: str
    user_id: int
