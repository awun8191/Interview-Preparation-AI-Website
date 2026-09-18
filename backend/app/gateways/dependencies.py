"""FastAPI dependency providers for gateway services.

Automatically injects synthetic gateways when settings.USE_SYNTHETIC_GATEWAYS is True
or when individual API keys/credentials are unconfigured, ensuring 100% offline testability.
"""

import logging
import os
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.gateways.firestore import FirestoreGateway
from app.gateways.gemini import GeminiGateway
from app.gateways.groq import GroqGateway
from app.gateways.protocols import (
    FirestoreGatewayProtocol,
    GeminiGatewayProtocol,
    GroqGatewayProtocol,
    JevGatewayProtocol,
)
from app.gateways.synthetic import (
    SyntheticFirestoreGateway,
    SyntheticGeminiGateway,
    SyntheticGroqGateway,
    SyntheticJevGateway,
)
from app.gateways.typesafe import TypeSafeGateway

logger = logging.getLogger(__name__)

# Cached singletons for synthetic gateways to maintain in-memory state
_synthetic_gemini_instance = SyntheticGeminiGateway()
_synthetic_groq_instance = SyntheticGroqGateway()
_synthetic_jev_instance = SyntheticJevGateway()
_synthetic_firestore_instance = SyntheticFirestoreGateway()


def get_synthetic_firestore() -> SyntheticFirestoreGateway:
    """Return the shared in-memory Firestore synthetic instance."""
    return _synthetic_firestore_instance


def get_gemini_gateway(
    settings: Annotated[Settings | None, Depends(get_settings)] = None,
) -> GeminiGatewayProtocol:
    """Provide Gemini gateway, falling back to synthetic if unconfigured or requested."""
    cfg = settings or get_settings()
    if cfg.USE_SYNTHETIC_GATEWAYS or not cfg.GEMINI_API_KEY.strip():
        return _synthetic_gemini_instance
    return GeminiGateway(settings=cfg)


def get_groq_gateway(
    settings: Annotated[Settings | None, Depends(get_settings)] = None,
) -> GroqGatewayProtocol:
    """Provide Groq STT gateway, falling back to synthetic if unconfigured or requested."""
    cfg = settings or get_settings()
    if cfg.USE_SYNTHETIC_GATEWAYS or not cfg.GROQ_API_KEY.strip():
        return _synthetic_groq_instance
    return GroqGateway(settings=cfg)


def get_jev_gateway(
    settings: Annotated[Settings | None, Depends(get_settings)] = None,
) -> JevGatewayProtocol:
    """Provide TypeSafe AI Jev gateway, falling back to synthetic if unconfigured or requested."""
    cfg = settings or get_settings()
    if cfg.USE_SYNTHETIC_GATEWAYS or not cfg.TYPESAFE_API_KEY.strip():
        return _synthetic_jev_instance
    return TypeSafeGateway(settings=cfg)


def _has_firestore_credentials(settings: Settings) -> bool:
    """Check if any Firestore connection configuration is provided."""
    if settings.FIRESTORE_EMULATOR_HOST or os.environ.get("FIRESTORE_EMULATOR_HOST"):
        return True
    if settings.FIREBASE_CREDENTIALS_PATH or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        return True
    return bool(os.environ.get("FIREBASE_CREDENTIALS_JSON"))


# Module-level holder for the live Firestore gateway.
# A Settings object is not hashable, so this cannot be an lru_cache key.
_live_firestore_instance: FirestoreGateway | None = None


def get_firestore_gateway(
    settings: Annotated[Settings | None, Depends(get_settings)] = None,
) -> FirestoreGatewayProtocol:
    """Provide Firestore gateway, falling back to synthetic if unconfigured or requested."""
    global _live_firestore_instance

    cfg = settings or get_settings()
    if cfg.USE_SYNTHETIC_GATEWAYS or not _has_firestore_credentials(cfg):
        return _synthetic_firestore_instance

    if _live_firestore_instance is None:
        try:
            _live_firestore_instance = FirestoreGateway(settings=cfg)
        except Exception:
            # Fall back so the app stays usable offline, but never silently: a
            # swallowed error here means writes go to memory and vanish on restart.
            logger.exception(
                "Live Firestore gateway failed to initialize; falling back to the "
                "in-memory synthetic store. Sessions will NOT persist."
            )
            return _synthetic_firestore_instance

    return _live_firestore_instance


# Aliases for compatibility
get_firestore_repo = get_firestore_gateway
