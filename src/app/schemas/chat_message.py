import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ChatMessageSenderType(str, Enum):
    user = "user"
    assistant = "assistant"


class ChatMessageBase(BaseModel):
    role: ChatMessageSenderType
    message: str


class ChatMessageCreate(ChatMessageBase):
    tutor_session_id: int


class ChatMessageResponse(ChatMessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tutor_session_title: str | None = None
    created_at: datetime.datetime
