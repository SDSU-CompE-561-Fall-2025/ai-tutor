from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.file import File
from app.repository.file import FileRepository
from app.schemas.file import FileCreate, FileResponse

FILE_NOT_FOUND_MSG = "File not found or access denied."

def create_file(
    db: Session,
    file: FileCreate,
    user_id: int,
) -> FileResponse:
    """Create a new file.

    Args:
        db: database session
        file: file creation data
        user_id: id of the user creating the file

    Returns:
        FileResponse: Created file response

    Raises:
        HTTPException: If file name already exists in the course
    """

    try:
        db_file = FileRepository.create(db, file, user_id)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"A file with the name '{file.name}' already exists in this course.",
        ) from e

    course_name = FileRepository.get_course_name(db, file.course_id)

    return FileResponse(
        id=db_file.id,  # pyright: ignore[reportArgumentType]
        name=db_file.name,  # pyright: ignore[reportArgumentType]
        google_drive_id=db_file.google_drive_id,  # pyright: ignore[reportArgumentType]
        course_name=course_name,
        created_at=db_file.created_at,  # pyright: ignore[reportArgumentType]
    )


def get_all_files(db: Session, user_id: int) -> list[FileResponse]:
    """Get all files for a user.

    Args:
        db: database session
        user_id: id of the user

    Returns:
        list[FileResponse]: List of FileResponse instances

    Raises:
        HTTPException: If no files are found for the user
    """
    files = FileRepository.get_all(db, user_id)

    if (files is None) or (len(files) == 0):
        raise HTTPException(status_code=404, detail="No files found for the user.")
    return [
        FileResponse(
            id=file.id,  # pyright: ignore[reportArgumentType]
            name=file.name,  # pyright: ignore[reportArgumentType]
            google_drive_id=file.google_drive_id,  # pyright: ignore[reportArgumentType]
            course_name=FileRepository.get_course_name(db, file.course_id),  # pyright: ignore[reportArgumentType]
            created_at=file.created_at,  # pyright: ignore[reportArgumentType]
        )
        for file in files
    ]


def delete_file(
    db: Session,
    file_id: int,
    user_id: int,
) -> None:
    """Delete a file by ID.

    Args:
        db: database session
        file_id: id of the file to delete
        user_id: id of the user

    Returns:
        None
    """
    file = FileRepository.get_file_by_id(db, file_id, user_id)
    if file is None or file.user_id != user_id:
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND_MSG)
    FileRepository.delete(db, file)


def update_file_name(
    db: Session,
    file_id: int,
    new_name: str,
    user_id: int,
) -> FileResponse:
    """Update the name of a file.

    Args:
        db: database session
        file_id: id of the file to update
        new_name: new name for the file
        user_id: id of the user

    Returns:
        FileResponse: Updated file data
    """
    file = FileRepository.get_file_by_id(db, file_id, user_id)
    if not file or file.user_id != user_id:  # pyright: ignore[reportOptionalOperand]
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND_MSG)

    updated_file = FileRepository.update_file_name(db, file, new_name)
    course_name = FileRepository.get_course_name(db, updated_file.course_id)

    return FileResponse(
        id=updated_file.id,  # pyright: ignore[reportArgumentType]
        name=updated_file.name,  # pyright: ignore[reportArgumentType]
        google_drive_id=updated_file.google_drive_id,  # pyright: ignore[reportArgumentType]
        course_name=course_name,
        created_at=updated_file.created_at,  # pyright: ignore[reportArgumentType]
    )


def get_file_by_id(
    db: Session,
    file_id: int,
    user_id: int,
) -> File:
    """Get a file by ID.

    Args:
        db: database session
        file_id: id of the file to retrieve
        user_id: id of the user

    Returns:
        File: Retrieved file instance
    """
    file = FileRepository.get_file_by_id(db, file_id, user_id)
    if not file or file.user_id != user_id:  # pyright: ignore[reportOptionalOperand]
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND_MSG)
    return file


def get_file_response_by_id(
    db: Session,
    file_id: int,
    user_id: int,
) -> FileResponse:
    """Get a file by ID as a FileResponse.

    Args:
        db: database session
        file_id: id of the file to retrieve
        user_id: id of the user

    Returns:
        FileResponse: Retrieved file as FileResponse with all fields

    Raises:
        ValueError: If file not found or access denied
    """
    file = FileRepository.get_file_by_id(db, file_id, user_id)
    if not file or file.user_id != user_id:  # pyright: ignore[reportOptionalOperand]
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND_MSG)

    course_name = FileRepository.get_course_name(db, file.course_id)

    return FileResponse(
        id=file.id,  # pyright: ignore[reportArgumentType]
        name=file.name,  # pyright: ignore[reportArgumentType]
        google_drive_id=file.google_drive_id,  # pyright: ignore[reportArgumentType]
        course_name=course_name,
        created_at=file.created_at,  # pyright: ignore[reportArgumentType]
    )


def get_all_files_from_user_course(
    db: Session,
    user_id: int,
    course_id: int,
) -> list[FileResponse]:
    """Get all files for a specific course of a user.

    Args:
        db: database session
        user_id: ID of the user to retrieve files for
        course_id: ID of the course to retrieve files for

    Returns:
        list[FileResponse]: List of FileResponse instances
    """
    files = FileRepository.get_all_files_from_user_course(db, user_id, course_id)
    course_name = FileRepository.get_course_name(db, course_id)

    if (files is None) or (len(files) == 0):
        raise HTTPException(status_code=404, detail="No files found for the specified course and user.")

    return [
        FileResponse(
            id=file.id,  # pyright: ignore[reportArgumentType]
            name=file.name,  # pyright: ignore[reportArgumentType]
            google_drive_id=file.google_drive_id,  # pyright: ignore[reportArgumentType]
            course_name=course_name,
            created_at=file.created_at,  # pyright: ignore[reportArgumentType]
        )
        for file in files
    ]
