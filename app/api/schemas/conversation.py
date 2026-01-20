"""Pydantic schemas for conversation endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationCreateRequest(BaseModel):
    """Conversation creation request schema."""

    title: str | None = Field(None, max_length=255)


class ConversationResponse(BaseModel):
    """Conversation response schema."""

    id: UUID
    user_id: UUID
    title: str | None
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    """Message response schema."""

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    citations: dict | None = None
    created_at: datetime


class ConversationDetailResponse(BaseModel):
    """Conversation detail response schema."""

    id: UUID
    user_id: UUID
    title: str | None
    messages: list[MessageResponse]
    created_at: datetime
    updated_at: datetime


class AskQuestionRequest(BaseModel):
    """Ask question request schema."""

    question: str = Field(..., min_length=1)
    conversation_id: UUID | None = None


class AskQuestionResponse(BaseModel):
    """Ask question response schema."""

    conversation_id: UUID
    answer: str
    citations: list[dict] | None = None
