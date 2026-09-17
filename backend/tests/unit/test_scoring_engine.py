"""Unit tests for the Deterministic Scoring Engine across all 11 Communication Frameworks."""

import pytest

from app.frameworks import ALL_CATALOGS
from app.services.analytics import DeliveryAnalyticsResult
from app.services.scoring import ScorecardResult, ScoringEngine


@pytest.fixture
def scoring_engine():
    return ScoringEngine()


# ---------------------------------------------------------------------------
# 1. Verification of 0-100 Scoring Math Across All 11 Frameworks
# ---------------------------------------------------------------------------


def test_empty_findings_yield_zero_score_for_all_frameworks(scoring_engine):
    """Verify that an empty dictionary of findings safely produces 0.0 for all 11 frameworks."""
    for cat in ALL_CATALOGS:
        result = scoring_engine.score_session(cat.framework, {})
        assert isinstance(result, ScorecardResult)
        assert result.composite_score == 0.0
        assert result.framework == cat.framework
        for dim in cat.dimensions:
            assert result.subscores[dim] == 0.0


def test_perfect_scores_yield_100_for_all_11_frameworks(scoring_engine):
    """Verify optimal criteria in each question yields 100.0 score across all frameworks."""
    optimal_findings = {
        "STAR": {
            "star_situation_grounding": "well_grounded",
            "star_task_clarity": "clearly_defined",
            "star_action_ownership_and_depth": "Level 5",
            "star_result_and_impact": "meaningful_qualitative_impact",
            "star_narrative_balance": "well_balanced_action_focus",
            "star_prompt_relevance": "directly_relevant",
        },
        "CARL": {
            "carl_context_framing": "well_framed_context",
            "carl_action_ownership_and_rigor": "Level 5",
            "carl_result_and_impact": "quantified_metric_impact",
            "carl_learning_metacognitive_depth": "Level 5",
            "carl_narrative_balance": "rich_learning_climax",
            "carl_vulnerability_and_humility": "authentic_humility_and_ownership",
        },
        "PAR": {
            "par_problem_sharpness": "sharp_and_immediate",
            "par_action_decisiveness": "Level 5",
            "par_result_and_impact": "meaningful_qualitative_impact",
            "par_brevity_and_information_density": "crisp_executive_brevity",
            "par_prompt_relevance": "directly_relevant",
        },
        "SCQA": {
            "scqa_situation_baseline": "uncontroversial_clear_baseline",
            "scqa_complication_friction": "sharp_urgent_friction",
            "scqa_governing_question": "explicitly_articulated",
            "scqa_bluf_efficiency": "Level 5",
            "scqa_recommendation_substance": "actionable_high_impact_solution",
            "scqa_structural_flow": "textbook_minto_flow",
        },
        "SBI": {
            "sbi_situation_anchoring": "specifically_anchored_time_place",
            "sbi_behavioral_camera_test": "Level 5",
            "sbi_impact_operational_clarity": "clear_operational_or_relational_impact",
            "sbi_feedback_sandwich_filter": "clean_direct_candor",
            "sbi_solution_co_creation": "collaborative_co_creation",
        },
        "RADICAL_CANDOR": {
            "candor_quadrant_classification": "radical_candor",
            "candor_challenge_directly_clarity": "Level 5",
            "candor_care_personally_signals": "Level 5",
            "candor_private_developmental_setting": "private_developmental_frame",
            "candor_openness_to_counter_feedback": {"yes": 1.0, "no": 0.0},
        },
        "STATE": {
            "state_facts_first_sequencing": {"yes": 1.0, "no": 0.0},
            "state_story_framing_awareness": "properly_framed_as_story",
            "state_tentative_language_calibration": "Level 5",
            "state_mutual_purpose_safety": "explicit_mutual_purpose",
            "state_ask_and_encourage_testing": "genuine_inquiry_and_testing",
            "state_emotional_composure": "Level 5",
        },
        "GOTTMAN": {
            "gottman_four_horsemen_marker": "none_clean_de_escalated",
            "gottman_soft_startup_presence": {"yes": 1.0, "no": 0.0},
            "gottman_responsibility_acceptance": "Level 5",
            "gottman_repair_attempt_usage": "active_repair_attempt_used",
            "gottman_flooding_awareness_timeout": "structured_timeout_called",
            "gottman_validation_of_counterpart": "Level 5",
        },
        "VOSS": {
            "voss_emotion_labeling": {"yes": 1.0, "no": 0.0},
            "voss_calibrated_questions": "calibrated_how_what",
            "voss_no_oriented_inquiry": "no_oriented_question_present",
            "voss_vocal_tone_estimate": "late_night_dj_calm",
            "voss_reciprocal_concession_framing": "Level 5",
            "voss_mirroring_technique": "mirror_used_effectively",
        },
        "SPARKLINE": {
            "sparkline_what_is_vs_could_be_contrast": "Level 5",
            "sparkline_audience_as_hero": "audience_is_the_hero",
            "sparkline_hook_first_30s": "Level 5",
            "sparkline_star_moment_presence": "star_moment_present",
            "sparkline_new_bliss_vision": "inspiring_new_bliss",
            "sparkline_call_to_adventure": "clear_call_to_adventure",
        },
        "MONROE": {
            "monroe_attention_hook": "Level 5",
            "monroe_need_urgency": "acute_need_proven",
            "monroe_satisfaction_viability": "concrete_viable_solution",
            "monroe_visualization_polarity": "Level 5",
            "monroe_action_friction_and_clarity": "singular_frictionless_ask",
            "monroe_sequence_progression": "flawless_five_step_progression",
        },
    }

    from app.frameworks.cross_cutting import (
        AMBIGUITY_QUESTION_ID,
        CLARITY_SCORE_QUESTION_ID,
    )

    for fw, findings in optimal_findings.items():
        findings = {
            **findings,
            CLARITY_SCORE_QUESTION_ID: "Level 5",
            AMBIGUITY_QUESTION_ID: "unambiguous_and_precise",
        }
        res = scoring_engine.score_session(fw, findings)
        assert pytest.approx(res.composite_score, abs=0.1) == 100.0, (
            f"Framework {fw} failed to score 100 on optimal findings: {res.composite_score}"
        )
        for dim, score in res.subscores.items():
            assert pytest.approx(score, abs=0.1) == 100.0, (
                f"Framework {fw} dimension {dim} scored {score}, expected 100.0"
            )


# ---------------------------------------------------------------------------
# 2. Gottman Domain Rules & Contempt Multiplicative Collapse
# ---------------------------------------------------------------------------


def test_gottman_contempt_collapse_penalty(scoring_engine):
    """Verify that detecting Contempt in Gottman causes a 0.1x score collapse (90% reduction)."""
    base_clean = {
        "gottman_soft_startup_presence": {"yes": 1.0, "no": 0.0},
        "gottman_responsibility_acceptance": "Level 5",
        "gottman_repair_attempt_usage": "active_repair_attempt_used",
        "gottman_flooding_awareness_timeout": "structured_timeout_called",
        "gottman_validation_of_counterpart": "Level 5",
    }

    # Clean de-escalation: score is 100
    res_clean = scoring_engine.score_session(
        "GOTTMAN",
        {**base_clean, "gottman_four_horsemen_marker": "none_clean_de_escalated"},
    )
    assert res_clean.composite_score == 100.0
    assert "Masterful De-escalation" in res_clean.badge_names

    # Contempt detected: score collapses to 10.0 (100 * 0.1)
    res_contempt = scoring_engine.score_session(
        "GOTTMAN",
        {**base_clean, "gottman_four_horsemen_marker": "contempt_detected"},
    )
    assert res_contempt.composite_score == 10.0
    assert "Contempt Alert" in res_contempt.badge_names
    assert any("Contempt is the #1 predictor" in tip for tip in res_contempt.tips)

    # Defensiveness: score is 60.0 (100 * 0.6)
    res_def = scoring_engine.score_session(
        "GOTTMAN",
        {**base_clean, "gottman_four_horsemen_marker": "defensiveness_detected"},
    )
    assert res_def.composite_score == 60.0
    assert "Defensive Trap" in res_def.badge_names

    # Criticism: score is 50.0 (100 * 0.5)
    res_crit = scoring_engine.score_session(
        "GOTTMAN",
        {**base_clean, "gottman_four_horsemen_marker": "criticism_detected"},
    )
    assert res_crit.composite_score == 50.0

    # Stonewalling: score is 40.0 (100 * 0.4)
    res_stone = scoring_engine.score_session(
        "GOTTMAN",
        {**base_clean, "gottman_four_horsemen_marker": "stonewalling_detected"},
    )
    assert res_stone.composite_score == 40.0


# ---------------------------------------------------------------------------
# 3. Chris Voss Negotiation Rules: Accusatory 'Why' & Tactical Empathy
# ---------------------------------------------------------------------------


def test_voss_accusatory_why_penalty(scoring_engine):
    """Verify asking accusatory 'Why' incurs severe penalty and triggers coaching tip."""
    base_voss = {
        "voss_emotion_labeling": {"yes": 1.0, "no": 0.0},
        "voss_no_oriented_inquiry": "no_oriented_question_present",
        "voss_vocal_tone_estimate": "late_night_dj_calm",
        "voss_reciprocal_concession_framing": "Level 5",
        "voss_mirroring_technique": "mirror_used_effectively",
    }

    # Good Calibrated Question: 'How' / 'What'
    res_good = scoring_engine.score_session(
        "VOSS",
        {**base_voss, "voss_calibrated_questions": "calibrated_how_what"},
    )
    assert res_good.subscores["calibrated_questions"] == 100.0
    assert res_good.composite_score == 100.0
    assert "Cognitive Burden Shift" in res_good.badge_names
    assert "Tactical Empathy Master" in res_good.badge_names

    # Bad: Accusatory 'Why' (0.1 score = 10.0 subscore)
    res_why = scoring_engine.score_session(
        "VOSS",
        {**base_voss, "voss_calibrated_questions": "accusatory_why"},
    )
    assert res_why.subscores["calibrated_questions"] == 10.0
    assert res_why.composite_score < 100.0
    assert "The 'Why' Trap" in res_why.badge_names
    assert any("The 'Why' Trap" in tip or "Why did you raise" in tip for tip in res_why.tips)


# ---------------------------------------------------------------------------
# 4. CARL Non-Linear Metacognitive Learning Rubric
# ---------------------------------------------------------------------------


def test_carl_non_linear_learning_scale(scoring_engine):
    """Verify the non-linear grading scale of CARL's Learning dimension."""
    base_carl = {
        "carl_context_framing": "well_framed_context",
        "carl_action_ownership_and_rigor": "Level 5",
        "carl_result_and_impact": "meaningful_qualitative_impact",
        "carl_narrative_balance": "rich_learning_climax",
        "carl_vulnerability_and_humility": "authentic_humility_and_ownership",
    }

    # Level 5: 1.0 -> 100.0
    r5 = scoring_engine.score_session(
        "CARL",
        {**base_carl, "carl_learning_metacognitive_depth": "Level 5"},
    )
    assert r5.subscores["learning"] == 100.0
    assert "Systemic Wisdom" in r5.badge_names

    # Level 4: 0.85 -> 85.0
    r4 = scoring_engine.score_session(
        "CARL",
        {**base_carl, "carl_learning_metacognitive_depth": "Level 4"},
    )
    assert r4.subscores["learning"] == 85.0
    assert "Systemic Wisdom" in r4.badge_names

    # Level 3: 0.65 -> 65.0
    r3 = scoring_engine.score_session(
        "CARL",
        {**base_carl, "carl_learning_metacognitive_depth": "Level 3"},
    )
    assert r3.subscores["learning"] == 65.0

    # Level 2: 0.30 -> 30.0 (superficial)
    r2 = scoring_engine.score_session(
        "CARL",
        {**base_carl, "carl_learning_metacognitive_depth": "Level 2"},
    )
    assert r2.subscores["learning"] == 30.0
    assert "Superficial Learning" in r2.badge_names

    # Level 1: 0.0 -> 0.0 (defensive blame)
    r1 = scoring_engine.score_session(
        "CARL",
        {**base_carl, "carl_learning_metacognitive_depth": "Level 1"},
    )
    assert r1.subscores["learning"] == 0.0
    assert "Defensive Blame Alert" in r1.badge_names
    assert any("externalized blame" in tip.lower() for tip in r1.tips)


# ---------------------------------------------------------------------------
# 5. PAR Brevity and Delivery Analytics Integration
# ---------------------------------------------------------------------------


def test_par_brevity_and_analytics_integration(scoring_engine):
    """Verify PAR executive brevity and speech analytics badges and tips."""
    findings_par = {
        "par_problem_sharpness": "sharp_and_immediate",
        "par_action_decisiveness": "Level 4",
        "par_result_and_impact": "meaningful_qualitative_impact",
        "par_brevity_and_information_density": "crisp_executive_brevity",
        "par_prompt_relevance": "directly_relevant",
    }

    analytics = DeliveryAnalyticsResult(
        word_count=145,
        duration_seconds=52.0,
        words_per_minute=167.3,
        filler_count=2,
        filler_words_breakdown={"um": 2},
        filler_density_percentage=1.38,
        pause_count=4,
        power_pauses_count=3,
    )

    res = scoring_engine.score_session("PAR", findings_par, analytics=analytics)
    assert res.composite_score > 90.0
    assert "Executive Brevity" in res.badge_names
    assert "Optimal Pace" in res.badge_names
    assert "Clean Cadence" in res.badge_names
    assert "Power Pauser" in res.badge_names


def test_delivery_analytics_warnings(scoring_engine):
    """Verify speech analytics triggers fast pacing and filler warnings."""
    analytics_fast = DeliveryAnalyticsResult(
        word_count=250,
        duration_seconds=65.0,
        words_per_minute=230.0,
        filler_count=18,
        filler_words_breakdown={"like": 10, "um": 8},
        filler_density_percentage=7.2,
        pause_count=1,
        power_pauses_count=0,
    )

    res = scoring_engine.score_session("STAR", {}, analytics=analytics_fast)
    assert "Fast Pacing Warning" in res.badge_names
    assert any("speaking rate was 230 WPM" in tip for tip in res.tips)
    assert any("Filler word density was 7.2%" in tip for tip in res.tips)


def test_coaching_tips_generation_across_all_frameworks(scoring_engine):
    """Verify targeted behavioral coaching tips are produced for all frameworks."""
    # SCQA: Buried lede
    r_scqa = scoring_engine.score_session(
        "SCQA",
        {"scqa_bluf_efficiency": "Level 1"},
    )
    assert any(
        "state the answer in the first 20" in t.lower()
        or "delivering your recommendation" in t.lower()
        for t in r_scqa.tips
    )

    # SBI: Artificial sandwich
    r_sbi = scoring_engine.score_session(
        "SBI",
        {"sbi_feedback_sandwich_filter": "artificial_sandwiching_detected"},
    )
    assert any("sandwich" in t.lower() or "compliments" in t.lower() for t in r_sbi.tips)

    # Radical Candor: Obnoxious aggression
    r_rc = scoring_engine.score_session(
        "RADICAL_CANDOR",
        {"candor_quadrant_classification": "obnoxious_aggression"},
    )
    assert any("challenging directly without" in t.lower() for t in r_rc.tips)

    # STATE: Dogmatic absolutes
    r_state = scoring_engine.score_session(
        "STATE",
        {"state_tentative_language_calibration": "Level 1"},
    )
    assert any("absolutes provoke" in t.lower() for t in r_state.tips)

    # Sparkline: Flat contrast
    r_spark = scoring_engine.score_session(
        "SPARKLINE",
        {"sparkline_what_is_vs_could_be_contrast": "Level 1"},
    )
    assert any("flat feature list" in t.lower() for t in r_spark.tips)

    # Monroe: Weak ask
    r_monroe = scoring_engine.score_session(
        "MONROE",
        {"monroe_action_friction_and_clarity": "vague_non_committal_close"},
    )
    assert any("non-committal ask" in t.lower() for t in r_monroe.tips)


# ---------------------------------------------------------------------------
# 6. Score-Type Question Multi-Representation Handling
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw_repr", "expected_action_score"),
    [
        # Level 4 formats (0.8 score -> 80.0 subscore)
        ({"choice": "Level 4"}, 80.0),
        ({"level": "Level 4"}, 80.0),
        ({"score": "Level 4"}, 80.0),
        ({"value": "Level 4"}, 80.0),
        ({"choice": 4}, 80.0),
        ({"level": 4}, 80.0),
        ({"score": 4}, 80.0),
        ({"value": 4}, 80.0),
        ("Level 4", 80.0),
        (4, 80.0),
        (
            {
                "type": "score",
                "level": "Level 4",
                "choice": "Level 4",
                "probabilities": {"Level 4": 0.65},
            },
            80.0,
        ),
        (
            {
                "type": "score",
                "choice": "Level 4",
                "probabilities": {"Level 4": 0.65},
            },
            80.0,
        ),
        (
            {
                "type": "score",
                "level": "Level 4",
                "probabilities": {"Level 4": 0.65},
            },
            80.0,
        ),
        (
            {
                "type": "score",
                "score": "Level 4",
                "probabilities": {"Level 4": 0.65},
            },
            80.0,
        ),
        (
            {
                "type": "score",
                "value": "Level 4",
                "probabilities": {"Level 4": 0.65},
            },
            80.0,
        ),
        # Level 5 formats (1.0 score -> 100.0 subscore)
        ({"choice": "Level 5"}, 100.0),
        ({"level": "Level 5"}, 100.0),
        ({"score": "Level 5"}, 100.0),
        ({"value": "Level 5"}, 100.0),
        ({"choice": 5}, 100.0),
        ({"level": 5}, 100.0),
        ({"score": 5}, 100.0),
        ({"value": 5}, 100.0),
        ("Level 5", 100.0),
        (5, 100.0),
        (
            {
                "type": "score",
                "level": "Level 5",
                "choice": "Level 5",
                "probabilities": {"Level 5": 0.70},
            },
            100.0,
        ),
    ],
)
def test_score_question_representation_formats(
    scoring_engine, raw_repr, expected_action_score
) -> None:
    """Verify SCORE questions evaluate correctly across choice, level, score, value formats."""
    findings = {"star_action_ownership_and_depth": raw_repr}
    res = scoring_engine.score_session("STAR", findings)
    assert pytest.approx(res.subscores["action"], abs=0.1) == expected_action_score


def test_extract_score_value_direct() -> None:
    """Direct unit verification of ScoringEngine._extract_score_value fallback resolution."""
    assert ScoringEngine._extract_score_value({"choice": "Level 4"}) == "Level 4"
    assert ScoringEngine._extract_score_value({"level": "Level 4"}) == "Level 4"
    assert ScoringEngine._extract_score_value({"score": "Level 4"}) == "Level 4"
    assert ScoringEngine._extract_score_value({"value": "Level 4"}) == "Level 4"
    assert ScoringEngine._extract_score_value({"choice": 4}) == "4"
    assert ScoringEngine._extract_score_value({"level": 4}) == "4"
    assert ScoringEngine._extract_score_value({"score": 4}) == "4"
    assert ScoringEngine._extract_score_value({"value": 4}) == "4"
    assert ScoringEngine._extract_score_value("Level 4") == "Level 4"
    assert ScoringEngine._extract_score_value(4) == "4"
    assert ScoringEngine._extract_score_value({}) is None
    assert ScoringEngine._extract_score_value(None) is None

    # Priority check: score -> level -> value -> choice
    assert (
        ScoringEngine._extract_score_value(
            {"score": "Level 5", "level": "Level 4", "value": "Level 3", "choice": "Level 2"}
        )
        == "Level 5"
    )
    assert (
        ScoringEngine._extract_score_value(
            {"score": None, "level": "Level 4", "value": "Level 3", "choice": "Level 2"}
        )
        == "Level 4"
    )
    assert (
        ScoringEngine._extract_score_value(
            {"score": None, "level": None, "value": "Level 3", "choice": "Level 2"}
        )
        == "Level 3"
    )
    assert (
        ScoringEngine._extract_score_value(
            {"score": None, "level": None, "value": None, "choice": "Level 2"}
        )
        == "Level 2"
    )


@pytest.mark.asyncio
async def test_synthetic_jev_gateway_score_question_integration(scoring_engine) -> None:
    """Verify SyntheticJevGateway populates both level and choice, and ScoringEngine scores it."""
    from app.gateways.synthetic import SyntheticJevGateway

    gateway = SyntheticJevGateway()
    questions = {
        "star_action_ownership_and_depth": {
            "type": "score",
            "criteria": {
                "Level 1": "Passive / zero agency",
                "Level 2": "Weak contribution",
                "Level 3": "Adequate ownership",
                "Level 4": "Strong leadership & specificity",
                "Level 5": "Exemplary strategic agency",
            },
        },
    }

    state = {
        "transcript": (
            "I designed the schema, I diagnosed the root cause, and I owned the deployment."
        ),
        "target_framework": "STAR",
        "scenario_prompt": "Incident response",
    }
    findings = await gateway.evaluate_questions(state, questions)
    finding = findings["star_action_ownership_and_depth"]

    # Verify both level and choice are populated by SyntheticJevGateway
    assert "level" in finding
    assert "choice" in finding
    assert finding["level"] == finding["choice"]
    assert finding["level"] in ["Level 4", "Level 5"]

    # Verify ScoringEngine evaluates this finding to non-zero (either 80.0 or 100.0)
    res = scoring_engine.score_session("STAR", findings)
    assert res.subscores["action"] in [80.0, 100.0]


def test_scoring_engine_guards_against_nan_and_inf(scoring_engine) -> None:
    """Verify ScoringEngine sanitizes NaN and Inf floats without awarding bypass scores."""
    # NOUL with NaN
    nan_findings = {"gottman_soft_startup_presence": {"yes": float("nan")}}
    res_nan = scoring_engine.score_session("GOTTMAN", nan_findings)
    assert res_nan.composite_score == 0.0

    # NOUL with Inf
    inf_findings = {"gottman_soft_startup_presence": {"yes": float("inf"), "no": float("-inf")}}
    res_inf = scoring_engine.score_session("GOTTMAN", inf_findings)
    assert res_inf.composite_score == 0.0

    # SCORE with NaN and Inf
    score_nan = {"star_action_ownership_and_depth": float("nan")}
    res_score_nan = scoring_engine.score_session("STAR", score_nan)
    assert res_score_nan.subscores["action"] == 0.0

    score_dict_nan = {"star_action_ownership_and_depth": {"score": float("nan")}}
    res_score_dict_nan = scoring_engine.score_session("STAR", score_dict_nan)
    assert res_score_dict_nan.subscores["action"] == 0.0


def test_scoring_engine_rejects_negative_level_matches(scoring_engine) -> None:
    """Verify negative integers and strings do not match positive criteria levels (e.g. -5 != 5)."""
    negative_inputs = [-5, "-5", -1, "-1", -3, "-3", -10, "-5.0"]
    for neg_val in negative_inputs:
        findings = {"star_action_ownership_and_depth": neg_val}
        res = scoring_engine.score_session("STAR", findings)
        assert res.subscores["action"] == 0.0, (
            f"Expected 0.0 for negative input {neg_val}, got {res.subscores['action']}"
        )


# ---------------------------------------------------------------------------
# Cross-Cutting Clarity Questions (auxiliary dimension)
# ---------------------------------------------------------------------------


def test_clarity_questions_are_scored_into_details(scoring_engine) -> None:
    """Verify the injected clarity questions are scored and reported for every framework."""
    from app.frameworks.cross_cutting import (
        AMBIGUITY_QUESTION_ID,
        CLARITY_DIMENSION,
        CLARITY_SCORE_QUESTION_ID,
    )

    for cat in ALL_CATALOGS:
        findings = {
            CLARITY_SCORE_QUESTION_ID: "Level 5",
            AMBIGUITY_QUESTION_ID: "unambiguous_and_precise",
        }
        res = scoring_engine.score_session(cat.framework, findings)
        assert res.details["question_scores"][CLARITY_SCORE_QUESTION_ID] == 1.0
        assert res.details["question_scores"][AMBIGUITY_QUESTION_ID] == 1.0

        # Reported as a subscore, but with zero composite weight.
        assert res.subscores[CLARITY_DIMENSION] == 100.0
        clarity_item = next(
            item for item in res.subscore_items if item.dimension == CLARITY_DIMENSION
        )
        assert clarity_item.weight == 0.0
        assert clarity_item.score == 100.0


def test_clarity_findings_do_not_change_composite_score(scoring_engine) -> None:
    """Verify clarity/ambiguity findings leave the composite score untouched."""
    from app.frameworks.cross_cutting import (
        AMBIGUITY_QUESTION_ID,
        CLARITY_SCORE_QUESTION_ID,
    )

    for cat in ALL_CATALOGS:
        baseline = {
            q.id: (
                "Level 5"
                if q.type.value == "score"
                else ({"yes": 1.0, "no": 0.0} if q.type.value == "noul" else list(q.criteria)[0])
            )
            for q in cat.questions
            if q.id not in (CLARITY_SCORE_QUESTION_ID, AMBIGUITY_QUESTION_ID)
        }
        with_clarity = dict(baseline)
        with_clarity[CLARITY_SCORE_QUESTION_ID] = "Level 1"
        with_clarity[AMBIGUITY_QUESTION_ID] = "materially_ambiguous"

        score_without = scoring_engine.score_session(cat.framework, baseline).composite_score
        score_with = scoring_engine.score_session(cat.framework, with_clarity).composite_score

        assert score_with == score_without, cat.framework
