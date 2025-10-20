"""User routes.

This module defines API routes for user management and authentication.
"""

import os
from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_user_oauth_token
from app.core.google_auth import (
    get_auth_url,
    get_google_email,
    handle_oauth_callback,
)
from app.models.user import User
from app.schemas.auth_token import AuthTokenBase
from app.schemas.user import RedirectResponseSchema, Token, UserCreate
from app.schemas.user import User as UserSchema
from app.services.user import UserService

api_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@api_router.post("/register", status_code=status.HTTP_200_OK)
def register(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> RedirectResponseSchema:
    """
    Register a new user and initiate Google OAuth2 flow.
    Args:
        user: User creation data
        db: Database session
    """
    UserService.create(db=db, user=user)
    auth_url, _ = get_auth_url()
    return RedirectResponseSchema(redirect_url=auth_url)


@api_router.get("/auth/google/callback")
def auth_google_callback(
    code: str,
    db: Annotated[Session, Depends(get_db)],
) -> JSONResponse:
    creds = handle_oauth_callback(code)
    email = get_google_email(creds["access_token"])
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to retrieve email from Google.",
        )
    try:
        user = UserService.get_user_by_email(db, email)
    except HTTPException:
        user = None

    if user:
        uid = cast("int", user.id)
        UserService.create_auth_token(db, uid, creds)

    return JSONResponse(
        {
            "message": "OAuth signup successful!",
            "access_token": creds["access_token"],
            "refresh_token": creds["refresh_token"],
            "expiry": creds["expiry"],
            "email": email,
        },
    )


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
        AuthToken: Current user's auth token data
    """
    return current_user


@api_router.get("/token")
def get_google_token(
    token: Annotated[User, Depends(get_current_user_oauth_token)],
) -> AuthTokenBase:
    """
    Get current user's access token.

    Args:
        current_user: Current authenticated user

    Returns:
        Token: Access token
    """
    return token
