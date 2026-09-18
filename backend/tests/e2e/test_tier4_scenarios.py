"""Tier 4 E2E Tests: Real-World Executive Coaching Scenarios.

Realistic high-stakes communication coaching workflows:
1. Staff Engineer STAR system redesign scenario.
2. VP Engineering CARL post-incident retro scenario.
3. Founder PAR rapid 45s pitch scenario.
4. Product Director SCQA executive board proposal scenario.
5. Manager SBI camera-recordable performance review scenario.
6. Difficult negotiation Gottman de-escalation scenario (verifying contempt collapse).
7. Hostage negotiation / vendor dispute Voss scenario (calibrated questions vs why trap).
"""

from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.gateways.dependencies import get_jev_gateway, get_synthetic_firestore
from app.main import app


@pytest.fixture(autouse=True)
def clean_isolation() -> Generator[None]:
    """Ensure clean repository state and clean dependency overrides per test."""
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()
    yield
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# 1. Staff Engineer STAR System Redesign Scenario
# ---------------------------------------------------------------------------


def test_tier4_scenario1_staff_engineer_star_system_redesign(client: TestClient) -> None:
    """Scenario 1: Staff Backend Engineer behavioral interview on urgent system redesign."""
    user_id = "staff_eng_star_scenario"
    prompt = (
        "Tell me about a time you led an urgent technical intervention or system redesign "
        "under high uncertainty. What specific actions did you take and what was the outcome?"
    )
    transcript = (
        "At PaySync last November, during our Black Friday peak, our PostgreSQL checkout ledger "
        "experienced cascading lock timeouts threatening 15000 customer checkouts. "
        "My challenge was to eliminate connection saturation without taking payments offline. "
        "I personally diagnosed the lock contention in the checkout funnel, isolated offending "
        "table locks, and refactored our connection pooling logic with a read-replica partition. "
        "This completely resolved the outage in fifteen minutes, stabilized transactional latency "
        "at 18ms, and unblocked checkout processing for all customers with zero dropped orders."
    )

    class StarJevGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "star_situation_grounding": {"choice": "well_grounded", "type": "choice"},
                "star_task_clarity": {"choice": "clearly_defined", "type": "choice"},
                "star_action_ownership_and_depth": {"level": "Level 5", "type": "score"},
                "star_result_and_impact": {
                    "choice": "meaningful_qualitative_impact",
                    "type": "choice",
                },
                "star_narrative_balance": {
                    "choice": "well_balanced_action_focus",
                    "type": "choice",
                },
                "star_prompt_relevance": {"choice": "directly_relevant", "type": "choice"},
            }

    app.dependency_overrides[get_jev_gateway] = lambda: StarJevGateway()

    payload = {
        "framework": "STAR",
        "scenario_prompt": prompt,
        "speaker_role": "Staff Backend Engineer",
        "user_id": user_id,
        "transcript": transcript,
        "duration_seconds": 78.0,
    }

    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "STAR"
    assert data["user_id"] == user_id

    # Verify Result dimension full credit under Balanced Impact Rule
    result_subscore = next(s for s in data["subscores"] if s["dimension"] == "result")
    assert result_subscore["score"] == 100.0

    # Verify Jev findings
    findings = data["findings"]
    assert findings["star_result_and_impact"]["choice"] == "meaningful_qualitative_impact"
    assert findings["star_situation_grounding"]["choice"] == "well_grounded"

    # Verify high composite score and badges
    assert data["score"] == 100.0
    badge_titles = [b["title"] for b in data["badges"]]
    assert "High-Impact Outcome" in badge_titles
    assert "Strong Agency & Leadership" in badge_titles

    # Verify session persisted and retrievable
    hist_resp = client.get(f"/api/v1/sessions?user_id={user_id}")
    assert hist_resp.status_code == 200
    assert hist_resp.json()["total"] == 1
    assert hist_resp.json()["items"][0]["session_id"] == data["session_id"]


# ---------------------------------------------------------------------------
# 2. VP Engineering CARL Post-Incident Retro Scenario
# ---------------------------------------------------------------------------


def test_tier4_scenario2_vp_engineering_carl_incident_retro(client: TestClient) -> None:
    """Scenario 2: VP of Engineering CARL retro verifying systemic safeguards & learning."""
    user_id = "vp_eng_carl_scenario"
    prompt = (
        "Describe a significant project failure or setback you experienced. What flawed "
        "assumptions did you uncover, and what permanent safeguards did you establish?"
    )
    transcript = (
        "Last quarter, I spearheaded our active-active multi-region cloud database cutover. "
        "During live traffic migration, cross-region replication lag caused data inconsistencies, "
        "forcing an immediate rollback. I personally took ownership of our flawed assumption. "
        "Rather than blaming the vendor, I paused the rollout and instituted automated canary "
        "gates and chaos engineering test suites across all staging environments. "
        "This eliminated migration regressions, and our rescheduled deployment completed with 100% "
        "data integrity across 3 regions."
    )

    class CarlJevGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "carl_context_framing": {"choice": "well_framed_context", "type": "choice"},
                "carl_action_ownership_and_rigor": {"level": "Level 5", "type": "score"},
                "carl_result_and_impact": {
                    "choice": "meaningful_qualitative_impact",
                    "type": "choice",
                },
                "carl_learning_metacognitive_depth": {"level": "Level 5", "type": "score"},
                "carl_narrative_balance": {"choice": "rich_learning_climax", "type": "choice"},
                "carl_vulnerability_and_humility": {
                    "choice": "authentic_humility_and_ownership",
                    "type": "choice",
                },
            }

    app.dependency_overrides[get_jev_gateway] = lambda: CarlJevGateway()

    payload = {
        "framework": "CARL",
        "scenario_prompt": prompt,
        "speaker_role": "VP of Engineering",
        "user_id": user_id,
        "transcript": transcript,
        "duration_seconds": 95.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "CARL"

    # Learning subscore must be 100.0
    learn_sub = next(s for s in data["subscores"] if s["dimension"] == "learning")
    assert learn_sub["score"] == 100.0

    # Badges awarded for high metacognition
    badge_titles = [b["title"] for b in data["badges"]]
    assert "Systemic Wisdom" in badge_titles
    assert "Defensive Blame Alert" not in badge_titles


# ---------------------------------------------------------------------------
# 3. Founder PAR Rapid 45s Pitch Scenario
# ---------------------------------------------------------------------------


def test_tier4_scenario3_founder_par_rapid_pitch(client: TestClient) -> None:
    """Scenario 3: Startup Founder delivering a crisp 45-second PAR bottleneck pitch."""
    user_id = "founder_par_scenario"
    prompt = "In 45 to 60 seconds, describe a high-stakes bottleneck, your action, and result."
    transcript = (
        "Enterprise compliance teams were blocking our AI deployment due to fear of leaks. "
        "I designed an on-premise confidential enclave with verifiable zero-knowledge proofs. "
        "This unlocked 8 Fortune 500 pilots, eliminated compliance objections, and secured 3.2M "
        "dollars in annual recurring revenue."
    )

    class ParJevGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "par_problem_sharpness": {"choice": "sharp_and_immediate", "type": "choice"},
                "par_action_decisiveness": {"level": "Level 5", "type": "score"},
                "par_result_and_impact": {"choice": "quantified_metric_impact", "type": "choice"},
                "par_brevity_and_information_density": {
                    "choice": "crisp_executive_brevity",
                    "type": "choice",
                },
                "par_prompt_relevance": {"choice": "directly_relevant", "type": "choice"},
            }

    app.dependency_overrides[get_jev_gateway] = lambda: ParJevGateway()

    # Audio upload representing spoken pitch
    files = {"audio_file": ("pitch.wav", transcript.encode("utf-8"), "audio/wav")}
    form = {
        "framework": "PAR",
        "scenario_prompt": prompt,
        "speaker_role": "Startup Founder & CEO",
        "user_id": user_id,
    }
    response = client.post("/api/v1/sessions/evaluate", data=form, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "PAR"
    assert data["score"] >= 90.0

    badge_titles = [b["title"] for b in data["badges"]]
    assert "Executive Brevity" in badge_titles


# ---------------------------------------------------------------------------
# 4. Product Director SCQA Executive Board Proposal Scenario
# ---------------------------------------------------------------------------


def test_tier4_scenario4_product_director_scqa_board_proposal(client: TestClient) -> None:
    """Scenario 4: Product Director pitching a platform re-architecture to the Board."""
    user_id = "pd_scqa_scenario"
    prompt = "Present your strategic recommendation using Barbara Minto's SCQA framework."
    transcript = (
        "Our digital banking customer base grew 180% over the past two quarters with high uptime. "
        "However, our legacy ledger cannot process batch settlements without freezing mobile apps. "
        "How can we scale batch settlement capacity tenfold before the holiday season? "
        "My recommendation is to transition transaction accounting to an event-streamed ledger on "
        "Apache Pulsar, decoupling batch settlement from queries and cutting latency by 80%."
    )

    class ScqaJevGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "scqa_situation_baseline": {
                    "choice": "uncontroversial_clear_baseline",
                    "type": "choice",
                },
                "scqa_complication_friction": {
                    "choice": "sharp_urgent_friction",
                    "type": "choice",
                },
                "scqa_governing_question": {
                    "choice": "explicitly_articulated",
                    "type": "choice",
                },
                "scqa_bluf_efficiency": {"level": "Level 5", "type": "score"},
                "scqa_recommendation_substance": {
                    "choice": "actionable_high_impact_solution",
                    "type": "choice",
                },
                "scqa_structural_flow": {
                    "choice": "textbook_minto_flow",
                    "type": "choice",
                },
            }

    app.dependency_overrides[get_jev_gateway] = lambda: ScqaJevGateway()

    payload = {
        "framework": "SCQA",
        "scenario_prompt": prompt,
        "speaker_role": "Director of Product Management",
        "user_id": user_id,
        "transcript": transcript,
        "duration_seconds": 65.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "SCQA"
    assert data["score"] == 100.0

    badge_titles = [b["title"] for b in data["badges"]]
    assert "Executive BLUF" in badge_titles


# ---------------------------------------------------------------------------
# 5. Manager SBI Camera-Recordable Performance Review Scenario
# ---------------------------------------------------------------------------


def test_tier4_scenario5_manager_sbi_camera_recordable_review(client: TestClient) -> None:
    """Scenario 5: Engineering Manager delivering camera-recordable feedback without sandwiching."""
    user_id = "mgr_sbi_scenario"
    prompt = "Deliver constructive feedback using Situation-Behavior-Impact: anchor in facts."
    transcript = (
        "During yesterday morning's 10am sprint review in room B, you interrupted Alex twice while "
        "they presented the diagram, stating 'that will never scale' before they finished. "
        "The impact was that Alex stopped speaking, junior engineers went silent, losing safety. "
        "I want to partner with you to establish ground rules where every engineer presents "
        "their diagram uninterrupted."
    )

    class SbiJevGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "sbi_situation_anchoring": {
                    "choice": "specifically_anchored_time_place",
                    "type": "choice",
                },
                "sbi_behavioral_camera_test": {"level": "Level 5", "type": "score"},
                "sbi_impact_operational_clarity": {
                    "choice": "clear_operational_or_relational_impact",
                    "type": "choice",
                },
                "sbi_feedback_sandwich_filter": {
                    "choice": "clean_direct_candor",
                    "type": "choice",
                },
                "sbi_solution_co_creation": {
                    "choice": "collaborative_co_creation",
                    "type": "choice",
                },
            }

    app.dependency_overrides[get_jev_gateway] = lambda: SbiJevGateway()

    payload = {
        "framework": "SBI",
        "scenario_prompt": prompt,
        "speaker_role": "Engineering Manager",
        "user_id": user_id,
        "transcript": transcript,
        "duration_seconds": 50.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "SBI"
    assert data["score"] == 100.0

    badge_titles = [b["title"] for b in data["badges"]]
    assert "Camera-Recordable Precision" in badge_titles
    assert "Co-Authored Solution" in badge_titles
    assert "Sandwich Detected" not in badge_titles


# ---------------------------------------------------------------------------
# 6. Difficult Negotiation Gottman De-escalation Scenario (Contempt Collapse)
# ---------------------------------------------------------------------------


def test_tier4_scenario6_gottman_deescalation_and_contempt_collapse(client: TestClient) -> None:
    """Scenario 6: Gottman de-escalation verifying 0.1x contempt collapse penalty."""
    user_id = "gottman_scenario_user"
    prompt = "De-escalate an aggressive cross-functional standoff using Gottman antidotes."

    # Part A: Masterful De-escalation (No Contempt)
    class GottmanCleanGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "gottman_four_horsemen_marker": {
                    "choice": "none_clean_de_escalated",
                    "type": "choice",
                },
                "gottman_soft_startup_presence": {"choice": "yes", "type": "noul", "yes": 1.0},
                "gottman_responsibility_acceptance": {"level": "Level 5", "type": "score"},
                "gottman_repair_attempt_usage": {
                    "choice": "active_repair_attempt_used",
                    "type": "choice",
                },
                "gottman_flooding_awareness_timeout": {
                    "choice": "structured_timeout_called",
                    "type": "choice",
                },
                "gottman_validation_of_counterpart": {"level": "Level 5", "type": "score"},
            }

    app.dependency_overrides[get_jev_gateway] = lambda: GottmanCleanGateway()

    clean_payload = {
        "framework": "GOTTMAN",
        "scenario_prompt": prompt,
        "speaker_role": "Conflict Mediator",
        "user_id": user_id,
        "transcript": (
            "I feel concerned about the stress between our teams and want to understand you. "
            "I acknowledge that I should have provided the API release notes earlier. "
            "I understand why your support team was so frustrated by customer escalations. "
            "Let us take a ten minute breath and reconvene to solve this together."
        ),
        "duration_seconds": 60.0,
    }
    resp_clean = client.post("/api/v1/sessions/evaluate", json=clean_payload)
    assert resp_clean.status_code == 200
    data_clean = resp_clean.json()
    assert data_clean["score"] == 100.0
    clean_badges = [b["title"] for b in data_clean["badges"]]
    assert "Masterful De-escalation" in clean_badges
    assert "Contempt Alert" not in clean_badges

    # Part B: Hostile Sarcasm / Contempt Collapse
    class GottmanContemptGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "gottman_four_horsemen_marker": {
                    "choice": "contempt_detected",
                    "type": "choice",
                },
                "gottman_soft_startup_presence": {"choice": "yes", "type": "noul", "yes": 1.0},
                "gottman_responsibility_acceptance": {"level": "Level 5", "type": "score"},
                "gottman_repair_attempt_usage": {
                    "choice": "active_repair_attempt_used",
                    "type": "choice",
                },
                "gottman_flooding_awareness_timeout": {
                    "choice": "structured_timeout_called",
                    "type": "choice",
                },
                "gottman_validation_of_counterpart": {"level": "Level 5", "type": "score"},
            }

    app.dependency_overrides[get_jev_gateway] = lambda: GottmanContemptGateway()

    contempt_payload = {
        "framework": "GOTTMAN",
        "scenario_prompt": prompt,
        "speaker_role": "Combatant Lead",
        "user_id": user_id,
        "transcript": (
            "It is hilarious that you think you can lecture our team on distributed systems; "
            "maybe read a book instead of wasting our engineering bandwidth with your incompetence."
        ),
        "duration_seconds": 25.0,
    }
    resp_contempt = client.post("/api/v1/sessions/evaluate", json=contempt_payload)
    assert resp_contempt.status_code == 200
    data_contempt = resp_contempt.json()

    # Severe multiplicative penalty (100 * 0.1 = 10.0)
    assert data_contempt["score"] == 10.0

    contempt_badges = [b["title"] for b in data_contempt["badges"]]
    assert "Contempt Alert" in contempt_badges

    # Verify actionable warning tip
    tips = data_contempt["tips"]
    assert any("Contempt is the #1 predictor" in t for t in tips)


# ---------------------------------------------------------------------------
# 7. Hostage Negotiation / Vendor Dispute Voss Scenario
# ---------------------------------------------------------------------------


def test_tier4_scenario7_voss_calibrated_questions_vs_why_trap(client: TestClient) -> None:
    """Scenario 7: Chris Voss tactical empathy negotiation vs accusatory 'why' trap."""
    user_id = "voss_scenario_user"
    prompt = "Negotiate with a cloud vendor demanding an abrupt 40% mid-contract rate increase."

    # Part A: Calibrated Questions & Tactical Empathy
    class VossCalibratedGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "voss_emotion_labeling": {"choice": "yes", "type": "noul", "yes": 1.0},
                "voss_calibrated_questions": {
                    "choice": "calibrated_how_what",
                    "type": "choice",
                },
                "voss_no_oriented_inquiry": {
                    "choice": "no_oriented_question_present",
                    "type": "choice",
                },
                "voss_vocal_tone_estimate": {
                    "choice": "late_night_dj_calm",
                    "type": "choice",
                },
                "voss_reciprocal_concession_framing": {"level": "Level 5", "type": "score"},
                "voss_mirroring_technique": {
                    "choice": "mirror_used_effectively",
                    "type": "choice",
                },
            }

    app.dependency_overrides[get_jev_gateway] = lambda: VossCalibratedGateway()

    calibrated_payload = {
        "framework": "VOSS",
        "scenario_prompt": prompt,
        "speaker_role": "Head of Strategic Sourcing",
        "user_id": user_id,
        "transcript": (
            "It seems like your executive team is facing stringent revenue targets this year. "
            "How am I supposed to justify an unbudgeted 40% price increase to our board? "
            "Would it be completely unreasonable to maintain our current terms for 90 days while "
            "we explore extending our commitment to a multi-year enterprise tier?"
        ),
        "duration_seconds": 65.0,
    }
    resp_calib = client.post("/api/v1/sessions/evaluate", json=calibrated_payload)
    assert resp_calib.status_code == 200
    data_calib = resp_calib.json()
    assert data_calib["score"] == 100.0

    calib_sub = next(s for s in data_calib["subscores"] if s["dimension"] == "calibrated_questions")
    assert calib_sub["score"] == 100.0

    badges_calib = [b["title"] for b in data_calib["badges"]]
    assert "Tactical Empathy Master" in badges_calib
    assert "Cognitive Burden Shift" in badges_calib
    assert "The 'Why' Trap" not in badges_calib

    # Part B: Accusatory 'Why' Trap
    class VossWhyGateway:
        async def evaluate_questions(self, state: Any, questions: dict[str, Any]) -> dict[str, Any]:
            return {
                "voss_emotion_labeling": {"choice": "yes", "type": "noul", "yes": 1.0},
                "voss_calibrated_questions": {
                    "choice": "accusatory_why",
                    "type": "choice",
                },
                "voss_no_oriented_inquiry": {
                    "choice": "no_oriented_question_present",
                    "type": "choice",
                },
                "voss_vocal_tone_estimate": {
                    "choice": "late_night_dj_calm",
                    "type": "choice",
                },
                "voss_reciprocal_concession_framing": {"level": "Level 5", "type": "score"},
                "voss_mirroring_technique": {
                    "choice": "mirror_used_effectively",
                    "type": "choice",
                },
            }

    app.dependency_overrides[get_jev_gateway] = lambda: VossWhyGateway()

    why_payload = {
        "framework": "VOSS",
        "scenario_prompt": prompt,
        "speaker_role": "Angry Buyer",
        "user_id": user_id,
        "transcript": "Why did you raise rates by 40%? Why are you trying to extort us?",
        "duration_seconds": 30.0,
    }
    resp_why = client.post("/api/v1/sessions/evaluate", json=why_payload)
    assert resp_why.status_code == 200
    data_why = resp_why.json()

    # Calibrated questions subscore drops from 100.0 to 10.0 (0.1 score)
    why_sub = next(s for s in data_why["subscores"] if s["dimension"] == "calibrated_questions")
    assert why_sub["score"] == 10.0

    badges_why = [b["title"] for b in data_why["badges"]]
    assert "The 'Why' Trap" in badges_why

    # Verify coaching tip points out the 'Why' question trigger
    tips_why = data_why["tips"]
    assert any("You asked a 'Why' question" in t or "Why did you raise" in t for t in tips_why)
