"""Common Pydantic models for error envelopes and health status."""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    """Payload containing structured error information."""

    model_config = ConfigDict(extra="allow")

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable explanation")
    retryable: bool = Field(default=False, description="Whether the request can be retried")
    details: Any = Field(default=None, description="Detailed field errors or contextual metadata")


class ErrorEnvelope(BaseModel):
    """Standard top-level envelope for all non-2xx responses."""

    model_config = ConfigDict(extra="forbid")

    error: ErrorDetail = Field(..., description="The error detail object")
    request_id: str = Field(..., description="Unique request tracing ID")


class HealthResponse(BaseModel):
    """System health check response payload."""

    model_config = ConfigDict(extra="allow")

    status: str = Field(default="healthy", description="Overall system health status")
    version: str = Field(default="0.1.0", description="Application semantic version")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp of health check (UTC)",
    )
    environment: str = Field(default="development", description="Current execution environment")
    services: dict[str, str] = Field(
        default_factory=dict,
        description="Health status of external services and gateways",
    )
