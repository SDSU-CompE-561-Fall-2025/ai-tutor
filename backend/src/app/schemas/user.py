"""User schemas.

This module defines Pydantic schemas for user data validation and serialization.
"""

from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str
    first_name: str
    last_name: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password is more than 8 characters."""
        if len(v) <= 8:
            raise ValueError("Password must be more than 8 characters")
        return v


class User(UserBase):
    """Schema for user response."""

    id: int
    first_name: str
    last_name: str
    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    first_name: str | None = None
    last_name: str | None = None


class Token(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    token_type: str


class RedirectResponseSchema(BaseModel):
    """Schema for redirect response."""

    redirect_url: str
