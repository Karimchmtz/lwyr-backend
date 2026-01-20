"""Admin API routes."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.config import get_settings
from app.database import get_db
from app.repositories import TrainedDocumentRepository
from app.services import EmbeddingService, PdfService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

settings = get_settings()


@router.post("/train", responses={200: {"description": "Training started"}})
def train_documents(
    user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> dict:
    """Train embeddings on PDFs in the resources folder."""
    logger.info(f"Admin {user['id']} starting document training")

    pdf_service = PdfService()
    embedding_service = EmbeddingService(db)
    document_repository = TrainedDocumentRepository(db)

    pdf_folder = settings.resources_path / "pdfs"
    if not pdf_folder.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDFs folder not found",
        )

    pdf_files = list(pdf_folder.glob("*.pdf"))
    if not pdf_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No PDF files found in resources folder",
        )

    trained_count = 0
    skipped_count = 0

    for pdf_file in pdf_files:
        logger.info(f"Processing: {pdf_file.name}")

        file_content = pdf_file.read_bytes()
        checksum = pdf_service.calculate_checksum(file_content)

        existing_doc = document_repository.find_by_checksum(checksum)
        if existing_doc:
            logger.info(f"Skipping {pdf_file.name} - already trained")
            skipped_count += 1
            continue

        text = pdf_service.extract_text(file_content, pdf_file.name)
        chunks = pdf_service.chunk_text(text, pdf_file.name)

        document = document_repository.create(
            filename=pdf_file.name,
            checksum=checksum,
            chunk_count=0,
        )

        embedding_service.store_embeddings(
            trained_document_id=document["id"],
            chunks=chunks,
        )

        trained_count += 1
        logger.info(f"Trained {pdf_file.name}: {len(chunks)} chunks")

    return {
        "message": "Training complete",
        "trained": trained_count,
        "skipped": skipped_count,
        "total": len(pdf_files),
    }
