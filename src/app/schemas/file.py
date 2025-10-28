"""
User schemas: 
this module defines the Pydantic schemas for file data validation and serialization
"""

from pydantic import BaseModel
from datetime import datetime

class FileBase(BaseModel):
    name: str

class FileCreate(FileBase): 
    course_id: int

class FileResponse(FileBase):
    id: int
    course_name: str
    created_at: datetime

    class Config:
        from_attributes = True
