from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.chat_message as chat_mesage_service
from app.core.auth import oauth2_scheme
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.chat_message import ChatMessageCreate, ChatMessageResponse

api_router = APIRouter(
    prefix="/chat-messages",
    tags=["chat_messages"],
)


@api_router.post("/")
async def create_message(
    message: ChatMessageCreate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> ChatMessageResponse:
    user = get_current_user(token, db)
    return chat_mesage_service.create_chat_message(db, message, user.id)  # pyright: ignore[reportArgumentType]


@api_router.get("/{message_id}")
async def get_message(
    message_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> ChatMessageResponse:
    user = get_current_user(token, db)
    return chat_mesage_service.get_chat_message(db, message_id, user.id)  # pyright: ignore[reportArgumentType]


@api_router.patch("/{message_id}")
async def update_message(
    message_id: int,
    message: ChatMessageCreate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> ChatMessageResponse:
    user = get_current_user(token, db)
    return chat_mesage_service.update_chat_message(db, message_id, message, user.id)  # pyright: ignore[reportArgumentType]


@api_router.delete("/{message_id}")
async def remove_message(
    message_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    user = get_current_user(token, db)
    return chat_mesage_service.delete_chat_message(db, message_id, user.id)  # pyright: ignore[reportArgumentType]


@api_router.get("/")
def get_all_messages(  # noqa: ANN201
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    user = get_current_user(token, db)
    return chat_mesage_service.get_all_chat_messages(db, user.id)  # pyright: ignore[reportArgumentType]
