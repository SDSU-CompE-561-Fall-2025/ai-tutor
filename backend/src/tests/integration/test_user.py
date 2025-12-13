"""Integration tests for user endpoints."""

import unittest

from tests.base import BaseTestCase


class TestUserLogin(BaseTestCase):
    """Tests for user login endpoint."""

    def test_user_login_endpoint(self) -> None:
        """Test user login endpoint."""
        self.create_registered_user()
        response = self.client.post(
            "/api/v1/user/login",
            data={
                "username": self.test_user_data["email"],
                "password": self.test_user_data["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_user_login_invalid_credentials(self) -> None:
        """Test login with invalid credentials."""
        self.create_registered_user()
        response = self.client.post(
            "/api/v1/user/login",
            data={
                "username": self.test_user_data["email"],
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_user_login_nonexistent_email(self) -> None:
        """Test login with non-existent email."""
        response = self.client.post(
            "/api/v1/user/login",
            data={
                "username": "nonexistent@example.com",
                "password": "password",
            },
        )
        assert response.status_code == 401

    def test_user_registration_invalid_password(self) -> None:
        """Test user registration with invalid password."""
        # Password too short
        response = self.client.post(
            "/api/v1/user/register",
            json={
                "email": "newuser@example.com",
                "password": "Pass@1",  # Too short
                "first_name": "New",
                "last_name": "User",
            },
        )
        assert response.status_code == 422
        assert "at least 8 characters" in response.text.lower()

    def test_user_registration_invalid_name_length(self) -> None:
        """Test user registration with name exceeding max length."""
        response = self.client.post(
            "/api/v1/user/register",
            json={
                "email": "newuser@example.com",
                "password": "Valid@123",
                "first_name": "A" * 16,  # Too long
                "last_name": "User",
            },
        )
        assert response.status_code == 422

    def test_user_registration_invalid_email_length(self) -> None:
        """Test user registration with email exceeding max length."""
        response = self.client.post(
            "/api/v1/user/register",
            json={
                "email": "a" * 25 + "@example.com",  # >30 chars
                "password": "Valid@123",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        assert response.status_code == 422


class TestUserProfile(BaseTestCase):
    """Tests for user profile endpoints."""

    def test_get_current_user_endpoint(self) -> None:
        """Test getting current user profile."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.get("/api/v1/user/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == self.test_user_data["email"]
        assert "first_name" in data
        assert "last_name" in data

    def test_get_current_user_unauthorized(self) -> None:
        """Test getting current user without authentication."""
        response = self.client.get("/api/v1/user/me")
        assert response.status_code in [401, 403]

    def test_update_user_profile(self) -> None:
        """Test updating user profile."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.put(
            "/api/v1/user/me",
            json={
                "first_name": "Updated",
                "last_name": "Name",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"

    def test_update_user_profile_partial(self) -> None:
        """Test partial user profile update."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.put(
            "/api/v1/user/me",
            json={
                "first_name": None,
                "last_name": None,
            },
        )
        assert response.status_code == 200

    def test_update_user_profile_unauthorized(self) -> None:
        """Test updating user profile without authentication."""
        response = self.client.put(
            "/api/v1/user/me",
            json={
                "name": "Updated Name",
            },
        )
        assert response.status_code in [401, 403]

    def test_get_user_token_endpoint(self) -> None:
        """Test getting user's OAuth token."""
        authenticated_client = self.get_authenticated_client()
        response = authenticated_client.get("/api/v1/user/token")
        # Will be 404 if no auth token was created for the user
        assert response.status_code in [200, 404]


if __name__ == "__main__":
    unittest.main()
