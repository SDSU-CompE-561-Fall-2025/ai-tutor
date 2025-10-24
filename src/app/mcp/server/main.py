"""
Google Drive MCP Server Module integrated with a shared  database.
OAuth tokens are stored in the UserToken table .
"""

import io

from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.http import MediaIoBaseDownload

from app.core.database import SessionLocal
from app.core.settings import settings
from app.services.auth_token import AuthTokenService

mcp = FastMCP()


class GoogleDriveClient:
    """
    Google Drive MCP Server that uses shared database for OAuth tokens.
    """

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.db = SessionLocal()
        self.SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
        self.service = self._get_service()

    def _get_credentials(self) -> dict | None:
        """
        Retrieve stored OAuth tokens for a user from the database given their ID

        Args:
            user_id: User ID
        """

        tokens = AuthTokenService.get_auth_token(self.db, self.user_id)
        return Credentials(
            token=tokens.access_token,  # pyright: ignore[reportOptionalMemberAccess]
            refresh_token=tokens.refresh_token,  # type: ignore  # noqa: PGH003
            token_uri=settings.token_uri,
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            scopes=self.SCOPES,
        )

    def _get_service(self) -> Resource:
        creds = self._get_credentials()
        return build("drive", "v3", credentials=creds)

    def search_files(self, query: str, page_size: int = 10) -> dict:
        """Search for files in Google Drive."""
        try:
            results = (
                self.service.files()  # pyright: ignore[reportAttributeAccessIssue]
                .list(
                    q=f"name contains '{query}'",
                    pageSize=page_size,
                    fields="nextPageToken, files(id, name, mimeType, webViewLink)",
                )
                .execute()
            )

            return {
                "files": [
                    {
                        "id": f["id"],
                        "name": f["name"],
                        "mime_type": f["mimeType"],
                        "web_view_link": f["webViewLink"],
                    }
                    for f in results.get("files", [])
                ],
                "next_page_token": results.get("nextPageToken"),
            }
        except Exception as e:  # noqa: BLE001
            return {"error": str(e)}

    def get_file(self, file_id: str) -> dict:
        try:
            # Get file metadata
            file_metadata = (
                self.service.files()  # pyright: ignore[reportAttributeAccessIssue]
                .get(fileId=file_id, fields="id, name, mimeType, webViewLink")
                .execute()
            )

            mime_type = file_metadata.get("mimeType")

            # Handle Google Docs/Sheets/Slides with export
            if mime_type.startswith("application/vnd.google-apps"):
                if mime_type == "application/vnd.google-apps.document":
                    export_mime = "text/plain"
                elif mime_type == "application/vnd.google-apps.spreadsheet":
                    export_mime = "text/csv"
                elif mime_type == "application/vnd.google-apps.presentation":
                    export_mime = "text/plain"
                else:
                    export_mime = "text/plain"

                exported = (
                    self.service.files()  # pyright: ignore[reportAttributeAccessIssue]
                    .export(fileId=file_id, mimeType=export_mime)
                    .execute()
                )

                return {"metadata": file_metadata, "content": exported}

            # Otherwise, download file directly
            request = self.service.files().get_media(fileId=file_id)  # pyright: ignore[reportAttributeAccessIssue]
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                done = downloader.next_chunk()

            return {
                "metadata": file_metadata,
                "content": fh.getvalue().decode("utf-8", errors="ignore"),
            }

        except Exception as e:  # noqa: BLE001
            return {"error": str(e)}


# -------------------------------
# MCP Tool Definitions
# -------------------------------
@mcp.tool()
def gdrive_search(query: str, user_id: int, page_size: int = 10) -> dict:
    """Search for files in Google Drive."""
    drive_client = GoogleDriveClient(int(user_id))
    return drive_client.search_files(query=query, page_size=page_size)


@mcp.tool()
def gdrive_read_file(file_id: str, user_id: int) -> dict:
    """Read file content + metadata from Google Drive."""
    drive_client = GoogleDriveClient(user_id)
    return drive_client.get_file(file_id=file_id)


# -------------------------------
# Main Entry Point
# -------------------------------
def main() -> None:
    mcp.run(transport="http", port=8000)


if __name__ == "__main__":
    main()
