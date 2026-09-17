## 2026-09-17T18:39:06Z

You are worker_m2, a teamwork_preview_worker.
Your working directory is: /home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/worker_m2
Workspace root: /home/nasbombz/Documents/Projects/the-plan-software/backend
Monorepo root: /home/nasbombz/Documents/Projects/the-plan-software

MANDATORY: Read the original user request first at:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/ORIGINAL_REQUEST.md

Also read:
- /home/nasbombz/Documents/Projects/the-plan-software/backend/PROJECT.md
- /home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2/analysis.md
- /home/nasbombz/Documents/Projects/the-plan-software/CLAUDE.md
- /home/nasbombz/Documents/Projects/the-plan-software/AGENTS.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

YOUR ASSIGNMENT — MILESTONE 2: Gateway Layer, Data Models & Delivery Analytics Service

You exclusively own the following files:
- `app/models/scenario.py`
- `app/models/evaluation.py`
- `app/models/session.py`
- `app/gateways/__init__.py`
- `app/gateways/protocols.py`
- `app/gateways/gemini.py`
- `app/gateways/groq.py`
- `app/gateways/typesafe.py`
- `app/gateways/firestore.py`
- `app/gateways/synthetic.py`
- `app/gateways/dependencies.py`
- `app/services/__init__.py`
- `app/services/analytics.py`
- `tests/unit/test_delivery_analytics.py`
- `tests/unit/test_synthetic_gateways.py`

SPECIFIC REQUIREMENTS:
1. Pydantic Models (`app/models/`):
   - `scenario.py`: `FrameworkEnum` (STAR, CARL, PAR, SCQA, SBI, RADICAL_CANDOR, STATE, GOTTMAN, VOSS, SPARKLINE, MONROE), `DifficultyLevel` (beginner, intermediate, advanced), `GenerateScenarioRequest`, `ScenarioResponse`.
   - `evaluation.py`: `EvaluateSessionRequest` (supports `framework: FrameworkEnum`, `speaker_role: str`, `scenario_prompt: str`, `scenario_context: str | None`, `transcript: str | None`, `duration_seconds: float | None`), `ScorecardSubscore`, `BadgeItem`, `EvaluateSessionResponse`, `JevEvaluationState`.
   - `session.py`: `UserRecord` (`user_id`, `email`, `display_name`, `role` in ["user", "admin"], `subscription_tier` in ["free", "pro"], `created_at: datetime`), `SessionRecord` (`session_id`, `user_id`, `framework: str`, `prompt: str`, `transcript: str`, `score: float`, `findings: dict[str, Any]`, `tips: list[str]`, `created_at: datetime`), `SessionListResponse` (`items: list[SessionRecord]`, `total: int`, `cursor: str | None`).
2. Gateway Protocols (`app/gateways/protocols.py`):
   - Abstract `Protocol` classes for `GeminiGatewayProtocol`, `GroqGatewayProtocol`, `JevGatewayProtocol`, `FirestoreGatewayProtocol`.
3. Concrete Gateways:
   - `gemini.py`: Implements `GeminiGatewayProtocol` using `httpx.AsyncClient` calling Google Generative AI / Gemini API to generate scenarios.
   - `groq.py`: Implements `GroqGatewayProtocol` uploading multipart audio to Groq Whisper (`whisper-large-v3`) and returning transcript, duration, and word timings.
   - `typesafe.py`: Implements `JevGatewayProtocol` calling `POST https://api.typesafe.ai/v1/systemone` with `state` and `questions` dict in parallel.
   - `firestore.py`: Implements `FirestoreGatewayProtocol` with `firebase_admin` connecting to project `theplan-9311e`. Supports `save_user`, `get_user`, `save_session`, `get_user_sessions`. Handles `FIRESTORE_EMULATOR_HOST` and credentials cleanly.
4. Synthetic Gateways (`app/gateways/synthetic.py`):
   - `SyntheticGeminiGateway`: Deterministic high-quality scenario generator tailored to framework, role, and domain.
   - `SyntheticGroqGateway`: In-memory STT provider returning transcript and word timings from audio or synthetic buffer.
   - `SyntheticJevGateway`: Genuine mock evaluating Jev question criteria against the transcript keywords/heuristics, strictly enforcing the Balanced Impact Rule (returning 1.0 for both qualitative operational outcomes and quantitative metrics).
   - `SyntheticFirestoreGateway`: In-memory thread-safe dictionary storage simulating Firestore collections for `users` and `sessions`.
5. Dependency Injection (`app/gateways/dependencies.py`):
   - FastAPI `Depends()` functions providing instances of each gateway. If `settings.USE_SYNTHETIC_GATEWAYS` is True OR if the respective API key is empty/unconfigured, automatically inject the synthetic gateway. This guarantees 100% offline testability.
6. Delivery Analytics Service (`app/services/analytics.py`):
   - `calculate_delivery_analytics(transcript: str, duration_seconds: float, word_timestamps: list[dict] | None = None) -> DeliveryAnalyticsResult`
   - Calculates: `word_count`, `duration_seconds`, `words_per_minute` (guards against duration <= 0, returning 0), `filler_count`, `filler_words_breakdown` (detects "um", "uh", "like", "you know", "sort of", "kind of", "actually", "basically"), `filler_density_percentage`, `pause_count`, `power_pauses_count`.
7. Tests:
   - `tests/unit/test_delivery_analytics.py`: tests WPM calculation, division by zero protection, filler word density, power pauses.
   - `tests/unit/test_synthetic_gateways.py`: tests all 4 synthetic gateways end-to-end (Gemini scenario generation, Groq transcription, Jev question grading with balanced impact, Firestore user and session persistence).
8. Verification:
   - Run `uv run pytest tests/unit/test_delivery_analytics.py tests/unit/test_synthetic_gateways.py`
   - Run `uv run ruff check .`
   - Run `uv run ruff format --check .`
