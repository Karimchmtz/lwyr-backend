"""Conversation API routes."""

import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.schemas import (
    AskQuestionRequest,
    AskQuestionResponse,
    ConversationCreateRequest,
    ConversationDetailResponse,
    ConversationResponse,
    MessageResponse,
)
from app.database import get_db
from app.models import MessageRole
from app.repositories import ConversationRepository, MessageRepository
from app.services import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    request: ConversationCreateRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ConversationResponse:
    """Create a new conversation."""
    logger.info(f"Creating conversation for user: {user['id']}")

    conversation_repository = ConversationRepository(db)
    conversation = conversation_repository.create(
        user_id=UUID(user["id"]),
        title=request.title,
    )

    return ConversationResponse(
        id=conversation["id"],
        user_id=conversation["user_id"],
        title=conversation["title"],
        created_at=conversation["created_at"],
        updated_at=conversation["updated_at"],
    )


@router.get("", response_model=list[ConversationResponse])
def list_conversations(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ConversationResponse]:
    """List all conversations for the current user."""
    logger.info(f"Listing conversations for user: {user['id']}")

    conversation_repository = ConversationRepository(db)
    conversations = conversation_repository.find_by_user(UUID(user["id"]))

    return [
        ConversationResponse(
            id=c["id"],
            user_id=c["user_id"],
            title=c["title"],
            created_at=c["created_at"],
            updated_at=c["updated_at"],
        )
        for c in conversations
    ]


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation(
    conversation_id: UUID,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ConversationDetailResponse:
    """Get a conversation with all messages."""
    logger.info(f"Getting conversation {conversation_id} for user: {user['id']}")

    conversation_repository = ConversationRepository(db)
    message_repository = MessageRepository(db)

    conversation = conversation_repository.find_by_id(conversation_id, UUID(user["id"]))
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    messages = message_repository.find_by_conversation(conversation_id)

    return ConversationDetailResponse(
        id=conversation["id"],
        user_id=conversation["user_id"],
        title=conversation["title"],
        messages=[
            MessageResponse(
                id=m["id"],
                conversation_id=m["conversation_id"],
                role=m["role"].value if isinstance(m["role"], MessageRole) else m["role"],
                content=m["content"],
                citations=json.loads(m["citations"]) if m.get("citations") else None,
                created_at=m["created_at"],
            )
            for m in messages
        ],
        created_at=conversation["created_at"],
        updated_at=conversation["updated_at"],
    )


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: UUID,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a conversation."""
    logger.info(f"Deleting conversation {conversation_id} for user: {user['id']}")

    conversation_repository = ConversationRepository(db)
    deleted = conversation_repository.delete(conversation_id, UUID(user["id"]))

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )


@router.post("/{conversation_id}/message", response_model=AskQuestionResponse)
def ask_question(
    conversation_id: UUID,
    request: AskQuestionRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AskQuestionResponse:
    """Ask a question in a conversation."""
    logger.info(f"Question in conversation {conversation_id} from user: {user['id']}")

    rag_service = RAGService(db)
    answer, citations, actual_conversation_id = rag_service.ask_question(
        question=request.question,
        user_id=UUID(user["id"]),
        conversation_id=conversation_id,
    )

    return AskQuestionResponse(
        conversation_id=actual_conversation_id,
        answer=answer,
        citations=citations,
    )
