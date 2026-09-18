"""Domain exceptions and standardized error codes."""

from enum import StrEnum
from typing import Any


class ErrorCode(StrEnum):
    """Standard error code identifiers for the API."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    GROQ_STT_FAILED = "GROQ_STT_FAILED"
    TYPESAFE_UNAVAILABLE = "TYPESAFE_UNAVAILABLE"
    FIRESTORE_ERROR = "FIRESTORE_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    BAD_REQUEST = "BAD_REQUEST"
    RATE_LIMITED = "RATE_LIMITED"


class AppError(Exception):
    """Base application exception supporting standardized error envelopes."""

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        code: str | ErrorCode = ErrorCode.INTERNAL_ERROR,
        status_code: int = 500,
        retryable: bool = False,
        details: Any = None,
    ) -> None:
        self.message = message
        self.code = str(code.value if isinstance(code, ErrorCode) else code)
        self.status_code = status_code
        self.retryable = retryable
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found.",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.NOT_FOUND,
            status_code=404,
            retryable=False,
            details=details,
        )


class UnauthorizedError(AppError):
    """Raised when authentication credentials are missing or invalid."""

    def __init__(
        self,
        message: str = "Authentication required or invalid credentials.",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.UNAUTHORIZED,
            status_code=401,
            retryable=False,
            details=details,
        )


class ValidationError(AppError):
    """Raised when business validation fails."""

    def __init__(
        self,
        message: str = "Validation failed.",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            status_code=422,
            retryable=False,
            details=details,
        )


class ProviderUnavailableError(AppError):
    """Raised when an external service provider is temporarily unavailable."""

    def __init__(
        self,
        message: str = "External provider temporarily unavailable.",
        code: str | ErrorCode = ErrorCode.PROVIDER_UNAVAILABLE,
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=503,
            retryable=True,
            details=details,
        )


class GroqSTTError(AppError):
    """Raised when Groq speech-to-text processing fails."""

    def __init__(
        self,
        message: str = "Groq speech-to-text transcription failed.",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.GROQ_STT_FAILED,
            status_code=502,
            retryable=True,
            details=details,
        )


class TypeSafeUnavailableError(AppError):
    """Raised when TypeSafe AI Jev evaluation service is unavailable."""

    def __init__(
        self,
        message: str = "TypeSafe AI Jev System One evaluation failed or timed out.",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.TYPESAFE_UNAVAILABLE,
            status_code=503,
            retryable=True,
            details=details,
        )


class FirestoreError(AppError):
    """Raised when Firebase Firestore operations fail."""

    def __init__(
        self,
        message: str = "Firestore database operation failed.",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.FIRESTORE_ERROR,
            status_code=500,
            retryable=False,
            details=details,
        )


class InternalError(AppError):
    """Raised when an unexpected internal error occurs."""

    def __init__(
        self,
        message: str = "An internal server error occurred.",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.INTERNAL_ERROR,
            status_code=500,
            retryable=False,
            details=details,
        )
