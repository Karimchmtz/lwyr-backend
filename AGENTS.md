# OpenCode Agent Instructions

This document contains instructions for OpenCode agents working on this codebase.

## Project Overview

Lwyr is a Legal RAG (Retrieval-Augmented Generation) agent trained on Lebanese law documents. It provides:
- Legal document Q&A with citations
- Translation between Arabic, French, and English
- Conversational context for follow-up questions

## Tech Stack

- **Backend**: Kotlin 2.0 + Spring Boot 3.4
- **Database**: PostgreSQL 17 with pgvector
- **ORM**: JOOQ
- **LLM**: OpenRouter API (Qwen models)
- **PDF Processing**: Apache PDFBox
- **Build**: Gradle 8.10
- **Testing**: JUnit 5, Testcontainers

## Development Commands

```bash
# Build project
./gradlew build

# Run tests
./gradlew test

# Run application
./gradlew bootRun

# Run with Docker
docker-compose up -d

# Lint (if configured)
./gradlew ktlintCheck

# Type check (if configured)
./gradlew detekt
```

## Architecture Notes

### Database Tables
- `users` - User accounts with email, password hash, role
- `conversations` - Chat sessions linked to users
- `messages` - Individual messages with role (USER/ASSISTANT)
- `trained_documents` - PDF documents ready for RAG
- `embeddings` - Vector embeddings stored with pgvector

### Key Services
- `AuthService` - Signup/login with BCrypt + JWT
- `OpenRouterService` - LLM and embedding API calls
- `PdfService` - PDF text extraction and chunking
- `EmbeddingService` - Vector storage and similarity search
- `RAGService` - Question answering with context

### Configuration
All configuration is managed via `application.yml` (Spring Boot). Environment variables can override settings.

## Code Style

- Follow Kotlin coding conventions
- Use data classes for DTOs
- Prefer immutability
- Write unit tests for all new services
- Use JOOQ for database queries (type-safe SQL)

## Testing Approach

- Unit tests: Mock external dependencies
- Integration tests: Use Testcontainers for PostgreSQL
- API tests: MockMvc for controller tests

## Git Workflow

1. Create feature branch from `main`
2. Make changes with tests
3. Ensure build passes
4. Create pull request for review
