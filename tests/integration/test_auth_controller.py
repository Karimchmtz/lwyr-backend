"""Integration tests for auth controller."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import UserRole
from app.repositories import UserRepository
from app.security import hash_password


class TestAuthController:
    """Integration tests for authentication endpoints."""

    def test_signup_success(self, client: TestClient) -> None:
        """Test successful signup returns 201."""
        response = client.post(
            "/auth/signup",
            json={"email": "test@example.com", "password": "password123"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["role"] == "USER"
        assert data["user_id"] is not None

    def test_signup_invalid_email(self, client: TestClient) -> None:
        """Test signup with invalid email returns 422."""
        response = client.post(
            "/auth/signup",
            json={"email": "invalid-email", "password": "password123"},
        )

        assert response.status_code == 422

    def test_signup_short_password(self, client: TestClient) -> None:
        """Test signup with short password returns 422."""
        response = client.post(
            "/auth/signup",
            json={"email": "test@example.com", "password": "short"},
        )

        assert response.status_code == 422

    def test_signup_duplicate_email(self, client: TestClient) -> None:
        """Test signup with duplicate email returns 409."""
        client.post(
            "/auth/signup",
            json={"email": "existing@example.com", "password": "password123"},
        )

        response = client.post(
            "/auth/signup",
            json={"email": "existing@example.com", "password": "password123"},
        )

        assert response.status_code == 409

    def test_login_success(self, client: TestClient, db: Session) -> None:
        """Test successful login returns 200."""
        user_repo = UserRepository(db)
        user_repo.create(
            email="login@example.com",
            password_hash=hash_password("correctpassword"),
            role=UserRole.USER,
        )

        response = client.post(
            "/auth/login",
            json={"email": "login@example.com", "password": "correctpassword"},
            auth=("login@example.com", "correctpassword"),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "login@example.com"
        assert data["role"] == "USER"

    def test_login_wrong_password(self, client: TestClient, db: Session) -> None:
        """Test login with wrong password returns 401."""
        user_repo = UserRepository(db)
        user_repo.create(
            email="test@example.com",
            password_hash=hash_password("correctpassword"),
            role=UserRole.USER,
        )

        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
            auth=("test@example.com", "wrongpassword"),
        )

        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient) -> None:
        """Test login with nonexistent user returns 401."""
        response = client.post(
            "/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
            auth=("nonexistent@example.com", "password123"),
        )

        assert response.status_code == 401


class TestHealthEndpoints:
    """Tests for health and root endpoints."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test root endpoint returns app info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Lwyr - Legal RAG Agent"
        assert data["version"] == "1.0.0"
