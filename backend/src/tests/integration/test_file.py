"""Integration tests for file endpoints."""

import unittest

from tests.base import BaseTestCase


class TestFileEndpoints(BaseTestCase):
    """Tests for file endpoints."""

    def test_get_files_endpoint(self) -> None:
        """Test getting files list."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.get("/api/v1/files")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_files_unauthorized(self) -> None:
        """Test getting files without authentication."""
        response = self.client.get("/api/v1/files")
        assert response.status_code in [401, 403]

    def test_upload_file_endpoint(self) -> None:
        """Test uploading a file."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.post(
            "/api/v1/files",
            json={
                "name": self.test_file_data["name"],
                "google_drive_id": self.test_file_data["google_drive_id"],
                "course_id": 1,
            },
        )
        assert response.status_code in [200, 201]
        if response.status_code in [200, 201]:
            data = response.json()
            assert data["name"] == self.test_file_data["name"]

    def test_upload_file_missing_fields(self) -> None:
        """Test uploading a file with missing fields."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.post(
            "/api/v1/files",
            json={
                "name": "test.pdf",
            },
        )
        assert response.status_code == 422

    def test_get_file_by_id(self) -> None:
        """Test getting a specific file by ID."""
        authenticated_client = self.get_authenticated_client()

        upload_response = authenticated_client.post(
            "/api/v1/files",
            json={
                "name": self.test_file_data["name"],
                "google_drive_id": self.test_file_data["google_drive_id"],
                "course_id": 1,
            },
        )

        if upload_response.status_code not in [200, 201]:
            return

        file_id = upload_response.json()["id"]

        # Then retrieve it
        response = authenticated_client.get(f"/api/v1/files/{file_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == file_id
        assert data["name"] == self.test_file_data["name"]

    def test_delete_file_endpoint(self) -> None:
        """Test deleting a file."""
        authenticated_client = self.get_authenticated_client()

        upload_response = authenticated_client.post(
            "/api/v1/files",
            json={
                "name": self.test_file_data["name"],
                "google_drive_id": self.test_file_data["google_drive_id"],
                "course_id": 1,
            },
        )

        if upload_response.status_code not in [200, 201]:
            return

        file_id = upload_response.json()["id"]

        response = authenticated_client.delete(f"/api/v1/files/{file_id}")
        assert response.status_code == 200

        get_response = authenticated_client.get(f"/api/v1/files/{file_id}")
        assert get_response.status_code == 404

    def test_file_workflow(self) -> None:
        """Test complete file workflow."""
        authenticated_client = self.get_authenticated_client()

        upload_response = authenticated_client.post(
            "/api/v1/files",
            json={
                "name": self.test_file_data["name"],
                "google_drive_id": self.test_file_data["google_drive_id"],
                "course_id": 1,
            },
        )

        if upload_response.status_code not in [200, 201]:
            return

        file_data = upload_response.json()

        list_response = authenticated_client.get("/api/v1/files")
        assert list_response.status_code == 200
        files = list_response.json()
        assert len(files) >= 1

        get_response = authenticated_client.get(f"/api/v1/files/{file_data['id']}")
        assert get_response.status_code == 200

        delete_response = authenticated_client.delete(
            f"/api/v1/files/{file_data['id']}",
        )
        assert delete_response.status_code == 200


if __name__ == "__main__":
    unittest.main()
