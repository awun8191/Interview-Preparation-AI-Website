"""Tier 1 E2E Tests: Happy-Path Opaque-Box Feature Verification.

Covers all core API endpoints in isolation under standard conditions:
- GET /api/v1/health
- POST /api/v1/scenarios/generate
- POST /api/v1/sessions/evaluate (JSON text payload)
- POST /api/v1/sessions/evaluate (multipart/form-data audio file upload)
- POST /api/v1/sessions/evaluate (multipart/form-data text-only form)
- GET /api/v1/sessions (user history retrieval & cursor pagination)
- Balanced Impact Rule full credit enforcement on endpoints
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.gateways.dependencies import get_synthetic_firestore
from app.main import app
from app.models.scenario import FrameworkEnum


@pytest.fixture(autouse=True)
def clean_isolation() -> Generator[None]:
    """Ensure repository and dependency overrides are cleanly isolated per test."""
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()
    yield
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()


def test_tier1_health_liveness(client: TestClient) -> None:
    """Verify GET /api/v1/health returns 200, healthy status, and dependency diagnostics."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data
    assert "environment" in data

    services = data.get("services", {})
    for expected_svc in ("gemini", "groq", "typesafe", "firestore"):
        assert expected_svc in services
        assert services[expected_svc] in ("healthy", "unconfigured")

    # Standard X-Request-ID header must be returned
    assert "X-Request-ID" in response.headers or "x-request-id" in response.headers


def test_tier1_health_request_id_tracing(client: TestClient) -> None:
    """Verify GET /api/v1/health echoes back a client-supplied X-Request-ID."""
    trace_id = "trace-tier1-opaque-box-12345"
    response = client.get("/api/v1/health", headers={"X-Request-ID": trace_id})
    assert response.status_code == 200
    returned_id = response.headers.get("X-Request-ID") or response.headers.get("x-request-id")
    assert returned_id == trace_id


def test_tier1_scenario_generate_star_happy_path(client: TestClient) -> None:
    """Verify POST /api/v1/scenarios/generate generates an authentic STAR prompt."""
    payload = {
        "target_framework": "STAR",
        "user_domain": "Principal Distributed Systems Architect",
        "difficulty_level": "intermediate",
        "focus_theme": "High-Concurrency Kafka Partition Outage",
    }
    response = client.post("/api/v1/scenarios/generate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["scenario_id"].startswith("synthetic-")
    assert "High-Concurrency Kafka Partition Outage" in data["title"]
    assert "Principal Distributed Systems Architect" in data["context_background"]
    assert len(data["prompt_question"]) > 10
    assert isinstance(data["key_dimensions_to_test"], list)
    assert len(data["key_dimensions_to_test"]) >= 3
    assert data["target_duration_seconds"] == 90
    assert data["target_framework"] == "STAR"
    assert data["difficulty_level"] == "intermediate"


def test_tier1_scenario_generate_all_11_frameworks(client: TestClient) -> None:
    """Verify POST /api/v1/scenarios/generate produces valid scenarios for all 11 frameworks."""
    for fw in FrameworkEnum:
        payload = {
            "target_framework": fw.value,
            "user_domain": "Engineering Leader",
            "difficulty_level": "advanced",
        }
        res = client.post("/api/v1/scenarios/generate", json=payload)
        assert res.status_code == 200, f"Failed for {fw.value}: {res.text}"
        data = res.json()
        assert data["target_framework"] == fw.value
        assert data["difficulty_level"] == "advanced"
        assert len(data["prompt_question"]) > 0
        assert data["target_duration_seconds"] > 0


def test_tier1_scenario_generate_difficulty_levels(client: TestClient) -> None:
    """Verify scenario generation accepts beginner, intermediate, and advanced levels."""
    for level in ("beginner", "intermediate", "advanced"):
        payload = {
            "target_framework": "CARL",
            "user_domain": "Software Architect",
            "difficulty_level": level,
        }
        res = client.post("/api/v1/scenarios/generate", json=payload)
        assert res.status_code == 200
        assert res.json()["difficulty_level"] == level


def test_tier1_evaluate_session_text_star(client: TestClient) -> None:
    """Verify POST /api/v1/sessions/evaluate evaluates JSON text under the STAR framework."""
    payload = {
        "framework": "STAR",
        "scenario_prompt": (
            "Tell me about a high-concurrency outage and your technical intervention."
        ),
        "scenario_context": "Black Friday transaction spikes caused database locks.",
        "speaker_role": "Staff Backend Engineer",
        "user_id": "tier1_user_star_1",
        "transcript": (
            "At PaySync last November, I took full ownership of the PostgreSQL ledger migration. "
            "When query timeouts occurred, I diagnosed lock contention in the checkout funnel, "
            "isolated the offending table locks, and refactored the connection pooling. "
            "This resolved the outage in fifteen minutes and stabilized transactional latency."
        ),
        "duration_seconds": 45.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert "session_id" in data
    assert data["user_id"] == "tier1_user_star_1"
    assert data["framework"] == "STAR"
    assert 0.0 <= data["score"] <= 100.0

    # Dimension subscores verification
    assert "subscores" in data
    assert len(data["subscores"]) >= 4
    dim_names = [s["dimension"] for s in data["subscores"]]
    for expected_dim in ("situation", "task", "action", "result"):
        assert expected_dim in dim_names

    # Jev findings verification
    findings = data["findings"]
    assert isinstance(findings, dict)
    assert "star_situation_grounding" in findings
    assert "star_action_ownership_and_depth" in findings
    assert "star_result_and_impact" in findings

    # Delivery metrics
    metrics = data["delivery_metrics"]
    assert metrics["word_count"] > 0
    assert metrics["duration_seconds"] == 45.0
    assert metrics["words_per_minute"] > 0.0


def test_tier1_evaluate_session_text_carl(client: TestClient) -> None:
    """Verify POST /api/v1/sessions/evaluate evaluates JSON text under the CARL framework."""
    payload = {
        "framework": "CARL",
        "scenario_prompt": "Describe a project failure and what systemic safeguards you built.",
        "speaker_role": "VP of Engineering",
        "user_id": "tier1_user_carl_1",
        "transcript": (
            "During our multi-region database migration, I led the cutover that encountered "
            "unexpected replication lag, causing us to roll back. I owned the faulty assumption "
            "and instituted automated canary testing and circuit breakers. This eliminated "
            "future migration regressions."
        ),
        "duration_seconds": 55.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "CARL"
    dim_names = [s["dimension"] for s in data["subscores"]]
    assert "learning" in dim_names
    assert "context" in dim_names
    assert "action" in dim_names
    assert "result" in dim_names


def test_tier1_evaluate_session_text_scqa(client: TestClient) -> None:
    """Verify POST /api/v1/sessions/evaluate evaluates JSON text under the SCQA framework."""
    payload = {
        "framework": "SCQA",
        "scenario_prompt": "Recommend an infrastructure modernization strategy using Minto BLUF.",
        "speaker_role": "Director of Product",
        "user_id": "tier1_user_scqa_1",
        "transcript": (
            "Our transaction volume grew 300% last quarter while maintaining 99.99% availability. "
            "However, our monolithic billing system cannot scale to handle holiday peak load. "
            "How can we prevent catastrophic payment timeouts without delaying product releases? "
            "My recommendation is to immediately decouple the payment worker into an isolated "
            "Go microservice with dedicated queue workers."
        ),
        "duration_seconds": 50.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "SCQA"
    dim_names = [s["dimension"] for s in data["subscores"]]
    for d in ("situation", "complication", "question", "bluf", "recommendation", "flow"):
        assert d in dim_names


def test_tier1_evaluate_session_audio_multipart_wav(client: TestClient) -> None:
    """Verify POST /api/v1/sessions/evaluate handles multipart WAV audio upload."""
    audio_content = b"RIFFfake_audio_wav_header_for_testing"
    files = {"audio_file": ("answer.wav", audio_content, "audio/wav")}
    form_data = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about an urgent production incident.",
        "speaker_role": "Lead Architect",
        "user_id": "tier1_user_audio_1",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form_data, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert "session_id" in data
    assert data["user_id"] == "tier1_user_audio_1"
    assert data["framework"] == "STAR"
    assert data["score"] >= 0.0
    assert data["delivery_metrics"]["duration_seconds"] > 0.0
    assert data["delivery_metrics"]["word_count"] > 0


def test_tier1_evaluate_session_audio_multipart_custom_transcript(client: TestClient) -> None:
    """Verify multipart audio file embedding custom text bytes produces accurate transcript."""
    custom_transcript = (
        "During our Black Friday deployment, I led the database failover and re-indexed the locks. "
        "This stabilized our transaction throughput and eliminated checkout timeouts."
    )
    files = {"audio_file": ("speech.wav", custom_transcript.encode("utf-8"), "audio/wav")}
    form_data = {
        "framework": "STAR",
        "scenario_prompt": "Describe how you resolved an operational incident.",
        "user_id": "tier1_user_audio_custom",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form_data, files=files)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["user_id"] == "tier1_user_audio_custom"
    assert data["delivery_metrics"]["word_count"] == len(custom_transcript.split())


def test_tier1_evaluate_session_multipart_form_text_only(client: TestClient) -> None:
    """Verify POST /api/v1/sessions/evaluate supports form-data without an audio file."""
    form_data = {
        "framework": "PAR",
        "scenario_prompt": "State the bottleneck and the result in under 60 seconds.",
        "transcript": (
            "The challenge was an unbounded query causing 30-second cart delays. "
            "I rewrote the query with composite indexing. "
            "This brought latency down to 12ms and saved 40 engineering hours."
        ),
        "duration_seconds": "48.5",
        "user_id": "tier1_form_text_user",
        "speaker_role": "Senior Engineer",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form_data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "PAR"
    assert data["delivery_metrics"]["duration_seconds"] == 48.5


def test_tier1_session_history_retrieval_and_persistence(client: TestClient) -> None:
    """Verify an evaluated session is persisted to Firestore and retrievable via GET /sessions."""
    user_id = "tier1_persist_user_1"
    prompt = "Tell me about a technical bottleneck you resolved."
    eval_resp = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "STAR",
            "scenario_prompt": prompt,
            "user_id": user_id,
            "transcript": "I diagnosed the issue and resolved the outage in ten minutes.",
        },
    )
    assert eval_resp.status_code == 200
    session_id = eval_resp.json()["session_id"]
    eval_score = eval_resp.json()["score"]

    # Retrieve history
    history_resp = client.get(f"/api/v1/sessions?user_id={user_id}")
    assert history_resp.status_code == 200
    hist_data = history_resp.json()

    assert hist_data["total"] == 1
    assert hist_data["cursor"] is None
    record = hist_data["items"][0]
    assert record["session_id"] == session_id
    assert record["user_id"] == user_id
    assert record["framework"] == "STAR"
    assert record["prompt"] == prompt
    assert record["score"] == eval_score


def test_tier1_session_history_pagination(client: TestClient) -> None:
    """Verify GET /api/v1/sessions pagination with limit and cursor traversal."""
    user_id = "tier1_pagination_user"

    # Create 3 sessions
    for i in range(3):
        res = client.post(
            "/api/v1/sessions/evaluate",
            json={
                "framework": "STAR",
                "scenario_prompt": f"Pagination Prompt {i}",
                "user_id": user_id,
                "transcript": f"I owned resolution step {i} and unblocked the system.",
            },
        )
        assert res.status_code == 200

    # Query Page 1: limit 2
    res_p1 = client.get(f"/api/v1/sessions?user_id={user_id}&limit=2")
    assert res_p1.status_code == 200
    data_p1 = res_p1.json()
    assert data_p1["total"] == 2
    assert data_p1["cursor"] is not None
    cursor = data_p1["cursor"]

    # Query Page 2: limit 2 with cursor
    res_p2 = client.get(f"/api/v1/sessions?user_id={user_id}&limit=2&cursor={cursor}")
    assert res_p2.status_code == 200
    data_p2 = res_p2.json()
    assert data_p2["total"] == 1
    assert data_p2["cursor"] is None


def test_tier1_balanced_impact_rule_qualitative_and_quantitative(client: TestClient) -> None:
    """Verify Balanced Impact Rule grants top score for both outcome types."""
    # 1. Pure Qualitative (zero numbers/metrics)
    qual_resp = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "STAR",
            "scenario_prompt": "Describe your incident resolution.",
            "user_id": "tier1_qual_user",
            "transcript": (
                "When the incident escalated, I took full ownership of the payment pipeline. "
                "I isolated the faulty connection pool and restructured our database locks. "
                "This completely resolved the outage, stabilized transactional latency, "
                "and unblocked all customer checkouts."
            ),
        },
    )
    assert qual_resp.status_code == 200
    data_qual = qual_resp.json()
    qual_sub = next(s for s in data_qual["subscores"] if s["dimension"] == "result")
    assert qual_sub["score"] == 100.0

    # 2. Quantitative (metrics and numbers)
    quant_resp = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "STAR",
            "scenario_prompt": "Describe your incident resolution.",
            "user_id": "tier1_quant_user",
            "transcript": (
                "When the incident escalated, I took full ownership of the payment pipeline. "
                "I isolated the faulty connection pool and restructured our database locks. "
                "This reduced p99 latency by 65 percent and recovered 500000 dollars in sales."
            ),
        },
    )
    assert quant_resp.status_code == 200
    data_quant = quant_resp.json()
    quant_sub = next(s for s in data_quant["subscores"] if s["dimension"] == "result")
    assert quant_sub["score"] == 100.0
