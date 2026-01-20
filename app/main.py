"""Main FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import (
    admin_router,
    auth_router,
    conversations_router,
    embedding_router,
    translation_router,
)
from app.config import get_settings
from app.database import engine
from app.models import metadata

settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Application lifespan events."""
    logger.info("Starting Lwyr application...")
    logger.info(f"Database: {settings.database_host}:{settings.database_port}/{settings.database_name}")

    logger.info("Creating database tables...")
    metadata.create_all(bind=engine)

    logger.info("Application started successfully")
    yield

    logger.info("Shutting down application...")
    logger.info("Application shut down")


app = FastAPI(
    title="Lwyr - Legal RAG Agent",
    description="Legal RAG agent trained on Lebanese law PDFs. Provides translation (Arabic, French, English) and conversational Q&A with citations.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation Error", "message": str(errors)},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Error", "message": exc.detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic exceptions."""
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal Server Error", "message": "An unexpected error occurred"},
    )


app.include_router(auth_router)
app.include_router(conversations_router)
app.include_router(translation_router)
app.include_router(embedding_router)
app.include_router(admin_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint."""
    return {
        "name": "Lwyr - Legal RAG Agent",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.debug,
    )
