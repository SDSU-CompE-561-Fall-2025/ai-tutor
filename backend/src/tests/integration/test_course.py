"""Integration tests for class/course endpoints."""

import unittest

from tests.base import BaseTestCase


class TestCourseEndpoints(BaseTestCase):
    """Tests for course endpoints."""

    def test_get_courses_endpoint(self) -> None:
        """Test getting courses list."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.get("/api/v1/courses")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_courses_unauthorized(self) -> None:
        """Test getting courses without authentication."""
        response = self.client.get("/api/v1/courses")
        assert response.status_code in [401, 403]

    def test_create_course_endpoint(self) -> None:
        """Test creating a course."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.post(
            "/api/v1/courses",
            json=self.test_class_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == self.test_class_data["name"]

    def test_create_course_missing_fields(self) -> None:
        """Test creating a course with missing fields."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.post(
            "/api/v1/courses",
            json={
                "name": "",
            },
        )
        assert response.status_code in 422

    def test_get_course_by_id(self) -> None:
        """Test getting a specific course by ID."""
        authenticated_client = self.get_authenticated_client()
        # First create a course
        create_response = authenticated_client.post(
            "/api/v1/courses",
            json=self.test_class_data,
        )
        course_id = create_response.json()["id"]

        # Then retrieve it
        response = authenticated_client.get(f"/api/v1/courses/{course_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == course_id
        assert data["name"] == self.test_class_data["name"]

    def test_update_course_endpoint(self) -> None:
        """Test updating a course."""
        authenticated_client = self.get_authenticated_client()
        # Create a course first
        create_response = authenticated_client.post(
            "/api/v1/courses",
            json=self.test_class_data,
        )
        course_id = create_response.json()["id"]

        # Update it
        updated_data = {
            "name": "Updated Class Name",
        }
        response = authenticated_client.put(
            f"/api/v1/courses/{course_id}",
            json=updated_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == updated_data["name"]

    def test_delete_course_endpoint(self) -> None:
        """Test deleting a course."""
        authenticated_client = self.get_authenticated_client()
        # Create a course first
        create_response = authenticated_client.post(
            "/api/v1/courses",
            json=self.test_class_data,
        )
        course_id = create_response.json()["id"]

        # Delete it
        response = authenticated_client.delete(f"/api/v1/courses/{course_id}")
        assert response.status_code == 200

        # Verify it's deleted
        get_response = authenticated_client.get(f"/api/v1/courses/{course_id}")
        assert get_response.status_code == 404


if __name__ == "__main__":
    unittest.main()
