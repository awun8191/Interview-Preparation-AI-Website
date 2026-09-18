"""Base abstractions and data models for communication framework catalogs.

Defines the structure for Jev System One question definitions, rubric criteria,
and framework catalogs.
"""

from enum import StrEnum
from typing import Any

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class QuestionType(StrEnum):
    """Jev System One typed question primitive."""

    CHOICE = "choice"
    SCORE = "score"
    NOUL = "noul"


class CriteriaOption(BaseModel):
    """An individual scoring option or rubric level within a question."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalized scoring credit (0.0 to 1.0) awarded for this choice or level",
    )
    description: str = Field(
        default="",
        description="Descriptive rubric definition passed to Jev System One wire protocol",
    )


class JevQuestionDefinition(BaseModel):
    """Defines a single Jev System One question evaluated in parallel."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str = Field(
        ...,
        description="Unique question identifier slug (e.g. 'star_situation_grounding')",
    )
    type: QuestionType = Field(
        ...,
        description="Jev question primitive type: 'choice', 'score', or 'noul'",
    )
    prompt_instructions: str = Field(
        ...,
        validation_alias=AliasChoices("prompt_instructions", "instructions"),
        description="Instruction text specifying how Jev should grade the transcript",
    )
    criteria: dict[str, CriteriaOption] = Field(
        ...,
        description="Map of option keys/levels to CriteriaOption objects",
    )
    dimension: str = Field(
        ...,
        description="Subscore dimension category (e.g. 'situation', 'action', 'learning')",
    )
    weight_in_dimension: float = Field(
        default=1.0,
        ge=0.0,
        description="Relative weight of this question within its dimension grouping",
    )
    domain_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata such as badges, anti-patterns, or thresholds",
    )

    @field_validator("criteria", mode="before")
    @classmethod
    def normalize_criteria(cls, v: Any) -> dict[str, Any]:
        """Allow criteria to be specified with CriteriaOption, dict, float, or tuple."""
        if not isinstance(v, dict):
            raise ValueError("Criteria must be a dictionary")
        normalized: dict[str, Any] = {}
        for key, value in v.items():
            if isinstance(value, CriteriaOption):
                normalized[key] = value
            elif isinstance(value, dict):
                normalized[key] = CriteriaOption(**value)
            elif isinstance(value, (int, float)):
                normalized[key] = CriteriaOption(score=float(value), description=str(key))
            elif isinstance(value, (list, tuple)) and len(value) == 2:
                # (score, description)
                normalized[key] = CriteriaOption(score=float(value[0]), description=str(value[1]))
            else:
                raise ValueError(f"Unsupported criteria value format for key {key}: {value}")
        return normalized

    @property
    def instructions(self) -> str:
        """Alias for prompt_instructions."""
        return self.prompt_instructions

    @property
    def criteria_scores(self) -> dict[str, float]:
        """Mapping from option keys to their numeric score credit."""
        return {k: opt.score for k, opt in self.criteria.items()}

    @property
    def criteria_descriptions(self) -> dict[str, str]:
        """Mapping from option keys to descriptive text for Jev System One."""
        return {k: opt.description for k, opt in self.criteria.items()}

    def to_jev_dict(self) -> dict[str, Any]:
        """Convert this question into the wire dictionary expected by Jev System One."""
        return {
            "type": self.type.value,
            "instructions": self.prompt_instructions,
            "criteria": self.criteria_descriptions,
        }


class FrameworkCatalog(BaseModel):
    """Complete rubric catalog and scoring parameters for a communication framework."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    framework: str = Field(
        ...,
        description="Canonical framework key (e.g. 'STAR', 'CARL', 'VOSS')",
    )
    name: str = Field(
        ...,
        description="Human-readable title (e.g. 'STAR (Situation, Task, Action, Result)')",
    )
    description: str = Field(
        ...,
        description="Overview of theoretical origins, core philosophy, and best practices",
    )
    target_pacing_seconds: int = Field(
        default=90,
        description="Recommended spoken answer pacing budget in seconds",
    )
    dimension_weights: dict[str, float] = Field(
        ...,
        description="Weights assigned to each dimension (must sum to 1.0)",
    )
    questions: list[JevQuestionDefinition] = Field(
        ...,
        description="The exhaustive list of Jev questions for this framework",
    )
    domain_rules: dict[str, Any] = Field(
        default_factory=dict,
        description="Domain rules such as multiplicative collapse factors or threshold penalties",
    )

    @model_validator(mode="after")
    def validate_weights_and_dimensions(self) -> "FrameworkCatalog":
        """Verify dimension weights sum to approximately 1.0 and cover question dimensions."""
        total = sum(self.dimension_weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Dimension weights for framework {self.framework} must sum to 1.0, got {total:.4f}"
            )
        # Verify that question dimensions are present in dimension_weights or explicitly mapped
        question_dimensions = {q.dimension for q in self.questions}
        for dim in question_dimensions:
            if dim not in self.dimension_weights:
                # Handled as an auxiliary dimension (e.g. relevance, clarity)
                pass
        return self

    @model_validator(mode="after")
    def inject_cross_cutting_questions(self) -> "FrameworkCatalog":
        """Attach the clarity/ambiguity questions to every framework catalog.

        These are cross-cutting criteria graded for every answer. They are
        registered under the auxiliary ``clarity`` dimension with a composite
        weight of 0.0, so they surface as a reported subscore while leaving the
        framework's 0-100 composite score untouched.
        """
        from app.frameworks.cross_cutting import CLARITY_DIMENSION, build_clarity_questions

        existing_ids = {q.id for q in self.questions}
        self.questions.extend(q for q in build_clarity_questions() if q.id not in existing_ids)
        self.dimension_weights.setdefault(CLARITY_DIMENSION, 0.0)
        return self

    @property
    def question_map(self) -> dict[str, JevQuestionDefinition]:
        """Fast lookup dictionary mapping question ID to definition."""
        return {q.id: q for q in self.questions}

    @property
    def dimensions(self) -> list[str]:
        """Ordered list of dimensions in this catalog."""
        return list(self.dimension_weights.keys())

    def get_question(self, question_id: str) -> JevQuestionDefinition | None:
        """Retrieve question definition by ID."""
        return self.question_map.get(question_id)

    def questions_by_dimension(self, dimension: str) -> list[JevQuestionDefinition]:
        """Retrieve all questions assigned to a specific dimension."""
        return [q for q in self.questions if q.dimension == dimension]

    def to_jev_questions_payload(self) -> dict[str, Any]:
        """Format all questions into the parallel payload for POST /v1/systemone."""
        return {q.id: q.to_jev_dict() for q in self.questions}
