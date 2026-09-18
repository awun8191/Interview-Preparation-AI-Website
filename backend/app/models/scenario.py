"""Pydantic models for scenario generation and framework definitions."""

from enum import StrEnum

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class FrameworkEnum(StrEnum):
    """The 11 cataloged communication methodologies."""

    STAR = "STAR"
    CARL = "CARL"
    PAR = "PAR"
    SCQA = "SCQA"
    SBI = "SBI"
    RADICAL_CANDOR = "RADICAL_CANDOR"
    STATE = "STATE"
    GOTTMAN = "GOTTMAN"
    VOSS = "VOSS"
    SPARKLINE = "SPARKLINE"
    MONROE = "MONROE"


class DifficultyLevel(StrEnum):
    """Calibrated scenario difficulty levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class GenerateScenarioRequest(BaseModel):
    """Request payload for generating a tailored practice scenario."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    target_framework: FrameworkEnum = Field(
        ...,
        validation_alias=AliasChoices("target_framework", "framework"),
        description="Target communication methodology from the 11 cataloged frameworks.",
    )
    user_domain: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Professional domain, functional discipline, or role title.",
        examples=["Staff Backend Engineer", "Engineering Manager", "Fintech Founder"],
    )
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.INTERMEDIATE,
        description="Difficulty setting calibrating scenario friction and trade-off complexity.",
    )
    focus_theme: str | None = Field(
        default=None,
        max_length=160,
        description="Optional thematic focus or operational context.",
        examples=["Production Outage", "Challenging Leadership", "Cross-Functional Friction"],
    )


class ScenarioResponse(BaseModel):
    """Generated practice scenario response."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )

    scenario_id: str = Field(
        ...,
        description="Unique slug or identifier for the scenario.",
        examples=["staff-be-db-migration-outage"],
    )
    title: str = Field(
        ...,
        description="Concise headline for the scenario.",
        examples=["PostgreSQL Migration Ledger Failure"],
    )
    context_background: str = Field(
        ...,
        description="Organizational context, stakes, timeline, and friction.",
    )
    prompt_question: str = Field(
        ...,
        description="The exact prompt question presented to the user.",
    )
    key_dimensions_to_test: list[str] = Field(
        default_factory=list,
        description="Core behavioral and technical competencies evaluated in this scenario.",
    )
    target_duration_seconds: int = Field(
        default=90,
        description="Recommended answer duration budget in seconds.",
    )
    target_framework: FrameworkEnum = Field(
        ...,
        description="The framework being tested.",
    )
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.INTERMEDIATE,
        description="The calibrated difficulty.",
    )


# Type alias for protocol consistency
ScenarioModel = ScenarioResponse
