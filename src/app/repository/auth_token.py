"""
AuthToken repository.

Data access for OAuth tokens linked to users.
"""

from sqlalchemy.orm import Session

from app.models.auth_token import AuthToken


class AuthTokenRepository:
    """Repository for auth token data access."""

    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> AuthToken | None:
        return db.query(AuthToken).filter(AuthToken.user_id == user_id).first()

    @staticmethod
    def create(db: Session, auth_data: dict) -> AuthToken:
        db_token = AuthToken(
            user_id=auth_data.get("user_id"),
            access_token=auth_data.get("access_token"),
            refresh_token=auth_data.get("refresh_token"),
            expiry=auth_data.get("expiry"),
            email=auth_data.get("email", ""),
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return db_token

    @staticmethod
    def update(db: Session, db_token: AuthToken, auth_data: dict) -> AuthToken:
        db_token.access_token = auth_data.get("access_token", db_token.access_token)
        db_token.refresh_token = auth_data.get("refresh_token", db_token.refresh_token)
        db_token.expiry = auth_data.get("expiry", db_token.expiry)
        db_token.email = auth_data.get("email", db_token.email)
        db.commit()
        db.refresh(db_token)
        return db_token

    @staticmethod
    def delete(db: Session, db_token: AuthToken) -> None:
        db.delete(db_token)
        db.commit()
