"""
Google Drive Schema
Pydantic models for Google Drive operations.
"""

from pydantic import BaseModel


class FileIdRequest(BaseModel):
    """Request body for file operations."""

    fileid: str
