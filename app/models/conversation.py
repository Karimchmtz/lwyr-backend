"""Conversation and Message models."""

import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    MetaData,
    String,
    Table,
    Text,
    Uuid,
)

metadata = MetaData()


class MessageRole(str, enum.Enum):
    """Message role enumeration."""

    USER = "USER"
    ASSISTANT = "ASSISTANT"


conversations = Table(
    "conversations",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("title", String(255)),
    Column("created_at", DateTime(timezone=True), default=lambda: datetime.now()),
    Column("updated_at", DateTime(timezone=True), default=lambda: datetime.now(), onupdate=lambda: datetime.now()),
)

messages = Table(
    "messages",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("conversation_id", Uuid(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
    Column("role", Enum(MessageRole, name="message_role", create_constraint=False), nullable=False),
    Column("content", Text, nullable=False),
    Column("citations", Text),  # JSONB stored as text
    Column("created_at", DateTime(timezone=True), default=lambda: datetime.now()),
)
