# Original User Request

## Initial Request — 2026-09-17T18:25:53Z

Build the production-ready FastAPI backend for The-Plan-Software communication coaching platform, integrating Gemini for scenario generation, Groq for speech-to-text, TypeSafe AI (Jev) for deterministic grading, and Firebase (Cloud Firestore theplan-9311e) for session persistence.

Working directory: /home/nasbombz/Documents/Projects/the-plan-software/backend
Integrity mode: development

Reference material: ../docs/frameworks/ (11 communication frameworks: STAR, CARL, PAR, SCQA, SBI, Radical Candor, STATE, Gottman, Voss, Sparkline, Monroe)

## Requirements

### R1. Cognitive Orchestration Endpoints
Implement the FastAPI application exposing:
- `POST /api/v1/scenarios/generate`: Generates authentic, role-tailored practice prompts via Gemini Flash.
- `POST /api/v1/sessions/evaluate`: Receives audio or text + prompt metadata, executes Groq STT (if audio), evaluates Jev System One questions in parallel against `docs/frameworks/` rubrics, calculates deterministic scores and coaching badges, and persists the session to Firestore.
- `GET /api/v1/sessions`: Retrieves session history for a user from Firestore.
- `GET /api/v1/health`: Liveness check.

### R2. Firebase Firestore Persistence
Connect to Firebase project `theplan-9311e` using `firebase-admin` to persist streamlined `users` and `sessions` collections per the data model:
- `users/{user_id}`: `email`, `display_name`, `role` (`user` | `admin`), `subscription_tier` (`free` | `pro`), `created_at`.
- `sessions/{session_id}`: `user_id`, `framework`, `prompt`, `transcript`, `score` (0–100), `findings` (Jev map), `tips` (list of strings), `created_at`.

### R3. Test Suite & Verification Harness
Deliver automated synthetic unit and integration tests using `pytest` verifying request validation, gateway error handling, scoring math, and Firestore operations.

## Acceptance Criteria

### API Functionality & Contracts
- [ ] Endpoints validate requests using Pydantic and return standardized non-2xx error envelopes (`error.code`, `error.message`, `retryable`).
- [ ] Jev gateway correctly formats `state` and parallel `questions` dict matching the schemas in `../docs/frameworks/`.
- [ ] Scoring engine computes composite scores (0–100) and triggers appropriate coaching tips.
- [ ] Balanced Impact Rule enforced: both qualitative/operational outcomes and quantitative metrics receive full credit.

### Verification & Testing
- [ ] `uv run pytest` passes cleanly with synthetic fixtures (no external API keys required during test suite).
- [ ] `uv run ruff check .` and `uv run ruff format --check .` pass with zero errors.
