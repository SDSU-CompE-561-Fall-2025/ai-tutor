from sqlalchemy.orm import Session

from app.models.tutor_session import TutorSession
from app.repository.tutor_session import TutorSessionRepository
from app.schemas.tutor_session import TutorSessionCreate, TutorSessionResponse


def create_tutor_session(
    db: Session,
    tutor_session: TutorSessionCreate,
    user_id: int,
) -> TutorSessionResponse:
    """
    Create a new tutor session.

    Args:
        db: Database session
        tutor_session: Tutor session creation data
        user_id: ID of the user creating the tutor session

    Returns:
        TutorSession: Created tutor session
    """
    tutor_session = TutorSessionRepository.create(db, tutor_session, user_id)
    course_name = tutor_session.course.name
    return TutorSessionResponse(
        id=tutor_session.id,  # pyright: ignore[reportArgumentType]
        title=tutor_session.title,  # pyright: ignore[reportArgumentType]
        course_name=course_name,
        chat_messages=tutor_session.chat_messages,
        created_at=tutor_session.created_at,  # pyright: ignore[reportArgumentType]
    )


def get_tutor_session(
    db: Session,
    tutor_session_id: int,
    user_id: int,
) -> TutorSession:
    """
    Get a tutor session by ID.

    Args:
        db: Database session
        tutor_session_id: ID of the tutor session to retrieve
        user_id: ID of the user
    Returns:
        TutorSession: Retrieved tutor session
    """
    tutor_session = TutorSessionRepository.get_by_id(db, tutor_session_id)
    if tutor_session is None or tutor_session.user_id != user_id:  # type: ignore[union-attr]
        msg = "Tutor session not found or access denied."
        raise ValueError(msg)

    return tutor_session


def get_tutor_session_by_course(
    db: Session,
    course_id: int,
    user_id: int,
) -> TutorSession:
    """
    Get a tutor session by course ID.

    Args:
        db: Database session
        tutor_session_id: ID of the tutor session to retrieve
        user_id: ID of the user
    Returns:
        TutorSession: Retrieved tutor session
    """
    tutor_session = TutorSessionRepository.get_by_course(db, course_id)
    if tutor_session is None or tutor_session.user_id != user_id:  # type: ignore[union-attr]
        msg = "Tutor session not found or access denied."
        raise ValueError(msg)

    return tutor_session


def get_tutor_session_by_user(
    db: Session,
    user_id: int,
) -> TutorSession:
    """
    Get a tutor session by user ID.

    Args:
        db: Database session
        user_id: ID of the user
    Returns:
        TutorSession: Retrieved tutor session
    """
    tutor_session = TutorSessionRepository.get_by_user(db, user_id)
    if tutor_session is None:  # type: ignore[union-attr]
        msg = "Tutor session not found or access denied."
        raise ValueError(msg)

    return tutor_session


def get_tutor_sessions_for_user(db: Session, user_id: int) -> list[TutorSession]:
    """
    Get all tutor session by user ID.

    Args:
        db: Database session
        user_id: ID of the user
    Returns:
        list[TutorSession]: list of retrieved tutor sessions
    """
    tutor_sessions = TutorSessionRepository.get_all_for_user(db, user_id)
    for session in tutor_sessions:
        if session is None or session.user_id != user_id:  # type: ignore[union-attr]
            msg = "Tutor session not found or access denied."
            raise ValueError(msg)

    return tutor_sessions


def get_tutor_sessions_by_course(
    db: Session,
    course_id: int,
    user_id: int,
) -> list[TutorSession]:
    """
    Get all tutor session by course ID.

    Args:
        db: Database session
        course_id: ID of the course
        user_id: ID of the user
    Returns:
        list[TutorSession]: list of retrieved tutor sessions
    """
    tutor_sessions = TutorSessionRepository.get_all_for_course(db, course_id)
    for session in tutor_sessions:
        if session is None or session.user_id != user_id:  # type: ignore[union-attr]
            msg = "Tutor session not found or access denied."
            raise ValueError(msg)

    return tutor_sessions


def update_tutor_session_title(
    db: Session,
    tutor_session_id: int,
    title: str,
    user_id: int,
) -> TutorSession:
    """Update the session title."""
    tutor_session = TutorSessionRepository.get_by_id(db, tutor_session_id)
    if tutor_session is None or tutor_session.user_id != user_id:  # type: ignore[union-attr]
        msg = "Tutor session not found or access denied."
        raise ValueError(msg)
    tutor_session.title = title  # pyright: ignore[reportAttributeAccessIssue]

    return TutorSessionRepository.update(db, tutor_session)


def delete_tutor_session(
    db: Session,
    tutor_session_id: int,
    user_id: int,
) -> None:
    """Delete a tutor session if owned by the user."""
    tutor_session = TutorSessionRepository.get_by_id(db, tutor_session_id)
    if tutor_session is None or tutor_session.user_id != user_id:  # type: ignore[union-attr]
        msg = "Tutor session not found or access denied."
        raise ValueError(msg)

    TutorSessionRepository.delete(db, tutor_session)
