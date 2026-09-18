"""Explicit verification of the Balanced Impact Rule across communication frameworks.

The Balanced Impact Rule mandates that meaningful qualitative / operational achievements
(e.g. unblocking cross-functional squads, preventing client churn, eliminating single points
of failure, resolving contract deadlocks) receive the EXACT SAME full credit (1.0 / 100%)
as numerical statistics (e.g. 45% latency drop, $10M saved).
"""

from app.frameworks import get_framework_catalog
from app.services.scoring import ScoringEngine


def test_balanced_impact_criteria_in_catalogs():
    """Verify catalogs award identical 1.0 credit to qualitative and quantitative outcomes."""
    for fw_name, q_id in [
        ("STAR", "star_result_and_impact"),
        ("CARL", "carl_result_and_impact"),
        ("PAR", "par_result_and_impact"),
    ]:
        catalog = get_framework_catalog(fw_name)
        q = catalog.get_question(q_id)
        assert q is not None, f"Missing question {q_id} in {fw_name}"
        assert q.criteria["quantified_metric_impact"].score == 1.0, (
            f"{fw_name} quantified metric impact score != 1.0"
        )
        assert q.criteria["meaningful_qualitative_impact"].score == 1.0, (
            f"{fw_name} qualitative impact score != 1.0 (Balanced Impact Violation!)"
        )
        assert q.criteria["weak_or_vague_outcome"].score == 0.3
        # Lowest score is 0.0
        absent_key = (
            "absent_or_unresolved"
            if "absent_or_unresolved" in q.criteria
            else "absent_or_trailing_off"
        )
        assert q.criteria[absent_key].score == 0.0


def test_star_balanced_impact_rule():
    """Verify STAR composite and subscore equality for qualitative vs quantitative outcomes."""
    engine = ScoringEngine()

    base_findings = {
        "star_situation_grounding": "well_grounded",
        "star_task_clarity": "clearly_defined",
        "star_action_ownership_and_depth": "Level 5",
        "star_narrative_balance": "well_balanced_action_focus",
        "star_prompt_relevance": "directly_relevant",
    }

    # Case A: Quantitative metrics (e.g. 50% latency drop)
    findings_quant = {**base_findings, "star_result_and_impact": "quantified_metric_impact"}
    result_quant = engine.score_session("STAR", findings_quant)

    # Case B: Meaningful qualitative impact (e.g. unblocking a squad, preventing churn)
    findings_qual = {**base_findings, "star_result_and_impact": "meaningful_qualitative_impact"}
    result_qual = engine.score_session("STAR", findings_qual)

    # Core Assertion: Identical 100% composite score
    assert result_quant.composite_score == 100.0
    assert result_qual.composite_score == 100.0
    assert result_quant.composite_score == result_qual.composite_score

    # Subscore assertion
    assert result_quant.subscores["result"] == 100.0
    assert result_qual.subscores["result"] == 100.0

    # Badges: Both award top tier badges
    assert "Quantified Mastery" in result_quant.badge_names
    assert "High-Impact Outcome" in result_qual.badge_names

    # Case C: Vague outcome penalty
    findings_vague = {**base_findings, "star_result_and_impact": "weak_or_vague_outcome"}
    result_vague = engine.score_session("STAR", findings_vague)
    assert result_vague.subscores["result"] == 30.0
    assert result_vague.composite_score < 100.0
    assert "Vague Impact" in result_vague.badge_names

    # Case D: Absent outcome
    findings_absent = {**base_findings, "star_result_and_impact": "absent_or_unresolved"}
    result_absent = engine.score_session("STAR", findings_absent)
    assert result_absent.subscores["result"] == 0.0
    assert result_absent.composite_score < result_vague.composite_score


def test_carl_balanced_impact_rule():
    """Verify CARL composite and subscore equality for qualitative vs quantitative outcomes."""
    engine = ScoringEngine()

    base_findings = {
        "carl_context_framing": "well_framed_context",
        "carl_action_ownership_and_rigor": "Level 5",
        "carl_learning_metacognitive_depth": "Level 5",
        "carl_narrative_balance": "rich_learning_climax",
        "carl_vulnerability_and_humility": "authentic_humility_and_ownership",
    }

    # Case A: Quantitative metrics
    findings_quant = {**base_findings, "carl_result_and_impact": "quantified_metric_impact"}
    result_quant = engine.score_session("CARL", findings_quant)

    # Case B: Qualitative operational outcome
    findings_qual = {**base_findings, "carl_result_and_impact": "meaningful_qualitative_impact"}
    result_qual = engine.score_session("CARL", findings_qual)

    assert result_quant.composite_score == 100.0
    assert result_qual.composite_score == 100.0
    assert result_quant.composite_score == result_qual.composite_score
    assert result_quant.subscores["result"] == 100.0
    assert result_qual.subscores["result"] == 100.0

    assert "Quantified Mastery" in result_quant.badge_names
    assert "High Operational Impact" in result_qual.badge_names

    # Penalties for weak or absent outcomes
    result_vague = engine.score_session(
        "CARL", {**base_findings, "carl_result_and_impact": "weak_or_vague_outcome"}
    )
    assert result_vague.subscores["result"] == 30.0
    assert result_vague.composite_score < 100.0

    result_absent = engine.score_session(
        "CARL", {**base_findings, "carl_result_and_impact": "absent_or_unresolved"}
    )
    assert result_absent.subscores["result"] == 0.0


def test_par_balanced_impact_rule():
    """Verify PAR composite and subscore equality for qualitative vs quantitative outcomes."""
    engine = ScoringEngine()

    base_findings = {
        "par_problem_sharpness": "sharp_and_immediate",
        "par_action_decisiveness": "Level 5",
        "par_brevity_and_information_density": "crisp_executive_brevity",
        "par_prompt_relevance": "directly_relevant",
    }

    # Case A: Quantitative metrics
    findings_quant = {**base_findings, "par_result_and_impact": "quantified_metric_impact"}
    result_quant = engine.score_session("PAR", findings_quant)

    # Case B: Qualitative operational outcome
    findings_qual = {**base_findings, "par_result_and_impact": "meaningful_qualitative_impact"}
    result_qual = engine.score_session("PAR", findings_qual)

    assert result_quant.composite_score == 100.0
    assert result_qual.composite_score == 100.0
    assert result_quant.composite_score == result_qual.composite_score
    assert result_quant.subscores["result"] == 100.0
    assert result_qual.subscores["result"] == 100.0

    assert "High Operational Impact" in result_qual.badge_names

    # Weak outcome
    result_vague = engine.score_session(
        "PAR", {**base_findings, "par_result_and_impact": "weak_or_vague_outcome"}
    )
    assert result_vague.subscores["result"] == 30.0
    assert result_vague.composite_score < 100.0


def test_scqa_recommendation_balanced_impact():
    """Verify SCQA full credit for high-impact recommendation solutions."""
    engine = ScoringEngine()

    base_findings = {
        "scqa_situation_baseline": "uncontroversial_clear_baseline",
        "scqa_complication_friction": "sharp_urgent_friction",
        "scqa_governing_question": "explicitly_articulated",
        "scqa_bluf_efficiency": "Level 5",
        "scqa_structural_flow": "textbook_minto_flow",
    }

    findings_top = {
        **base_findings,
        "scqa_recommendation_substance": "actionable_high_impact_solution",
    }
    result_top = engine.score_session("SCQA", findings_top)

    assert result_top.composite_score == 100.0
    assert result_top.subscores["recommendation"] == 100.0

    # Hedged solution
    findings_hedged = {
        **base_findings,
        "scqa_recommendation_substance": "partial_hedged_solution",
    }
    result_hedged = engine.score_session("SCQA", findings_hedged)
    assert result_hedged.subscores["recommendation"] == 50.0
    assert result_hedged.composite_score < 100.0

    # Vague non-committal
    findings_vague = {
        **base_findings,
        "scqa_recommendation_substance": "vague_non_committal",
    }
    result_vague = engine.score_session("SCQA", findings_vague)
    assert result_vague.subscores["recommendation"] == 10.0
    assert result_vague.composite_score < result_hedged.composite_score
