"""OpenRouter LLM service."""

import logging
import re

from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

from app.config import get_settings
from app.exceptions import (
    OpenRouterBadRequestException,
    OpenRouterRateLimitException,
    OpenRouterServerException,
    OpenRouterUnauthorizedException,
)

logger = logging.getLogger(__name__)
settings = get_settings()


class OpenRouterService:
    """Service for OpenRouter API operations."""

    def __init__(self) -> None:
        self.embedding_model = OpenAIEmbeddings(
            model=settings.openrouter_embedding_model,
            openai_api_key=settings.openrouter_api_key,
            openai_api_base=settings.openrouter_base_url,
        )
        self.chat_model = ChatOpenAI(
            model=settings.openrouter_chat_model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            temperature=settings.openrouter_temperature,
            max_tokens=settings.openrouter_max_tokens,
        )

    def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        try:
            logger.debug(f"Generating embedding for text ({len(text)} chars)")
            vector = self.embedding_model.embed_query(text)
            return vector
        except Exception as e:
            self._handle_error(e)

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        try:
            logger.debug(f"Generating embeddings for {len(texts)} texts")
            vectors = self.embedding_model.embed_documents(texts)
            return vectors
        except Exception as e:
            self._handle_error(e)

    def generate_chat_response(
        self,
        messages: list[dict],
        system_prompt: str | None = None,
    ) -> str:
        """Generate a chat response using the chat model."""
        try:
            from langchain_core.messages import HumanMessage, SystemMessage

            langchain_messages: list = []
            if system_prompt:
                langchain_messages.append(SystemMessage(content=system_prompt))

            for msg in messages:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(SystemMessage(content=msg["content"]))

            response = self.chat_model.invoke(langchain_messages)
            return response.content
        except Exception as e:
            self._handle_error(e)

    def _handle_error(self, e: Exception) -> None:
        """Handle OpenRouter API errors."""
        logger.error(e, exc_info=True)
        message = str(e)

        status_code = self._extract_status_code(message)
        error_message = self._extract_error_message(message)

        if status_code == 400:
            raise OpenRouterBadRequestException(error_message)
        elif status_code == 401:
            raise OpenRouterUnauthorizedException("Invalid API key or unauthorized access")
        elif status_code == 429:
            raise OpenRouterRateLimitException("Rate limit exceeded, please try again later")
        elif status_code >= 500:
            raise OpenRouterServerException(f"OpenRouter service error: {error_message}")
        else:
            raise OpenRouterServerException(error_message)

    def _extract_status_code(self, message: str) -> int:
        """Extract HTTP status code from error message."""
        patterns = [
            (r'"status":(\d+)', 400),
            (r"\b400\b", 400),
            (r"\b401\b", 401),
            (r"\b429\b", 429),
            (r"\b500\b", 500),
            (r"\b502\b", 502),
            (r"\b503\b", 503),
        ]

        for pattern, default in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return int(match.group(1)) if match.lastindex else default

        if "bad request" in message.lower():
            return 400
        if "unauthorized" in message.lower():
            return 401
        if "rate limit" in message.lower():
            return 429
        if "internal server error" in message.lower():
            return 500

        return 500

    def _extract_error_message(self, message: str) -> str:
        """Extract error message from response."""
        json_match = re.search(r'"message"\s*:\s*"([^"]+)"', message)
        if json_match:
            return json_match.group(1)
        return message
