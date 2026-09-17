"""Pydantic models for session evaluation, scorecards, and STT results."""

from datetime import UTC, datetime
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.models.scenario import FrameworkEnum


class TranscriptionResult(BaseModel):
    """Result of speech-to-text audio transcription."""

    model_config = ConfigDict(extra="allow")

    transcript: str = Field(..., description="Full transcribed text from audio")
    duration_seconds: float = Field(default=0.0, description="Duration of audio in seconds")
    words: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Word-level timestamps with start, end, and word tokens",
    )


class EvaluateSessionRequest(BaseModel):
    """Payload for evaluating a practice session response."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )

    framework: FrameworkEnum = Field(
        ...,
        validation_alias=AliasChoices("framework", "target_framework"),
        description="Framework methodology being evaluated.",
    )
    speaker_role: str = Field(
        default="Professional",
        validation_alias=AliasChoices("speaker_role", "role", "user_domain"),
        description="Speaker's professional role or seniority context.",
    )
    scenario_prompt: str = Field(
        ...,
        validation_alias=AliasChoices("scenario_prompt", "prompt"),
        description="The prompt or question posed to the candidate.",
    )
    scenario_context: str | None = Field(
        default=None,
        validation_alias=AliasChoices("scenario_context", "context", "context_background"),
        description="Optional organizational background or constraints.",
    )
    transcript: str | None = Field(
        default=None,
        description="Transcribed or typed response text (if already available).",
    )
    duration_seconds: float | None = Field(
        default=None,
        ge=0.0,
        description="Optional recorded audio duration in seconds.",
    )
    user_id: str = Field(
        default="anonymous",
        description="User identifier or Firebase Auth UID.",
    )


class ScorecardSubscore(BaseModel):
    """Subscore breakdown for an individual framework dimension."""

    model_config = ConfigDict(extra="allow")

    dimension: str = Field(..., description="Framework dimension name (e.g. Action, Situation)")
    score: float = Field(..., ge=0.0, le=100.0, description="Normalized dimension score (0-100)")
    weight: float = Field(..., ge=0.0, le=1.0, description="Relative weight in composite formula")
    feedback: str | None = Field(default=None, description="Dimension-specific feedback")


class BadgeItem(BaseModel):
    """Coaching badge or alert triggered by rubric evaluation."""

    model_config = ConfigDict(extra="allow")

    badge_id: str = Field(..., description="Unique badge code (e.g. HIGH_IMPACT_OUTCOME)")
    title: str = Field(..., description="Human-readable title for the badge")
    description: str = Field(..., description="Detailed description of badge achievement or alert")
    category: str = Field(
        default="mastery",
        description="Category: mastery, warning, delivery, or insight",
    )


class ClarityAssessment(BaseModel):
    """Cross-cutting clarity and ambiguity assessment for a spoken answer.

    Reported as a standalone metric: it is graded for every framework but is
    intentionally excluded from the composite score.
    """

    model_config = ConfigDict(extra="allow")

    score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Clarity score 0-100 (mean of the clarity and ambiguity questions)",
    )
    level: str = Field(
        ...,
        description=("Clarity band: exceptional, clear, adequate, unclear, or incoherent"),
    )
    clarity_level: str = Field(..., description="Raw clarity level from Jev (e.g. 'Level 4')")
    ambiguity: str = Field(
        ...,
        description=(
            "Ambiguity classification key: unambiguous_and_precise, minor_vagueness, "
            "materially_ambiguous, or unable_to_assess"
        ),
    )
    ambiguous: bool = Field(..., description="True when the answer contains material ambiguity")
    feedback: str | None = Field(default=None, description="Human-readable clarity coaching note")


class JevEvaluationState(BaseModel):
    """Context state payload passed to TypeSafe AI Jev System One."""

    model_config = ConfigDict(extra="allow")

    scenario_prompt: str = Field(..., description="Scenario question presented to speaker")
    target_framework: str = Field(..., description="Target framework name")
    transcript: str = Field(..., description="Spoken transcript to evaluate")
    scenario_context: str | None = Field(default=None, description="Scenario background context")
    speaker_role: str | None = Field(default="Professional", description="Candidate role context")
    word_count: int | None = Field(default=None, description="Word count in transcript")
    duration_seconds: float | None = Field(default=None, description="Audio duration")
    words_per_minute: float | None = Field(default=None, description="Speech pacing WPM")


class EvaluateSessionResponse(BaseModel):
    """Complete evaluation response returned to client."""

    model_config = ConfigDict(extra="allow")

    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    framework: FrameworkEnum = Field(..., description="Framework evaluated")
    score: float = Field(..., ge=0.0, le=100.0, description="Composite score 0-100")
    subscores: list[ScorecardSubscore] = Field(
        default_factory=list,
        description="Subscores for each framework component",
    )
    findings: dict[str, Any] = Field(
        default_factory=dict,
        description="Raw Jev System One question choices, scores, and probabilities",
    )
    tips: list[str] = Field(
        default_factory=list,
        description="Actionable deterministic coaching tips",
    )
    badges: list[BadgeItem | str] = Field(
        default_factory=list,
        description="Earned badges or triggered warnings",
    )
    clarity: ClarityAssessment | None = Field(
        default=None,
        description=(
            "Cross-cutting clarity and ambiguity assessment (separate from composite score)"
        ),
    )
    delivery_metrics: dict[str, Any] | None = Field(
        default=None,
        description="Pacing and acoustic delivery metrics",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp of session evaluation (UTC)",
    )
