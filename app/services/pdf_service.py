"""PDF processing service."""

import hashlib
import logging
from io import BytesIO

from pypdf import PdfReader

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PdfService:
    """Service for PDF processing operations."""

    def __init__(
        self,
        chunk_size: int = settings.pdf_chunk_size,
        chunk_overlap: int = settings.pdf_chunk_overlap,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text(self, file_content: bytes, filename: str) -> str:
        """Extract text from a PDF file."""
        logger.info(f"Extracting text from PDF: {filename}")
        pdf_document = PdfReader(BytesIO(file_content))
        text_parts: list[str] = []

        for page in pdf_document.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        text = "\n".join(text_parts)
        logger.info(f"Extracted {len(text)} characters from PDF: {filename}")
        return text

    def chunk_text(self, text: str, filename: str) -> list[str]:
        """Split text into overlapping chunks."""
        logger.info(f"Chunking text from {filename}")
        chunks: list[str] = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            if end >= len(text):
                break

            start = end - self.chunk_overlap

        logger.info(f"Created {len(chunks)} chunks from {filename}")
        return chunks

    def calculate_checksum(self, file_content: bytes) -> str:
        """Calculate SHA-256 checksum of file content."""
        digest = hashlib.sha256()
        digest.update(file_content)
        return digest.hexdigest()
