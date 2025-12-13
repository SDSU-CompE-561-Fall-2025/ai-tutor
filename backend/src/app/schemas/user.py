"""User schemas.

This module defines Pydantic schemas for user data validation and serialization.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr = Field(..., max_length=30)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str
    first_name: str = Field(..., min_length=1, max_length=15)
    last_name: str = Field(..., min_length=1, max_length=15)

    @field_validator("first_name", "last_name")
    @classmethod
    def name_must_not_be_blank(cls, name: str) -> str:
        if not name.strip():
            msg = "Name cannot be blank"
            raise ValueError(msg)
        return name.strip()

class User(UserBase):
    """Schema for user response."""

    id: int
    first_name: str
    last_name: str
    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    first_name: str | None = Field(None, min_length=1, max_length=15)
    last_name: str | None = Field(None, min_length=1, max_length=15)

    @field_validator("first_name", "last_name")
    @classmethod
    def name_must_not_be_blank(cls, name: str | None) -> str | None:
        if name is not None and not name.strip():
            msg = "Name cannot be blank"
            raise ValueError(msg)
        return name.strip() if name else None

class Token(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    token_type: str


class RedirectResponseSchema(BaseModel):
    """Schema for redirect response."""

    redirect_url: str
