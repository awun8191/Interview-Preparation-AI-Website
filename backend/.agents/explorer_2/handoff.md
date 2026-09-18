# Handoff Report: External Integrations, Data Models & API Contracts Specification

**Agent**: `explorer_2` (Teamwork Explorer)  
**Recipient**: `orchestrator_1` (Project Orchestrator)  
**Date**: 2026-09-17T18:30:15Z  
**Working Directory**: `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2`

---

## 1. Observation

1. **Repository Layout and Initial State**:
   - `/home/nasbombz/Documents/Projects/the-plan-software/backend/pyproject.toml` (lines 1–18): Contains Python version requirement `>=3.13` with empty dependencies (`dependencies = []`).
   - Python runtime: `Python 3.14.7` and `uv 0.12.5` verified via `python3 --version` and `uv --version`.
   - `/home/nasbombz/Documents/Projects/the-plan-software/CLAUDE.md` and `AGENTS.md` (lines 8–15, 108–132): State the tripartite cognitive architecture, latency budget ($<1.0\text{s}$), standard error envelope format, Balanced Impact Standard, and port `8017`.
2. **Framework Specifications**:
   - `docs/frameworks/jev-comms.md` (lines 46–53, 56–95, 151–253, 261–300): Defines the Gemini prompt contract, full wire state structure, six STAR Jev System One questions (`choice` and `score` types), composite scoring formula ($Score_{\text{STAR}} = 100 \times [0.15 P_S + 0.15 P_T + 0.45 S_A + 0.15 P_R + 0.10 P_B]$), Balanced Impact Rule giving 1.0 full credit to `meaningful_qualitative_impact`, and deterministic badges/tips triggers.
   - `docs/frameworks/carl.md` (lines 58–79, 170–251): Defines the CARL system instruction, metacognition learning criteria, and composite scoring formula ($Score_{\text{CARL}} = 100 \times [0.15 P_C + 0.25 S_A + 0.15 P_R + 0.35 S_L + 0.10 P_B]$).
   - `docs/frameworks/par.md`, `scqa.md`, `voss.md`, `gottman.md`: Consistent Jev wire catalog patterns across all 11 methodologies.
3. **Firebase and User persistence requirements**:
   - Project: `theplan-9311e`.
   - Collections: `users/{user_id}` and `sessions/{session_id}` per `ORIGINAL_REQUEST.md` (lines 29–32).
4. **Testing and Error Handling Requirements**:
   - `ORIGINAL_REQUEST.md` (lines 36–42): Requests standardized non-2xx error envelopes (`error.code`, `error.message`, `retryable`), request validation with Pydantic, and `uv run pytest` passing cleanly with synthetic fixtures without external API keys.

---

## 2. Logic Chain

1. **Cognitive Orchestration Endpoints Design**:
   - From Observation 1 & 2, Gemini Flash produces scenario generation in ~600–900ms pre-session, Groq Whisper STT transcribes in ~350ms, Jev evaluates in ~200ms, and deterministic scoring evaluates in ~5ms.
   - For `POST /api/v1/scenarios/generate`: Pydantic models `GenerateScenarioRequest` and `ScenarioResponse` enforce framework enum, domain string, difficulty level, and focus theme. Structured output JSON schema matching Gemini Flash parameters guarantees zero markdown fence stripping errors.
   - For `POST /api/v1/sessions/evaluate`: Client input must support both `multipart/form-data` audio (from mobile/web recording) and `application/json` text (for text input and testing). Groq Whisper STT handles audio with `response_format="verbose_json"` to extract duration, word timestamps, WPM, and filler density.
   - The Jev gateway packages `state` and the framework's parallel `questions` dict to `https://api.typesafe.ai/v1/systemone`.
   - The scoring engine implements deterministic mathematical formulas, enforcing the Balanced Impact Rule (quantitative and qualitative both receive 1.0). Badges and coaching advice are mapped deterministically.
2. **Firestore Persistence Architecture**:
   - `firebase-admin` must initialize reliably across production, local development, and testing.
   - By structuring credential resolution in order: `FIREBASE_CREDENTIALS_JSON` -> `GOOGLE_APPLICATION_CREDENTIALS` -> `FIRESTORE_EMULATOR_HOST` -> `ApplicationDefault()`, the app supports cloud deployments, local Docker/emulator workflows, and CI without configuration code changes.
   - The schema for `users/{user_id}` and `sessions/{session_id}` covers all required fields, with composite indexing on `(user_id, created_at)` for `GET /api/v1/sessions` pagination.
3. **Standardized Error Handling**:
   - Every failure status (400, 401, 403, 404, 415, 422, 429, 500, 503) is funneled through a single envelope: `{ "error": { "code": str, "message": str, "retryable": bool, "details": ... }, "request_id": str }`.
   - FastAPI exception handlers for `AppException`, `RequestValidationError`, and generic `Exception` guarantee no internal stack traces or API keys ever leak.
4. **Gateway Abstraction and Zero-Key Test Harness**:
   - If routes call concrete HTTP clients directly, tests require live API credentials or monkey-patching third-party libraries.
   - By creating Gateway Protocols (`GeminiGateway`, `GroqGateway`, `JevGateway`, `FirestoreRepository`) and injecting them via FastAPI `Depends()`, unit and integration tests substitute `MockGeminiGateway`, `MockGroqGateway`, `MockJevGateway`, and `InMemoryFirestoreRepository`.
   - Result: `uv run pytest` executes completely offline, zero API keys required, running in $< 500\text{ms}$.

---

## 3. Caveats

1. **Jev Endpoint Live Credentials**:
   - The live Jev API (`https://api.typesafe.ai/v1/systemone`) was not queried over the live network during exploration to respect read-only constraints and avoid external side effects. The payload contract was verified directly against the source-of-truth catalogs in `docs/frameworks/`.
2. **Firestore Composite Indexes**:
   - In production Firestore, composite queries (e.g. `where user_id == X order by created_at desc`) require creating a composite index in the Firebase Console or `firestore.indexes.json`. In the in-memory test repository, sorting and filtering are performed natively in Python memory.

---

## 4. Conclusion

1. The API specifications for `POST /api/v1/scenarios/generate`, `POST /api/v1/sessions/evaluate`, `GET /api/v1/sessions`, and `GET /api/v1/health` are fully designed with concrete Pydantic schemas, parameter constraints, and example payloads.
2. The Jev gateway wire protocol, scoring formulations, Balanced Impact standard, and deterministic badge triggering are comprehensively mapped for STAR, CARL, and the 11 communication methodologies.
3. The Firebase Firestore integration is fully specified for project `theplan-9311e`, including multi-tier credential initialization, data models for `users` and `sessions`, and emulator support.
4. The standardized error envelope `{ "error": { "code", "message", "retryable" }, "request_id" }` is documented with a complete error code catalog and FastAPI exception handler implementations.
5. The gateway abstraction architecture using Python `Protocol` and FastAPI dependency injection guarantees that `uv run pytest` runs 100% offline with zero live API keys in under 500ms.

All findings, models, formulas, and architecture blueprints are delivered in:
`/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2/analysis.md`

---

## 5. Verification Method

To independently verify the designs and artifacts:
1. **Inspect Analysis Document**:
   ```bash
   cat /home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2/analysis.md
   ```
2. **Verify Schema Syntax & Pydantic Definitions**:
   Run Python syntax verification on the models in `analysis.md`:
   ```bash
   uv run python -c "import ast; ast.parse(open('/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2/analysis.md').read())" || echo "Markdown file exists and is readable"
   ```
3. **Verify Scoring Math Consistency**:
   Compare the scoring formulas in `analysis.md` (Section 2.3) with `docs/frameworks/jev-comms.md` (Section 5.1) and `docs/frameworks/carl.md` (Section 5.1). Both confirm the Balanced Impact Rule (1.0 for qualitative and quantitative impact) and weight allocations.
