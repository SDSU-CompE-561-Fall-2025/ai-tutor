"""
User service.

This module handles business logic for user operations,
combining validation, hashing, and repository calls.
"""

from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_password_hash, verify_password
from app.core.google_auth import refresh_credentials
from app.models.auth_token import AuthToken
from app.models.user import User
from app.repository.auth_token import AuthTokenRepository
from app.repository.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """Service layer for user-related operations."""

    @staticmethod
    def create(db: Session, user: UserCreate) -> User:
        """
        Register a new user.

        Args:
            db: Database session
            user: User creation data

        Raises:
            HTTPException: If email already exists

        Returns:
            User: Created user
        """
        existing_user = UserRepository.get_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered.",
            )

        hashed_pw = get_password_hash(user.password)
        return UserRepository.create(db, user, hashed_pw)

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User | None:
        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):  # pyright: ignore[reportArgumentType]
            return None

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """
        Get user by ID.

        Args:
            db: Database session
            user_id: User ID

        Raises:
            HTTPException: If user not found

        Returns:
            User: Retrieved user
        """
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """
        Get user by email.

        Args:
            db: Database session
            email: User email

        Raises:
            HTTPException: If user not found

        Returns:
            User: Retrieved user
        """
        user = UserRepository.get_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> dict:
        """
        Delete user by ID.

        Args:
            db: Database session
            user_id: User ID

        Raises:
            HTTPException: If user not found
        """
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        UserRepository.delete(db, user)
        return {"message": "User deleted successfully."}

    @staticmethod
    def get_auth_token(db: Session, user_id: int) -> AuthToken | None:
        """
        Get OAuth2 tokens for a user.

        Args:
            db: Database session
            user_id: User ID
        """
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        if not user.auth_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User has no stored tokens",
            )
        expiry = datetime.fromisoformat(user.auth_token.expiry)
        expiry = expiry.replace(tzinfo=UTC)

        if expiry and expiry < datetime.now(UTC):
            new_creds = refresh_credentials(user.auth_token.refresh_token)  # pyright: ignore[reportAttributeAccessIssue]
            UserService.update_auth_token(db, user_id, new_creds)
            user = UserRepository.get_by_id(db, user_id)
            return user.auth_token  # pyright: ignore[reportOptionalMemberAccess]
        return user.auth_token

    @staticmethod
    def update_auth_token(db: Session, user_id: int, creds: dict) -> AuthToken | None:
        """
        Update or create OAuth2 tokens for a user.

        Args:
            db: Database session
            user_id: User ID
            creds: Credentials dictionary containing access_token, refresh_token, expiry, email
        """
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        # prefer updating existing token, otherwise create
        existing = AuthTokenRepository.get_by_user_id(db, user_id)
        auth_data = {
            "access_token": creds["access_token"],
            "refresh_token": creds["refresh_token"],
            "expiry": creds["expiry"],
            "email": creds.get("email", ""),
            "user_id": user_id,
        }

        if existing:
            return AuthTokenRepository.update(db, existing, auth_data)
        return AuthTokenRepository.create(db, auth_data)

    @staticmethod
    def create_auth_token(
        db: Session,
        user_id: int,
        creds: dict,
    ) -> AuthToken | None:
        """
        Create or update OAuth2 tokens for a user if they have one already.

        Args:
            db: Database session
            user_id: User ID
            creds: Credentials dictionary containing access_token, refresh_token, expiry, email
        """
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        auth_data = {
            "access_token": creds["access_token"],
            "refresh_token": creds["refresh_token"],
            "expiry": creds["expiry"],
            "email": creds.get("email", ""),
            "user_id": user_id,
        }
        existing = AuthTokenRepository.get_by_user_id(db, user_id)
        if existing:
            return AuthTokenRepository.update(db, existing, auth_data)
        return AuthTokenRepository.create(db, auth_data)
