"""Translation API routes."""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import TranslationRequest, TranslationResponse
from app.database import get_db
from app.services import TranslationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/translation", tags=["translation"])


@router.post("", response_model=TranslationResponse)
def translate(
    request: TranslationRequest,
    db: Session = Depends(get_db),  # noqa: ARG001
) -> TranslationResponse:
    """Translate text between languages."""
    logger.info(f"Translation request: {request.source} -> {request.target}")

    translation_service = TranslationService()
    translated_text = translation_service.translate(
        text=request.text,
        source=request.source,
        target=request.target,
    )

    return TranslationResponse(
        original_text=request.text,
        translated_text=translated_text,
        source=request.source,
        target=request.target,
    )
