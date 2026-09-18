"""Pydantic models for user profiles and saved coaching sessions."""

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class UserRecord(BaseModel):
    """User profile record persisted in Firestore users collection."""

    model_config = ConfigDict(extra="allow")

    user_id: str = Field(..., description="Firebase Auth UID of the user")
    email: str = Field(..., description="Registered email address")
    display_name: str = Field(..., description="User's display or preferred name")
    role: Literal["user", "admin"] = Field(
        default="user",
        description="Access role for permissions",
    )
    subscription_tier: Literal["free", "pro"] = Field(
        default="free",
        description="Subscription tier for quotas and features",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Account creation timestamp (UTC)",
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Last account update timestamp (UTC)",
    )


class SessionRecord(BaseModel):
    """Evaluation session record persisted in Firestore sessions collection."""

    model_config = ConfigDict(extra="allow")

    session_id: str = Field(..., description="UUID identifying the evaluation session")
    user_id: str = Field(..., description="User who completed the session")
    framework: str = Field(..., description="Framework identifier (e.g. STAR, CARL)")
    prompt: str = Field(..., description="Scenario prompt text presented to user")
    transcript: str = Field(..., description="Spoken or typed response text evaluated")
    score: float = Field(..., ge=0.0, le=100.0, description="Composite score (0-100)")
    findings: dict[str, Any] = Field(
        default_factory=dict,
        description="Jev System One raw question choices, scores, and probabilities",
    )
    tips: list[str] = Field(
        default_factory=list,
        description="Deterministic coaching tips",
    )
    badges: list[str] = Field(
        default_factory=list,
        description="Earned badges or alert codes",
    )
    clarity: dict[str, Any] | None = Field(
        default=None,
        description="Standalone clarity/ambiguity assessment (excluded from composite score)",
    )
    delivery_metrics: dict[str, Any] | None = Field(
        default=None,
        description="Pacing and acoustic delivery metrics",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Session creation timestamp (UTC)",
    )


class SessionListResponse(BaseModel):
    """Paginated list of historical user sessions."""

    model_config = ConfigDict(extra="allow")

    items: list[SessionRecord] = Field(
        default_factory=list,
        description="List of session records",
    )
    total: int = Field(..., description="Total count of sessions returned in current page")
    cursor: str | None = Field(
        default=None,
        description="Cursor token for fetching the next page, or None if no more",
    )
