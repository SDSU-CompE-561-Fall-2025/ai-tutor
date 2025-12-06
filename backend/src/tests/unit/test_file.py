"""Unit tests for file management."""

import unittest

from app.models.file import File
from app.schemas.file import FileCreate
from tests.base import BaseTestCase


class TestFileCreation(BaseTestCase):
    """Tests for file creation."""

    def test_file_creation(self) -> None:
        """Test creating a file."""
        user = self.create_registered_user()
        file = File(
            filename=self.test_file_data["filename"],
            file_type=self.test_file_data["file_type"],
            user_id=user.id,
            content="Sample file content",
        )
        self.db_session.add(file)
        self.db_session.commit()
        self.db_session.refresh(file)

        assert file.id is not None
        assert file.filename == self.test_file_data["filename"]
        assert file.file_type == self.test_file_data["file_type"]
        assert file.user_id == user.id
        assert file.content == "Sample file content"

    def test_file_model_fields(self) -> None:
        """Test that all required file model fields are present."""
        user = self.create_registered_user()
        file = File(
            filename=self.test_file_data["filename"],
            file_type=self.test_file_data["file_type"],
            user_id=user.id,
            content="Test content",
        )
        self.db_session.add(file)
        self.db_session.commit()
        self.db_session.refresh(file)

        assert hasattr(file, "id")
        assert hasattr(file, "filename")
        assert hasattr(file, "file_type")
        assert hasattr(file, "user_id")
        assert hasattr(file, "content")
        assert hasattr(file, "created_at")

    def test_multiple_files_same_user(self) -> None:
        """Test creating multiple files for the same user."""
        user = self.create_registered_user()
        file1 = File(
            filename="document1.pdf",
            file_type="pdf",
            user_id=user.id,
            content="First document",
        )
        file2 = File(
            filename="document2.docx",
            file_type="docx",
            user_id=user.id,
            content="Second document",
        )
        self.db_session.add(file1)
        self.db_session.add(file2)
        self.db_session.commit()

        files = self.db_session.query(File).filter_by(user_id=user.id).all()
        assert len(files) == 2

    def test_file_schema_validation(self) -> None:
        """Test file schema validation."""
        file_data = {
            "filename": "test.pdf",
            "file_type": "pdf",
        }
        file_create = FileCreate(**file_data)
        assert file_create.filename == file_data["filename"]
        assert file_create.file_type == file_data["file_type"]

    def test_file_types(self) -> None:
        """Test different file types."""
        file_types = ["pdf", "docx", "txt", "pptx", "xlsx"]
        for file_type in file_types:
            file_data = {
                "filename": f"test.{file_type}",
                "file_type": file_type,
            }
            file_create = FileCreate(**file_data)
            assert file_create.file_type == file_type


if __name__ == "__main__":
    unittest.main()
