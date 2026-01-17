# lwyr - Legal RAG Agent

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
./gradlew build                    # Full build (includes tests since build depends on test)
./gradlew compileKotlin            # Compile sources
./gradlew test                     # Run all tests
./gradlew test --tests "*Test"    # Run all test classes matching pattern
./gradlew test --tests "com.lwyr.ai.AuthServiceTest"  # Run specific test class
./gradlew test --tests "com.lwyr.ai.AuthServiceTest.testLogin"  # Run specific test method
./gradlew bootRun                  # Run application

# Docker
docker-compose up -d               # Start PostgreSQL
docker-compose down                # Stop containers
```

### Linting and Formatting
No specific lint or format commands configured. Follow code standards manually or use IDE formatting.

### Testing Guidelines
- Tests are located in `src/test/kotlin/`
- Use JUnit 5 with Testcontainers for integration tests
- Test database uses PostgreSQL with Testcontainers

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
- Custom exceptions extending RuntimeException
- GlobalExceptionHandler with proper HTTP status codes
- Log errors with context, never expose stack traces

### Logging
- Use SLF4J/Kotlin logging
- Log at appropriate levels (ERROR, WARN, INFO, DEBUG)
- Include user IDs in logs
- No sensitive data (passwords, tokens) in logs

### REST
- Proper HTTP methods (GET, POST, PUT, DELETE)
- Proper status codes (200, 201, 400, 401, 403, 404, 500)
- Consistent error response format
- Idempotent operations where appropriate

### Testing
- Use Testcontainers for integration tests
- Unit tests for services
- Integration tests for controllers
- Mock external dependencies
- Test error cases and edge cases

### Security
- Passwords: BCrypt
- Input validation on all endpoints
- SQL injection prevention via JOOQ
- Basic Auth, stateless sessions
- Role-based endpoint protection

## Docker Environment
- PostgreSQL 17 with pgvector extension
- Testcontainers for integration tests
- Health checks on database container

## Coding Style

### Code Organization
- **Private Methods**: Place all private methods at the bottom of classes or files. Public/protected methods come first, followed by private ones. This improves readability by prioritizing the API.
- **File Structure**: Group related functionality together; use blank lines to separate logical sections (e.g., imports, class definition, methods).
- **Comments**: Avoid dumb comments; code should be self-documenting. Use meaningful names and structure instead of redundant explanations.

### Compilation
- **No Warnings**: Ensure zero compilation warnings in Kotlin/Gradle builds. Treat warnings as errors (`kotlinOptions.allWarningsAsErrors = true` in build.gradle.kts). Fix issues like unused variables, deprecated APIs, or unchecked casts immediately.
- **Pre-Commit Run**: Always run the project (e.g., `./gradlew build`) before committing to ensure functionality and tests pass.

### Imports
- **Static Imports**: Use static imports for frequently used methods/constants (e.g., `import static org.assertj.core.api.Assertions.assertThat`). Limit to avoid clutter; prefer for AssertJ, JUnit, or utility classes.

### Testing
- **Avoid JSON Path**: Do not use `jsonPath` for assertions. Deserialize responses to real DTO/model classes and use `assertThat` for type-safe checks (e.g., `assertThat(response.userId).isNotNull()`).
- **Real Classes**: Test with actual objects; mock services/repositories as needed, but assert on domain objects for accuracy.
- **Examples**:
  - Instead of: `.andExpect(jsonPath("$.email").value("test@example.com"))`
  - Use: `val response = objectMapper.readValue(result.response.contentAsString, AuthResponse::class.java); assertThat(response.email).isEqualTo("test@example.com")`
- **High Accuracy**: Combine with existing testing guidelines for comprehensive coverage.

Follow these rules to maintain clean, warning-free code with robust, readable tests.
