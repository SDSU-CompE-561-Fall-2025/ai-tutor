from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.google_auth import refresh_credentials
from app.models.auth_token import AuthToken
from app.repository.auth_token import AuthTokenRepository
from app.repository.user import UserRepository


class AuthTokenService:
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
            AuthTokenService.update_auth_token(db, user_id, new_creds)
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
