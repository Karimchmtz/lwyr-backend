"""Trained document repository for database operations."""

import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import trained_documents

logger = logging.getLogger(__name__)


class TrainedDocumentRepository:
    """Repository for trained document-related database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def find_by_id(self, document_id: UUID) -> dict | None:
        """Find a trained document by ID."""
        query = select(trained_documents).where(trained_documents.c.id == document_id)
        result = self.db.execute(query)
        return result.mappings().fetch_one()

    def find_by_filename(self, filename: str) -> dict | None:
        """Find a trained document by filename."""
        query = select(trained_documents).where(trained_documents.c.filename == filename)
        result = self.db.execute(query)
        return result.mappings().fetch_one()

    def find_all(self) -> list[dict]:
        """Find all trained documents."""
        query = select(trained_documents).order_by(trained_documents.c.embedded_at.desc())
        result = self.db.execute(query)
        return result.mappings().fetchall()

    def create(self, filename: str, checksum: str, chunk_count: int = 0) -> dict:
        """Create a new trained document record."""
        query = trained_documents.insert().values(
            filename=filename,
            checksum=checksum,
            chunk_count=chunk_count,
            embedded_at=datetime.now(),
        )
        result = self.db.execute(query)
        self.db.commit()

        document_id = result.inserted_primary_key[0]
        return self.find_by_id(document_id)

    def update_chunk_count(self, document_id: UUID, chunk_count: int) -> dict | None:
        """Update the chunk count for a document."""
        query = (
            update(trained_documents)
            .where(trained_documents.c.id == document_id)
            .values(chunk_count=chunk_count)
        )
        self.db.execute(query)
        self.db.commit()

        return self.find_by_id(document_id)

    def exists_by_checksum(self, checksum: str) -> bool:
        """Check if a document with the given checksum exists."""
        document = self.find_by_checksum(checksum)
        return document is not None

    def find_by_checksum(self, checksum: str) -> dict | None:
        """Find a trained document by checksum."""
        query = select(trained_documents).where(trained_documents.c.checksum == checksum)
        result = self.db.execute(query)
        return result.mappings().fetch_one()
