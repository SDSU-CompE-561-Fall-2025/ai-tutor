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
        assert data["description"] == self.test_class_data["description"]

    def test_get_course_by_id(self) -> None:
        """Test getting a specific course by ID."""
        authenticated_client = self.get_authenticated_client()
        create_response = authenticated_client.post(
            "/api/v1/courses",
            json=self.test_class_data,
        )
        course_id = create_response.json()["id"]

        response = authenticated_client.get(f"/api/v1/courses/{course_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == course_id
        assert data["name"] == self.test_class_data["name"]
        assert data["description"] == self.test_class_data["description"]

    def test_update_course_endpoint(self) -> None:
        """Test updating a course."""
        authenticated_client = self.get_authenticated_client()
        create_response = authenticated_client.post(
            "/api/v1/courses",
            json=self.test_class_data,
        )
        course_id = create_response.json()["id"]

        updated_data = {
            "name": "Updated Class Name",
            "description": "Updated course description",
        }
        response = authenticated_client.put(
            f"/api/v1/courses/{course_id}",
            json=updated_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == updated_data["name"]
        assert data["description"] == updated_data["description"]

    def test_delete_course_endpoint(self) -> None:
        """Test deleting a course."""
        authenticated_client = self.get_authenticated_client()
        create_response = authenticated_client.post(
            "/api/v1/courses",
            json=self.test_class_data,
        )
        course_id = create_response.json()["id"]

        response = authenticated_client.delete(f"/api/v1/courses/{course_id}")
        assert response.status_code == 200

        get_response = authenticated_client.get(f"/api/v1/courses/{course_id}")
        assert get_response.status_code == 404

    def test_create_course_without_description(self) -> None:
        """Test creating a course without a description defaults to empty string."""
        authenticated_client = self.get_authenticated_client()
        course_data = {"name": "Course Without Description"}
        response = authenticated_client.post(
            "/api/v1/courses",
            json=course_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == course_data["name"]
        assert data["description"] == ""


if __name__ == "__main__":
    unittest.main()
