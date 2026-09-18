"""Cross-cutting Jev System One criteria applied to every framework catalog.

The clarity dimension evaluates how clearly a spoken answer is expressed and how
much material ambiguity it contains, independently of the framework-specific
rubric. It is an auxiliary dimension: it is graded and reported, but is
deliberately excluded from ``FrameworkCatalog.dimension_weights`` so it never
alters the deterministic composite score.
"""

from app.frameworks.base import CriteriaOption, JevQuestionDefinition, QuestionType

CLARITY_DIMENSION = "clarity"

CLARITY_SCORE_QUESTION_ID = "clarity_of_response"
AMBIGUITY_QUESTION_ID = "ambiguity_presence"

CLARITY_QUESTION_IDS = (CLARITY_SCORE_QUESTION_ID, AMBIGUITY_QUESTION_ID)

CLARITY_LEVEL_BANDS: tuple[tuple[float, str], ...] = (
    (90.0, "exceptional"),
    (70.0, "clear"),
    (50.0, "adequate"),
    (30.0, "unclear"),
    (0.0, "incoherent"),
)


def band_for_score(score: float) -> str:
    """Map a 0-100 clarity score to its human-readable band label."""
    for threshold, label in CLARITY_LEVEL_BANDS:
        if score >= threshold:
            return label
    return "incoherent"


def build_clarity_questions() -> list[JevQuestionDefinition]:
    """Build fresh clarity question definitions for a single catalog.

    Returns new instances on every call so that injected questions are never
    shared (and therefore never mutated) across the 11 framework catalogs.
    """
    return [
        JevQuestionDefinition(
            id=CLARITY_SCORE_QUESTION_ID,
            type=QuestionType.SCORE,
            prompt_instructions=(
                "Assess how clearly and precisely the speaker in `transcript` expresses "
                "their answer, independent of framework structure. Judge "
                "comprehensibility, logical ordering, economical phrasing, and freedom "
                "from vague or self-contradictory language. A clear answer is easy to "
                "follow on first listen, uses concrete nouns and specific verbs, and "
                "avoids filler, hedging, and undefined references."
            ),
            dimension=CLARITY_DIMENSION,
            weight_in_dimension=1.0,
            domain_metadata={"cross_cutting": True},
            criteria={
                "Level 1": CriteriaOption(
                    score=0.2,
                    description=(
                        "Incoherent or Unintelligible: Disjointed, contradictory, or "
                        "impossible to follow; the core meaning cannot be recovered."
                    ),
                ),
                "Level 2": CriteriaOption(
                    score=0.4,
                    description=(
                        "Fragmented or Hard to Follow: Frequent false starts, undefined "
                        "references, and filler obscure the point."
                    ),
                ),
                "Level 3": CriteriaOption(
                    score=0.6,
                    description=(
                        "Understandable with Effort: The main point is recoverable but "
                        "buried under vague phrasing, hedging, or erratic ordering."
                    ),
                ),
                "Level 4": CriteriaOption(
                    score=0.8,
                    description=(
                        "Clear and Well-Structured: Easy to follow on first listen with "
                        "concrete language and a discernible through-line."
                    ),
                ),
                "Level 5": CriteriaOption(
                    score=1.0,
                    description=(
                        "Exceptionally Clear and Economical: Crisp, precise, and "
                        "economical; every sentence advances an unambiguous point."
                    ),
                ),
            },
        ),
        JevQuestionDefinition(
            id=AMBIGUITY_QUESTION_ID,
            type=QuestionType.CHOICE,
            prompt_instructions=(
                "Determine whether `transcript` contains material ambiguity that would "
                "leave a listener unsure what the speaker means. Look for vague "
                "quantifiers and placeholders ('some things', 'stuff', 'a lot'), "
                "unresolved referents (unclear 'it', 'they', or 'this'), hedging that "
                "voids a claim ('kind of', 'maybe', 'sort of'), contradictory or "
                "underspecified timeframes and scope, and equivocation that never "
                "commits to a position."
            ),
            dimension=CLARITY_DIMENSION,
            weight_in_dimension=1.0,
            domain_metadata={"cross_cutting": True},
            criteria={
                "unambiguous_and_precise": CriteriaOption(
                    score=1.0,
                    description=(
                        "No material ambiguity; claims, referents, and scope are "
                        "specific and internally consistent."
                    ),
                ),
                "minor_vagueness": CriteriaOption(
                    score=0.6,
                    description=(
                        "Isolated vague phrasing or hedging that does not obscure the "
                        "core meaning of the answer."
                    ),
                ),
                "materially_ambiguous": CriteriaOption(
                    score=0.2,
                    description=(
                        "Meaning is genuinely unclear: undefined referents, "
                        "contradictory claims, or hedging that voids the point."
                    ),
                ),
                "unable_to_assess": CriteriaOption(
                    score=0.0,
                    description=("The transcript is severely garbled, unintelligible, or cut off."),
                ),
            },
        ),
    ]
