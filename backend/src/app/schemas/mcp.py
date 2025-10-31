"""Pydantic schemas for MCP (Model Context Protocol) server models."""

from pydantic import BaseModel


class FileResult(BaseModel):
    """File search result model."""

    id: str
    name: str
    mime_type: str
    web_view_link: str


class SearchResult(BaseModel):
    """Search results model."""

    files: list[FileResult]
    next_page_token: str | None = None


class FileContent(BaseModel):
    """File content model."""

    metadata: dict
    content: str | bytes
