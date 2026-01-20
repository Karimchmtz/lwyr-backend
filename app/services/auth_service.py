"""Authentication service."""

import logging
from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions import AuthenticationException, ResourceAlreadyExistsException
from app.models import UserRole
from app.repositories import UserRepository
from app.security import create_access_token, hash_password, verify_password

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    def signup(self, email: str, password: str) -> dict:
        """Register a new user."""
        logger.info(f"Processing signup for email: {email}")

        if self.user_repository.exists_by_email(email):
            logger.warning(f"Signup failed - email already exists: {email}")
            raise ResourceAlreadyExistsException("Email already registered")

        password_hash = hash_password(password)
        user = self.user_repository.create(email, password_hash, UserRole.USER)

        logger.info(f"User registered successfully: {user['id']}")

        return user

    def login(self, email: str, password: str) -> dict:
        """Authenticate a user and return user data."""
        logger.info(f"Processing login for email: {email}")

        user = self.user_repository.find_by_email(email)
        if user is None:
            logger.warning(f"Login failed - user not found: {email}")
            raise AuthenticationException("Invalid email or password")

        if not verify_password(password, user["password_hash"]):
            logger.warning(f"Login failed - invalid password for email: {email}")
            raise AuthenticationException("Invalid email or password")

        logger.info(f"Login successful for user: {user['id']}")

        return user

    def generate_token(self, user: dict) -> str:
        """Generate a JWT token for a user."""
        return create_access_token(
            user_id=str(user["id"]),
            email=user["email"],
            role=user["role"].value if isinstance(user["role"], UserRole) else user["role"],
        )

    def get_user_by_id(self, user_id: UUID) -> dict | None:
        """Get a user by ID."""
        return self.user_repository.find_by_id(user_id)
