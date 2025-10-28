from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.tutor_session as tutor_session_service
from app.core.auth import oauth2_scheme
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.tutor_session import TutorSession
from app.schemas.tutor_session import TutorSessionCreate, TutorSessionResponse

api_router = APIRouter (
    prefix="/tutor-session",
    tags=["tutor_session"],
)

@api_router.post("/chat")
async def create_tutor_session(
    tutor_session: TutorSessionCreate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TutorSessionResponse:
    """Create a new tutor session for user to chat with."""
    user = get_current_user(token, db)
    return tutor_session_service.create_tutor_session(db, tutor_session, user.id)

@api_router.get("/{tutor_session_id}")
async def get_tutor_session(
    tutor_session_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TutorSession:
    """Get a tutor session by ID."""
    user = get_current_user(token, db)
    return tutor_session_service.get_tutor_session(db, tutor_session_id, user.id)

@api_router.put("/endSession/{tutor_session_id}")
async def end_tutor_session(
    tutor_session_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TutorSession:
    """End a tutor session by ID."""
    user = get_current_user(token, db)
    return tutor_session_service.end_tutor_session(db, tutor_session_id, user.id)

@api_router.delete("/{tutor_session_id}")
async def delete_tutor_session(
    tutor_session_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    """Delete a tutor session by ID."""
    user = get_current_user(token, db)
    return tutor_session_service.delete_tutor_session(db, tutor_session_id, user.id)

@api_router.put("/{tutor_session_id}")
async def update_tutor_session_title(
    tutor_session_id: int,
    title: str,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TutorSessionResponse:
    """Update a tutor session by ID."""
    user = get_current_user(token, db)
    return tutor_session_service.update_tutor_session(db, tutor_session_id, title, user.id)
