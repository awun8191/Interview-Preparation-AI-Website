"""Google Gemini Flash scenario generation gateway."""

import json
import logging
from typing import Any

import httpx

from app.core.config import Settings, get_settings
from app.core.errors import AppError, ErrorCode, ProviderUnavailableError
from app.models.scenario import GenerateScenarioRequest, ScenarioResponse

logger = logging.getLogger(__name__)

GEMINI_SYSTEM_INSTRUCTION = """
You are the Scenario Architect for an executive-grade communication training platform.
Your objective is to generate authentic, high-stakes workplace scenarios designed specifically
to test the user's mastery of the target communication framework.

Framework Design Principles:
1. STAR: Test past execution, individual agency under pressure, and tangible outcomes.
2. CARL: Test metacognition, failure recovery, flawed assumptions, and systemic safeguards.
3. PAR: Test 45-60s executive brevity, high information density, and decisive problem-solving.
4. SCQA: Test Barbara Minto's BLUF—baseline, complication, governing question, and recommendation.
5. SBI: Test camera-recordable behavior, observable impact, and peer feedback.
6. RADICAL_CANDOR: Test caring personally while challenging directly.
7. STATE: Test Crucial Conversations facts-first delivery and path inquiry.
8. GOTTMAN: Test de-escalation, gentle start-up, and repair attempts.
9. VOSS: Test Tactical Empathy, calibrated questions, and emotion labeling.
10. SPARKLINE: Test Nancy Duarte oratorical rhythm contrasting 'What Is' vs 'What Could Be'.
11. MONROE: Test Monroe's 5-step motivated sequence:
    Attention, Need, Satisfaction, Visualization, Action.

Constraints:
- Ground scenarios in authentic domain trade-offs.
- Never embed coaching hints or answers inside the prompt_question itself.
- Return ONLY valid JSON matching the requested schema.
"""


class GeminiGateway:
    """Gateway for scenario prompt generation via Google Gemini API."""

    def __init__(
        self,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.client = client
        self.api_key = self.settings.GEMINI_API_KEY
        self.model = self.settings.GEMINI_MODEL or "gemini-3.8-flash"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate_scenario(self, request: GenerateScenarioRequest) -> ScenarioResponse:
        """Call Gemini to generate a tailored scenario prompt matching request parameters."""
        if not self.api_key:
            raise ProviderUnavailableError(
                message="Gemini API key is not configured.",
                code=ErrorCode.PROVIDER_UNAVAILABLE,
            )

        url = f"{self.base_url}/{self.model}:generateContent"
        params = {"key": self.api_key}

        user_prompt = (
            f"Generate a practice scenario for:\n"
            f"- Framework: {request.target_framework.value}\n"
            f"- User Domain / Role: {request.user_domain}\n"
            f"- Difficulty: {request.difficulty_level.value}\n"
            f"- Focus Theme: {request.focus_theme or 'General'}\n\n"
            f"Return a JSON object with fields: scenario_id (string slug), title (string), "
            f"context_background (string), prompt_question (string), "
            f"key_dimensions_to_test (list of strings), and target_duration_seconds (integer)."
        )

        payload: dict[str, Any] = {
            "contents": [{"parts": [{"text": user_prompt}]}],
            "systemInstruction": {"parts": [{"text": GEMINI_SYSTEM_INSTRUCTION}]},
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.7,
            },
        }

        async def _execute_request(http_client: httpx.AsyncClient) -> ScenarioResponse:
            try:
                response = await http_client.post(
                    url,
                    params=params,
                    json=payload,
                    timeout=15.0,
                )
                if response.status_code == 429:
                    raise AppError(
                        code=ErrorCode.RATE_LIMITED,
                        message="Gemini API rate limit exceeded. Please retry.",
                        status_code=429,
                        retryable=True,
                    )
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                logger.error("Gemini API HTTP error %d: %s", status_code, exc.response.text)
                raise ProviderUnavailableError(
                    message=f"Gemini API returned HTTP {status_code}.",
                    code=ErrorCode.PROVIDER_UNAVAILABLE,
                ) from exc
            except httpx.RequestError as exc:
                logger.error("Gemini connection error: %s", exc)
                raise ProviderUnavailableError(
                    message=f"Gemini connection failed: {exc}",
                    code=ErrorCode.PROVIDER_UNAVAILABLE,
                ) from exc

            try:
                candidates = data.get("candidates", [])
                if not candidates:
                    raise ValueError("No candidates returned from Gemini.")
                part_text = candidates[0]["content"]["parts"][0]["text"]
                scenario_data = json.loads(part_text)
            except Exception as exc:
                logger.error("Failed to parse Gemini response: %s; Data: %s", exc, data)
                raise ProviderUnavailableError(
                    message="Failed to parse valid scenario response from Gemini.",
                    code=ErrorCode.PROVIDER_UNAVAILABLE,
                ) from exc

            raw_slug = scenario_data.get(
                "scenario_id",
                f"gemini-{request.target_framework.lower()}",
            )
            return ScenarioResponse(
                scenario_id=str(raw_slug),
                title=str(scenario_data.get("title", f"{request.target_framework} Scenario")),
                context_background=str(scenario_data.get("context_background", "")),
                prompt_question=str(scenario_data.get("prompt_question", "")),
                key_dimensions_to_test=list(scenario_data.get("key_dimensions_to_test", [])),
                target_duration_seconds=int(scenario_data.get("target_duration_seconds", 90)),
                target_framework=request.target_framework,
                difficulty_level=request.difficulty_level,
            )

        if self.client:
            return await _execute_request(self.client)

        async with httpx.AsyncClient() as http_client:
            return await _execute_request(http_client)
