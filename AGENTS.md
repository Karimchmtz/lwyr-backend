# lwyr - Legal RAG Agent

## Overview
Legal RAG agent trained on Lebanese law PDFs (5-10 documents). Provides translation (Arabic, French, English) and conversational Q&A with citations.

## Tech Stack
- Language: Kotlin
- Framework: Spring Boot
- Database: PostgreSQL with pgvector for embeddings
- LLM: OpenRouter API (free Chinese models: Qwen, DeepSeek, GLM)
- Embedding: Open-source (sentence-transformers or similar)

## Authentication
- Basic Auth: credentials sent with every request
- Endpoints: `POST /auth/signup`, `POST /auth/login`
- Password: minimum 8 characters

## API Endpoints

### Auth
- `POST /auth/signup`
- `POST /auth/login`

### Translation
- `POST /translation`
  - Body: `{ "text": string, "source": "ar"|"en"|"fr", "target": "ar"|"en"|"fr" }`
  - Legal system prompt always applied
  - Raw text only

### Conversations (singular resource naming)
- `POST /conversation` - create new conversation
- `GET /conversations` - list user's conversations
- `GET /conversation/{id}` - get conversation with message history
- `DELETE /conversation/{id}`
- `POST /conversation/{id}/message` - ask question
  - Body: `{ "question": string }`
  - Returns answer with citations

### Admin
- `POST /admin/train` - admin only
  - Trains embeddings on PDFs in resources folder
  - Auto-trains untrained PDFs on startup

## Database Schema

### Users
- id (UUID)
- email (unique)
- password_hash
- role (USER | ADMIN)
- created_at, updated_at

### Conversations
- id (UUID)
- user_id (FK)
- title
- created_at, updated_at

### Messages
- id (UUID)
- conversation_id (FK)
- role (USER | ASSISTANT)
- content
- citations (JSONB) - source PDF, page, relevant excerpts
- created_at

### TrainedDocuments
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
./gradlew test                    # All tests
./gradlew test --tests "*Test"    # Single test class
./gradlew bootRun                 # Run application
```

## Code Standards

### Imports
- No wildcard imports
- Group: Kotlin → Spring → Project
- Sort alphabetically within groups

### Naming
- Classes: PascalCase (UserService, TranslationController)
- Functions/variables: camelCase (getUser, calculateTotal)
- Constants: UPPER_SNAKE_CASE
- Test classes: *Test or *Spec suffix

### Types
- Prefer val over var
- Use nullable types (? ) explicitly
- Avoid Any, use specific types
- Collection types: List, Map, Set (not Array)

### Error Handling
- Use Result<T> or sealed classes for operations that fail
- Custom exceptions with meaningful messages
- Global exception handler with proper HTTP status codes
- Log errors with context, never expose stack traces

### Logging
- Use SLF4J/Kotlin logging
- Log at appropriate levels (ERROR, WARN, INFO, DEBUG)
- Include request IDs and user IDs in logs
- No sensitive data in logs

### REST
- Proper HTTP methods (GET, POST, PUT, DELETE)
- Proper status codes (200, 201, 400, 401, 403, 404, 500)
- Consistent error response format
- Idempotent operations where appropriate

### Testing
- Unit tests for services
- Integration tests for controllers
- Mock external dependencies
- Test error cases and edge cases

### Security
- Passwords: bcrypt or Argon2
- Input validation on all endpoints
- SQL injection prevention
- CORS configured properly
