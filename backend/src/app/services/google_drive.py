"""
Google Drive Service
--------------------
Handles business logic for Google Drive operations via MCP.
"""

import json

from fastmcp import Client

from app.core.settings import settings


def get_mcp_client() -> Client:
    """Return a configured FastMCP client instance."""
    return Client(settings.mcp_server)


class GoogleDriveService:
    """Service layer for Google Drive MCP operations."""

    @staticmethod
    async def search(
        user_id: int,
        query: str = "",
    ) -> list | dict | None:
        """
        Search Google Drive files for a given user.

        Args:
            user_id: The user ID whose Drive to search.
            query: The text to search for in Drive.
            client: Optional MCP client; if not provided, one will be created.

        Returns:
            A parsed list of files.
        """
        client = get_mcp_client()

        async with client:
            result = await client.call_tool(
                "gdrive_search",
                {"query": query, "user_id": user_id},
            )

            # Extract text and parse JSON
            raw_text = result.content[0].text  # pyright: ignore[reportAttributeAccessIssue]
            parsed = json.loads(raw_text)

            return parsed.get("files", [])

    @staticmethod
    async def read_file(
        user_id: int,
        file_id: str,
    ) -> dict:
        """Read and extract a files metadata and content."""
        client = get_mcp_client()

        async with client:
            result = await client.call_tool(
                "gdrive_read_file",
                {"file_id": file_id, "user_id": user_id},
            )

            raw_text = result.content[0].text  # pyright: ignore[reportAttributeAccessIssue]
            parsed = json.loads(raw_text)

            return {
                "content": parsed.get("content", ""),
            }

    @staticmethod
    async def search_all(user_id: int) -> list | dict:
        client = get_mcp_client()
        async with client:
            result = await client.call_tool(
                "gdrive_search",
                {"query": "", "user_id": user_id},
            )

            # Extract text and parse JSON
            raw_text = result.content[0].text  # pyright: ignore[reportAttributeAccessIssue]
            parsed = json.loads(raw_text)

            return parsed.get("files", [])
