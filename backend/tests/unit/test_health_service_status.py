"""Unit tests for health-endpoint service status reporting."""

from app.api.v1.health import _firestore_configured
from app.core.config import Settings


def _settings(**overrides: object) -> Settings:
    """Settings with the local .env bypassed, so only explicit values apply."""
    base = {
        "USE_SYNTHETIC_GATEWAYS": False,
        "FIRESTORE_EMULATOR_HOST": None,
        "FIREBASE_CREDENTIALS_PATH": None,
        "_env_file": None,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def test_firestore_unconfigured_without_any_credential_source(monkeypatch) -> None:
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    monkeypatch.delenv("K_SERVICE", raising=False)

    assert _firestore_configured(_settings()) is False


def test_firestore_healthy_via_adc_on_cloud_run(monkeypatch) -> None:
    """Cloud Run provides ADC through the metadata server; no credential file exists."""
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    monkeypatch.setenv("K_SERVICE", "the-plan-api")

    assert _firestore_configured(_settings()) is True


def test_firestore_healthy_via_explicit_credentials_or_emulator() -> None:
    assert _firestore_configured(_settings(FIREBASE_CREDENTIALS_PATH="/tmp/sa.json")) is True
    assert _firestore_configured(_settings(FIRESTORE_EMULATOR_HOST="localhost:8080")) is True
    assert _firestore_configured(_settings(USE_SYNTHETIC_GATEWAYS=True)) is True
