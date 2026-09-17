"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings read from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "The-Plan-Software Backend"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: list[str] = ["*"]

    # Gemini Scenario Generation
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Groq Whisper STT
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "whisper-large-v3"

    # TypeSafe AI Jev System One
    TYPESAFE_API_KEY: str = ""
    TYPESAFE_MODEL: str = "jev-latest"
    TYPESAFE_API_URL: str = "https://api.typesafe.ai/v1/systemone"

    # Firebase Firestore
    FIREBASE_PROJECT_ID: str = "theplan-9311e"
    FIREBASE_CREDENTIALS_PATH: str | None = None
    FIRESTORE_EMULATOR_HOST: str | None = None

    # Testing & Fallbacks
    USE_SYNTHETIC_GATEWAYS: bool = False

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            v_stripped = v.strip()
            if v_stripped.startswith("[") and v_stripped.endswith("]"):
                import json

                return json.loads(v_stripped)
            return [origin.strip() for origin in v_stripped.split(",") if origin.strip()]
        if isinstance(v, (list, tuple)):
            return list(v)
        return ["*"]


@lru_cache
def get_settings() -> Settings:
    """Return cached instance of application settings."""
    return Settings()
