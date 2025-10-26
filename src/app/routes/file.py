from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session

from app.models.course import Course
import app.services.file as file_service
from app.core.auth import oauth2_scheme
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.file import FileCreate, FileResponse

api_router = APIRouter (
    prefix="/files",
    tags=["files"],
)

@api_router.post("/")
async def create_file(
    file: FileCreate, 
    # Annotated helps separate typing information from FASTAPI's dependency system cleanly
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> FileResponse:
    """create a new file"""
    user = get_current_user(token, db)
    return file_service.create_file(
        db, 
        file, 
        user.id
    )

@api_router.get("/")
async def get_all_files(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> list[FileResponse]:
    """get all files for the current user"""
    user = get_current_user(token, db)
    return file_service.get_all_files(db, user.id)

@api_router.get("/{file_id}")
async def get_file(
    file_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> FileResponse:
    """get a file by ID"""
    user = get_current_user(token, db)
    file = file_service.get_file_by_id(db, file_id, user.id)
    if file is None or file.user_id != user.id:
        raise HTTPException(status_code=404, detail="File not found or access denied.")
    
    # Get course name
    course = db.query(Course).filter(Course.id == file.course_id).first()
    course_name = course.name if course else "Unknown Course"
    
    return FileResponse(
        id = file.id,
        name = file.name,
        course_name = course_name,
        created_at = file.created_at
    )

@api_router.put("/{file_id}")
async def update_file_name(
    file_id: int,
    new_name: str,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> FileResponse:
    """update a file's name by ID"""
    user = get_current_user(token, db)
    return file_service.update_file_name(db, file_id, new_name, user.id)

@api_router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    """delete a file by ID"""
    user = get_current_user(token, db)
    file_service.delete_file(db, file_id, user.id)

