import datetime
from enum import Enum

from pydantic import BaseModel


class ChatMessageSenderType(str, Enum):
    user = "user"
    assistant = "assistant"


class ChatMessageBase(BaseModel):
    role: ChatMessageSenderType
    message: str


class ChatMessageCreate(ChatMessageBase):
    tutor_session_id: int


class ChatMessageResponse(ChatMessageBase):
    id: int
    tutor_session_title: str | None = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True
