"""Deterministic clarity and ambiguity assessment.

Turns the cross-cutting clarity/ambiguity Jev findings into an explicit
:class:`ClarityAssessment` for the evaluation response. This metric is reported
independently of the composite score.
"""

from typing import Any

from app.frameworks.cross_cutting import (
    AMBIGUITY_QUESTION_ID,
    CLARITY_DIMENSION,
    CLARITY_SCORE_QUESTION_ID,
    band_for_score,
)
from app.models.evaluation import ClarityAssessment

_UNABLE_TO_ASSESS = "unable_to_assess"

_FEEDBACK_BY_AMBIGUITY: dict[str, str] = {
    "unambiguous_and_precise": "",
    "minor_vagueness": ("Trim remaining vague phrasing: replace hedges with a specific claim."),
    "materially_ambiguous": (
        "Tighten vague references and commit to specific claims; the listener "
        "cannot tell exactly what you mean."
    ),
    _UNABLE_TO_ASSESS: "The answer was too garbled or incomplete to assess clearly.",
}

_FEEDBACK_BY_BAND: dict[str, str] = {
    "exceptional": "Exceptionally clear and economical delivery.",
    "clear": "Clear, well-structured answer.",
    "adequate": "Understandable but could be tightened for clarity.",
    "unclear": "Restructure the answer: lead with the point and cut filler.",
    "incoherent": "Rebuild the answer around a single, explicit through-line.",
}


class ClarityAssessor:
    """Builds a standalone clarity/ambiguity assessment from Jev findings."""

    @staticmethod
    def _extract_choice_key(raw: Any) -> str:
        if isinstance(raw, dict):
            return str(raw.get("choice") or raw.get("value") or raw.get("selected") or "")
        return str(raw or "")

    @staticmethod
    def _extract_clarity_level(raw: Any) -> str:
        """Resolve the raw clarity finding into a human-readable level.

        ``choice`` findings carry a named key. ``score`` findings instead carry a
        continuous, zero-indexed ``score`` plus a ``legend`` mapping index to
        rubric description (as returned by TypeSafe Jev), so derive the level
        from that rather than reporting an unassessable answer.
        """
        if isinstance(raw, dict):
            for key in ("level", "choice", "value", "selected"):
                val = raw.get(key)
                if val:
                    return str(val)

            raw_score = raw.get("score")
            if isinstance(raw_score, (int, float)):
                idx = max(0, min(4, int(round(float(raw_score)))))
                legend = raw.get("legend")
                if isinstance(legend, dict):
                    label = legend.get(str(idx))
                    if label is None:
                        label = legend.get(idx)
                    if label:
                        return str(label).split(":")[0].strip()
                return f"Level {idx + 1}"
            return _UNABLE_TO_ASSESS

        return str(raw) if raw else _UNABLE_TO_ASSESS

    def assess(
        self,
        question_scores: dict[str, float] | None,
        jev_findings: dict[str, Any] | None,
    ) -> ClarityAssessment:
        """Assess clarity from already-computed question scores and raw findings."""
        scores = question_scores or {}
        findings = jev_findings or {}

        clarity_credit = float(scores.get(CLARITY_SCORE_QUESTION_ID, 0.0) or 0.0)
        ambiguity_credit = float(scores.get(AMBIGUITY_QUESTION_ID, 0.0) or 0.0)

        score = round(max(0.0, min(100.0, ((clarity_credit + ambiguity_credit) / 2.0) * 100.0)), 1)
        level = band_for_score(score)

        clarity_level = self._extract_clarity_level(findings.get(CLARITY_SCORE_QUESTION_ID))

        ambiguity = (
            self._extract_choice_key(findings.get(AMBIGUITY_QUESTION_ID)) or _UNABLE_TO_ASSESS
        )

        feedback = _FEEDBACK_BY_AMBIGUITY.get(ambiguity) or _FEEDBACK_BY_BAND.get(level, "")

        return ClarityAssessment(
            score=score,
            level=level,
            clarity_level=clarity_level,
            ambiguity=ambiguity,
            ambiguous=ambiguity == "materially_ambiguous",
            feedback=feedback or None,
        )


__all__ = ["ClarityAssessor", "CLARITY_DIMENSION"]
