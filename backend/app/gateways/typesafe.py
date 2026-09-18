"""TypeSafe AI Jev System One rubric evaluation gateway."""

import logging
from typing import Any

import httpx

from app.core.config import Settings, get_settings
from app.core.errors import AppError, ErrorCode, ProviderUnavailableError, TypeSafeUnavailableError
from app.models.evaluation import JevEvaluationState

logger = logging.getLogger(__name__)


class TypeSafeGateway:
    """Gateway calling TypeSafe AI Jev System One endpoint for rubric evaluation."""

    def __init__(
        self,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.client = client
        self.api_key = self.settings.TYPESAFE_API_KEY
        self.model = getattr(self.settings, "TYPESAFE_MODEL", "jev-latest") or "jev-latest"
        self.url = self.settings.TYPESAFE_API_URL or "https://api.typesafe.ai/v1/systemone"

    async def evaluate_questions(
        self,
        state: JevEvaluationState | dict[str, Any],
        questions: dict[str, Any],
    ) -> dict[str, Any]:
        """Send state context and parallel question specs to TypeSafe Jev System One."""
        if not self.api_key:
            raise ProviderUnavailableError(
                message="TypeSafe AI API key is not configured.",
                code=ErrorCode.PROVIDER_UNAVAILABLE,
            )

        state_payload = state.model_dump() if isinstance(state, JevEvaluationState) else state

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        wire_questions: dict[str, Any] = {}
        for q_id, q_spec in questions.items():
            if isinstance(q_spec, dict):
                spec_copy = dict(q_spec)
                if spec_copy.get("type") == "score" and isinstance(spec_copy.get("criteria"), dict):
                    spec_copy["criteria"] = list(spec_copy["criteria"].values())
                elif spec_copy.get("type") == "noul" and "criteria" in spec_copy:
                    spec_copy.pop("criteria", None)
                wire_questions[q_id] = spec_copy
            else:
                wire_questions[q_id] = q_spec

        body = {
            "model": self.model,
            "state": state_payload,
            "questions": wire_questions,
        }

        async def _execute(http_client: httpx.AsyncClient) -> dict[str, Any]:
            try:
                response = await http_client.post(
                    self.url,
                    headers=headers,
                    json=body,
                    timeout=20.0,
                )
                if response.status_code == 429:
                    raise AppError(
                        code=ErrorCode.RATE_LIMITED,
                        message="TypeSafe AI rate limit exceeded. Please retry.",
                        status_code=429,
                        retryable=True,
                    )
                response.raise_for_status()
                payload = response.json()
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                logger.error("TypeSafe Jev HTTP error %d: %s", status_code, exc.response.text)
                raise TypeSafeUnavailableError(
                    message=f"TypeSafe AI Jev service returned HTTP {status_code}.",
                    details=exc.response.text,
                ) from exc
            except httpx.RequestError as exc:
                logger.error("TypeSafe Jev connection error: %s", exc)
                raise TypeSafeUnavailableError(
                    message=f"TypeSafe AI Jev connection failed: {exc}",
                ) from exc

            if not isinstance(payload, dict):
                raise TypeSafeUnavailableError(
                    message="TypeSafe AI Jev returned unexpected non-dictionary response.",
                )

            if "answers" in payload and isinstance(payload["answers"], dict):
                return payload["answers"]

            return payload

        if self.client:
            return await _execute(self.client)

        async with httpx.AsyncClient() as http_client:
            return await _execute(http_client)

    async def evaluate(
        self,
        state: JevEvaluationState | dict[str, Any],
        questions: dict[str, Any],
    ) -> dict[str, Any]:
        """Convenience alias for evaluate_questions."""
        return await self.evaluate_questions(state, questions)
