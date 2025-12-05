"""
User service.

This module handles business logic for user operations,
combining validation, hashing, and repository calls.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_password_hash, verify_password
from app.models.user import User
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
    def update_user_name(db: Session, user_id: int, first_name: str, last_name: str) -> User:
        """
        Update user's name.

        Args:
            db: Database session
            user_id: User ID
            firstName: New first name
            lastName: New last name

        Raises:
            HTTPException: If user not found

        Returns:
            User: Updated user
        """
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        user.first_name = first_name
        user.last_name = last_name
        return UserRepository.update(db, user)
