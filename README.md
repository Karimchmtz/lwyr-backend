# lwyr-backend

## Overview
Legal RAG agent trained on Lebanese law PDFs (5-10 documents). Provides translation (Arabic, French, English) and conversational Q&A with citations.

## Tech Stack
- Language: Kotlin 2.0.21
- Framework: Spring Boot 3.4.0
- Database: PostgreSQL 17 with pgvector (extension enabled)
- LLM: OpenRouter API (free Chinese models: Qwen, DeepSeek, GLM)
- Java: 21
- Build: Gradle 8.10

## Project Structure
```
src/main/kotlin/com/lwyr/ai/
├── LwyrApplication.kt              # Entry point
├── controller/                     # REST controllers
│   └── AuthController.kt
├── dto/                            # Data transfer objects
│   └── auth/AuthDto.kt
├── entity/                         # Domain entities
│   └── User.kt
├── repository/                     # JOOQ repositories
│   └── UserRepository.kt
├── service/                        # Business logic
│   └── AuthService.kt
├── security/                       # Security configuration
│   └── SecurityConfig.kt
├── config/                         # Configuration classes
│   └── DatabaseConfig.kt
└── exception/                      # Error handling
    ├── AppExceptions.kt
    └── GlobalExceptionHandler.kt
```

## Authentication
- Basic Auth: credentials sent with every request
- Password: BCrypt hashed, minimum 8 characters
- Endpoints: `POST /auth/signup`, `POST /auth/login`
- Role-based access: ADMIN role required for `/admin/**`

## API Endpoints

### Auth (COMPLETED)
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login with Basic Auth

### Translation (PENDING)
- `POST /translation`
  - Body: `{ "text": string, "source": "ar"|"en"|"fr", "target": "ar"|"en"|"fr" }`
  - Legal system prompt always applied
  - Raw text only

### Conversations (PENDING)
- `POST /conversation` - create new conversation
- `GET /conversations` - list user's conversations
- `GET /conversation/{id}` - get conversation with message history
- `DELETE /conversation/{id}`
- `POST /conversation/{id}/message` - ask question
  - Body: `{ "question": string }`
  - Returns answer with citations

### Admin (PENDING)
- `POST /admin/train` - admin only
  - Trains embeddings on PDFs in resources folder
  - Auto-trains untrained PDFs on startup

## Database Schema

### Users (COMPLETED)
- id (UUID)
- email (unique)
- password_hash (BCrypt)
- role (USER | ADMIN)
- created_at, updated_at

### Conversations (PENDING)
- id (UUID)
- user_id (FK)
- title
- created_at, updated_at

### Messages (PENDING)
- id (UUID)
- conversation_id (FK)
- role (USER | ASSISTANT)
- content
- citations (JSONB) - source PDF, page, relevant excerpts
- created_at

### TrainedDocuments (PENDING)
- id (UUID)
- filename
- checksum (to detect changes)
- embedded_at
- chunk_count

## System Prompts

### Translation
You are a legal translator specializing in Lebanese law. Translate accurately preserving legal terminology.

### RAG
You are a legal assistant specializing in Lebanese law. Answer based only on provided documents. Always cite sources. Stay in character as a legal professional.

## Build Commands
```bash
./gradlew build                    # Full build
./gradlew compileKotlin            # Compile sources
./gradlew test                     # All tests
./gradlew test --tests "*Test"    # Single test class
./gradlew bootRun                  # Run application

# Docker
docker-compose up -d               # Start PostgreSQL
docker-compose down                # Stop containers
```