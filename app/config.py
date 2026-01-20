"""Configuration management for Lwyr application."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = Field(default="lwyr-backend", validation_alias="APP_NAME")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    database_host: str = Field(default="localhost", validation_alias="DATABASE_HOST")
    database_port: int = Field(default=5432, validation_alias="DATABASE_PORT")
    database_name: str = Field(default="lwyr_db", validation_alias="DATABASE_NAME")
    database_user: str = Field(default="lwyr_user", validation_alias="DATABASE_USER")
    database_password: str = Field(default="lwyr_password", validation_alias="DATABASE_PASSWORD")

    @property
    def database_url(self) -> str:
        """Generate database URL for SQLAlchemy."""
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    openrouter_api_key: str = Field(default="", validation_alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", validation_alias="OPENROUTER_BASE_URL")
    openrouter_chat_model: str = Field(default="qwen/qwen3-0.6b:free", validation_alias="OPENROUTER_CHAT_MODEL")
    openrouter_embedding_model: str = Field(default="qwen/qwen3-embedding-0.6b", validation_alias="OPENROUTER_EMBEDDING_MODEL")
    openrouter_temperature: float = Field(default=0.7, validation_alias="OPENROUTER_TEMPERATURE")
    openrouter_max_tokens: int = Field(default=2000, validation_alias="OPENROUTER_MAX_TOKENS")

    jwt_secret_key: str = Field(default="your-super-secret-key-change-in-production", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, validation_alias="JWT_EXPIRATION_HOURS")

    pdf_chunk_size: int = Field(default=1000, validation_alias="PDF_CHUNK_SIZE")
    pdf_chunk_overlap: int = Field(default=200, validation_alias="PDF_CHUNK_OVERLAP")

    embedding_dimension: int = Field(default=8192, validation_alias="EMBEDDING_DIMENSION")
    embedding_similarity_threshold: float = Field(default=0.7, validation_alias="EMBEDDING_SIMILARITY_THRESHOLD")
    embedding_max_results: int = Field(default=5, validation_alias="EMBEDDING_MAX_RESULTS")

    resources_path: Path = Field(default=Path(__file__).parent.parent / "resources", validation_alias="RESOURCES_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
