"""User model and related database tables."""

import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    MetaData,
    String,
    Table,
    Uuid,
)

metadata = MetaData()


class UserRole(str, enum.Enum):
    """User role enumeration."""

    USER = "USER"
    ADMIN = "ADMIN"


users = Table(
    "users",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("email", String(255), nullable=False, unique=True, index=True),
    Column("password_hash", String(255), nullable=False),
    Column("role", Enum(UserRole, name="user_role", create_constraint=False), nullable=False),
    Column("created_at", DateTime(timezone=True), default=lambda: datetime.now()),
    Column("updated_at", DateTime(timezone=True), default=lambda: datetime.now(), onupdate=lambda: datetime.now()),
)
