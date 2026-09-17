"""Integration tests for the session evaluation endpoint."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.errors import ErrorCode
from app.gateways.dependencies import get_groq_gateway, get_jev_gateway
from app.main import app


@pytest.fixture(autouse=True)
def clean_overrides() -> Generator[None]:
    """Ensure clean dependency overrides for each test."""
    yield
    app.dependency_overrides.clear()


def test_evaluate_session_via_json_text(client: TestClient) -> None:
    """Verify evaluating a session via JSON body returns 200 with complete scorecard."""
    payload = {
        "framework": "STAR",
        "scenario_prompt": (
            "Tell me about a time you led an urgent technical intervention under high uncertainty."
        ),
        "scenario_context": "Production database failure during peak shopping traffic.",
        "speaker_role": "Staff Backend Engineer",
        "user_id": "user_test_json_1",
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
    assert len(data["session_id"]) > 0
    assert data["user_id"] == "user_test_json_1"
    assert data["framework"] == "STAR"
    assert 0.0 <= data["score"] <= 100.0

    # Subscores breakdown
    assert "subscores" in data
    assert len(data["subscores"]) > 0
    for subscore in data["subscores"]:
        assert "dimension" in subscore
        assert "score" in subscore
        assert "weight" in subscore

    # Findings from Jev
    assert "findings" in data
    assert isinstance(data["findings"], dict)
    assert "star_situation_grounding" in data["findings"]

    # Coaching tips and badges
    assert "tips" in data
    assert isinstance(data["tips"], list)
    assert "badges" in data
    assert isinstance(data["badges"], list)

    # Delivery metrics
    assert "delivery_metrics" in data
    metrics = data["delivery_metrics"]
    assert metrics["word_count"] > 0
    assert metrics["words_per_minute"] > 0.0
    assert metrics["duration_seconds"] == 45.0

    # Cross-cutting clarity assessment (separate from composite score)
    assert "clarity" in data and data["clarity"] is not None
    clarity = data["clarity"]
    assert 0.0 <= clarity["score"] <= 100.0
    assert clarity["level"] in {"exceptional", "clear", "adequate", "unclear", "incoherent"}
    assert clarity["clarity_level"] in {"Level 1", "Level 2", "Level 3", "Level 4", "Level 5"}
    assert clarity["ambiguity"] in {
        "unambiguous_and_precise",
        "minor_vagueness",
        "materially_ambiguous",
        "unable_to_assess",
    }
    assert isinstance(clarity["ambiguous"], bool)

    # Clarity is also reported as a subscore carrying zero composite weight.
    clarity_sub = next(s for s in data["subscores"] if s["dimension"] == "clarity")
    assert clarity_sub["weight"] == 0.0
    assert clarity_sub["score"] == clarity["score"]

    assert "filler_count" in metrics

    # Created at timestamp and envelope
    assert "created_at" in data
    assert "X-Request-ID" in response.headers or "x-request-id" in response.headers


def test_evaluate_session_flags_materially_ambiguous_answer(client: TestClient) -> None:
    """Verify a hedged, vague answer trips the material-ambiguity flag."""
    payload = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about a time you led an urgent technical intervention.",
        "transcript": (
            "So we did some things, and maybe it sort of worked out, "
            "and there was a lot of stuff going on, and yeah, etc."
        ),
        "duration_seconds": 20.0,
    }

    response = client.post("/api/v1/sessions/evaluate", json=payload)

    assert response.status_code == 200, response.text
    clarity = response.json()["clarity"]
    assert clarity["ambiguity"] == "materially_ambiguous"
    assert clarity["ambiguous"] is True
    assert clarity["score"] < 50.0
    assert clarity["level"] in {"unclear", "incoherent"}


def test_evaluate_session_via_multipart_audio_upload(client: TestClient) -> None:
    """Verify evaluating a session via multipart/form-data audio file upload."""
    audio_content = (
        b"At PaySync last November, I took full ownership of the PostgreSQL ledger migration. "
        b"When query timeouts occurred, I diagnosed lock contention in the checkout funnel, "
        b"isolated the offending table locks, and refactored the connection pooling. "
        b"This resolved the outage in fifteen minutes and stabilized transactional latency."
    )
    files = {"audio_file": ("answer.wav", audio_content, "audio/wav")}
    data = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about an urgent technical intervention.",
        "speaker_role": "Principal Engineer",
        "user_id": "user_test_audio_1",
    }

    response = client.post("/api/v1/sessions/evaluate", data=data, files=files)

    assert response.status_code == 200, response.text
    resp_data = response.json()

    assert "session_id" in resp_data
    assert resp_data["user_id"] == "user_test_audio_1"
    assert resp_data["framework"] == "STAR"
    assert 0.0 <= resp_data["score"] <= 100.0
    assert resp_data["delivery_metrics"]["word_count"] > 0
    assert resp_data["delivery_metrics"]["duration_seconds"] > 0.0


def test_evaluate_session_balanced_impact_rule_enforced(client: TestClient) -> None:
    """Verify Balanced Impact Rule: both qualitative and quantitative outcomes get full credit."""
    # Qualitative / Operational Outcome (Zero numbers or percentages)
    qualitative_payload = {
        "framework": "STAR",
        "scenario_prompt": "Describe a critical production incident and the resolution.",
        "user_id": "user_balanced_qual",
        "transcript": (
            "During a high-concurrency peak event, I took individual ownership of the degraded "
            "payment service. I diagnosed deadlock contention in the checkout database and "
            "refactored connection pooling. This completely resolved the outage, stabilized "
            "transactional latency, and unblocked payment processing for all customers."
        ),
        "duration_seconds": 60.0,
    }
    resp_qual = client.post("/api/v1/sessions/evaluate", json=qualitative_payload)
    assert resp_qual.status_code == 200
    data_qual = resp_qual.json()

    # Quantitative Outcome (Percentages, numbers)
    quantitative_payload = {
        "framework": "STAR",
        "scenario_prompt": "Describe a critical production incident and the resolution.",
        "user_id": "user_balanced_quant",
        "transcript": (
            "During a high-concurrency peak event, I took individual ownership of the degraded "
            "payment service. I diagnosed deadlock contention in the checkout database and "
            "refactored connection pooling. This reduced latency by 45 percent, saving 250ms "
            "per transaction across 5000 concurrent checkout requests."
        ),
        "duration_seconds": 60.0,
    }
    resp_quant = client.post("/api/v1/sessions/evaluate", json=quantitative_payload)
    assert resp_quant.status_code == 200
    data_quant = resp_quant.json()

    # Verify both achieved high scores under the Balanced Impact Rule
    assert (
        data_qual["findings"]["star_result_and_impact"]["choice"] == "meaningful_qualitative_impact"
    )
    assert data_quant["findings"]["star_result_and_impact"]["choice"] == "quantified_metric_impact"

    # Both must receive full credit (100.0 or equivalent top bracket) for Result
    qual_result_sub = next(s for s in data_qual["subscores"] if s["dimension"] == "result")
    quant_result_sub = next(s for s in data_quant["subscores"] if s["dimension"] == "result")

    assert qual_result_sub["score"] == 100.0
    assert quant_result_sub["score"] == 100.0


def test_evaluate_session_neither_audio_nor_text_returns_422(client: TestClient) -> None:
    """Verify 422 with VALIDATION_ERROR when neither audio nor text transcript is provided."""
    # 1. JSON without transcript
    payload_json = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about a challenging project.",
        "user_id": "user_empty_1",
    }
    response1 = client.post("/api/v1/sessions/evaluate", json=payload_json)
    assert response1.status_code == 422
    data1 = response1.json()
    assert data1["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "Neither audio nor text was provided" in data1["error"]["message"]

    # 2. JSON with empty/whitespace transcript
    payload_empty_str = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about a challenging project.",
        "transcript": "   \n\t   ",
        "user_id": "user_empty_2",
    }
    response2 = client.post("/api/v1/sessions/evaluate", json=payload_empty_str)
    assert response2.status_code == 422
    data2 = response2.json()
    assert data2["error"]["code"] == ErrorCode.VALIDATION_ERROR.value

    # 3. Multipart form without audio file and without transcript
    response3 = client.post(
        "/api/v1/sessions/evaluate",
        data={"framework": "STAR", "scenario_prompt": "Describe an outage."},
    )
    assert response3.status_code == 422
    data3 = response3.json()
    assert data3["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_evaluate_session_invalid_framework_returns_422_envelope(client: TestClient) -> None:
    """Verify invalid framework produces 422 VALIDATION_ERROR envelope in both JSON and form."""
    # 1. JSON
    payload_json = {
        "framework": "UNSUPPORTED_FRAMEWORK_XYZ",
        "scenario_prompt": "Valid prompt text.",
        "transcript": "Valid answer text.",
    }
    response1 = client.post("/api/v1/sessions/evaluate", json=payload_json)
    assert response1.status_code == 422
    data1 = response1.json()
    assert data1["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert data1["error"]["retryable"] is False

    # 2. Form/Multipart
    response2 = client.post(
        "/api/v1/sessions/evaluate",
        data={
            "framework": "FAKE_FRAMEWORK",
            "scenario_prompt": "Valid prompt text.",
            "transcript": "Valid answer text.",
        },
    )
    assert response2.status_code == 422
    data2 = response2.json()
    assert data2["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "Unsupported framework" in data2["error"]["message"]


def test_evaluate_session_missing_scenario_prompt_returns_422(client: TestClient) -> None:
    """Verify missing scenario_prompt returns 422 with VALIDATION_ERROR."""
    # JSON missing scenario_prompt
    response1 = client.post(
        "/api/v1/sessions/evaluate",
        json={"framework": "STAR", "transcript": "Some transcript"},
    )
    assert response1.status_code == 422
    assert response1.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value

    # Multipart missing scenario_prompt
    response2 = client.post(
        "/api/v1/sessions/evaluate",
        data={"framework": "STAR", "transcript": "Some transcript"},
    )
    assert response2.status_code == 422
    assert response2.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_evaluate_session_jev_gateway_failure_returns_503(client: TestClient) -> None:
    """Verify Jev System One gateway failure returns 503 TYPESAFE_UNAVAILABLE."""

    class FailingJevGateway:
        async def evaluate_questions(self, _state: object, _questions: object) -> object:
            raise RuntimeError("TypeSafe AI Jev System One network timeout.")

    app.dependency_overrides[get_jev_gateway] = lambda: FailingJevGateway()

    payload = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about a challenging incident.",
        "transcript": "I led the incident response and fixed the root cause.",
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)

    assert response.status_code == 503
    data = response.json()
    assert data["error"]["code"] == ErrorCode.TYPESAFE_UNAVAILABLE.value
    assert data["error"]["retryable"] is True
    assert (
        "TypeSafe AI Jev System One evaluation failed" in data["error"]["message"]
        or "TypeSafe AI Jev evaluation failed" in data["error"]["message"]
    )


def test_evaluate_session_groq_gateway_failure_returns_502(client: TestClient) -> None:
    """Verify Groq STT failure returns 502 GROQ_STT_FAILED."""

    class FailingGroqGateway:
        async def transcribe_audio(self, _bytes: bytes, _filename: str = "audio.wav") -> object:
            raise RuntimeError("Groq Whisper API returned 502 bad gateway.")

    app.dependency_overrides[get_groq_gateway] = lambda: FailingGroqGateway()

    files = {"audio_file": ("answer.wav", b"fake audio", "audio/wav")}
    data = {
        "framework": "CARL",
        "scenario_prompt": "Describe an architectural learning.",
    }
    response = client.post("/api/v1/sessions/evaluate", data=data, files=files)

    assert response.status_code == 502
    resp_data = response.json()
    assert resp_data["error"]["code"] == ErrorCode.GROQ_STT_FAILED.value
    assert resp_data["error"]["retryable"] is True
    assert "Groq speech-to-text transcription failed" in resp_data["error"]["message"]
