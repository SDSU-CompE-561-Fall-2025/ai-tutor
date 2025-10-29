import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.chat_message import ChatMessageResponse


class TutorSessionBase(BaseModel):
    title: str | None = None


class TutorSessionCreate(TutorSessionBase):
    course_id: int


class TutorSessionResponse(TutorSessionBase):
    id: int
    course_name: str
    chat_messages: list[ChatMessageResponse]
    created_at: datetime.datetime
    ended_at: datetime.datetime | None = None

    model_config = ConfigDict(from_attributes=True)
