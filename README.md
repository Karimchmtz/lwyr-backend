# lwyr-backend

A legal RAG (Retrieval-Augmented Generation) agent trained on Lebanese law documents. Provides multilingual translation and conversational Q&A with citations.

## Features
- **Translation**: Supports Arabic, French, and English for legal texts.
- **Conversations**: Interactive Q&A with source citations from trained PDFs.
- **Authentication**: Secure user management with role-based access.
- **Admin Tools**: Train embeddings on new legal documents.

## Tech Stack
- **Language**: Kotlin 2.0.21
- **Framework**: Spring Boot 3.4.0
- **Database**: PostgreSQL 17 with pgvector
- **LLM**: OpenRouter API (Qwen, DeepSeek, GLM models)
- **Build**: Gradle 8.10
- **Java**: 21

## Prerequisites
- JDK 21
- Docker (for PostgreSQL)
- Gradle (or use wrapper)

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

3. **Build and run**:
   ```bash
   ./gradlew build
   ./gradlew bootRun
   ```

4. **API available at**: `http://localhost:8080`

## API Endpoints

### Authentication
- `POST /auth/signup` - Register user
- `POST /auth/login` - Login (returns token)

### Core Features
- `POST /translation` - Translate legal text
- `POST /conversation` - Start Q&A session
- `POST /conversation/{id}/message` - Ask questions
- `GET /conversations` - List user conversations
- `POST /admin/train` - Train on new PDFs (admin only)

## Project Structure
```
src/main/kotlin/com/lwyr/ai/
├── LwyrApplication.kt           # Main entry point
├── controller/                  # REST endpoints
├── dto/                         # Data transfer objects
├── entity/                      # Domain models
├── repository/                  # Data access (JOOQ)
├── service/                     # Business logic
├── security/                    # Auth config
├── config/                      # App configuration
└── exception/                   # Error handling
```

## Database
Uses PostgreSQL with pgvector for embeddings. Schema includes users, conversations, messages, and trained documents. Migrations via Flyway.

## Build Commands
```bash
./gradlew build                 # Build (includes tests)
./gradlew test                  # Run tests
./gradlew test --tests "*Test"  # Run test classes
./gradlew bootRun               # Start app
./gradlew clean                 # Clean build
```