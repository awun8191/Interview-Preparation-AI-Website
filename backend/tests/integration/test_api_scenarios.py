"""Integration tests for the scenario generation endpoint."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.gateways.dependencies import get_gemini_gateway
from app.main import app
from app.models.scenario import FrameworkEnum


@pytest.fixture(autouse=True)
def clean_overrides() -> Generator[None]:
    """Ensure clean dependency overrides for each test."""
    yield
    app.dependency_overrides.clear()


def test_generate_scenario_happy_path(client: TestClient) -> None:
    """Verify POST /api/v1/scenarios/generate returns 200 with complete scenario payload."""
    payload = {
        "target_framework": "STAR",
        "user_domain": "Staff Backend Engineer",
        "difficulty_level": "intermediate",
        "focus_theme": "PostgreSQL Migration Outage",
    }
    response = client.post("/api/v1/scenarios/generate", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "scenario_id" in data
    assert data["scenario_id"].startswith("synthetic-")
    assert "title" in data
    assert "PostgreSQL Migration Outage" in data["title"]
    assert "context_background" in data
    assert "Staff Backend Engineer" in data["context_background"]
    assert "prompt_question" in data
    assert len(data["prompt_question"]) > 0
    assert "key_dimensions_to_test" in data
    assert isinstance(data["key_dimensions_to_test"], list)
    assert len(data["key_dimensions_to_test"]) > 0
    assert data["target_duration_seconds"] == 90
    assert data["target_framework"] == "STAR"
    assert data["difficulty_level"] == "intermediate"

    # Verify X-Request-ID propagation
    request_id = response.headers.get("X-Request-ID") or response.headers.get("x-request-id")
    assert request_id is not None
    assert len(request_id) > 0


def test_generate_scenario_all_11_frameworks(client: TestClient) -> None:
    """Verify scenario generation succeeds across all 11 communication methodologies."""
    for fw in FrameworkEnum:
        payload = {
            "target_framework": fw.value,
            "user_domain": "Director of Engineering",
            "difficulty_level": "advanced",
        }
        response = client.post("/api/v1/scenarios/generate", json=payload)
        assert response.status_code == 200, f"Failed for framework {fw.value}: {response.text}"
        data = response.json()
        assert data["target_framework"] == fw.value
        assert data["difficulty_level"] == "advanced"
        assert len(data["prompt_question"]) > 0


def test_generate_scenario_framework_alias_support(client: TestClient) -> None:
    """Verify 'framework' is accepted as an alias for 'target_framework'."""
    payload = {
        "framework": "CARL",
        "user_domain": "Engineering Manager",
    }
    response = client.post("/api/v1/scenarios/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_framework"] == "CARL"


def test_generate_scenario_invalid_framework_returns_422_envelope(client: TestClient) -> None:
    """Verify invalid framework produces 422 with standardized VALIDATION_ERROR envelope."""
    payload = {
        "target_framework": "INVALID_METHODOLOGY_123",
        "user_domain": "Staff Engineer",
    }
    response = client.post("/api/v1/scenarios/generate", json=payload)

    assert response.status_code == 422
    data = response.json()

    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["retryable"] is False
    assert "Request validation failed" in data["error"]["message"]
    assert "details" in data["error"]
    assert "request_id" in data
    assert len(data["request_id"]) > 0


def test_generate_scenario_missing_required_fields_returns_422(client: TestClient) -> None:
    """Verify missing required fields triggers 422 with VALIDATION_ERROR."""
    # 1. Missing user_domain
    response1 = client.post("/api/v1/scenarios/generate", json={"target_framework": "STAR"})
    assert response1.status_code == 422
    data1 = response1.json()
    assert data1["error"]["code"] == "VALIDATION_ERROR"
    assert any("user_domain" in str(err) for err in data1["error"]["details"])

    # 2. Missing target_framework
    response2 = client.post("/api/v1/scenarios/generate", json={"user_domain": "Backend Engineer"})
    assert response2.status_code == 422
    data2 = response2.json()
    assert data2["error"]["code"] == "VALIDATION_ERROR"

    # 3. Completely empty payload
    response3 = client.post("/api/v1/scenarios/generate", json={})
    assert response3.status_code == 422
    data3 = response3.json()
    assert data3["error"]["code"] == "VALIDATION_ERROR"


def test_generate_scenario_field_length_constraints(client: TestClient) -> None:
    """Verify user_domain min_length constraint produces 422."""
    payload = {
        "target_framework": "STAR",
        "user_domain": "x",  # min_length is 2
    }
    response = client.post("/api/v1/scenarios/generate", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_generate_scenario_gateway_failure_returns_503_error_envelope(
    client: TestClient,
) -> None:
    """Verify gateway exceptions are caught and returned as 503 PROVIDER_UNAVAILABLE."""

    class FailingGeminiGateway:
        async def generate_scenario(self, _request: object) -> object:
            raise RuntimeError("Upstream Gemini Flash service unavailable.")

    app.dependency_overrides[get_gemini_gateway] = lambda: FailingGeminiGateway()

    payload = {
        "target_framework": "STAR",
        "user_domain": "Lead Architect",
    }
    response = client.post("/api/v1/scenarios/generate", json=payload)

    assert response.status_code == 503
    data = response.json()

    assert "error" in data
    assert data["error"]["code"] == "PROVIDER_UNAVAILABLE"
    assert data["error"]["retryable"] is True
    assert "Upstream Gemini Flash service unavailable" in data["error"]["message"]
    assert "request_id" in data
    assert len(data["request_id"]) > 0
