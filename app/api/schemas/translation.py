"""Pydantic schemas for translation endpoint."""

from typing import Literal

from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    """Translation request schema."""

    text: str = Field(..., min_length=1)
    source: Literal["ar", "en", "fr"] = Field(..., description="Source language code")
    target: Literal["ar", "en", "fr"] = Field(..., description="Target language code")


class TranslationResponse(BaseModel):
    """Translation response schema."""

    original_text: str
    translated_text: str
    source: str
    target: str
