package com.lwyr.ai.exception

import com.lwyr.ai.dto.auth.ErrorResponse
import mu.KotlinLogging
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.security.authentication.BadCredentialsException
import org.springframework.validation.FieldError
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice

private val logger = KotlinLogging.logger(GlobalExceptionHandler::class.java.name)

@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidationExceptions(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.allErrors.associate { error ->
            val fieldName = (error as FieldError).field
            val errorMessage = error.defaultMessage ?: "Invalid value"
            fieldName to errorMessage
        }
        logger.warn { "Validation failed: $errors" }
        return createErrorResponse("Validation Error", errors.toString(), HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(ValidationException::class)
    fun handleValidationException(ex: ValidationException): ResponseEntity<ErrorResponse> {
        logger.warn { "Validation error: ${ex.message}" }
        return createErrorResponse("Validation Error", ex.message ?: "Invalid input", HttpStatus.BAD_REQUEST)
    }

    @ExceptionHandler(AuthenticationException::class)
    fun handleAuthenticationException(ex: AuthenticationException): ResponseEntity<ErrorResponse> {
        logger.warn { "Authentication failed: ${ex.message}" }
        return createErrorResponse("Authentication Error", ex.message ?: "Invalid credentials", HttpStatus.UNAUTHORIZED)
    }

    @ExceptionHandler(BadCredentialsException::class)
    fun handleBadCredentialsException(ex: BadCredentialsException): ResponseEntity<ErrorResponse> {
        logger.warn { "Bad credentials: ${ex.message}" }
        return createErrorResponse("Authentication Error", "Invalid email or password", HttpStatus.UNAUTHORIZED)
    }

    @ExceptionHandler(ResourceAlreadyExistsException::class)
    fun handleResourceAlreadyExistsException(ex: ResourceAlreadyExistsException): ResponseEntity<ErrorResponse> {
        logger.warn { "Resource already exists: ${ex.message}" }
        return createErrorResponse("Conflict", ex.message ?: "Resource already exists", HttpStatus.CONFLICT)
    }

    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleResourceNotFoundException(ex: ResourceNotFoundException): ResponseEntity<ErrorResponse> {
        logger.warn { "Resource not found: ${ex.message}" }
        return createErrorResponse("Not Found", ex.message ?: "Resource not found", HttpStatus.NOT_FOUND)
    }

    @ExceptionHandler(AuthorizationException::class)
    fun handleAuthorizationException(ex: AuthorizationException): ResponseEntity<ErrorResponse> {
        logger.warn { "Authorization failed: ${ex.message}" }
        return createErrorResponse("Forbidden", ex.message ?: "Access denied", HttpStatus.FORBIDDEN)
    }

    @ExceptionHandler(OpenRouterException::class)
    fun handleOpenRouterException(ex: OpenRouterException): ResponseEntity<ErrorResponse> {
        logger.warn { "OpenRouter error: ${ex.message}" }
        val status = when (ex) {
            is OpenRouterBadRequestException -> HttpStatus.BAD_REQUEST
            is OpenRouterUnauthorizedException -> HttpStatus.UNAUTHORIZED
            is OpenRouterRateLimitException -> HttpStatus.TOO_MANY_REQUESTS
            is OpenRouterServerException -> HttpStatus.INTERNAL_SERVER_ERROR
            else -> HttpStatus.INTERNAL_SERVER_ERROR
        }
        return createErrorResponse("OpenRouter Error", ex.message ?: "OpenRouter API error", status)
    }

    @ExceptionHandler(Exception::class)
    fun handleGenericException(ex: Exception): ResponseEntity<ErrorResponse> {
        logger.error(ex) { "Unexpected error occurred" }
        return createErrorResponse("Internal Server Error", "An unexpected error occurred", HttpStatus.INTERNAL_SERVER_ERROR)
    }

    private fun createErrorResponse(error: String, message: String, status: HttpStatus): ResponseEntity<ErrorResponse> {
        return ResponseEntity(ErrorResponse(error, message), status)
    }
}
