"""Translation service."""

import logging

from app.services import OpenRouterService

logger = logging.getLogger(__name__)

TRANSLATION_SYSTEM_PROMPT = """You are a legal translator specializing in Lebanese law. 
Translate accurately preserving legal terminology. 
Maintain the structure and meaning of the original text."""


LANGUAGE_NAMES = {
    "ar": "Arabic",
    "en": "English",
    "fr": "French",
}


class TranslationService:
    """Service for text translation."""

    def __init__(self) -> None:
        self.openrouter_service = OpenRouterService()

    def translate(
        self,
        text: str,
        source: str,
        target: str,
    ) -> str:
        """Translate text from source to target language."""
        logger.info(f"Translating text ({len(text)} chars) from {source} to {target}")

        source_name = LANGUAGE_NAMES.get(source, source)
        target_name = LANGUAGE_NAMES.get(target, target)

        system_prompt = f"""{TRANSLATION_SYSTEM_PROMPT}

        Translate from {source_name} to {target_name}."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]

        translated_text = self.openrouter_service.generate_chat_response(messages)

        logger.info(f"Translation complete: {len(translated_text)} chars")
        return translated_text
