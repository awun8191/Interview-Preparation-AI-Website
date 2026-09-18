"""Groq Whisper speech-to-text gateway."""

import logging
from typing import Any

import httpx

from app.core.config import Settings, get_settings
from app.core.errors import AppError, ErrorCode, GroqSTTError, ProviderUnavailableError
from app.models.evaluation import TranscriptionResult

logger = logging.getLogger(__name__)

# Max upload size: 25 MB
MAX_AUDIO_BYTES = 25 * 1024 * 1024


class GroqGateway:
    """Gateway for speech-to-text transcription via Groq Whisper API."""

    def __init__(
        self,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.client = client
        self.api_key = self.settings.GROQ_API_KEY
        self.model = self.settings.GROQ_MODEL or "whisper-large-v3"
        self.url = "https://api.groq.com/openai/v1/audio/transcriptions"

    async def transcribe_audio(
        self, audio_bytes: bytes, filename: str = "audio.wav"
    ) -> TranscriptionResult:
        """Upload audio to Groq Whisper and extract transcript, duration, and word timings."""
        if not self.api_key:
            raise ProviderUnavailableError(
                message="Groq API key is not configured.",
                code=ErrorCode.PROVIDER_UNAVAILABLE,
            )

        if not audio_bytes:
            raise AppError(
                code=ErrorCode.BAD_REQUEST,
                message="Audio file is empty.",
                status_code=400,
                retryable=False,
            )

        if len(audio_bytes) > MAX_AUDIO_BYTES:
            raise AppError(
                code=ErrorCode.BAD_REQUEST,
                message="Audio file exceeds the 25MB maximum upload limit.",
                status_code=400,
                retryable=False,
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        # Infer MIME type based on extension
        lower_name = filename.lower()
        if lower_name.endswith((".mp3", ".mpeg")):
            content_type = "audio/mpeg"
        elif lower_name.endswith(".m4a"):
            content_type = "audio/m4a"
        elif lower_name.endswith(".ogg"):
            content_type = "audio/ogg"
        elif lower_name.endswith(".webm"):
            content_type = "audio/webm"
        elif lower_name.endswith(".flac"):
            content_type = "audio/flac"
        else:
            content_type = "audio/wav"

        files = {
            "file": (filename, audio_bytes, content_type),
        }
        data = {
            "model": self.model,
            "response_format": "verbose_json",
            "temperature": "0.0",
            "timestamp_granularities[]": "word",
        }

        async def _execute(http_client: httpx.AsyncClient) -> TranscriptionResult:
            try:
                response = await http_client.post(
                    self.url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30.0,
                )
                if response.status_code == 429:
                    raise AppError(
                        code=ErrorCode.RATE_LIMITED,
                        message="Groq Whisper rate limit exceeded. Please retry.",
                        status_code=429,
                        retryable=True,
                    )
                response.raise_for_status()
                payload = response.json()
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                logger.error("Groq STT HTTP error %d: %s", status_code, exc.response.text)
                raise GroqSTTError(
                    message=f"Groq STT service returned HTTP {status_code}.",
                    details=exc.response.text,
                ) from exc
            except httpx.RequestError as exc:
                logger.error("Groq STT connection error: %s", exc)
                raise GroqSTTError(
                    message=f"Groq STT connection failed: {exc}",
                ) from exc

            transcript = str(payload.get("text", "")).strip()
            duration = float(payload.get("duration", 0.0))
            raw_words = payload.get("words", [])

            words: list[dict[str, Any]] = [
                {
                    "word": str(w.get("word", "")),
                    "start": float(w.get("start", 0.0)),
                    "end": float(w.get("end", 0.0)),
                }
                for w in raw_words
                if isinstance(w, dict)
            ]

            return TranscriptionResult(
                transcript=transcript,
                duration_seconds=duration,
                words=words,
            )

        if self.client:
            return await _execute(self.client)

        async with httpx.AsyncClient() as http_client:
            return await _execute(http_client)
