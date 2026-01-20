"""Trained document and embedding models."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Uuid,
)

metadata = MetaData()


trained_documents = Table(
    "trained_documents",
    metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, default=uuid4),
    Column("filename", String(255), nullable=False),
    Column("checksum", String(64), nullable=False),
    Column("embedded_at", DateTime(timezone=True), default=lambda: datetime.now()),
    Column("chunk_count", Integer, default=0),
)
