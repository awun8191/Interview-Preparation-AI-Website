"""Integration tests for the health check endpoint."""

from fastapi.testclient import TestClient


def test_health_returns_200_and_healthy_status(client: TestClient) -> None:
    """Verify GET /api/v1/health returns 200, valid payload, and X-Request-ID header."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data
    assert "environment" in data
    assert "services" in data
    assert isinstance(data["services"], dict)

    # Verify X-Request-ID header is present
    assert "x-request-id" in response.headers or "X-Request-ID" in response.headers
    request_id = response.headers.get("X-Request-ID") or response.headers.get("x-request-id")
    assert request_id is not None
    assert len(request_id) > 0


def test_health_propagates_client_request_id(client: TestClient) -> None:
    """Verify that an incoming X-Request-ID is preserved and returned in headers."""
    custom_id = "test-req-trace-98765"
    response = client.get("/api/v1/health", headers={"X-Request-ID": custom_id})

    assert response.status_code == 200
    returned_id = response.headers.get("X-Request-ID") or response.headers.get("x-request-id")
    assert returned_id == custom_id
