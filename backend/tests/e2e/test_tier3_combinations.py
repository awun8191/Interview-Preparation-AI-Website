"""Tier 3 E2E Tests: Cross-Feature Pairwise Combinations & Balanced Impact Rule.

Systematically verifies combinations across:
- All 11 Communication Frameworks
- Input Modalities: Text JSON vs Audio Multipart Upload vs Form Data
- Speaker Roles: Staff Engineer, VP Engineering, Founder, Product Director, etc.
- Outcome Types: Qualitative Operational Impact vs Quantitative Metrics
- Enforcing the Balanced Impact Rule across combinations
- Cross-user and cross-framework isolation
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.gateways.dependencies import get_synthetic_firestore
from app.main import app


@pytest.fixture(autouse=True)
def clean_isolation() -> Generator[None]:
    """Ensure repository and dependency overrides are cleanly isolated per test."""
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()
    yield
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# 1. Pairwise Combinations: Framework x Modality x Role x Outcome
# ---------------------------------------------------------------------------


def test_tier3_pairwise_star_audio_qualitative_staff_engineer(client: TestClient) -> None:
    """Combination: STAR + Audio Multipart + Staff Engineer + Qualitative Outcome."""
    transcript = (
        "At PaySync last November, I took full ownership of the PostgreSQL ledger migration. "
        "When query timeouts occurred, I diagnosed lock contention in the checkout funnel, "
        "isolated the offending table locks, and refactored the connection pooling. "
        "This completely resolved the outage, stabilized transactional latency, and unblocked "
        "checkout for all customers."
    )
    files = {"audio_file": ("answer.wav", transcript.encode("utf-8"), "audio/wav")}
    form = {
        "framework": "STAR",
        "scenario_prompt": "Describe how you resolved an urgent production incident.",
        "speaker_role": "Staff Backend Engineer",
        "user_id": "tier3_user_star_audio",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "STAR"
    assert data["user_id"] == "tier3_user_star_audio"
    res_sub = next(s for s in data["subscores"] if s["dimension"] == "result")
    assert res_sub["score"] == 100.0


def test_tier3_pairwise_carl_text_quantitative_vp_engineering(client: TestClient) -> None:
    """Combination: CARL + Text JSON + VP of Engineering + Quantitative Outcome."""
    payload = {
        "framework": "CARL",
        "scenario_prompt": "Describe an architectural setback and the systemic safeguard created.",
        "speaker_role": "VP of Engineering",
        "user_id": "tier3_user_carl_text",
        "transcript": (
            "During our multi-region cutover, I led the deployment that failed due to cross-region "
            "replication lag. I owned the flawed assumption, paused the migration, and instituted "
            "automated canary testing. This reduced rollout failure rate by 85 percent and saved "
            "400000 dollars in emergency failover overhead."
        ),
        "duration_seconds": 65.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "CARL"
    res_sub = next(s for s in data["subscores"] if s["dimension"] == "result")
    assert res_sub["score"] == 100.0
    learn_sub = next(s for s in data["subscores"] if s["dimension"] == "learning")
    assert 0.0 <= learn_sub["score"] <= 100.0


def test_tier3_pairwise_par_audio_qualitative_founder(client: TestClient) -> None:
    """Combination: PAR + Audio Multipart + Startup Founder + Qualitative Outcome."""
    transcript = (
        "The problem was a 70% customer drop-off at onboarding due to confusing API keys. "
        "I personally redesigned the authentication flow to use single-click OAuth. "
        "This completely eliminated user confusion, restored adoption momentum, and delighted "
        "our enterprise design partners."
    )
    files = {"audio_file": ("pitch.wav", transcript.encode("utf-8"), "audio/wav")}
    form = {
        "framework": "PAR",
        "scenario_prompt": "Deliver a 45-second summary of a solved bottleneck.",
        "speaker_role": "Startup Founder",
        "user_id": "tier3_user_par_audio",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "PAR"
    res_sub = next(s for s in data["subscores"] if s["dimension"] == "result")
    assert res_sub["score"] == 100.0


def test_tier3_pairwise_scqa_text_quantitative_product_director(client: TestClient) -> None:
    """Combination: SCQA + Text JSON + Director of Product + Quantitative Outcome."""
    payload = {
        "framework": "SCQA",
        "scenario_prompt": "Present an infrastructure recommendation to the board.",
        "speaker_role": "Director of Product",
        "user_id": "tier3_user_scqa_text",
        "transcript": (
            "Enterprise customers have grown 200% year-over-year. "
            "However, legacy billing sync limits us to 50 concurrent tenant provisioning jobs. "
            "How do we scale to 1000 tenants without hiring 20 operators? "
            "My recommendation is to deploy event-driven provisioning via Kafka, which reduces "
            "provisioning latency by 90 percent and saves 1.5 million dollars annually."
        ),
        "duration_seconds": 60.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "SCQA"
    rec_sub = next(s for s in data["subscores"] if s["dimension"] == "recommendation")
    assert rec_sub["score"] == 100.0


def test_tier3_pairwise_sbi_audio_qualitative_people_manager(client: TestClient) -> None:
    """Combination: SBI + Audio Multipart + Engineering Manager + Qualitative Outcome."""
    transcript = (
        "During yesterday morning's architecture sprint review at 10am, you interrupted the "
        "presenter three times and stated 'that will never scale' before seeing the diagrams. "
        "The impact was that junior engineers stopped participating and psychological safety "
        "dropped across the squad. I want to partner on establishing a meeting protocol where "
        "everyone presents uninterrupted."
    )
    files = {"audio_file": ("feedback.wav", transcript.encode("utf-8"), "audio/wav")}
    form = {
        "framework": "SBI",
        "scenario_prompt": "Deliver constructive camera-recordable feedback to a peer.",
        "speaker_role": "Engineering Manager",
        "user_id": "tier3_user_sbi_audio",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "SBI"
    assert data["score"] >= 0.0


def test_tier3_pairwise_radical_candor_text_qualitative_team_lead(client: TestClient) -> None:
    """Combination: Radical Candor + Text JSON + Tech Lead + Qualitative Outcome."""
    payload = {
        "framework": "RADICAL_CANDOR",
        "scenario_prompt": "Address declining sprint delivery with empathy and standards.",
        "speaker_role": "Tech Lead",
        "user_id": "tier3_user_rc_text",
        "transcript": (
            "I deeply respect your architectural insight and care about your career trajectory. "
            "However, your last three PRs missed our unit testing standards and introduced "
            "production regressions. I need you to personally author regression tests before "
            "merging, and I am committed to pairing with you to get them over the line."
        ),
        "duration_seconds": 50.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "RADICAL_CANDOR"
    assert data["score"] >= 0.0


def test_tier3_pairwise_state_audio_quantitative_architect(client: TestClient) -> None:
    """Combination: STATE + Audio Multipart + Principal Security Architect + Quantitative."""
    transcript = (
        "The production audit logs show 42 unauthorized schema export attempts last Tuesday. "
        "The story I am telling myself is that our database tokens may be over-permissioned. "
        "How do you see the access configuration? Perhaps we can inspect the role bindings "
        "together to verify if 2.4 million user records are properly segmented."
    )
    files = {"audio_file": ("crucial.wav", transcript.encode("utf-8"), "audio/wav")}
    form = {
        "framework": "STATE",
        "scenario_prompt": "Initiate a crucial conversation regarding security compliance.",
        "speaker_role": "Principal Security Architect",
        "user_id": "tier3_user_state_audio",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "STATE"
    assert data["score"] >= 0.0


def test_tier3_pairwise_gottman_text_qualitative_mediator(client: TestClient) -> None:
    """Combination: Gottman + Text JSON + Conflict Mediator + Qualitative Outcome."""
    payload = {
        "framework": "GOTTMAN",
        "scenario_prompt": "De-escalate a cross-team dispute using Gottman antidotes.",
        "speaker_role": "Lead Mediator",
        "user_id": "tier3_user_gottman_text",
        "transcript": (
            "I feel concerned about the tension between our platforms and want to find common "
            "ground. I realize that I should have shared our deployment schedule earlier in the "
            "week. I understand how frustrating it was for your team to handle customer tickets. "
            "Let us pause for ten minutes, take a breath, and reconvene to align our roadmaps."
        ),
        "duration_seconds": 60.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "GOTTMAN"
    assert data["score"] >= 0.0


def test_tier3_pairwise_voss_audio_quantitative_procurement(client: TestClient) -> None:
    """Combination: Voss + Audio Multipart + Procurement Negotiator + Quantitative."""
    transcript = (
        "It seems like your corporate leadership is applying heavy pressure to hit revenue quotas. "
        "How am I supposed to absorb a 40% hike when our departmental budget is locked? "
        "Would it be completely unreasonable to maintain our current 500000 dollar contract for "
        "another six months while we benchmark usage?"
    )
    files = {"audio_file": ("voss.wav", transcript.encode("utf-8"), "audio/wav")}
    form = {
        "framework": "VOSS",
        "scenario_prompt": "Negotiate with a vendor demanding a mid-contract price hike.",
        "speaker_role": "Procurement Director",
        "user_id": "tier3_user_voss_audio",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "VOSS"
    assert data["score"] >= 0.0


def test_tier3_pairwise_sparkline_text_qualitative_cto(client: TestClient) -> None:
    """Combination: Sparkline + Text JSON + CTO + Qualitative Contrast."""
    payload = {
        "framework": "SPARKLINE",
        "scenario_prompt": "Pitch organizational adoption of modern AI-driven development.",
        "speaker_role": "Chief Technology Officer",
        "user_id": "tier3_user_sparkline_text",
        "transcript": (
            "Today, our engineers spend 60% of their time resolving merge conflicts and writing "
            "boilerplate mocks. But imagine a future where our developers test ideas in minutes "
            "with zero cognitive friction. Today we struggle with slow releases; tomorrow we can "
            "empower every engineer to ship autonomously. Join me in embarking on this adventure."
        ),
        "duration_seconds": 75.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "SPARKLINE"
    assert data["score"] >= 0.0


def test_tier3_pairwise_monroe_audio_quantitative_cro(client: TestClient) -> None:
    """Combination: Monroe + Audio Multipart + Chief Revenue Officer + Quantitative."""
    transcript = (
        "Every single day our sales team loses 12 qualified leads because of checkout drop-off. "
        "We need an integrated checkout flow immediately. Our engineering team has completed "
        "the Stripe migration plan. If we deploy it next week, we will capture 2.4 million dollars "
        "in additional revenue this quarter. Authorize the deployment ticket today."
    )
    files = {"audio_file": ("monroe.wav", transcript.encode("utf-8"), "audio/wav")}
    form = {
        "framework": "MONROE",
        "scenario_prompt": "Deliver an executive proposal using Monroe Motivated Sequence.",
        "speaker_role": "Chief Revenue Officer",
        "user_id": "tier3_user_monroe_audio",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "MONROE"
    assert data["score"] >= 0.0


# ---------------------------------------------------------------------------
# 2. Balanced Impact Rule Across Combinations Matrix
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("framework", ["STAR", "CARL", "PAR"])
def test_tier3_balanced_impact_rule_matrix(client: TestClient, framework: str) -> None:
    """Verify Balanced Impact Rule awards 100.0 result subscore across all outcome frameworks."""
    # 1. Pure Qualitative Transcript
    qual_resp = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": framework,
            "scenario_prompt": f"Describe a high-stakes {framework} operational scenario.",
            "transcript": (
                "When the distributed system failed, I took ownership of the incident response. "
                "I diagnosed the lock contention and refactored the connection pool. "
                "This completely resolved the outage, stabilized transactional latency, "
                "and unblocked payment processing for all customers."
            ),
        },
    )
    assert qual_resp.status_code == 200
    res_sub_qual = next(s for s in qual_resp.json()["subscores"] if s["dimension"] == "result")
    assert res_sub_qual["score"] == 100.0

    # 2. Pure Quantitative Transcript
    quant_resp = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": framework,
            "scenario_prompt": f"Describe a high-stakes {framework} operational scenario.",
            "transcript": (
                "When the distributed system failed, I took ownership of the incident response. "
                "I diagnosed the lock contention and refactored the connection pool. "
                "This reduced p99 latency by 55 percent, saving 250ms per transaction "
                "across 10000 concurrent checkout requests."
            ),
        },
    )
    assert quant_resp.status_code == 200
    res_sub_quant = next(s for s in quant_resp.json()["subscores"] if s["dimension"] == "result")
    assert res_sub_quant["score"] == 100.0


def test_tier3_all_11_frameworks_subscore_weight_conservation(client: TestClient) -> None:
    """Verify all 11 frameworks return subscores whose weights conserve to 1.0."""
    from app.models.scenario import FrameworkEnum

    for fw in FrameworkEnum:
        resp = client.post(
            "/api/v1/sessions/evaluate",
            json={
                "framework": fw.value,
                "scenario_prompt": f"Practice prompt for {fw.value}.",
                "transcript": (
                    "I led the intervention, solved the bottleneck, and stabilized operations."
                ),
            },
        )
        assert resp.status_code == 200, f"Failed for framework {fw.value}: {resp.text}"
        data = resp.json()
        subscores = data["subscores"]
        assert len(subscores) > 0

        total_weight = sum(s["weight"] for s in subscores)
        assert pytest.approx(total_weight, abs=0.01) == 1.0, (
            f"Weights did not sum to 1.0 for framework {fw.value}: {total_weight}"
        )

        for sub in subscores:
            assert 0.0 <= sub["score"] <= 100.0
            # The auxiliary clarity dimension is reported with zero composite weight.
            if sub["dimension"] == "clarity":
                assert sub["weight"] == 0.0
            else:
                assert sub["weight"] > 0.0


def test_tier3_cross_feature_multi_user_modality_isolation(client: TestClient) -> None:
    """Verify multi-user concurrent sessions across modalities do not leak across users."""
    user_audio = "user_modality_audio"
    user_json = "user_modality_json"

    # User 1: Audio upload (STAR)
    files = {"audio_file": ("answer.wav", b"Audio recording bytes for STAR answer", "audio/wav")}
    client.post(
        "/api/v1/sessions/evaluate",
        data={"framework": "STAR", "scenario_prompt": "Audio prompt", "user_id": user_audio},
        files=files,
    )

    # User 2: JSON body (CARL)
    client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "CARL",
            "scenario_prompt": "JSON prompt",
            "user_id": user_json,
            "transcript": "I owned the failure and built systemic safeguards.",
        },
    )

    # Query User 1
    resp1 = client.get(f"/api/v1/sessions?user_id={user_audio}")
    assert resp1.status_code == 200
    d1 = resp1.json()
    assert d1["total"] == 1
    assert d1["items"][0]["user_id"] == user_audio
    assert d1["items"][0]["framework"] == "STAR"

    # Query User 2
    resp2 = client.get(f"/api/v1/sessions?user_id={user_json}")
    assert resp2.status_code == 200
    d2 = resp2.json()
    assert d2["total"] == 1
    assert d2["items"][0]["user_id"] == user_json
    assert d2["items"][0]["framework"] == "CARL"
