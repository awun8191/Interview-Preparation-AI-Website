"""Pytest fixtures and configuration."""

import os
from collections.abc import Generator

# The suite is offline by design. Force synthetic gateways before the app is
# imported so a developer's real .env credentials and API keys never leak into
# test runs. This assignment must precede the app imports below.
os.environ["USE_SYNTHETIC_GATEWAYS"] = "true"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app, create_app  # noqa: E402


@pytest.fixture
def client() -> Generator[TestClient]:
    """Provide a TestClient using the default application instance."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def custom_app_client() -> TestClient:
    """Factory fixture for custom test app instances."""
    test_app = create_app()
    return TestClient(test_app, raise_server_exceptions=False)
