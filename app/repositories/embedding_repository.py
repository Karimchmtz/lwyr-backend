"""Embedding repository for database operations."""

import json
import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import embeddings

logger = logging.getLogger(__name__)


class EmbeddingRepository:
    """Repository for embedding-related database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def find_by_id(self, embedding_id: UUID) -> dict | None:
        """Find an embedding by ID."""
        query = select(embeddings).where(embeddings.c.id == embedding_id)
        result = self.db.execute(query)
        return result.mappings().fetch_one()

    def find_by_document(self, document_id: UUID) -> list[dict]:
        """Find all embeddings for a document."""
        query = select(embeddings).where(
            embeddings.c.trained_document_id == document_id
        ).order_by(embeddings.c.chunk_index.asc())
        result = self.db.execute(query)
        return result.mappings().fetchall()

    def save(
        self,
        trained_document_id: UUID,
        chunk_index: int,
        content: str,
        embedding: list[float],
        page_numbers: list[int] | None = None,
        metadata: dict | None = None,
    ) -> dict:
        """Save a new embedding."""
        query = embeddings.insert().values(
            trained_document_id=trained_document_id,
            chunk_index=chunk_index,
            content=content,
            embedding=embedding,
            page_numbers=str(page_numbers) if page_numbers else None,
            metadata=json.dumps(metadata) if metadata else None,
            created_at=datetime.now(),
        )
        result = self.db.execute(query)
        self.db.commit()

        embedding_id = result.inserted_primary_key[0]
        return self.find_by_id(embedding_id)

    def delete_by_document(self, document_id: UUID) -> int:
        """Delete all embeddings for a document."""
        query = delete(embeddings).where(embeddings.c.trained_document_id == document_id)
        result = self.db.execute(query)
        self.db.commit()
        return result.rowcount

    def count_by_document(self, document_id: UUID) -> int:
        """Count embeddings for a document."""
        query = select(embeddings).where(embeddings.c.trained_document_id == document_id)
        result = self.db.execute(query)
        return len(result.mappings().fetchall())
