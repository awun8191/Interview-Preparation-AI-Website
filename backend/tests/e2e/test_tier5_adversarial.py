"""Tier 5 Adversarial Verification & Coverage Hardening Test Suite.

Executes white-box adversarial stress tests across:
1. Mathematical invariants: scoring formulas, clamping [0, 100], dimension weight sums,
   non-linear scales, domain penalties, and SCORE monotonicity.
2. Balanced Impact Rule: empirical verification that qualitative/operational outcomes
   receive full 100% credit and never score lower than quantitative metrics across all
   outcome-bearing frameworks.
3. Pacing & Delivery Analytics: division-by-zero guards, negative durations, 10,000+ words
   stress test, multi-script Unicode, emojis, and timestamp anomaly handling.
4. Concurrency & Race Conditions: concurrent session persistence, multi-user isolation,
   and pagination monotonicity under write load.
5. Error Envelopes & Security: malformed payloads, injection attempts, and envelope
   standardization without raw unhandled stack traces.
"""

import asyncio
import time
from collections.abc import Generator
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from app.core.errors import ErrorCode
from app.frameworks import QuestionType, get_framework_catalog, list_framework_catalogs
from app.gateways.dependencies import get_synthetic_firestore
from app.main import app
from app.services.analytics import DeliveryAnalyticsResult, calculate_delivery_analytics
from app.services.scoring import ScoringEngine


@pytest.fixture(autouse=True)
def clean_isolation() -> Generator[None]:
    """Ensure in-memory repository and app state are cleanly reset for every test."""
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()
    yield
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()


# ============================================================================
# Vector 1: Mathematical Invariants & Scoring Hardening
# ============================================================================


def test_tier5_all_11_frameworks_dimension_weight_conservation() -> None:
    """Verify that dimension weights in every framework sum strictly to 1.0 (epsilon 1e-6)."""
    catalogs = list_framework_catalogs()
    assert len(catalogs) == 11, f"Expected 11 framework catalogs, found {len(catalogs)}"

    for cat in catalogs:
        dim_sum = sum(cat.dimension_weights.values())
        assert abs(dim_sum - 1.0) < 1e-6, (
            f"Dimension weights for {cat.framework} do not sum to 1.0 (sum={dim_sum})"
        )

        for dim in cat.dimension_weights:
            dim_qs = [q for q in cat.questions if q.dimension == dim]
            assert len(dim_qs) > 0, f"Dimension '{dim}' in {cat.framework} has no questions"
            total_q_weight = sum(q.weight_in_dimension for q in dim_qs)
            assert total_q_weight > 0.0, (
                f"Total question weight for dimension '{dim}' in {cat.framework} must be > 0"
            )


def test_tier5_all_11_frameworks_criteria_score_bounds() -> None:
    """Verify that every criteria option across all questions has a score bounded in [0.0, 1.0]."""
    catalogs = list_framework_catalogs()
    for cat in catalogs:
        for q in cat.questions:
            for opt_key, opt in q.criteria.items():
                assert 0.0 <= opt.score <= 1.0, (
                    f"Out of bounds criteria score {opt.score} in {cat.framework}.{q.id}.{opt_key}"
                )


def test_tier5_scoring_fuzzing_missing_and_corrupted_inputs() -> None:
    """Fuzz ScoringEngine with malformed, out-of-range, and corrupted findings."""
    engine = ScoringEngine()

    fuzz_payloads: list[dict[str, Any]] = [
        {},  # Empty findings
        {"unknown_question_xyz": "foo_bar"},  # Unknown keys
        {"star_situation_grounding": None},  # Explicit None
        {"star_situation_grounding": ""},  # Empty string
        {"star_situation_grounding": 999999},  # Arbitrary int
        {"star_situation_grounding": -1.0},  # Negative float
        {"star_action_ownership_and_depth": {"invalid": "structure"}},  # Arbitrary dict
        {"star_action_ownership_and_depth": ["a", "b", "c"]},  # List
        {"star_result_and_impact": "non_existent_criteria_option"},
        {
            "star_situation_grounding": "well_grounded",
            "star_task_clarity": "clearly_defined",
            "star_action_ownership_and_depth": "Level 999",  # Out of range level
        },
    ]

    for p in fuzz_payloads:
        result = engine.score_session("STAR", p)
        assert 0.0 <= result.composite_score <= 100.0, (
            f"Composite score out of bounds: {result.composite_score}"
        )
        for dim, subscore in result.subscores.items():
            assert 0.0 <= subscore <= 100.0, (
                f"Subscore for {dim} out of bounds: {subscore} on payload {p}"
            )


def test_tier5_non_linear_domain_penalties_gottman_four_horsemen() -> None:
    """Verify Gottman Four Horsemen non-linear penalties and Contempt Collapse."""
    engine = ScoringEngine()
    cat = get_framework_catalog("GOTTMAN")
    horsemen_q = cat.get_question("gottman_four_horsemen_marker")
    assert horsemen_q is not None

    base_findings = {
        "gottman_soft_startup_presence": "yes",
        "gottman_responsibility_acceptance": "Level 5",
        "gottman_repair_attempt_usage": "active_repair_attempt_used",
        "gottman_flooding_awareness_timeout": "structured_timeout_called",
        "gottman_validation_of_counterpart": "Level 5",
    }

    # Baseline: no horsemen
    findings_none = {**base_findings, "gottman_four_horsemen_marker": "none_clean_de_escalated"}
    res_none = engine.score_session("GOTTMAN", findings_none)
    assert res_none.composite_score == 100.0

    # Defensiveness penalty (0.6 multiplier)
    findings_def = {**base_findings, "gottman_four_horsemen_marker": "defensiveness_detected"}
    res_def = engine.score_session("GOTTMAN", findings_def)
    assert res_def.composite_score == 60.0

    # Criticism penalty (0.5 multiplier)
    findings_crit = {**base_findings, "gottman_four_horsemen_marker": "criticism_detected"}
    res_crit = engine.score_session("GOTTMAN", findings_crit)
    assert res_crit.composite_score == 50.0

    # Stonewalling penalty (0.4 multiplier)
    findings_stone = {**base_findings, "gottman_four_horsemen_marker": "stonewalling_detected"}
    res_stone = engine.score_session("GOTTMAN", findings_stone)
    assert res_stone.composite_score == 40.0

    # Contempt Collapse (0.1 multiplier -> 90% reduction)
    findings_contempt = {**base_findings, "gottman_four_horsemen_marker": "contempt_detected"}
    res_contempt = engine.score_session("GOTTMAN", findings_contempt)
    assert res_contempt.composite_score == 10.0
    assert "Contempt Alert" in res_contempt.badge_names
    assert any("predictor of partnership destruction" in tip for tip in res_contempt.tips)


def test_tier5_non_linear_domain_penalties_voss_accusatory_why() -> None:
    """Verify Chris Voss Accusatory 'Why' Trap penalty."""
    engine = ScoringEngine()
    findings_why = {
        "voss_emotion_labeling": "yes",
        "voss_calibrated_questions": "accusatory_why",
        "voss_reciprocal_concessions": "calibrated_concession",
        "voss_vocal_tone": "late_night_fm_dj",
        "voss_no_oriented_inquiry": "no_oriented_question",
        "voss_mirroring": "mirror_exact_last_words",
    }
    result = engine.score_session("VOSS", findings_why)
    assert result.subscores["calibrated_questions"] == 10.0
    assert result.composite_score < 100.0
    assert "The 'Why' Trap" in result.badge_names
    assert any("Rephrase to a calibrated 'What'" in tip for tip in result.tips)


def test_tier5_non_linear_domain_penalties_par_brevity_and_duration() -> None:
    """Verify PAR bloated response and over-budget duration penalties."""
    engine = ScoringEngine()
    base_par = {
        "par_problem_sharpness": "sharp_and_immediate",
        "par_action_decisiveness": "Level 5",
        "par_result_and_impact": "meaningful_qualitative_impact",
        "par_prompt_relevance": "directly_relevant",
    }

    # Case A: Crisp executive brevity under duration budget
    normal_analytics = DeliveryAnalyticsResult(
        word_count=80,
        duration_seconds=50.0,
        words_per_minute=96.0,
        filler_count=0,
        filler_words_breakdown={},
        filler_density_percentage=0.0,
    )
    res_crisp = engine.score_session(
        "PAR",
        {**base_par, "par_brevity_and_information_density": "crisp_executive_brevity"},
        normal_analytics,
    )
    assert res_crisp.composite_score == 100.0

    # Case B: Bloated / rambling response
    over_analytics = DeliveryAnalyticsResult(
        word_count=250,
        duration_seconds=120.0,
        words_per_minute=125.0,
        filler_count=10,
        filler_words_breakdown={},
        filler_density_percentage=4.0,
    )
    res_bloated = engine.score_session(
        "PAR",
        {**base_par, "par_brevity_and_information_density": "bloated_or_rambling"},
        over_analytics,
    )
    assert res_bloated.subscores["brevity"] == 30.0
    assert res_bloated.composite_score < res_crisp.composite_score
    assert res_bloated.details["domain_penalties"].get("bloated_response") is True
    assert res_bloated.details["domain_penalties"].get("duration_over_budget") == 120.0


def test_tier5_score_level_monotonicity() -> None:
    """Verify that QuestionType.SCORE definitions yield non-decreasing scores from Level 1 to 5."""
    engine = ScoringEngine()
    catalogs = list_framework_catalogs()

    for cat in catalogs:
        score_qs = [q for q in cat.questions if q.type == QuestionType.SCORE]
        for q in score_qs:
            prev_score = -1.0
            for lvl in range(1, 6):
                score_val = engine._score_single_question(q, f"Level {lvl}")
                assert score_val >= prev_score, (
                    f"Non-monotonic score progression in {cat.framework}.{q.id}: "
                    f"Level {lvl} ({score_val}) < Level {lvl - 1} ({prev_score})"
                )
                prev_score = score_val


# ============================================================================
# Vector 2: Balanced Impact Rule Verification
# ============================================================================


def test_tier5_balanced_impact_rule_star_outcome_equality() -> None:
    """Verify STAR awards identical 100% credit for qualitative and quantitative impact."""
    engine = ScoringEngine()
    base_findings = {
        "star_situation_grounding": "well_grounded",
        "star_task_clarity": "clearly_defined",
        "star_action_ownership_and_depth": "Level 5",
        "star_narrative_balance": "well_balanced_action_focus",
        "star_prompt_relevance": "directly_relevant",
    }

    res_quant = engine.score_session(
        "STAR", {**base_findings, "star_result_and_impact": "quantified_metric_impact"}
    )
    res_qual = engine.score_session(
        "STAR", {**base_findings, "star_result_and_impact": "meaningful_qualitative_impact"}
    )

    assert res_quant.composite_score == 100.0
    assert res_qual.composite_score == 100.0
    assert res_qual.subscores["result"] == 100.0
    assert res_quant.subscores["result"] == 100.0
    assert res_qual.composite_score >= res_quant.composite_score


def test_tier5_balanced_impact_rule_carl_outcome_equality() -> None:
    """Verify CARL awards identical 100% credit for qualitative and quantitative impact."""
    engine = ScoringEngine()
    base_findings = {
        "carl_context_framing": "well_framed_context",
        "carl_action_ownership_and_rigor": "Level 5",
        "carl_learning_metacognitive_depth": "Level 5",
        "carl_narrative_balance": "rich_learning_climax",
        "carl_vulnerability_and_humility": "authentic_humility_and_ownership",
    }

    res_quant = engine.score_session(
        "CARL", {**base_findings, "carl_result_and_impact": "quantified_metric_impact"}
    )
    res_qual = engine.score_session(
        "CARL", {**base_findings, "carl_result_and_impact": "meaningful_qualitative_impact"}
    )

    assert res_quant.composite_score == 100.0
    assert res_qual.composite_score == 100.0
    assert res_qual.subscores["result"] == 100.0
    assert res_quant.subscores["result"] == 100.0
    assert res_qual.composite_score >= res_quant.composite_score


def test_tier5_balanced_impact_rule_par_outcome_equality() -> None:
    """Verify PAR awards identical 100% credit for qualitative and quantitative impact."""
    engine = ScoringEngine()
    base_findings = {
        "par_problem_sharpness": "sharp_and_immediate",
        "par_action_decisiveness": "Level 5",
        "par_brevity_and_information_density": "crisp_executive_brevity",
        "par_prompt_relevance": "directly_relevant",
    }

    res_quant = engine.score_session(
        "PAR", {**base_findings, "par_result_and_impact": "quantified_metric_impact"}
    )
    res_qual = engine.score_session(
        "PAR", {**base_findings, "par_result_and_impact": "meaningful_qualitative_impact"}
    )

    assert res_quant.composite_score == 100.0
    assert res_qual.composite_score == 100.0
    assert res_qual.subscores["result"] == 100.0
    assert res_quant.subscores["result"] == 100.0
    assert res_qual.composite_score >= res_quant.composite_score


def test_tier5_balanced_impact_rule_scqa_and_sbi_outcomes() -> None:
    """Verify SCQA and SBI award full credit for operational and strategic impact."""
    engine = ScoringEngine()

    # SCQA recommendation dimension
    scqa_findings = {
        "scqa_situation_baseline": "uncontroversial_clear_baseline",
        "scqa_complication_friction": "sharp_urgent_friction",
        "scqa_governing_question": "explicitly_articulated",
        "scqa_bluf_efficiency": "Level 5",
        "scqa_structural_flow": "textbook_minto_flow",
        "scqa_recommendation_substance": "actionable_high_impact_solution",
    }
    res_scqa = engine.score_session("SCQA", scqa_findings)
    assert res_scqa.subscores["recommendation"] == 100.0
    assert res_scqa.composite_score == 100.0

    # SBI impact dimension
    sbi_findings = {
        "sbi_situation_anchoring": "specifically_anchored_time_place",
        "sbi_behavioral_camera_test": "Level 5",
        "sbi_impact_operational_clarity": "clear_operational_or_relational_impact",
        "sbi_feedback_sandwich_filter": "clean_direct_candor",
        "sbi_solution_co_creation": "collaborative_co_creation",
    }
    res_sbi = engine.score_session("SBI", sbi_findings)
    assert res_sbi.subscores["impact"] == 100.0
    assert res_sbi.composite_score == 100.0


def test_tier5_balanced_impact_rule_never_scores_lower_than_quantitative() -> None:
    """Exhaustive check: in all outcome-bearing frameworks, qualitative never scores lower."""
    engine = ScoringEngine()
    frameworks_to_check = [
        ("STAR", "star_result_and_impact"),
        ("CARL", "carl_result_and_impact"),
        ("PAR", "par_result_and_impact"),
    ]

    for fw, q_id in frameworks_to_check:
        cat = get_framework_catalog(fw)
        # Create a baseline with lowest scores for all other questions
        baseline: dict[str, Any] = {
            q.id: list(q.criteria.keys())[0] for q in cat.questions if q.id != q_id
        }

        quant_payload = {**baseline, q_id: "quantified_metric_impact"}
        qual_payload = {**baseline, q_id: "meaningful_qualitative_impact"}

        res_quant = engine.score_session(fw, quant_payload)
        res_qual = engine.score_session(fw, qual_payload)

        dim_name = cat.get_question(q_id).dimension  # type: ignore[union-attr]
        assert res_qual.subscores[dim_name] >= res_quant.subscores[dim_name], (
            f"Balanced Impact Rule violation in {fw}: qualitative subscore "
            f"({res_qual.subscores[dim_name]}) < quantitative ({res_quant.subscores[dim_name]})"
        )
        assert res_qual.composite_score >= res_quant.composite_score, (
            f"Balanced Impact Rule violation in {fw}: qualitative composite "
            f"({res_qual.composite_score}) < quantitative ({res_quant.composite_score})"
        )


# ============================================================================
# Vector 3: Pacing & Delivery Analytics Adversarial Stress
# ============================================================================


def test_tier5_delivery_analytics_zero_and_negative_duration_guards() -> None:
    """Verify zero division prevention and negative duration clamping."""
    # Negative duration
    res_neg = calculate_delivery_analytics("Testing negative speech duration", -45.0)
    assert res_neg.duration_seconds == 0.0
    assert res_neg.words_per_minute == 0.0
    assert res_neg.word_count == 4

    # Zero duration
    res_zero = calculate_delivery_analytics("Testing zero speech duration", 0.0)
    assert res_zero.duration_seconds == 0.0
    assert res_zero.words_per_minute == 0.0
    assert res_zero.word_count == 4

    # Empty transcript with negative duration
    res_empty_neg = calculate_delivery_analytics("", -10.0)
    assert res_empty_neg.duration_seconds == 0.0
    assert res_empty_neg.words_per_minute == 0.0
    assert res_empty_neg.word_count == 0
    assert res_empty_neg.filler_density_percentage == 0.0


def test_tier5_delivery_analytics_10k_words_stress_performance() -> None:
    """Stress-test delivery analytics with a massive 12,000+ word transcript."""
    chunk = (
        "actually we deployed the change and like you know sort of kind of basically "
        "stabilized the database cluster while monitoring the metrics uh um "
    )
    # 20 words per chunk * 600 repetitions = 12,000 words
    massive_transcript = chunk * 600
    expected_word_count = len(massive_transcript.split())
    assert expected_word_count >= 10000

    start_time = time.perf_counter()
    analytics = calculate_delivery_analytics(massive_transcript, duration_seconds=300.0)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    # Must complete within latency budget (< 100ms for 12,000 words)
    assert elapsed_ms < 100.0, f"Analytics took too long: {elapsed_ms:.2f}ms"
    assert analytics.word_count == expected_word_count
    assert analytics.duration_seconds == 300.0
    assert analytics.words_per_minute > 0.0
    assert analytics.filler_count > 1000
    assert 0.0 < analytics.filler_density_percentage <= 100.0


def test_tier5_delivery_analytics_multilingual_unicode_emojis() -> None:
    """Verify analytics processing on Arabic, Cyrillic, CJK, and emoji transcripts."""
    multilingual = (
        "مرحبا بك في المؤتمر 🚀 Привет мир! 💻 你好世界 🌟 "
        "We, you know, actually shipped the update! 👍 🎯 like sort of kind of"
    )
    analytics = calculate_delivery_analytics(multilingual, duration_seconds=15.0)

    assert analytics.word_count > 0
    assert analytics.duration_seconds == 15.0
    assert analytics.words_per_minute > 0.0
    # Expected fillers in text: "you know", "actually", "like", "sort of", "kind of"
    assert analytics.filler_count >= 5
    assert analytics.filler_words_breakdown["you know"] >= 1
    assert analytics.filler_words_breakdown["actually"] >= 1


def test_tier5_delivery_analytics_overlapping_and_inverted_timestamps() -> None:
    """Verify acoustic pause calculation under overlapping and inverted timestamps."""
    timestamps = [
        {"word": "first", "start": 0.0, "end": 0.5},
        {"word": "overlap", "start": 0.3, "end": 0.8},  # overlap
        {"word": "pause1", "start": 1.4, "end": 1.8},  # gap: 1.4 - 0.8 = 0.6s (standard pause)
        {
            "word": "powerpause",
            "start": 3.5,
            "end": 4.0,
        },  # gap: 3.5 - 1.8 = 1.7s (power pause >= 1.5s)
    ]
    analytics = calculate_delivery_analytics(
        transcript="first overlap pause1 powerpause",
        duration_seconds=5.0,
        word_timestamps=timestamps,
    )

    assert analytics.pause_count == 2
    assert analytics.power_pauses_count == 1


# ============================================================================
# Vector 4: Concurrency & Race Conditions in Session Persistence
# ============================================================================


async def test_tier5_concurrent_session_evaluations_load() -> None:
    """Verify thread-safety and session isolation under 20 concurrent evaluations."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        tasks = []
        for i in range(20):
            payload = {
                "framework": "STAR",
                "scenario_prompt": f"Concurrent test incident prompt #{i}",
                "transcript": (
                    f"During incident #{i}, I found a leak at "
                    "our service boundary. I rolled back and restored SLA in 8 min."
                ),
                "user_id": f"concurrent-user-{i % 4}",  # 4 distinct users
            }
            tasks.append(async_client.post("/api/v1/sessions/evaluate", json=payload))

        responses = await asyncio.gather(*tasks)

        assert len(responses) == 20
        session_ids = []
        for r in responses:
            assert r.status_code == 200, f"Evaluate failed with {r.status_code}: {r.text}"
            data = r.json()
            assert "session_id" in data
            assert data["score"] >= 0.0
            session_ids.append(data["session_id"])

        # All session IDs must be unique
        assert len(set(session_ids)) == 20, "Duplicate session IDs generated under concurrency"


async def test_tier5_concurrent_multi_user_isolation_and_pagination() -> None:
    """Verify user tenant isolation and cursor pagination under concurrent read/writes."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        user_alpha = "tenant-alpha"
        user_beta = "tenant-beta"

        # Concurrently create 6 sessions for Alpha and 6 for Beta
        eval_tasks = []
        for i in range(6):
            eval_tasks.append(
                async_client.post(
                    "/api/v1/sessions/evaluate",
                    json={
                        "framework": "PAR",
                        "scenario_prompt": f"Alpha prompt #{i}",
                        "transcript": "Resolved database deadlock promptly.",
                        "user_id": user_alpha,
                    },
                )
            )
            eval_tasks.append(
                async_client.post(
                    "/api/v1/sessions/evaluate",
                    json={
                        "framework": "PAR",
                        "scenario_prompt": f"Beta prompt #{i}",
                        "transcript": "Resolved networking loop promptly.",
                        "user_id": user_beta,
                    },
                )
            )

        await asyncio.gather(*eval_tasks)

        # Concurrently query Alpha and Beta history
        alpha_resp, beta_resp = await asyncio.gather(
            async_client.get(f"/api/v1/sessions?user_id={user_alpha}&limit=20"),
            async_client.get(f"/api/v1/sessions?user_id={user_beta}&limit=20"),
        )

        assert alpha_resp.status_code == 200
        assert beta_resp.status_code == 200

        alpha_items = alpha_resp.json()["items"]
        beta_items = beta_resp.json()["items"]

        assert len(alpha_items) == 6
        assert len(beta_items) == 6

        # Check tenant isolation
        for item in alpha_items:
            assert item["user_id"] == user_alpha
        for item in beta_items:
            assert item["user_id"] == user_beta

        # Test cursor pagination on Alpha
        page1_resp = await async_client.get(f"/api/v1/sessions?user_id={user_alpha}&limit=3")
        page1_data = page1_resp.json()
        assert len(page1_data["items"]) == 3
        cursor = page1_data["cursor"]
        assert cursor is not None

        page2_resp = await async_client.get(
            f"/api/v1/sessions?user_id={user_alpha}&limit=3&cursor={cursor}"
        )
        page2_data = page2_resp.json()
        assert len(page2_data["items"]) == 3

        # Disjoint pages
        page1_ids = {s["session_id"] for s in page1_data["items"]}
        page2_ids = {s["session_id"] for s in page2_data["items"]}
        assert page1_ids.isdisjoint(page2_ids)


# ============================================================================
# Vector 5: Adversarial Error Envelopes & Security Leakage Defense
# ============================================================================


def test_tier5_malformed_json_and_boundary_error_envelopes(client: TestClient) -> None:
    """Verify arbitrary malformed JSON and bad bodies produce standard 422 envelope."""
    # 1. Broken JSON syntax
    res1 = client.post(
        "/api/v1/sessions/evaluate",
        content=b'{"framework": "STAR", broken_syntax',
        headers={"Content-Type": "application/json"},
    )
    assert res1.status_code == 422
    data1 = res1.json()
    assert "error" in data1
    assert data1["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert data1["error"]["retryable"] is False
    assert "request_id" in data1

    # 2. Non-object JSON (list)
    res2 = client.post(
        "/api/v1/sessions/evaluate",
        content=b'["not", "a", "dict"]',
        headers={"Content-Type": "application/json"},
    )
    assert res2.status_code == 422
    data2 = res2.json()
    assert data2["error"]["code"] == ErrorCode.VALIDATION_ERROR.value

    # 3. Non-object JSON (int)
    res3 = client.post(
        "/api/v1/sessions/evaluate",
        content=b"12345",
        headers={"Content-Type": "application/json"},
    )
    assert res3.status_code == 422
    assert res3.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_tier5_injection_and_oversized_payload_handling(client: TestClient) -> None:
    """Verify SQL injection, XSS, and large strings are handled cleanly without server crash."""
    injection_payload = {
        "framework": "STAR",
        "scenario_prompt": "'; DROP TABLE sessions; -- <script>alert('xss')</script>",
        "transcript": (
            "SELECT * FROM users WHERE '1'='1'; " * 20
            + "I led the team and resolved the issue safely."
        ),
        "user_id": "test-injection-user",
    }
    response = client.post("/api/v1/sessions/evaluate", json=injection_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] is not None
    assert 0.0 <= data["score"] <= 100.0


def test_tier5_error_envelope_structure_and_no_unhandled_tracebacks(client: TestClient) -> None:
    """Verify non-existent endpoints and validation failures return standardized envelope."""
    # 404 Not Found
    res_404 = client.get("/api/v1/non_existent_endpoint")
    assert res_404.status_code == 404
    data_404 = res_404.json()
    assert "error" in data_404
    assert data_404["error"]["code"] == ErrorCode.NOT_FOUND.value
    assert data_404["error"]["retryable"] is False
    assert "request_id" in data_404

    # 422 Missing required query parameter
    res_query = client.get("/api/v1/sessions")
    assert res_query.status_code == 422
    data_query = res_query.json()
    assert data_query["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert data_query["error"]["retryable"] is False
    assert "request_id" in data_query
