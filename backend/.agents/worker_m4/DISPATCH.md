## 2026-09-17T18:57:16Z

You are worker_m4, a teamwork_preview_worker.
Your working directory is: /home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/worker_m4
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

YOUR ASSIGNMENT — MILESTONE 4: Cognitive Orchestration Endpoints & Firestore Persistence Integration

You exclusively own the following files:
- `app/api/v1/scenarios.py`
- `app/api/v1/sessions.py`
- `app/api/v1/router.py`
- `tests/integration/test_api_scenarios.py`
- `tests/integration/test_api_sessions.py`
- `tests/integration/test_firestore_persistence.py`

SPECIFIC REQUIREMENTS:
1. Scenario Generation Endpoint (`app/api/v1/scenarios.py`):
   - `POST /api/v1/scenarios/generate`:
     - Accepts `GenerateScenarioRequest` (validates `target_framework`, `user_domain`, `difficulty_level`, `focus_theme`).
     - Injects `GeminiGatewayProtocol` via `Depends(get_gemini_gateway)`.
     - Calls `await gateway.generate_scenario(request)` and returns `ScenarioResponse`.
     - Handles errors converting to standardized error envelope (`PROVIDER_UNAVAILABLE`, retryable=True).
2. Session Evaluation & History Endpoints (`app/api/v1/sessions.py`):
   - `POST /api/v1/sessions/evaluate`:
     - Supports both `application/json` (`EvaluateSessionRequest`) and `multipart/form-data` (uploading audio file `audio_file: UploadFile` with form fields `framework`, `speaker_role`, `scenario_prompt`, `user_id`).
     - If audio file is provided, invokes `GroqGatewayProtocol.transcribe_audio()` to get `transcript`, `duration_seconds`, and `word_timestamps`.
     - If text is provided, uses `request.transcript` and `request.duration_seconds`. If transcript is empty and no audio, raises 422 `ValidationError` with envelope.
     - Runs Delivery Analytics: `calculate_delivery_analytics(transcript, duration_seconds, word_timestamps)`.
     - Formats Jev wire payload: pulls framework catalog via `get_framework_catalog(framework)` to get Jev questions dictionary and formats `JevEvaluationState`.
     - Evaluates via `JevGatewayProtocol.evaluate_questions(state, questions)`.
     - Computes deterministic scoring: `ScoringEngine().score_session(framework, findings, analytics)`.
     - Persists to Firestore: creates `SessionRecord` (`session_id=str(uuid4())`, `user_id`, `framework`, `prompt`, `transcript`, `score`, `findings`, `tips`, `created_at`) and saves via `FirestoreGatewayProtocol.save_session(record)`.
     - Returns `EvaluateSessionResponse` with `session_id`, `scorecard`, `delivery_analytics`, `badges`, `tips`, and `created_at`.
   - `GET /api/v1/sessions`:
     - Query params: `user_id: str` (required), `limit: int = 20`, `cursor: str | None = None`.
     - Injects `FirestoreGatewayProtocol`.
     - Returns `SessionListResponse` containing `items: list[SessionRecord]`, `total: int`, `cursor: str | None`.
3. Router Integration (`app/api/v1/router.py`):
   - Include `health.router`, `scenarios.router`, and `sessions.router`.
4. Integration Tests:
   - `tests/integration/test_api_scenarios.py`: Tests scenario generation happy path across frameworks, invalid framework 422 error, missing user_domain 422 error, standard error envelope.
   - `tests/integration/test_api_sessions.py`: Tests session evaluation via JSON text, session evaluation via audio multipart upload, balanced impact score in evaluate response, 422 when neither audio nor text is provided, invalid framework error envelope.
   - `tests/integration/test_firestore_persistence.py`: Tests that evaluating a session persists it to Firestore and that `GET /api/v1/sessions?user_id=...` retrieves the saved session, pagination, and user isolation.
5. Verification:
   - Run `uv run pytest tests/integration`
   - Run `uv run pytest` (all tests in repository)
   - Run `uv run ruff check .`
   - Run `uv run ruff format --check .`

DELIVERABLE:
Write your report to:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/worker_m4/analysis.md
and handoff report to:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/worker_m4/handoff.md
Update progress in:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/worker_m4/progress.md

When done, message the orchestrator.
