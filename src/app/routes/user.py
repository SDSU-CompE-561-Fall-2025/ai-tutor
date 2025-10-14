"""User routes.

This module defines API routes for user management and authentication.
"""

import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import Token, UserCreate
from app.schemas.user import User as UserSchema
from app.services.user import UserService

api_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@api_router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Register a new user.

    Args:
        user: User registration data
        db: Database session

    Returns:
        User: Created user

    Raises:
        HTTPException: If email already registered
    """
    return UserService.create(db=db, user=user)


@api_router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """
    Login and get access token.

    Args:
        form_data: OAuth2 login form (username=email, password)
        db: Database session

    Returns:
        Token: Access token

    Raises:
        HTTPException: If credentials are invalid
    """
    user = UserService.authenticate(
        db,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    token_type = os.environ.get("TOKEN_TYPE", "bearer")
    return Token(access_token=access_token, token_type=token_type)


@api_router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Get current user profile.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current user data
    """
    return current_user
