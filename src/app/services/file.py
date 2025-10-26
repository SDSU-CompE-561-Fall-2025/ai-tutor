from sqlalchemy.orm import Session 
from app.models.file import File 
from app.repository.file import FileRepository 
from app.models.course import Course
from app.schemas.file import FileCreate, FileResponse

FILE_NOT_FOUND_MSG = "File not found or access denied."

def create_file(
    db: Session, 
    file: FileCreate, 
    user_id: int 
) -> FileResponse:
    """
    Create a new file

    Args: 
        db: database session
        file: file creation data
        user_id: id of the user creating the file

    Returns:
        File: Created file instance
    """

    db_file = FileRepository.create(db, file, user_id)
    
    # Get course name separately to avoid relationship loading issues
    course = db.query(Course).filter(Course.id == file.course_id).first()
    course_name = course.name if course else "Unknown Course"
    
    return FileResponse(
        id = db_file.id, 
        name = db_file.name, 
        course_name = course_name, 
        created_at = db_file.created_at
    )

def get_all_files(db: Session, user_id: int) -> list[FileResponse]:
    """
    Get all files for a user. 

    Args: 
        db: database session
        user_id: id of the user 
    Returns: 
        list[FileResponse]: List of FileResponse instances
    """
    files = FileRepository.get_all(db, user_id)
    result = []
    for file in files:
        # Get course name for each file
        course = db.query(Course).filter(Course.id == file.course_id).first()
        course_name = course.name if course else "Unknown Course"
        
        result.append(FileResponse(
            id=file.id,
            name=file.name,
            course_name=course_name,
            created_at=file.created_at
        ))
    return result

def delete_file(db: Session, file_id: int, user_id: int) -> None: 
    """
    Delete a file by ID
    
    Args: 
        db: database session
        file_id: id of the file to delete
        user_id: id of the user
        
    Returns:
        None
    """
    file = FileRepository.get_file_by_id(db, file_id, user_id)
    if file is None or file.user_id != user_id:
        raise ValueError(FILE_NOT_FOUND_MSG)
    FileRepository.delete(db, file)

def update_file_name(
    db: Session, 
    file_id: int, 
    new_name: str, 
    user_id: int
) -> FileResponse:
    """
    Update the name of a file.
    
    Args: 
        db: database session
        file_id: id of the file to update
        new_name: new name for the file
        user_id: id of the user

    Returns:
        FileResponse: Updated file data
    """
    file = FileRepository.get_file_by_id(db, file_id, user_id)
    if file is None or file.user_id != user_id:
        raise ValueError(FILE_NOT_FOUND_MSG)
    
    file.name = new_name
    db.commit()
    db.refresh(file)

    # Get course name separately to avoid relationship loading issues
    course = db.query(Course).filter(Course.id == file.course_id).first()
    course_name = course.name if course else "Unknown Course"
    
    return FileResponse(
        id = file.id, 
        name = file.name, 
        course_name = course_name, 
        created_at = file.created_at
)

def get_file_by_id(
    db: Session, 
    file_id: int, 
    user_id: int
) -> File:
    """
    Get a file by ID.
    
    Args: 
        db: database session
        file_id: id of the file to retrieve
        user_id: id of the user

    Returns:
        File: Retrieved file instance
    """
    file = FileRepository.get_file_by_id(db, file_id, user_id)
    if file is None or file.user_id != user_id:
        raise ValueError(FILE_NOT_FOUND_MSG)
    return file

 