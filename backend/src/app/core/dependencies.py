from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import oauth2_scheme, verify_token
from app.core.database import get_db
from app.models.auth_token import AuthToken
from app.models.user import User
from app.services.auth_token import AuthTokenService
from app.services.user import UserService


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Get the current authenticated user from JWT token.

    Args:
        token: JWT access token
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = UserService.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user


def get_current_user_oauth_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> AuthToken:
    """
    Get the Oauth Token using user from JWT token.

    Args:
        token: JWT access token
        db: Database session

    Returns:
        AuthToken: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = UserService.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    auth_token = AuthTokenService.get_auth_token(db, user_id=user.id)  # pyright: ignore[reportArgumentType]
    if auth_token is None:
        raise credentials_exception
    user.auth_token = auth_token

    return auth_token
