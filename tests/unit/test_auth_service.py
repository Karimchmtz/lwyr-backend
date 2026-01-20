"""Unit tests for auth service."""

import pytest
from sqlalchemy.orm import Session

from app.exceptions import AuthenticationException, ResourceAlreadyExistsException
from app.models import UserRole
from app.security import hash_password, verify_password
from app.services import AuthService


class TestAuthService:
    """Tests for AuthService."""

    def test_signup_success(self, db: Session) -> None:
        """Test successful user signup."""
        auth_service = AuthService(db)

        user = auth_service.signup("new@example.com", "password123")

        assert user is not None
        assert user["email"] == "new@example.com"
        assert user["role"] == UserRole.USER
        assert user["id"] is not None
        assert user["password_hash"] != "password123"

    def test_signup_duplicate_email(self, db: Session) -> None:
        """Test signup with duplicate email raises exception."""
        auth_service = AuthService(db)

        auth_service.signup("existing@example.com", "password123")

        with pytest.raises(ResourceAlreadyExistsException) as exc_info:
            auth_service.signup("existing@example.com", "anotherpassword")

        assert "Email already registered" in str(exc_info.value.message)

    def test_login_success(self, db: Session) -> None:
        """Test successful login."""
        auth_service = AuthService(db)

        auth_service.signup("login@example.com", "correctpassword")

        user = auth_service.login("login@example.com", "correctpassword")

        assert user is not None
        assert user["email"] == "login@example.com"

    def test_login_wrong_password(self, db: Session) -> None:
        """Test login with wrong password raises exception."""
        auth_service = AuthService(db)

        auth_service.signup("test@example.com", "correctpassword")

        with pytest.raises(AuthenticationException):
            auth_service.login("test@example.com", "wrongpassword")

    def test_login_nonexistent_user(self, db: Session) -> None:
        """Test login with nonexistent user raises exception."""
        auth_service = AuthService(db)

        with pytest.raises(AuthenticationException):
            auth_service.login("nonexistent@example.com", "password123")


class TestPasswordHashing:
    """Tests for password hashing functions."""

    def test_password_hash_is_different_from_plain(self) -> None:
        """Test that hashed password is different from plain password."""
        plain_password = "mysecretpassword"
        hashed = hash_password(plain_password)

        assert hashed != plain_password

    def test_password_verification_success(self) -> None:
        """Test successful password verification."""
        plain_password = "mysecretpassword"
        hashed = hash_password(plain_password)

        assert verify_password(plain_password, hashed) is True

    def test_password_verification_failure(self) -> None:
        """Test failed password verification."""
        plain_password = "mysecretpassword"
        wrong_password = "wrongpassword"
        hashed = hash_password(plain_password)

        assert verify_password(wrong_password, hashed) is False

    def test_different_passwords_produce_different_hashes(self) -> None:
        """Test that different passwords produce different hashes."""
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")

        assert hash1 != hash2
