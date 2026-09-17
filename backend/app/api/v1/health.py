"""Health check endpoint."""

import os
from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import Settings, get_settings
from app.models.common import HealthResponse

router = APIRouter(tags=["health"])


def _firestore_configured(settings: Settings) -> bool:
    """Whether Firestore has a usable credential source.

    Explicit paths and the emulator are obvious; the remaining case is
    Application Default Credentials, which the gateway falls back to. On Google
    Cloud the metadata server supplies those, so no credential file is present.
    """
    if (
        settings.FIRESTORE_EMULATOR_HOST
        or settings.FIREBASE_CREDENTIALS_PATH
        or settings.USE_SYNTHETIC_GATEWAYS
    ):
        return True
    return bool(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.environ.get("K_SERVICE"))


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Return health status of the application and connected services."""
    settings = get_settings()
    environment = (
        "production"
        if (settings.ENVIRONMENT == "production" and not settings.DEBUG)
        else "development"
    )

    services = {
        "gemini": (
            "healthy"
            if (settings.GEMINI_API_KEY or settings.USE_SYNTHETIC_GATEWAYS)
            else "unconfigured"
        ),
        "groq": (
            "healthy"
            if (settings.GROQ_API_KEY or settings.USE_SYNTHETIC_GATEWAYS)
            else "unconfigured"
        ),
        "typesafe": (
            "healthy"
            if (settings.TYPESAFE_API_KEY or settings.USE_SYNTHETIC_GATEWAYS)
            else "unconfigured"
        ),
        "firestore": "healthy" if _firestore_configured(settings) else "unconfigured",
    }

    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now(UTC),
        environment=environment,
        services=services,
    )
