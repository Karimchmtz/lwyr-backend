# Lwyr - Legal RAG Agent

A legal RAG (Retrieval-Augmented Generation) agent trained on Lebanese law documents. Provides multilingual translation and conversational Q&A with citations.

## Features
- **Translation**: Supports Arabic, French, and English for legal texts.
- **Conversations**: Interactive Q&A with source citations from trained PDFs.
- **Authentication**: Secure user management with role-based access.
- **Admin Tools**: Train embeddings on new legal documents.

## Tech Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL 17 with pgvector
- **LLM**: OpenRouter API (Qwen, DeepSeek, GLM models)
- **Build**: uv / Poetry

## Prerequisites
- Python 3.11+
- Docker (for PostgreSQL with pgvector)

## Getting Started

1. **Clone the repo**:
   ```bash
   git clone <repo-url>
   cd lwyr-backend
   ```

2. **Start PostgreSQL**:
   ```bash
   docker-compose up -d
   ```

3. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

4. **Run**:
   ```bash
   uvicorn app.main:app --reload --port 8080
   ```

5. **API available at**: `http://localhost:8080`
   - **Docs**: `http://localhost:8080/docs`

## API Endpoints

### Authentication
- `POST /auth/signup` - Register user
- `POST /auth/login` - Login (Basic Auth)

### Core Features
- `POST /translation` - Translate legal text
- `POST /conversations` - Start Q&A session
- `POST /conversations/{id}/message` - Ask questions
- `GET /conversations` - List user conversations
- `POST /admin/train` - Train on new PDFs (admin only)

## Project Structure
```
app/
├── main.py                    # FastAPI entry point
├── config.py                  # Settings (Pydantic)
├── database.py                # SQLAlchemy engine
├── security.py                # Auth utilities
├── models/                    # Database tables
├── repositories/              # Data access layer
├── services/                  # Business logic
└── api/
    ├── routes/                # REST endpoints
    └── schemas/               # Pydantic DTOs
tests/
├── unit/
└── integration/
resources/pdfs/                # Legal PDFs for RAG
```

## Database
Uses PostgreSQL with pgvector for embeddings. Schema includes users, conversations, messages, and trained documents. Migrations via Alembic.

## Commands

```bash
# Install
pip install -e .

# Run development
uvicorn app.main:app --reload --port 8080

# Run tests
pytest tests/unit/ -v

# Lint
ruff check app/ tests/

# Type check
mypy app/ --ignore-missing-imports
```

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`
- `OPENROUTER_API_KEY`
- `JWT_SECRET_KEY`
