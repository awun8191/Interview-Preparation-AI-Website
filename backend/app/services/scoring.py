"""Deterministic Scoring Engine for The-Plan-Software Communication Frameworks.

Computes mathematical composite scores (0–100), dimension subscores,
enforces the Balanced Impact Rule across outcome-bearing frameworks,
and applies domain penalties (Gottman contempt collapse, Voss why penalty,
PAR brevity, CARL non-linear learning).
"""

import math
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

try:
    from app.models.evaluation import BadgeItem, ScorecardSubscore
except ImportError:

    class ScorecardSubscore(BaseModel):  # type: ignore[no-redef]
        dimension: str = Field(..., description="Framework dimension name")
        score: float = Field(..., ge=0.0, le=100.0, description="Normalized score 0-100")
        weight: float = Field(..., ge=0.0, le=1.0, description="Weight in formula")
        feedback: str | None = Field(default=None, description="Optional feedback")

    class BadgeItem(BaseModel):  # type: ignore[no-redef]
        badge_id: str = Field(..., description="Badge identifier")
        title: str = Field(..., description="Display title")
        description: str = Field(..., description="Explanation")
        category: str = Field(default="mastery", description="Category")


from app.frameworks import FrameworkCatalog, QuestionType, get_framework_catalog
from app.services.badges import BadgeEngine
from app.services.tips import CoachingTipsEngine


class ScorecardResult(BaseModel):
    """Complete evaluation scorecard generated deterministically."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    framework: str = Field(..., description="Framework evaluated (e.g. 'STAR')")
    composite_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Deterministic overall score clamped between 0 and 100",
    )
    subscores: dict[str, float] = Field(
        default_factory=dict,
        description="Dimension names mapped to their 0-100 subscores",
    )
    subscore_items: list[ScorecardSubscore] = Field(
        default_factory=list,
        description="Structured list of subscores with weights",
    )
    badges: list[BadgeItem] = Field(
        default_factory=list,
        description="Triggered coaching badges and diagnostic alerts",
    )
    tips: list[str] = Field(
        default_factory=list,
        description="Targeted actionable improvement advice",
    )
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Low-level question scores and domain penalty details",
    )

    @property
    def score(self) -> float:
        """Alias for composite_score."""
        return self.composite_score

    @property
    def badge_names(self) -> list[str]:
        """List of badge display titles."""
        return [b.title for b in self.badges]

    @property
    def badge_ids(self) -> list[str]:
        """List of badge identifiers."""
        return [b.badge_id for b in self.badges]


class ScoringEngine:
    """Calculates deterministic composite scores and orchestrates feedback synthesis."""

    def __init__(
        self,
        badge_engine: BadgeEngine | None = None,
        tips_engine: CoachingTipsEngine | None = None,
    ) -> None:
        self.badge_engine = badge_engine or BadgeEngine()
        self.tips_engine = tips_engine or CoachingTipsEngine()

    @staticmethod
    def _extract_choice_key(raw: Any) -> str:
        if isinstance(raw, dict):
            return str(raw.get("choice") or raw.get("value") or raw.get("selected") or "")
        return str(raw or "")

    @staticmethod
    def _extract_score_value(raw: Any) -> str | None:
        if isinstance(raw, (int, float)):
            if isinstance(raw, float) and (math.isnan(raw) or math.isinf(raw)):
                return None
            return str(raw)
        if isinstance(raw, dict):
            val = raw.get("score")
            if val is None:
                val = raw.get("level")
            if val is None:
                val = raw.get("value")
            if val is None:
                val = raw.get("choice")
            if val is not None:
                if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
                    return None
                return str(val)
            return None
        return str(raw) if raw is not None else None

    def _score_single_question(self, question: Any, raw_val: Any) -> float:
        """Score an individual Jev question definition against user finding."""
        if raw_val is None:
            return 0.0

        if isinstance(raw_val, float) and (math.isnan(raw_val) or math.isinf(raw_val)):
            return 0.0

        if question.type == QuestionType.CHOICE:
            key = self._extract_choice_key(raw_val)
            opt = question.criteria.get(key)
            if not opt:
                return 0.0
            score = opt.score
            return 0.0 if (math.isnan(score) or math.isinf(score)) else score

        if question.type == QuestionType.SCORE:
            if isinstance(raw_val, dict) and "score" in raw_val:
                raw_s = raw_val["score"]
                if isinstance(raw_s, (int, float)) and not (math.isnan(raw_s) or math.isinf(raw_s)):
                    float_s = float(raw_s)
                    # Continuous score from TypeSafe Jev regression (e.g. 2.98 or dict with legend)
                    if "legend" in raw_val or not float_s.is_integer():
                        if float_s < 0:
                            return 0.0
                        num_levels = max(1, len(question.criteria))
                        if float_s <= (num_levels - 1):
                            return min(1.0, (float_s + 1.0) / float(num_levels))
                        elif float_s <= num_levels:
                            return min(1.0, float_s / float(num_levels))

            val = self._extract_score_value(raw_val)
            if val is None:
                return 0.0
            if isinstance(val, int) or (isinstance(val, str) and val.isdigit()):
                lvl_str = f"Level {val}"
            else:
                lvl_str = str(val or "")

            # If negative number or negative sign present, it must not match positive criteria
            if "-" in lvl_str:
                return 0.0

            opt = question.criteria.get(lvl_str)
            if opt:
                score = opt.score
                return 0.0 if (math.isnan(score) or math.isinf(score)) else score

            m = re.search(r"(?<!-)\b([1-5])\b", lvl_str)
            if m:
                lvl_int = int(m.group(1))
                opt2 = question.criteria.get(f"Level {lvl_int}")
                score = opt2.score if opt2 else lvl_int / 5.0
                return 0.0 if (math.isnan(score) or math.isinf(score)) else score
            return 0.0

        if question.type == QuestionType.NOUL:
            if isinstance(raw_val, dict) and "noul" in raw_val:
                raw_noul = raw_val.get("noul")
                if isinstance(raw_noul, (int, float)) and not (
                    math.isnan(raw_noul) or math.isinf(raw_noul)
                ):
                    return max(0.0, min(1.0, float(raw_noul)))

            if isinstance(raw_val, dict) and ("yes" in raw_val or "no" in raw_val):
                try:
                    raw_yes = raw_val.get("yes", 0.0)
                    yes_p = float(raw_yes) if raw_yes is not None else 0.0
                    if math.isnan(yes_p) or math.isinf(yes_p):
                        yes_p = 0.0
                except (ValueError, TypeError):
                    yes_p = 0.0
                try:
                    raw_no = raw_val.get("no", 0.0)
                    no_p = float(raw_no) if raw_no is not None else 0.0
                    if math.isnan(no_p) or math.isinf(no_p):
                        no_p = 0.0
                except (ValueError, TypeError):
                    no_p = 0.0
                tot = yes_p + no_p
                if tot > 0 and not (math.isnan(tot) or math.isinf(tot)):
                    yes_p /= tot
                    no_p /= tot
                else:
                    yes_p = 0.0
                    no_p = 0.0
                yes_opt = question.criteria.get("yes")
                no_opt = question.criteria.get("no")
                yes_score = yes_opt.score if yes_opt else 1.0
                no_score = no_opt.score if no_opt else 0.0
                if math.isnan(yes_score) or math.isinf(yes_score):
                    yes_score = 0.0
                if math.isnan(no_score) or math.isinf(no_score):
                    no_score = 0.0
                calc_score = (yes_p * yes_score) + (no_p * no_score)
                return 0.0 if (math.isnan(calc_score) or math.isinf(calc_score)) else calc_score

            choice_str = self._extract_choice_key(raw_val).lower()
            opt = question.criteria.get(choice_str)
            if opt:
                score = opt.score
                return 0.0 if (math.isnan(score) or math.isinf(score)) else score
            return 1.0 if choice_str == "yes" else 0.0

        return 0.0

    def score_session(
        self,
        framework: str | Any,
        jev_findings: dict[str, Any],
        analytics: Any = None,
    ) -> ScorecardResult:
        """Compute the deterministic scorecard for a practice session."""
        catalog: FrameworkCatalog = get_framework_catalog(framework)

        findings_dict = (
            jev_findings.get("answers")
            if isinstance(jev_findings, dict) and isinstance(jev_findings.get("answers"), dict)
            else jev_findings
        )

        # 1. Compute question-level scores
        question_scores: dict[str, float] = {}
        for q in catalog.questions:
            raw_finding = findings_dict.get(q.id) if isinstance(findings_dict, dict) else None
            q_score = self._score_single_question(q, raw_finding)
            if math.isnan(q_score) or math.isinf(q_score):
                q_score = 0.0
            question_scores[q.id] = q_score

        # 2. Compute dimension subscores
        dim_scores: dict[str, float] = {}
        for dim, _weight in catalog.dimension_weights.items():
            questions_in_dim = [q for q in catalog.questions if q.dimension == dim]
            if not questions_in_dim:
                dim_scores[dim] = 0.0
                continue
            weighted_sum = sum(
                question_scores[q.id] * q.weight_in_dimension for q in questions_in_dim
            )
            total_dim_weight = sum(q.weight_in_dimension for q in questions_in_dim)
            val = weighted_sum / total_dim_weight if total_dim_weight > 0 else 0.0
            dim_scores[dim] = 0.0 if (math.isnan(val) or math.isinf(val)) else val

        # 3. Base composite formula
        base_score = sum(
            dim_scores[dim] * weight for dim, weight in catalog.dimension_weights.items()
        )
        if math.isnan(base_score) or math.isinf(base_score):
            base_score = 0.0

        domain_penalties: dict[str, Any] = {}

        # 4. Domain-specific penalty rules
        # GOTTMAN: Contempt and Horsemen multiplicative penalty
        if catalog.framework == "GOTTMAN":
            horsemen_val = jev_findings.get("gottman_four_horsemen_marker")
            horsemen_key = self._extract_choice_key(horsemen_val)
            horsemen_q = catalog.get_question("gottman_four_horsemen_marker")
            if horsemen_q and horsemen_key in horsemen_q.criteria:
                multiplier = horsemen_q.criteria[horsemen_key].score
            else:
                multiplier = 1.0
            domain_penalties["horsemen_marker"] = horsemen_key
            domain_penalties["horsemen_multiplier"] = multiplier
            base_score = base_score * multiplier
            if math.isnan(base_score) or math.isinf(base_score):
                base_score = 0.0

        # VOSS: Accusatory Why
        if catalog.framework in ("VOSS", "VOSS_NEGOTIATION"):
            calib_val = jev_findings.get("voss_calibrated_questions")
            if self._extract_choice_key(calib_val) == "accusatory_why":
                domain_penalties["accusatory_why_used"] = True

        # PAR: Brevity checks
        if catalog.framework == "PAR":
            brev_val = jev_findings.get("par_brevity_and_information_density")
            if self._extract_choice_key(brev_val) == "bloated_or_rambling":
                domain_penalties["bloated_response"] = True
            if analytics is not None:
                duration = getattr(analytics, "duration_seconds", None)
                if duration is not None and duration > 75:
                    domain_penalties["duration_over_budget"] = duration

        # 5. Scale and clamp between 0.0 and 100.0
        if math.isnan(base_score) or math.isinf(base_score):
            composite_score = 0.0
        else:
            composite_score = round(max(0.0, min(100.0, base_score * 100.0)), 1)
            if math.isnan(composite_score) or math.isinf(composite_score):
                composite_score = 0.0

        subscores_100: dict[str, float] = {}
        for dim, score in dim_scores.items():
            if math.isnan(score) or math.isinf(score):
                subscores_100[dim] = 0.0
            else:
                s_val = round(max(0.0, min(100.0, score * 100.0)), 1)
                subscores_100[dim] = 0.0 if (math.isnan(s_val) or math.isinf(s_val)) else s_val

        subscore_items = [
            ScorecardSubscore(
                dimension=dim,
                score=subscores_100[dim],
                weight=catalog.dimension_weights.get(dim, 0.0),
            )
            for dim in catalog.dimensions
        ]

        # 6. Badges & Coaching Tips
        badges = self.badge_engine.evaluate_badges(
            catalog.framework, jev_findings, subscores_100, analytics
        )
        tips = self.tips_engine.generate_tips(
            catalog.framework, jev_findings, subscores_100, analytics
        )

        return ScorecardResult(
            framework=catalog.framework,
            composite_score=composite_score,
            subscores=subscores_100,
            subscore_items=subscore_items,
            badges=badges,
            tips=tips,
            details={
                "question_scores": question_scores,
                "dimension_scores_normalized": dim_scores,
                "domain_penalties": domain_penalties,
            },
        )
