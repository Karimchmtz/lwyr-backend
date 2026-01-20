"""Custom exceptions for the application."""


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationException(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid email or password") -> None:
        super().__init__(message, status_code=401)


class AuthorizationException(AppException):
    """Raised when user is not authorized to access a resource."""

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message, status_code=403)


class ResourceNotFoundException(AppException):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class ResourceAlreadyExistsException(AppException):
    """Raised when a resource already exists."""

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(message, status_code=409)


class ValidationException(AppException):
    """Raised when validation fails."""

    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(message, status_code=400)


class OpenRouterException(AppException):
    """Base exception for OpenRouter API errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class OpenRouterBadRequestException(OpenRouterException):
    """Raised when OpenRouter returns a 400 error."""

    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(message, status_code=400)


class OpenRouterUnauthorizedException(OpenRouterException):
    """Raised when OpenRouter returns a 401 error."""

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, status_code=401)


class OpenRouterRateLimitException(OpenRouterException):
    """Raised when OpenRouter returns a 429 error."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message, status_code=429)


class OpenRouterServerException(OpenRouterException):
    """Raised when OpenRouter returns a 5xx error."""

    def __init__(self, message: str = "OpenRouter server error") -> None:
        super().__init__(message, status_code=500)
