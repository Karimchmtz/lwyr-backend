"""API routes package."""

from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.conversations import router as conversations_router
from app.api.routes.embedding import router as embedding_router
from app.api.routes.translation import router as translation_router

__all__ = [
    "auth_router",
    "conversations_router",
    "translation_router",
    "embedding_router",
    "admin_router",
]
