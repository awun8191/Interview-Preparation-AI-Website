"""Unit tests for the cross-cutting ClarityAssessor."""

import pytest

from app.services.clarity import ClarityAssessor


@pytest.fixture
def assessor():
    return ClarityAssessor()


@pytest.mark.parametrize(
    (
        "clarity_credit",
        "ambiguity_credit",
        "clarity_key",
        "ambiguity_key",
        "expected_score",
        "expected_level",
        "expected_ambiguous",
    ),
    [
        (1.0, 1.0, "Level 5", "unambiguous_and_precise", 100.0, "exceptional", False),
        (0.8, 1.0, "Level 4", "unambiguous_and_precise", 90.0, "exceptional", False),
        (0.8, 0.6, "Level 4", "minor_vagueness", 70.0, "clear", False),
        (0.6, 0.6, "Level 3", "minor_vagueness", 60.0, "adequate", False),
        (0.4, 0.2, "Level 2", "materially_ambiguous", 30.0, "unclear", True),
        (0.2, 0.2, "Level 1", "materially_ambiguous", 20.0, "incoherent", True),
        (1.0, 0.0, "Level 5", "unable_to_assess", 50.0, "adequate", False),
    ],
)
def test_assess_clarity_matrix(
    assessor,
    clarity_credit,
    ambiguity_credit,
    clarity_key,
    ambiguity_key,
    expected_score,
    expected_level,
    expected_ambiguous,
):
    question_scores = {
        "clarity_of_response": clarity_credit,
        "ambiguity_presence": ambiguity_credit,
    }
    findings = {
        "clarity_of_response": {"type": "score", "level": clarity_key, "choice": clarity_key},
        "ambiguity_presence": {"type": "choice", "choice": ambiguity_key},
    }

    result = assessor.assess(question_scores, findings)

    assert result.score == expected_score
    assert result.level == expected_level
    assert result.clarity_level == clarity_key
    assert result.ambiguity == ambiguity_key
    assert result.ambiguous is expected_ambiguous


def test_assess_degrades_gracefully_when_findings_missing(assessor):
    """Missing scores/findings must not raise and must degrade to unable_to_assess."""
    result = assessor.assess({}, {})

    assert result.score == 0.0
    assert result.level == "incoherent"
    assert result.clarity_level == "unable_to_assess"
    assert result.ambiguity == "unable_to_assess"
    assert result.ambiguous is False


def test_assess_accepts_bare_string_findings(assessor):
    """Raw string findings (no dict wrapper) are handled by the choice-key extractor."""
    result = assessor.assess(
        {"clarity_of_response": 0.8, "ambiguity_presence": 0.6},
        {"clarity_of_response": "Level 4", "ambiguity_presence": "minor_vagueness"},
    )

    assert result.clarity_level == "Level 4"
    assert result.ambiguity == "minor_vagueness"
    assert result.ambiguous is False


def test_feedback_prefers_ambiguity_note_then_falls_back_to_band(assessor):
    """Ambiguity-specific advice wins; clean answers fall back to band feedback."""
    ambiguous = assessor.assess(
        {"clarity_of_response": 0.4, "ambiguity_presence": 0.2},
        {
            "clarity_of_response": "Level 2",
            "ambiguity_presence": "materially_ambiguous",
        },
    )
    assert ambiguous.feedback is not None
    assert "vague" in ambiguous.feedback.lower()

    clean = assessor.assess(
        {"clarity_of_response": 1.0, "ambiguity_presence": 1.0},
        {
            "clarity_of_response": "Level 5",
            "ambiguity_presence": "unambiguous_and_precise",
        },
    )
    assert clean.feedback is not None
    assert "clear" in clean.feedback.lower()


def test_extracts_level_from_jev_continuous_score_with_legend(assessor):
    """Real Jev returns score primitives as a continuous zero-indexed score + legend."""
    finding = {
        "type": "score",
        "score": 3.85,
        "confidence": 0.88,
        "legend": {
            "0": "Incoherent or Unintelligible: Disjointed.",
            "1": "Fragmented or Hard to Follow: False starts.",
            "2": "Understandable with Effort: Buried.",
            "3": "Clear and Well-Structured: Easy to follow.",
            "4": "Exceptionally Clear and Economical: Crisp.",
        },
        "probabilities": {"3": 0.12, "4": 0.87},
    }

    result = assessor.assess(
        {"clarity_of_response": 0.97, "ambiguity_presence": 1.0},
        {"clarity_of_response": finding, "ambiguity_presence": "unambiguous_and_precise"},
    )

    assert result.clarity_level == "Exceptionally Clear and Economical"
    assert result.level == "exceptional"


def test_extracts_level_from_continuous_score_without_legend(assessor):
    """Without a legend, a continuous score still resolves to a Level label.

    Jev's score primitive is zero-indexed, so 1.6 rounds to index 2 -> Level 3.
    """
    result = assessor.assess(
        {"clarity_of_response": 0.52, "ambiguity_presence": 0.6},
        {
            "clarity_of_response": {"type": "score", "score": 1.6},
            "ambiguity_presence": "minor_vagueness",
        },
    )

    assert result.clarity_level == "Level 3"
