"""Pydantic schemas for embedding endpoints."""


from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    """Embedding generation request schema."""

    text: str = Field(..., min_length=1, description="Text to generate embedding for")


class EmbeddingResponse(BaseModel):
    """Embedding generation response schema."""

    embedding: list[float]
    dimensions: int


class SearchResult(BaseModel):
    """Search result schema."""

    content: str
    document_id: str
    chunk_index: int
    score: float
    metadata: dict | None = None


class SearchRequest(BaseModel):
    """Similarity search request schema."""

    query: str = Field(..., min_length=1)
    max_results: int = Field(default=5, ge=1, le=20)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Similarity search response schema."""

    results: list[SearchResult]
    query: str
