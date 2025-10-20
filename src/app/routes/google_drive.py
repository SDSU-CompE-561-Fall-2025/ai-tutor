from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.google_drive import GoogleDriveService

api_router = APIRouter(
    prefix="/drive",
    tags=["Google_Drive"],
)


@api_router.get("/search/")
async def search_with_query(
    current_user: Annotated[User, Depends(get_current_user)],
    q: Annotated[str | None, Query()] = None,
) -> list | dict | None:
    if q:
        return await GoogleDriveService.search(str(current_user.id), q)
    return await GoogleDriveService.search_all(str(current_user.id))


@api_router.get("/search/all")
async def search_user_files(
    current_user: Annotated[User, Depends(get_current_user)],
) -> list | dict:
    """
    Get current user profile.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current user data
        AuthToken: Current user's auth token data
    """
    return await GoogleDriveService.search_all(str(current_user.id))


@api_router.get("/read/")
async def read_by_file_id(
    current_user: Annotated[User, Depends(get_current_user)],
    q: Annotated[str | None, Query()] = None,
) -> list | dict | None:
    if q:
        return await GoogleDriveService.read_file(str(current_user.id), q)
    return {"Error": "Need File ID to read file"}
