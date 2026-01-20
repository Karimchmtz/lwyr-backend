"""Embedding model for vector storage."""

from datetime import datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    Uuid,
)

metadata = MetaData()


embeddings = Table(
    "embeddings",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("trained_document_id", Uuid(as_uuid=True), ForeignKey("trained_documents.id", ondelete="CASCADE"), nullable=False),
    Column("chunk_index", Integer, nullable=False),
    Column("content", Text, nullable=False),
    Column("embedding", Vector(8192), nullable=False),
    Column("page_numbers", String),  # INTEGER[] stored as string
    Column("metadata", Text),  # JSONB stored as text
    Column("created_at", DateTime(timezone=True), default=lambda: datetime.now()),
)
