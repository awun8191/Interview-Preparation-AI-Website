"""Gateway abstractions, concrete clients, synthetic mocks, and DI dependencies."""

from app.gateways.dependencies import (
    get_firestore_gateway,
    get_firestore_repo,
    get_gemini_gateway,
    get_groq_gateway,
    get_jev_gateway,
    get_synthetic_firestore,
)
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

__all__ = [
    "FirestoreGateway",
    "FirestoreGatewayProtocol",
    "GeminiGateway",
    "GeminiGatewayProtocol",
    "GroqGateway",
    "GroqGatewayProtocol",
    "JevGatewayProtocol",
    "SyntheticFirestoreGateway",
    "SyntheticGeminiGateway",
    "SyntheticGroqGateway",
    "SyntheticJevGateway",
    "TypeSafeGateway",
    "get_firestore_gateway",
    "get_firestore_repo",
    "get_gemini_gateway",
    "get_groq_gateway",
    "get_jev_gateway",
    "get_synthetic_firestore",
]
