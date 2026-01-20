"""User repository for database operations."""

import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import UserRole, users

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user-related database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def find_by_id(self, user_id: UUID) -> dict | None:
        """Find a user by ID."""
        query = select(users).where(users.c.id == user_id)
        result = self.db.execute(query)
        return result.mappings().fetchone()

    def find_by_email(self, email: str) -> dict | None:
        """Find a user by email."""
        query = select(users).where(users.c.email == email)
        result = self.db.execute(query)
        return result.mappings().fetchone()

    def exists_by_email(self, email: str) -> bool:
        """Check if a user exists by email."""
        user = self.find_by_email(email)
        return user is not None

    def create(self, email: str, password_hash: str, role: UserRole) -> dict:
        """Create a new user."""
        now = datetime.now()
        query = users.insert().values(
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=now,
            updated_at=now,
        )
        result = self.db.execute(query)
        self.db.commit()

        user_id = result.inserted_primary_key[0]
        return self.find_by_id(user_id)

    def save(self, user_data: dict) -> dict:
        """Save a user (alias for create)."""
        return self.create(
            email=user_data["email"],
            password_hash=user_data["password_hash"],
            role=user_data["role"],
        )
