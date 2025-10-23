"""tutor session repository.

This module provides data access layer for tutor session operations.
"""

from sqlalchemy.orm import Session

from app.models.tutor_session import TutorSession
from app.schemas.tutor_session import (
    TutorSessionCreate,
)


class TutorSessionRepository:
    """Repository for TutorSession data access."""

    @staticmethod
    def get_by_id(db: Session, tutor_session_id: int) -> TutorSession | None:
        """
        Get tutor session by ID.

        Args:
            db: Database session
            tutor_session_id: tutor session ID

        Returns:
            TutorSession | None: TutorSession if found, None otherwise
        """
        return db.query(TutorSession).filter(TutorSession.id == tutor_session_id).first()

    @staticmethod
    def get_by_course(db: Session, course_id: int) -> TutorSession | None:
        """
        Get tutor session by course.

        Args:
            db: Database session
            course_id: course ID

        Returns:
            TutorSession | None: TutorSession if found, None otherwise
        """
        return db.query(TutorSession).filter(TutorSession.course_id == course_id).first()

    @staticmethod
    def get_by_user(db: Session, user_id: int) -> TutorSession | None:
        """
        Get tutor session by user.

        Args:
            db: Database session
            user_id: user ID

        Returns:
            TutorSession | None: TutorSession if found, None otherwise
        """
        return db.query(TutorSession).filter(TutorSession.user_id == user_id).first()

    @staticmethod
    def create(
        db: Session,
        tutor_session: TutorSessionCreate,
        user_id: int,
    ) -> TutorSession:
        """
        Create a new tutor session.

        Args:
            db: Database session
            tutorSession: Tutor session creation data

        Returns:
            TutorSession: Created tutor session
        """
        db_tutor_session = TutorSession(
            title=tutor_session.title,
            course_id=tutor_session.course_id,
            user_id=user_id,
        )
        db.add(db_tutor_session)
        db.commit()
        db.refresh(db_tutor_session)
        return db_tutor_session

    @staticmethod
    def update(db: Session, db_tutor_session: TutorSession) -> TutorSession:
        """
        Update transaction.

        Args:
            db: Database session
            db_transaction: Transaction instance to update

        Returns:
            Transaction: Updated transaction
        """
        db.commit()
        db.refresh(db_tutor_session)
        return db_tutor_session

    @staticmethod
    def delete(db: Session, db_tutor_session: TutorSession) -> None:
        """
        Delete tutor session.

        Args:
            db: Database session
            db_tutor_session: TutorSession instance to delete
        """
        db.delete(db_tutor_session)
        db.commit()

    @staticmethod
    def get_all_for_user(db: Session, user_id: int) -> list[TutorSession]:
        """
        Return all tutor sessions for a user ordered by created_at desc.

        Args:
            db: Database session
            user_id: ID of the user

        Returns:
            list[TutorSession]: List of tutor sessions
        """
        return (
            db.query(TutorSession)
            .filter(TutorSession.user_id == user_id)
            .order_by(TutorSession.created_at.desc())
            .all()
        )

    @staticmethod
    def get_all_for_course(db: Session, course_id: int) -> list[TutorSession]:
        """
        Return all tutor sessions for a course ordered by created_at desc.

        Args:
            db: Database session
            user_id: ID of the user

        Returns:
            list[TutorSession]: List of tutor sessions
        """
        return (
            db.query(TutorSession)
            .filter(TutorSession.course_id == course_id)
            .order_by(TutorSession.created_at.desc())
            .all()
        )
