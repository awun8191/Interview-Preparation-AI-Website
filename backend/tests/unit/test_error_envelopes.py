"""Unit tests verifying standard error envelopes and exception handlers."""

from typing import Any

from fastapi import APIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.core.errors import (
    AppError,
    ErrorCode,
    FirestoreError,
    GroqSTTError,
    NotFoundError,
    ProviderUnavailableError,
    TypeSafeUnavailableError,
    UnauthorizedError,
)
from app.main import create_app
from app.models.common import ErrorEnvelope


class ValidationTestPayload(BaseModel):
    required_name: str = Field(..., min_length=2)
    score: int = Field(..., ge=0, le=100)


def _create_test_client() -> TestClient:
    """Create test client with routes that trigger various exceptions."""
    app = create_app()
    test_router = APIRouter(prefix="/test-errors")

    @test_router.post("/validation")
    def trigger_validation(payload: ValidationTestPayload) -> dict[str, Any]:
        return {"received": payload.model_dump()}

    @test_router.get("/not-found")
    def trigger_not_found() -> None:
        raise NotFoundError("User record not found in database.", details={"user_id": "u-123"})

    @test_router.get("/unauthorized")
    def trigger_unauthorized() -> None:
        raise UnauthorizedError("Missing or invalid authorization token.")

    @test_router.get("/provider-unavailable")
    def trigger_provider_unavailable() -> None:
        raise ProviderUnavailableError("Gemini API connection timed out.")

    @test_router.get("/groq-error")
    def trigger_groq_error() -> None:
        raise GroqSTTError("Whisper transcription gateway failed.")

    @test_router.get("/typesafe-error")
    def trigger_typesafe_error() -> None:
        raise TypeSafeUnavailableError("Jev System One grading service timed out.")

    @test_router.get("/firestore-error")
    def trigger_firestore_error() -> None:
        raise FirestoreError("Failed to persist session to Firestore collection.")

    @test_router.get("/custom-app-error")
    def trigger_custom_app_error() -> None:
        raise AppError(
            code="CUSTOM_BUSINESS_ERROR",
            message="Domain business rule violated.",
            status_code=400,
            retryable=False,
            details={"violation": "rule_xyz"},
        )

    @test_router.get("/unhandled-exception")
    def trigger_unhandled() -> None:
        raise RuntimeError("Catastrophic database connection failure")

    app.include_router(test_router)
    return TestClient(app, raise_server_exceptions=False)


def test_422_validation_error_envelope() -> None:
    """Verify HTTP 422 produces strict standardized error envelope."""
    client = _create_test_client()
    response = client.post("/test-errors/validation", json={"required_name": "A", "score": 150})

    assert response.status_code == 422
    data = response.json()

    # Validate against ErrorEnvelope model
    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.VALIDATION_ERROR.value
    assert envelope.error.retryable is False
    assert isinstance(envelope.error.details, list)
    assert len(envelope.error.details) >= 1

    # Verify request ID header consistency
    header_id = response.headers.get("X-Request-ID") or response.headers.get("x-request-id")
    assert envelope.request_id == header_id


def test_custom_app_error_not_found() -> None:
    """Verify NotFoundError produces 404 with NOT_FOUND code."""
    client = _create_test_client()
    response = client.get("/test-errors/not-found")

    assert response.status_code == 404
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.NOT_FOUND.value
    assert envelope.error.message == "User record not found in database."
    assert envelope.error.retryable is False
    assert envelope.error.details == {"user_id": "u-123"}
    assert envelope.request_id == response.headers.get("X-Request-ID")


def test_custom_app_error_unauthorized() -> None:
    """Verify UnauthorizedError produces 401 with UNAUTHORIZED code."""
    client = _create_test_client()
    response = client.get("/test-errors/unauthorized")

    assert response.status_code == 401
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.UNAUTHORIZED.value
    assert envelope.error.retryable is False


def test_custom_app_error_provider_unavailable() -> None:
    """Verify ProviderUnavailableError produces 503 with retryable=True."""
    client = _create_test_client()
    response = client.get("/test-errors/provider-unavailable")

    assert response.status_code == 503
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.PROVIDER_UNAVAILABLE.value
    assert envelope.error.retryable is True


def test_custom_app_error_groq_stt() -> None:
    """Verify GroqSTTError produces 502 with GROQ_STT_FAILED code and retryable=True."""
    client = _create_test_client()
    response = client.get("/test-errors/groq-error")

    assert response.status_code == 502
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.GROQ_STT_FAILED.value
    assert envelope.error.retryable is True


def test_custom_app_error_typesafe() -> None:
    """Verify TypeSafeUnavailableError produces 503 with TYPESAFE_UNAVAILABLE code."""
    client = _create_test_client()
    response = client.get("/test-errors/typesafe-error")

    assert response.status_code == 503
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.TYPESAFE_UNAVAILABLE.value
    assert envelope.error.retryable is True


def test_custom_app_error_firestore() -> None:
    """Verify FirestoreError produces 500 with FIRESTORE_ERROR code."""
    client = _create_test_client()
    response = client.get("/test-errors/firestore-error")

    assert response.status_code == 500
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.FIRESTORE_ERROR.value
    assert envelope.error.retryable is False


def test_custom_app_error_with_custom_code() -> None:
    """Verify arbitrary custom AppError adheres to envelope contract."""
    client = _create_test_client()
    response = client.get("/test-errors/custom-app-error")

    assert response.status_code == 400
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == "CUSTOM_BUSINESS_ERROR"
    assert envelope.error.details == {"violation": "rule_xyz"}
    assert envelope.error.retryable is False


def test_unhandled_exception_returns_500_without_leaking_details() -> None:
    """Verify unhandled 500 internal errors do not leak stack traces or internal info."""
    client = _create_test_client()
    response = client.get("/test-errors/unhandled-exception")

    assert response.status_code == 500
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.INTERNAL_ERROR.value
    assert envelope.error.message == "An unexpected internal server error occurred."
    assert envelope.error.retryable is False
    assert envelope.error.details is None
    assert "Catastrophic" not in response.text
    assert envelope.request_id == response.headers.get("X-Request-ID")


def test_unmapped_route_404_returns_standard_envelope() -> None:
    """Verify standard Starlette 404 not found returns the standardized error envelope."""
    client = _create_test_client()
    response = client.get("/api/v1/nonexistent-endpoint-abc")

    assert response.status_code == 404
    data = response.json()

    envelope = ErrorEnvelope.model_validate(data)
    assert envelope.error.code == ErrorCode.NOT_FOUND.value
    assert envelope.error.retryable is False
    assert envelope.request_id == response.headers.get("X-Request-ID")
