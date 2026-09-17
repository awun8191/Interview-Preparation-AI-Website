"""Abstract protocol interfaces for external service gateways."""

from typing import Any, Protocol, runtime_checkable

from app.models.evaluation import JevEvaluationState, TranscriptionResult
from app.models.scenario import GenerateScenarioRequest, ScenarioResponse
from app.models.session import SessionRecord, UserRecord


@runtime_checkable
class GeminiGatewayProtocol(Protocol):
    """Protocol for scenario generation gateways."""

    async def generate_scenario(self, request: GenerateScenarioRequest) -> ScenarioResponse:
        """Generate a tailored practice scenario matching framework and seniority context."""
        ...


@runtime_checkable
class GroqGatewayProtocol(Protocol):
    """Protocol for speech-to-text audio transcription gateways."""

    async def transcribe_audio(
        self, audio_bytes: bytes, filename: str = "audio.wav"
    ) -> TranscriptionResult:
        """Transcribe audio bytes to text with word-level timestamps and duration."""
        ...


@runtime_checkable
class JevGatewayProtocol(Protocol):
    """Protocol for TypeSafe AI Jev System One rubric evaluation gateways."""

    async def evaluate_questions(
        self,
        state: JevEvaluationState | dict[str, Any],
        questions: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate rubric questions against state and transcript."""
        ...

    async def evaluate(
        self,
        state: JevEvaluationState | dict[str, Any],
        questions: dict[str, Any],
    ) -> dict[str, Any]:
        """Convenience alias for evaluate_questions."""
        ...


@runtime_checkable
class FirestoreGatewayProtocol(Protocol):
    """Protocol for Firebase Firestore persistence gateways."""

    async def save_user(self, user: UserRecord) -> None:
        """Upsert a user profile record."""
        ...

    async def get_user(self, user_id: str) -> UserRecord | None:
        """Retrieve a user profile record by ID."""
        ...

    async def save_session(self, session: SessionRecord) -> str:
        """Persist an evaluation session record and return the session_id."""
        ...

    async def get_user_sessions(
        self,
        user_id: str,
        limit: int = 20,
        cursor: str | None = None,
    ) -> list[SessionRecord]:
        """Retrieve paginated evaluation sessions for a given user ordered by created_at desc."""
        ...
