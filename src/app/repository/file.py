"""
file repository: data access layer for file operations
"""

from sqlalchemy.orm import Session

from app.models.file import File 
from app.schemas.file import FileCreate

class FileRepository: 
    """Repository for File data access"""

    @staticmethod
    def get_file_by_id(db: Session, file_id: int, user_id: int) -> File | None: 
        """
        Get file by ID

        Args: 
            db (Session): database session
            file_id (int): ID of the file to retrieve
        """
        return db.query(File).filter(File.id == file_id, File.user_id == user_id).first()
    
    @staticmethod
    def create(
        db: Session, 
        file: FileCreate,
        user_id: int, 
    ) -> File: 
        """
        Create a new file. 
        
        Args: 
            db (Session): database session
            file (FileCreate): file data
            user_id (int): ID of the user creating the file
        """

        db_file = File(
            name = file.name, 
            user_id = user_id, 
            course_id = file.course_id,
        )

        db.add(db_file)
        db.commit() 
        db.refresh(db_file)
        return db_file
    
    @staticmethod 
    def delete(db: Session, db_file: File) -> None: 
        """
        Delete a file

        Args: 
            db (Session): database session
            db_file (File): File instance to delete
        """
        db.delete(db_file)
        db.commit() 

    @staticmethod
    def get_all(db: Session, user_id: int) -> list[File]:
        """
        Get all files for a user

        Args:
            db: database session
            user_id: ID of the user to retrieve files for
        """
        return db.query(File).filter(File.user_id == user_id).all()

    @staticmethod
    def update_file_name(
        db: Session, 
        db_file: File, 
        new_name: str
    ) -> File: 
        """
        Update the name of a file. 
        
        Args: 
            db: database session 
            db_file: File instance to update
            new_name: new name for the file
        """
        db_file.name = new_name
        db.commit()
        db.refresh(db_file)
        return db_file
    
    @staticmethod
    def get_all_files_from_user_course(
        db: Session, 
        user_id: int, 
        course_id: int
    ) -> list[File]:
        """
        Get all files for a specific course of a user

        Args:
            db: database session
            user_id: ID of the user to retrieve files for
            course_id: ID of the course to retrieve files for
        """
        return db.query(File).filter(File.user_id == user_id, File.course_id == course_id).all()