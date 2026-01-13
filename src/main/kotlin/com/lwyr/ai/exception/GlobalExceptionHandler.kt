package com.lwyr.ai.exception

import com.lwyr.ai.dto.auth.ErrorResponse
import org.slf4j.LoggerFactory
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.security.authentication.BadCredentialsException
import org.springframework.validation.FieldError
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice

@RestControllerAdvice
class GlobalExceptionHandler {

    private val logger = LoggerFactory.getLogger(GlobalExceptionHandler::class.java)

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidationExceptions(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.allErrors.associate { error ->
            val fieldName = (error as FieldError).field
            val errorMessage = error.defaultMessage ?: "Invalid value"
            fieldName to errorMessage
        }
        logger.warn("Validation failed: {}", errors)
        return ResponseEntity(
            ErrorResponse(
                error = "Validation Error",
                message = errors.toString()
            ),
            HttpStatus.BAD_REQUEST
        )
    }

    @ExceptionHandler(ValidationException::class)
    fun handleValidationException(ex: ValidationException): ResponseEntity<ErrorResponse> {
        logger.warn("Validation error: {}", ex.message)
        return ResponseEntity(
            ErrorResponse(
                error = "Validation Error",
                message = ex.message ?: "Invalid input"
            ),
            HttpStatus.BAD_REQUEST
        )
    }

    @ExceptionHandler(AuthenticationException::class)
    fun handleAuthenticationException(ex: AuthenticationException): ResponseEntity<ErrorResponse> {
        logger.warn("Authentication failed: {}", ex.message)
        return ResponseEntity(
            ErrorResponse(
                error = "Authentication Error",
                message = ex.message ?: "Invalid credentials"
            ),
            HttpStatus.UNAUTHORIZED
        )
    }

    @ExceptionHandler(BadCredentialsException::class)
    fun handleBadCredentialsException(ex: BadCredentialsException): ResponseEntity<ErrorResponse> {
        logger.warn("Bad credentials: {}", ex.message)
        return ResponseEntity(
            ErrorResponse(
                error = "Authentication Error",
                message = "Invalid email or password"
            ),
            HttpStatus.UNAUTHORIZED
        )
    }

    @ExceptionHandler(ResourceAlreadyExistsException::class)
    fun handleResourceAlreadyExistsException(ex: ResourceAlreadyExistsException): ResponseEntity<ErrorResponse> {
        logger.warn("Resource already exists: {}", ex.message)
        return ResponseEntity(
            ErrorResponse(
                error = "Conflict",
                message = ex.message ?: "Resource already exists"
            ),
            HttpStatus.CONFLICT
        )
    }

    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleResourceNotFoundException(ex: ResourceNotFoundException): ResponseEntity<ErrorResponse> {
        logger.warn("Resource not found: {}", ex.message)
        return ResponseEntity(
            ErrorResponse(
                error = "Not Found",
                message = ex.message ?: "Resource not found"
            ),
            HttpStatus.NOT_FOUND
        )
    }

    @ExceptionHandler(AuthorizationException::class)
    fun handleAuthorizationException(ex: AuthorizationException): ResponseEntity<ErrorResponse> {
        logger.warn("Authorization failed: {}", ex.message)
        return ResponseEntity(
            ErrorResponse(
                error = "Forbidden",
                message = ex.message ?: "Access denied"
            ),
            HttpStatus.FORBIDDEN
        )
    }

    @ExceptionHandler(Exception::class)
    fun handleGenericException(ex: Exception): ResponseEntity<ErrorResponse> {
        logger.error("Unexpected error occurred", ex)
        return ResponseEntity(
            ErrorResponse(
                error = "Internal Server Error",
                message = "An unexpected error occurred"
            ),
            HttpStatus.INTERNAL_SERVER_ERROR
        )
    }
}
