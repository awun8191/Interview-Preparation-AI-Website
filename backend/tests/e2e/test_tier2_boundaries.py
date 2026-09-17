"""Tier 2 E2E Tests: Boundary, Corner Cases, and Defensive Error Envelopes.

Covers input boundaries, negative limits, malformed payloads, and edge cases:
- Empty strings and whitespace-only payloads
- Missing required fields in JSON and multipart forms
- Invalid framework names
- Unmapped/exotic speaker roles
- Zero and negative audio/text durations
- Extreme transcript lengths (1000+ words) and minimal transcripts (single word)
- Query limit boundaries (<= 0, > 100)
- Missing required query parameters
- Invalid pagination cursors
- Scenario generation domain length and difficulty level bounds
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.errors import ErrorCode
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


def test_tier2_evaluate_empty_transcript_json(client: TestClient) -> None:
    """Verify empty string transcript in JSON returns 422 VALIDATION_ERROR envelope."""
    payload = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about a high-stakes challenge.",
        "transcript": "",
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert data["error"]["retryable"] is False
    assert "Neither audio nor text was provided" in data["error"]["message"]
    assert "request_id" in data


def test_tier2_evaluate_whitespace_transcript_json(client: TestClient) -> None:
    """Verify whitespace-only transcript in JSON returns 422 VALIDATION_ERROR envelope."""
    payload = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about a high-stakes challenge.",
        "transcript": "   \n\t   ",
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "Neither audio nor text was provided" in data["error"]["message"]


def test_tier2_evaluate_empty_prompt_json(client: TestClient) -> None:
    """Verify empty scenario_prompt in JSON returns 422 VALIDATION_ERROR envelope."""
    payload = {
        "framework": "STAR",
        "scenario_prompt": "   ",
        "transcript": "I diagnosed the issue and resolved it.",
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    err_msg = data["error"]["message"].lower()
    assert "scenario_prompt" in err_msg or "validation" in err_msg


def test_tier2_evaluate_missing_framework_json(client: TestClient) -> None:
    """Verify missing framework in JSON returns 422 VALIDATION_ERROR envelope."""
    payload = {
        "scenario_prompt": "Tell me about an outage.",
        "transcript": "I diagnosed the issue and fixed the service.",
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_tier2_evaluate_missing_prompt_json(client: TestClient) -> None:
    """Verify missing scenario_prompt in JSON returns 422 VALIDATION_ERROR envelope."""
    payload = {
        "framework": "STAR",
        "transcript": "I resolved the issue.",
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_tier2_evaluate_invalid_framework_name_json(client: TestClient) -> None:
    """Verify invalid framework name in JSON returns 422 VALIDATION_ERROR envelope."""
    payload = {
        "framework": "INVALID_FRAMEWORK_NAME_999",
        "scenario_prompt": "Tell me about an outage.",
        "transcript": "I solved the issue.",
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert data["error"]["retryable"] is False


def test_tier2_evaluate_invalid_framework_name_multipart(client: TestClient) -> None:
    """Verify invalid framework name in multipart form returns 422 VALIDATION_ERROR."""
    form_data = {
        "framework": "NON_EXISTENT_METHODOLOGY",
        "scenario_prompt": "Tell me about an outage.",
        "transcript": "I solved the issue.",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form_data)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "Unsupported framework" in data["error"]["message"]


def test_tier2_evaluate_missing_audio_and_transcript_multipart(client: TestClient) -> None:
    """Verify multipart form with neither audio file nor transcript returns 422."""
    form_data = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about an outage.",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form_data)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "Neither audio nor text was provided" in data["error"]["message"]


def test_tier2_evaluate_empty_prompt_multipart(client: TestClient) -> None:
    """Verify multipart form with empty scenario_prompt returns 422."""
    form_data = {
        "framework": "STAR",
        "scenario_prompt": "    ",
        "transcript": "I solved the incident.",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form_data)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "scenario_prompt" in data["error"]["message"]


def test_tier2_evaluate_empty_audio_bytes_without_transcript_multipart(client: TestClient) -> None:
    """Verify empty audio file upload with zero bytes and no transcript returns 422."""
    files = {"audio_file": ("empty.wav", b"", "audio/wav")}
    form_data = {
        "framework": "STAR",
        "scenario_prompt": "Tell me about an outage.",
    }
    response = client.post("/api/v1/sessions/evaluate", data=form_data, files=files)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "Neither audio nor text was provided" in data["error"]["message"]


def test_tier2_evaluate_unmapped_exotic_speaker_role(client: TestClient) -> None:
    """Verify unmapped/exotic speaker roles are accepted gracefully without 500 error."""
    exotic_role = "Quantum Cryogenic Systems Lead & Deep-Sea Salvage Director"
    payload = {
        "framework": "STAR",
        "scenario_prompt": "Explain your resolution of an operational failure.",
        "speaker_role": exotic_role,
        "transcript": (
            "At the laboratory, I owned the cooling pump repair and stabilized temperatures."
        ),
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["framework"] == "STAR"
    assert data["score"] >= 0.0


def test_tier2_evaluate_zero_and_negative_duration(client: TestClient) -> None:
    """Verify duration_seconds=0.0 and negative durations are clamped without division errors."""
    # Zero duration
    resp_zero = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "PAR",
            "scenario_prompt": "Briefly state the problem and result.",
            "transcript": "The cache was failing. I added backoff. Latency recovered.",
            "duration_seconds": 0.0,
        },
    )
    assert resp_zero.status_code == 200
    assert resp_zero.json()["delivery_metrics"]["duration_seconds"] == 0.0

    # Negative duration in form data
    resp_neg = client.post(
        "/api/v1/sessions/evaluate",
        data={
            "framework": "PAR",
            "scenario_prompt": "Briefly state the problem and result.",
            "transcript": "The cache was failing. I added backoff. Latency recovered.",
            "duration_seconds": "-25.5",
        },
    )
    assert resp_neg.status_code == 200
    assert resp_neg.json()["delivery_metrics"]["duration_seconds"] == 0.0


def test_tier2_evaluate_extreme_length_transcript_1200_words(client: TestClient) -> None:
    """Verify extreme length transcript (1200 words) evaluates without crashing."""
    base_sentence = (
        "I analyzed distributed database trace, isolated lock contention, and deployed an index. "
    )
    # 12 words per repetition; 100 repetitions = 1200 words
    long_transcript = (
        "During our high-concurrency event, " + (base_sentence * 99) + "This resolved the outage."
    )
    word_count = len(long_transcript.split())
    assert word_count > 1000

    payload = {
        "framework": "STAR",
        "scenario_prompt": "Explain an architectural intervention under load.",
        "transcript": long_transcript,
        "duration_seconds": 480.0,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["delivery_metrics"]["word_count"] == word_count
    assert data["score"] >= 0.0


def test_tier2_evaluate_single_word_transcript(client: TestClient) -> None:
    """Verify single-word transcript evaluates gracefully without index or zero-length errors."""
    payload = {
        "framework": "STAR",
        "scenario_prompt": "Did you resolve the outage?",
        "transcript": "Resolved.",
        "duration_seconds": 1.5,
    }
    response = client.post("/api/v1/sessions/evaluate", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["delivery_metrics"]["word_count"] == 1
    assert data["score"] >= 0.0


def test_tier2_get_sessions_negative_or_zero_limit(client: TestClient) -> None:
    """Verify limit <= 0 returns 422 VALIDATION_ERROR envelope."""
    # limit = 0
    resp_zero = client.get("/api/v1/sessions?user_id=test_user&limit=0")
    assert resp_zero.status_code == 422
    assert resp_zero.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value

    # limit = -10
    resp_neg = client.get("/api/v1/sessions?user_id=test_user&limit=-10")
    assert resp_neg.status_code == 422
    assert resp_neg.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_tier2_get_sessions_excessive_limit_over_100(client: TestClient) -> None:
    """Verify limit > 100 returns 422 VALIDATION_ERROR envelope."""
    resp_over = client.get("/api/v1/sessions?user_id=test_user&limit=101")
    assert resp_over.status_code == 422
    assert resp_over.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_tier2_get_sessions_missing_user_id(client: TestClient) -> None:
    """Verify GET /sessions with missing user_id returns 422 VALIDATION_ERROR envelope."""
    response = client.get("/api/v1/sessions")
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert "request_id" in data


def test_tier2_get_sessions_invalid_nonexistent_cursor(client: TestClient) -> None:
    """Verify query with a nonexistent cursor returns empty list gracefully without 500 error."""
    response = client.get("/api/v1/sessions?user_id=user_with_no_sessions&cursor=fake_cursor_xyz")
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
    assert data["cursor"] is None


def test_tier2_scenario_generate_domain_length_boundaries(client: TestClient) -> None:
    """Verify user_domain min_length=2 boundary: len=1 returns 422, len=2 returns 200."""
    # len = 1 (below min_length 2)
    resp_short = client.post(
        "/api/v1/scenarios/generate",
        json={"target_framework": "STAR", "user_domain": "x"},
    )
    assert resp_short.status_code == 422
    assert resp_short.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value

    # len = 2 (valid boundary)
    resp_valid = client.post(
        "/api/v1/scenarios/generate",
        json={"target_framework": "STAR", "user_domain": "ML"},
    )
    assert resp_valid.status_code == 200
    assert "ML" in resp_valid.json()["context_background"]


def test_tier2_scenario_generate_invalid_difficulty(client: TestClient) -> None:
    """Verify invalid difficulty level produces 422 VALIDATION_ERROR envelope."""
    payload = {
        "target_framework": "STAR",
        "user_domain": "Infrastructure Engineer",
        "difficulty_level": "impossible_super_master",
    }
    response = client.post("/api/v1/scenarios/generate", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
