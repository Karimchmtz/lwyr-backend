"""RAG (Retrieval-Augmented Generation) service."""

import json
import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import MessageRole
from app.repositories import ConversationRepository, MessageRepository
from app.services import EmbeddingService, OpenRouterService

logger = logging.getLogger(__name__)
settings = get_settings()

RAG_SYSTEM_PROMPT = """You are a legal assistant specializing in Lebanese law. 
Answer based only on the provided documents. Always cite your sources. 
Stay in character as a legal professional. Use Arabic, French, or English as appropriate."""


class RAGService:
    """Service for RAG-based question answering."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.embedding_service = EmbeddingService(db)
        self.openrouter_service = OpenRouterService()
        self.conversation_repository = ConversationRepository(db)
        self.message_repository = MessageRepository(db)

    def ask_question(
        self,
        question: str,
        user_id: UUID,
        conversation_id: UUID | None = None,
    ) -> tuple[str, list[dict], UUID]:
        """Answer a question using RAG."""
        logger.info(f"Processing question for user {user_id}: {question[:100]}...")

        if conversation_id is None:
            conversation = self.conversation_repository.create(
                user_id=user_id,
                title=question[:100] if len(question) > 100 else question,
            )
            conversation_id = conversation["id"]
        else:
            conversation = self.conversation_repository.find_by_id(
                conversation_id, user_id
            )
            if conversation is None:
                raise ValueError("Conversation not found")

        context_results = self.embedding_service.similarity_search(
            question,
            max_results=settings.embedding_max_results,
            similarity_threshold=settings.embedding_similarity_threshold,
        )

        context = self._build_context(context_results)

        messages = self.message_repository.find_by_conversation(conversation_id)
        chat_history = [
            {"role": m["role"].value if isinstance(m["role"], MessageRole) else m["role"], "content": m["content"]}
            for m in messages
        ]

        augmented_messages = self._build_augmented_messages(
            question, chat_history, context
        )

        answer = self.openrouter_service.generate_chat_response(
            augmented_messages, system_prompt=RAG_SYSTEM_PROMPT
        )

        citations = self._build_citations(context_results)

        self.message_repository.create(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=question,
        )
        self.message_repository.create(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=answer,
            citations=json.dumps(citations) if citations else None,
        )

        self.conversation_repository.update(
            conversation_id, user_id, updated_at=datetime.now()
        )

        logger.info(f"Generated answer with {len(citations)} citations")
        return answer, citations, conversation_id

    def _build_context(self, results: list[dict]) -> str:
        """Build context string from search results."""
        if not results:
            return "No relevant documents found."

        context_parts = []
        for i, result in enumerate(results, 1):
            content = result.get("content", "")
            doc_id = result.get("trained_document_id", "unknown")
            chunk_idx = result.get("chunk_index", 0)
            similarity = result.get("similarity", 0)
            context_parts.append(
                f"[Document {doc_id}, Chunk {chunk_idx}, Score: {similarity:.2f}]\n{content}"
            )

        return "\n\n".join(context_parts)

    def _build_augmented_messages(
        self,
        question: str,
        chat_history: list[dict],
        context: str,
    ) -> list[dict]:
        """Build messages for the LLM with context."""
        system_message = {
            "role": "system",
            "content": f"""{RAG_SYSTEM_PROMPT}

            Use the following context from legal documents to answer the user's question:

            {context}

            Cite your sources using the format [Document ID, Chunk Index] after each relevant statement.""",
        }

        messages = [system_message]
        messages.extend(chat_history)
        messages.append({"role": "user", "content": question})

        return messages

    def _build_citations(self, results: list[dict]) -> list[dict]:
        """Build citations from search results."""
        citations = []
        for result in results:
            citations.append({
                "document_id": str(result.get("trained_document_id", "")),
                "chunk_index": result.get("chunk_index", 0),
                "similarity": result.get("similarity", 0),
                "excerpt": result.get("content", "")[:200],
            })
        return citations
