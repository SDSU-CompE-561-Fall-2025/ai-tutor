"""
User schemas:
this module defines the Pydantic schemas for file data validation and serialization
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    name: str
    google_drive_id: str


class FileCreate(FileBase):
    course_id: int


class FileResponse(BaseModel):
    id: int
    name: str
    google_drive_id: str | None = None
    course_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
