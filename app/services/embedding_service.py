"""Embedding service for vector operations."""

import json
import logging
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.repositories import EmbeddingRepository, TrainedDocumentRepository
from app.services.openrouter_service import OpenRouterService

logger = logging.getLogger(__name__)
settings = get_settings()


class EmbeddingService:
    """Service for embedding generation and storage."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.openrouter_service = OpenRouterService()
        self.embedding_repository = EmbeddingRepository(db)
        self.trained_document_repository = TrainedDocumentRepository(db)

    def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        logger.info(f"Generating embedding for text ({len(text)} chars)")
        embedding = self.openrouter_service.generate_embedding(text)
        logger.debug(f"Embedding generated with {len(embedding)} dimensions")
        return embedding

    def store_embeddings(
        self,
        trained_document_id: UUID,
        chunks: list[str],
    ) -> int:
        """Store embeddings for document chunks."""
        logger.info(f"Storing {len(chunks)} embeddings for document {trained_document_id}")

        embeddings = self.openrouter_service.generate_embeddings(chunks)

        for index, chunk in enumerate(chunks):
            embedding_record = self.embedding_repository.save(
                trained_document_id=trained_document_id,
                chunk_index=index,
                content=chunk,
                embedding=embeddings[index],
                metadata={"chunk_size": len(chunk)},
            )
            logger.debug(f"Stored embedding {index + 1}/{len(chunks)}")

        self.trained_document_repository.update_chunk_count(
            trained_document_id, len(chunks)
        )

        logger.info(f"Successfully stored {len(chunks)} embeddings")
        return len(chunks)

    def similarity_search(
        self,
        query: str,
        max_results: int = settings.embedding_max_results,
        similarity_threshold: float = settings.embedding_similarity_threshold,
    ) -> list[dict]:
        """Search for similar embeddings."""
        logger.info(f"Performing similarity search for query ({len(query)} chars)")

        query_embedding = self.openrouter_service.generate_embedding(query)

        similarity_query = text("""
            SELECT
                id,
                trained_document_id,
                chunk_index,
                content,
                1 - (embedding <=> :query_vector) AS similarity
            FROM embeddings
            WHERE 1 - (embedding <=> :query_vector) > :threshold
            ORDER BY embedding <=> :query_vector
            LIMIT :limit
        """)

        result = self.db.execute(
            similarity_query,
            {
                "query_vector": query_embedding,
                "threshold": similarity_threshold,
                "limit": max_results,
            },
        )

        rows = result.mappings().fetchall()
        results = []
        for row in rows:
            row_dict = dict(row)
            if row_dict.get("metadata"):
                try:
                    row_dict["metadata"] = json.loads(row_dict["metadata"])
                except (json.JSONDecodeError, TypeError):
                    row_dict["metadata"] = None
            results.append(row_dict)

        logger.info(f"Found {len(results)} similar embeddings")
        return results
