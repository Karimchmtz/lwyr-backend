"""Conversation repository for database operations."""

import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.models import MessageRole, conversations, messages

logger = logging.getLogger(__name__)


class ConversationRepository:
    """Repository for conversation-related database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def find_by_id(self, conversation_id: UUID, user_id: UUID) -> dict | None:
        """Find a conversation by ID, verifying ownership."""
        query = select(conversations).where(
            conversations.c.id == conversation_id,
            conversations.c.user_id == user_id,
        )
        result = self.db.execute(query)
        return result.mappings().fetchone()

    def find_by_user(self, user_id: UUID) -> list[dict]:
        """Find all conversations for a user."""
        query = select(conversations).where(conversations.c.user_id == user_id).order_by(
            conversations.c.created_at.desc()
        )
        result = self.db.execute(query)
        return result.mappings().fetchall()

    def create(self, user_id: UUID, title: str | None = None) -> dict:
        """Create a new conversation."""
        now = datetime.now()
        query = conversations.insert().values(
            user_id=user_id,
            title=title,
            created_at=now,
            updated_at=now,
        )
        result = self.db.execute(query)
        self.db.commit()

        conversation_id = result.inserted_primary_key[0]
        return self.find_by_id(conversation_id, user_id)

    def update(self, conversation_id: UUID, user_id: UUID, **kwargs: dict) -> dict | None:
        """Update a conversation."""
        kwargs["updated_at"] = datetime.now()
        query = (
            update(conversations)
            .where(conversations.c.id == conversation_id, conversations.c.user_id == user_id)
            .values(**kwargs)
        )
        self.db.execute(query)
        self.db.commit()

        return self.find_by_id(conversation_id, user_id)

    def delete(self, conversation_id: UUID, user_id: UUID) -> bool:
        """Delete a conversation."""
        query = delete(conversations).where(
            conversations.c.id == conversation_id,
            conversations.c.user_id == user_id,
        )
        result = self.db.execute(query)
        self.db.commit()
        return result.rowcount > 0


class MessageRepository:
    """Repository for message-related database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def find_by_conversation(self, conversation_id: UUID) -> list[dict]:
        """Find all messages for a conversation."""
        query = select(messages).where(
            messages.c.conversation_id == conversation_id
        ).order_by(messages.c.created_at.asc())
        result = self.db.execute(query)
        return result.mappings().fetchall()

    def create(
        self,
        conversation_id: UUID,
        role: MessageRole,
        content: str,
        citations: str | None = None,
    ) -> dict:
        """Create a new message."""
        query = messages.insert().values(
            conversation_id=conversation_id,
            role=role,
            content=content,
            citations=citations,
        )
        result = self.db.execute(query)
        self.db.commit()

        message_id = result.inserted_primary_key[0]
        query = select(messages).where(messages.c.id == message_id)
        result = self.db.execute(query)
        return result.mappings().fetch_one()
