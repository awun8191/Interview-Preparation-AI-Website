"""Integration tests for Firestore session persistence and history retrieval."""

import time
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.errors import ErrorCode
from app.gateways.dependencies import get_firestore_gateway, get_synthetic_firestore
from app.main import app


@pytest.fixture(autouse=True)
def clean_state() -> Generator[None]:
    """Reset in-memory Firestore repository and dependency overrides for test isolation."""
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()
    yield
    get_synthetic_firestore().clear()
    app.dependency_overrides.clear()


def test_evaluate_session_persists_to_firestore_and_is_retrievable(client: TestClient) -> None:
    """Verify that POST /evaluate saves the session and GET /sessions retrieves it."""
    user_id = "user_persist_integration_1"
    prompt = "Tell me about a time you led an urgent technical intervention."
    transcript = (
        "At PaySync last November, I took full ownership of the PostgreSQL ledger migration. "
        "When query timeouts occurred, I diagnosed lock contention in the checkout funnel, "
        "isolated the offending table locks, and refactored the connection pooling. "
        "This resolved the outage in fifteen minutes and stabilized transactional latency."
    )

    # 1. Post evaluation
    eval_response = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "STAR",
            "scenario_prompt": prompt,
            "speaker_role": "Staff Engineer",
            "user_id": user_id,
            "transcript": transcript,
            "duration_seconds": 45.0,
        },
    )
    assert eval_response.status_code == 200, eval_response.text
    eval_data = eval_response.json()
    session_id = eval_data["session_id"]
    score = eval_data["score"]

    # 2. Query sessions list
    list_response = client.get(f"/api/v1/sessions?user_id={user_id}")
    assert list_response.status_code == 200, list_response.text
    list_data = list_response.json()

    assert list_data["total"] == 1
    assert list_data["cursor"] is None
    assert len(list_data["items"]) == 1

    saved = list_data["items"][0]
    assert saved["session_id"] == session_id
    assert saved["user_id"] == user_id
    assert saved["framework"] == "STAR"
    assert saved["prompt"] == prompt
    assert saved["transcript"] == transcript
    assert saved["score"] == score
    assert isinstance(saved["findings"], dict)
    assert isinstance(saved["tips"], list)
    assert isinstance(saved["badges"], list)
    assert saved["delivery_metrics"]["words_per_minute"] > 0
    assert "created_at" in saved


def test_sessions_user_isolation(client: TestClient) -> None:
    """Verify strict user isolation: users only see their own sessions."""
    user_a = "user_alice_123"
    user_b = "user_bob_456"

    # Alice creates 2 sessions
    for fw in ["STAR", "CARL"]:
        res = client.post(
            "/api/v1/sessions/evaluate",
            json={
                "framework": fw,
                "scenario_prompt": f"Alice prompt for {fw}",
                "user_id": user_a,
                "transcript": "I owned the incident response and resolved it.",
            },
        )
        assert res.status_code == 200

    # Bob creates 1 session
    res_b = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "SCQA",
            "scenario_prompt": "Bob prompt for SCQA",
            "user_id": user_b,
            "transcript": "Situation complication question and bottom line up front answer.",
        },
    )
    assert res_b.status_code == 200

    # Query Alice
    resp_alice = client.get(f"/api/v1/sessions?user_id={user_a}")
    assert resp_alice.status_code == 200
    alice_data = resp_alice.json()
    assert alice_data["total"] == 2
    assert all(item["user_id"] == user_a for item in alice_data["items"])
    alice_frameworks = {item["framework"] for item in alice_data["items"]}
    assert alice_frameworks == {"STAR", "CARL"}

    # Query Bob
    resp_bob = client.get(f"/api/v1/sessions?user_id={user_b}")
    assert resp_bob.status_code == 200
    bob_data = resp_bob.json()
    assert bob_data["total"] == 1
    assert bob_data["items"][0]["user_id"] == user_b
    assert bob_data["items"][0]["framework"] == "SCQA"

    # Query non-existent user
    resp_empty = client.get("/api/v1/sessions?user_id=user_nonexistent_999")
    assert resp_empty.status_code == 200
    empty_data = resp_empty.json()
    assert empty_data["total"] == 0
    assert empty_data["items"] == []
    assert empty_data["cursor"] is None


def test_sessions_ordered_by_created_at_desc(client: TestClient) -> None:
    """Verify sessions are returned ordered by created_at descending (newest first)."""
    user_id = "user_ordering_test"

    # Create session 1
    res1 = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "STAR",
            "scenario_prompt": "Prompt 1 First",
            "user_id": user_id,
            "transcript": "First session transcript.",
        },
    )
    assert res1.status_code == 200
    id1 = res1.json()["session_id"]

    # Small delay to ensure distinct timestamp
    time.sleep(0.01)

    # Create session 2
    res2 = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "CARL",
            "scenario_prompt": "Prompt 2 Second",
            "user_id": user_id,
            "transcript": "Second session transcript.",
        },
    )
    assert res2.status_code == 200
    id2 = res2.json()["session_id"]

    # Query
    list_res = client.get(f"/api/v1/sessions?user_id={user_id}")
    assert list_res.status_code == 200
    items = list_res.json()["items"]

    assert len(items) == 2
    assert items[0]["session_id"] == id2  # newest first
    assert items[1]["session_id"] == id1


def test_sessions_pagination_with_cursor_and_limit(client: TestClient) -> None:
    """Verify pagination across multiple pages with limit and cursor."""
    user_id = "user_pagination_test"
    created_ids: list[str] = []

    # Create 5 sessions
    for i in range(5):
        res = client.post(
            "/api/v1/sessions/evaluate",
            json={
                "framework": "STAR",
                "scenario_prompt": f"Pagination prompt {i}",
                "user_id": user_id,
                "transcript": f"I took ownership of project step {i} and resolved it.",
            },
        )
        assert res.status_code == 200
        created_ids.append(res.json()["session_id"])
        time.sleep(0.01)

    # Note: Sessions returned in reverse order of creation
    expected_order = list(reversed(created_ids))

    # Page 1: limit 2
    p1 = client.get(f"/api/v1/sessions?user_id={user_id}&limit=2")
    assert p1.status_code == 200
    d1 = p1.json()
    assert d1["total"] == 2
    assert d1["cursor"] is not None
    assert [s["session_id"] for s in d1["items"]] == expected_order[0:2]
    cursor1 = d1["cursor"]

    # Page 2: limit 2, cursor from page 1
    p2 = client.get(f"/api/v1/sessions?user_id={user_id}&limit=2&cursor={cursor1}")
    assert p2.status_code == 200
    d2 = p2.json()
    assert d2["total"] == 2
    assert d2["cursor"] is not None
    assert [s["session_id"] for s in d2["items"]] == expected_order[2:4]
    cursor2 = d2["cursor"]

    # Page 3: limit 2, cursor from page 2 (should return the final 1 item)
    p3 = client.get(f"/api/v1/sessions?user_id={user_id}&limit=2&cursor={cursor2}")
    assert p3.status_code == 200
    d3 = p3.json()
    assert d3["total"] == 1
    assert d3["cursor"] is None
    assert [s["session_id"] for s in d3["items"]] == expected_order[4:5]


def test_get_sessions_missing_user_id_returns_422(client: TestClient) -> None:
    """Verify GET /api/v1/sessions without user_id query param returns 422 VALIDATION_ERROR."""
    response = client.get("/api/v1/sessions")
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == ErrorCode.VALIDATION_ERROR.value
    assert data["error"]["retryable"] is False
    assert "request_id" in data


def test_get_sessions_invalid_limit_bounds_returns_422(client: TestClient) -> None:
    """Verify limit < 1 or limit > 100 returns 422 VALIDATION_ERROR."""
    # limit = 0 (< 1)
    res_zero = client.get("/api/v1/sessions?user_id=test&limit=0")
    assert res_zero.status_code == 422
    assert res_zero.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value

    # limit = 101 (> 100)
    res_over = client.get("/api/v1/sessions?user_id=test&limit=101")
    assert res_over.status_code == 422
    assert res_over.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR.value


def test_get_sessions_firestore_gateway_failure_returns_500(client: TestClient) -> None:
    """Verify query failures return 500 FIRESTORE_ERROR envelope."""

    class FailingFirestoreGateway:
        async def get_user_sessions(
            self,
            _user_id: str,
            limit: int = 20,
            cursor: str | None = None,
        ) -> list[object]:
            raise RuntimeError("Cloud Firestore connection timed out.")

    app.dependency_overrides[get_firestore_gateway] = lambda: FailingFirestoreGateway()

    response = client.get("/api/v1/sessions?user_id=any_user")
    assert response.status_code == 500
    data = response.json()
    assert data["error"]["code"] == ErrorCode.FIRESTORE_ERROR.value
    assert data["error"]["retryable"] is False
    assert "Failed to retrieve sessions" in data["error"]["message"]


def test_evaluate_session_save_failure_returns_500(client: TestClient) -> None:
    """Verify failure during session save returns 500 FIRESTORE_ERROR envelope."""

    class FailingSaveFirestoreGateway:
        async def save_session(self, _session: object) -> str:
            raise RuntimeError("Firestore quota exceeded.")

    app.dependency_overrides[get_firestore_gateway] = lambda: FailingSaveFirestoreGateway()

    response = client.post(
        "/api/v1/sessions/evaluate",
        json={
            "framework": "STAR",
            "scenario_prompt": "Describe an incident.",
            "transcript": "I fixed the outage.",
        },
    )
    assert response.status_code == 500
    data = response.json()
    assert data["error"]["code"] == ErrorCode.FIRESTORE_ERROR.value
    assert "Failed to persist evaluation session" in data["error"]["message"]
