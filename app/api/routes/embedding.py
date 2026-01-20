"""Embedding API routes."""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.schemas import (
    EmbeddingRequest,
    EmbeddingResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from app.database import get_db
from app.services import EmbeddingService, OpenRouterService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/embedding", tags=["embeddings"])


@router.post("/generate", response_model=EmbeddingResponse)
def generate_embedding(
    request: EmbeddingRequest,
    db: Session = Depends(get_db),  # noqa: ARG001
) -> EmbeddingResponse:
    """Generate embedding for text."""
    logger.info(f"Generating embedding for text ({len(request.text)} chars)")

    openrouter_service = OpenRouterService()
    embedding = openrouter_service.generate_embedding(request.text)

    return EmbeddingResponse(
        embedding=embedding,
        dimensions=len(embedding),
    )


@router.post("/search", response_model=SearchResponse)
def search_similar(
    request: SearchRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SearchResponse:
    """Search for similar embeddings."""
    logger.info(f"Searching for: {request.query[:100]}...")

    embedding_service = EmbeddingService(db)
    results = embedding_service.similarity_search(
        query=request.query,
        max_results=request.max_results,
        similarity_threshold=request.similarity_threshold,
    )

    return SearchResponse(
        results=[
            SearchResult(
                content=r["content"],
                document_id=str(r["trained_document_id"]),
                chunk_index=r["chunk_index"],
                score=r["similarity"],
                metadata=r.get("metadata"),
            )
            for r in results
        ],
        query=request.query,
    )
