# Project: The-Plan-Software Backend

## Architecture
Production-ready FastAPI backend implementing a tripartite cognitive architecture:
1. **Scenario Generation (Pre-session)**: Role- and framework-tailored scenario prompts via Google Gemini Flash.
2. **Perception Engine**: Sub-second speech-to-text with word-level timestamps and duration via Groq Whisper Large-v3.
3. **Delivery Analytics Engine**: Pacing ($WPM$), pause detection, filler word frequency count ($< 5\text{ms}$).
4. **Judgment Engine (Jev System One)**: Deterministic, typed rubric grading (`choice`, `score`, `noul`) evaluated in parallel over HTTP POST to TypeSafe AI in $\sim 120\text{--}280\text{ms}$.
5. **Deterministic Coaching & Scoring Engine**: Mathematical composite scoring (0--100), Balanced Impact Rule enforcement (full credit for both qualitative and quantitative outcomes), badge assignment, and targeted coaching tips in $< 10\text{ms}$.
6. **Persistence Engine**: Firebase Firestore (`theplan-9311e`) integration persisting `users` and `sessions` collections.
7. **Standardized Error Handling**: Uniform `{ "error": { "code": "...", "message": "...", "retryable": bool }, "request_id": "..." }` envelope.

```
                   [Client: Web / Mobile]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   POST /scenarios/generate           POST /sessions/evaluate
   (Gemini Flash Gateway)             (Audio / Text Input)
                                              │
                                              ▼
                                      Groq Whisper STT
                                              │
                                              ▼
                                      Delivery Analytics
                                      (WPM, Fillers, Pauses)
                                              │
                                              ▼
                                      Jev System One Wire
                                      (Parallel Evaluation)
                                              │
                                              ▼
                                      Deterministic Scoring
                                      (0-100, Badges, Tips)
                                              │
                                      ┌───────┴────────┐
                                      ▼                ▼
                                Client Response   Firestore DB
                                (< 1000ms E2E)   (theplan-9311e)
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Runtime Environment & Packaging | Python >= 3.13 configuration, `pyproject.toml` with `hatchling`, dependencies, `uv`, `ruff`, `pytest` | M1 | Survey |
| 2 | Core Configuration & Settings | Environment-driven settings with Pydantic BaseSettings, API keys, CORS, logging, constants | M1 | Survey |
| 3 | Standardized Error Envelope | Non-2xx envelope: `{ "error": { "code", "message", "retryable" }, "request_id" }` with global exception handlers | M1 | Survey |
| 4 | Liveness & Health Endpoint | `GET /api/v1/health` returning system status, version, and dependency check | M1 | Survey |
| 5 | Gemini Gateway Client | Client for Gemini Flash scenario prompt generation with protocol abstraction and synthetic mock | M2 | Survey |
| 6 | Groq STT Gateway Client | Multipart audio upload to Groq Whisper (`whisper-large-v3`) with protocol abstraction and synthetic mock | M2 | Survey |
| 7 | TypeSafe AI (Jev) Gateway Client | Parallel evaluation client dispatching `state` + `questions` to `https://api.typesafe.ai/v1/systemone` | M2 | Survey |
| 8 | Firebase Firestore Client | Client for project `theplan-9311e` using `firebase-admin` supporting emulator/creds with synthetic mock | M2 | Survey |
| 9 | Delivery Analytics Service | Calculates WPM, duration, pause count, filler word density from transcript and audio metadata | M2 | Survey |
| 10 | 11 Frameworks Question Catalog | Exhaustive catalog of Jev questions (`choice`, `score`, `noul`) for all 11 frameworks | M3 | Survey |
| 11 | Balanced Impact Rule | Grants equal full credit (1.0) for qualitative/operational outcomes and quantitative metrics | M3 | Survey |
| 12 | Deterministic Scoring Engine | Math formulas for 11 frameworks calculating composite score (0-100), subscores, non-linear steps | M3 | Survey |
| 13 | Badge & Coaching Tip Engine | Triggers UI badges and actionable improvement tips based on Jev criteria and analytics metrics | M3 | Survey |
| 14 | Scenario Generation Endpoint | `POST /api/v1/scenarios/generate` validating request and orchestrating Gemini scenario generator | M4 | Survey |
| 15 | Session Evaluation Endpoint | `POST /api/v1/sessions/evaluate` handling audio/text, Groq STT, Jev grading, scoring, and saving | M4 | Survey |
| 16 | Session History Endpoint | `GET /api/v1/sessions` retrieving paginated session history for a user from Firestore | M4 | Survey |
| 17 | Firestore Data Model Persistence | Schemas and persistence for `users/{user_id}` and `sessions/{session_id}` | M4 | Survey |
| 18 | Opaque-Box E2E Test Suite | Comprehensive synthetic test suite covering Tiers 1-4 across all 11 frameworks and endpoints | E2E | Survey |
| 19 | Adversarial Coverage Hardening | White-box stress testing, boundary fuzzing, error injection, edge cases (Tier 5) | E2E | Survey |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Suite | Independent opaque-box test harness & test suite (Tiers 1-4) creating `TEST_READY.md` | none | DONE |
| M1 | Core Foundation & Config | Packaging (`pyproject.toml`), environment settings, standardized error envelope, logging, and health endpoint | none | DONE |
| M2 | Gateway Clients & Delivery Analytics | Gemini, Groq, Jev, and Firestore clients with protocol interfaces & synthetic test providers, plus Delivery Analytics | M1 | DONE |
| M3 | 11 Frameworks & Scoring Engine | All 11 framework catalogs, Jev rubrics, Balanced Impact Rule, deterministic 0-100 scoring, badges, and tips | M1 | DONE |
| M4 | Cognitive Endpoints & Persistence | `POST /scenarios/generate`, `POST /sessions/evaluate`, `GET /sessions`, and Firestore persistence integration | M2, M3 | DONE |
| M5 | Final E2E Pass & Adversarial Hardening | Verify 100% pass of E2E test suite (Tiers 1-4), followed by Tier 5 adversarial hardening | E2E, M4 | DONE |

## Interface Contracts

### Gateway Protocol Abstractions (`app/gateways/protocols.py`)
```python
class GeminiGatewayProtocol(Protocol):
    async def generate_scenario(self, request: GenerateScenarioRequest) -> ScenarioModel: ...


class GroqGatewayProtocol(Protocol):
    async def transcribe_audio(self, audio_bytes: bytes, filename: str) -> TranscriptionResult: ...


class JevGatewayProtocol(Protocol):
    async def evaluate_questions(
        self, state: JevEvaluationState, questions: dict[str, Any]
    ) -> dict[str, Any]: ...


class FirestoreGatewayProtocol(Protocol):
    async def save_user(self, user: UserRecord) -> None: ...
    async def get_user(self, user_id: str) -> UserRecord | None: ...
    async def save_session(self, session: SessionRecord) -> str: ...
    async def get_user_sessions(
        self, user_id: str, limit: int = 20, cursor: str | None = None
    ) -> list[SessionRecord]: ...
```

### Error Envelope Schema (`app/core/errors.py`)
```json
{
  "error": {
    "code": "STRING_ENUM",
    "message": "Human readable error description",
    "retryable": false,
    "details": null
  },
  "request_id": "uuid-string"
}
```

### Scoring Engine Contract (`app/services/scoring.py`)
```python
class ScoringEngine:
    def score_session(
        self,
        framework: FrameworkEnum,
        jev_findings: dict[str, Any],
        analytics: DeliveryAnalyticsResult,
    ) -> ScorecardResult:
        # returns composite_score (0-100), subscores, badges, tips
        ...
```

## Code Layout
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application factory & routes inclusion
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py           # v1 router mounting sub-routers
│   │       ├── health.py           # GET /api/v1/health
│   │       ├── scenarios.py        # POST /api/v1/scenarios/generate
│   │       └── sessions.py         # POST /api/v1/sessions/evaluate, GET /api/v1/sessions
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Pydantic BaseSettings & env loading
│   │   ├── errors.py               # Standardized error envelope & custom exceptions
│   │   ├── exception_handlers.py   # Global FastAPI error handlers (422, 500, gateway errors)
│   │   └── logging.py              # Structured logging configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py               # ErrorEnvelope, RequestId, HealthStatus
│   │   ├── scenario.py             # ScenarioRequest, ScenarioResponse, FrameworkEnum
│   │   ├── evaluation.py           # EvaluateSessionRequest, EvaluateSessionResponse, Scorecard
│   │   └── session.py              # UserRecord, SessionRecord, SessionListResponse
│   ├── frameworks/
│   │   ├── __init__.py             # Framework registry
│   │   ├── base.py                 # Framework definition interface
│   │   ├── catalogs/               # Jev question catalogs & rubrics for all 11 frameworks
│   │   │   ├── star.py
│   │   │   ├── carl.py
│   │   │   ├── par.py
│   │   │   ├── scqa.py
│   │   │   ├── sbi.py
│   │   │   ├── radical_candor.py
│   │   │   ├── state.py
│   │   │   ├── gottman.py
│   │   │   ├── voss.py
│   │   │   ├── sparkline.py
│   │   │   └── monroe.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analytics.py            # Speech analytics (WPM, filler words, pauses)
│   │   ├── scoring.py              # Deterministic scoring engine (0-100, Balanced Impact)
│   │   ├── badges.py               # UI badge triggering logic
│   │   └── tips.py                 # Actionable coaching tip generator
│   └── gateways/
│       ├── __init__.py
│       ├── protocols.py            # Abstract Protocol definitions for DI
│       ├── dependencies.py         # FastAPI Depends() providers
│       ├── gemini.py               # Google Gemini Flash scenario generator
│       ├── groq.py                 # Groq Whisper STT client
│       ├── typesafe.py             # TypeSafe AI Jev System One client
│       ├── firestore.py            # Firebase Firestore client (theplan-9311e)
│       └── synthetic.py            # In-memory synthetic gateways for 100% offline tests
├── tests/
│   ├── conftest.py                 # Test fixtures, TestClient, synthetic gateway overrides
│   ├── e2e/
│   │   ├── test_tier1_features.py  # Tier 1: Happy-path feature coverage
│   │   ├── test_tier2_boundaries.py# Tier 2: Boundary & corner cases
│   │   ├── test_tier3_combinations.py # Tier 3: Cross-feature combinations
│   │   └── test_tier4_scenarios.py # Tier 4: Real-world communication scenarios
│   ├── integration/
│   │   ├── test_api_health.py
│   │   ├── test_api_scenarios.py
│   │   ├── test_api_sessions.py
│   │   └── test_firestore_persistence.py
│   └── unit/
│       ├── test_scoring_engine.py
│       ├── test_balanced_impact_rule.py
│       ├── test_delivery_analytics.py
│       ├── test_error_envelopes.py
│       └── test_framework_catalogs.py
├── pyproject.toml                  # Dependencies, hatchling build, ruff, pytest settings
└── README.md
```
