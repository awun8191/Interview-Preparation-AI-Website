"""Unit tests for production FirestoreGateway offloading blocking I/O to asyncio.to_thread."""

from unittest.mock import MagicMock, patch

import pytest

from app.gateways.firestore import FirestoreGateway
from app.models.session import SessionRecord, UserRecord


@pytest.fixture
def mock_client() -> MagicMock:
    return MagicMock()


@pytest.mark.asyncio
async def test_firestore_gateway_save_user_uses_thread(mock_client: MagicMock) -> None:
    gateway = FirestoreGateway(client=mock_client)
    user = UserRecord(
        user_id="u123",
        email="test@example.com",
        display_name="Tester",
        role="user",
        subscription_tier="free",
    )

    with patch("asyncio.to_thread", wraps=__import__("asyncio").to_thread) as mock_to_thread:
        await gateway.save_user(user)
        assert mock_to_thread.called
        mock_client.collection.assert_called_with("users")
        mock_client.collection().document.assert_called_with("u123")


@pytest.mark.asyncio
async def test_firestore_gateway_get_user_uses_thread(mock_client: MagicMock) -> None:
    gateway = FirestoreGateway(client=mock_client)
    doc_mock = MagicMock()
    doc_mock.exists = True
    doc_mock.to_dict.return_value = {
        "user_id": "u123",
        "email": "test@example.com",
        "display_name": "Tester",
        "role": "user",
        "subscription_tier": "free",
    }
    mock_client.collection().document().get.return_value = doc_mock

    with patch("asyncio.to_thread", wraps=__import__("asyncio").to_thread) as mock_to_thread:
        user = await gateway.get_user("u123")
        assert mock_to_thread.called
        assert user is not None
        assert user.user_id == "u123"


@pytest.mark.asyncio
async def test_firestore_gateway_save_session_uses_thread(mock_client: MagicMock) -> None:
    gateway = FirestoreGateway(client=mock_client)
    session = SessionRecord(
        session_id="s123",
        user_id="u123",
        framework="STAR",
        prompt="Tell me about a project",
        transcript="I led the project successfully",
        score=95.0,
        findings={},
        tips=["Great job"],
    )

    with patch("asyncio.to_thread", wraps=__import__("asyncio").to_thread) as mock_to_thread:
        sid = await gateway.save_session(session)
        assert mock_to_thread.called
        assert sid == "s123"
        mock_client.collection.assert_called_with("sessions")
        mock_client.collection().document.assert_called_with("s123")


@pytest.mark.asyncio
async def test_firestore_gateway_get_user_sessions_uses_thread(mock_client: MagicMock) -> None:
    gateway = FirestoreGateway(client=mock_client)
    doc_mock = MagicMock()
    doc_mock.to_dict.return_value = {
        "session_id": "s123",
        "user_id": "u123",
        "framework": "STAR",
        "prompt": "Tell me about a project",
        "transcript": "I led the project successfully",
        "score": 95.0,
        "findings": {},
        "tips": ["Great job"],
    }
    query_mock = mock_client.collection().where().order_by().limit()
    query_mock.stream.return_value = [doc_mock]

    with patch("asyncio.to_thread", wraps=__import__("asyncio").to_thread) as mock_to_thread:
        sessions = await gateway.get_user_sessions(user_id="u123", limit=10)
        assert mock_to_thread.called
        assert len(sessions) == 1
        assert sessions[0].session_id == "s123"
