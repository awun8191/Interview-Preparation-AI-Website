# Technical Analysis & Implementation Report: Milestone 2
**Gateway Layer, Data Models & Delivery Analytics Service**
**Author:** worker_m2 (Teamwork Worker)  
**Target Project:** `theplan-9311e` | **Environment:** Python >= 3.13 (`uv`)

---

## 1. Executive Summary

Milestone 2 delivers the core foundational data contracts, external service gateways, synthetic offline test providers, and speech delivery analytics engine for **The-Plan-Software** backend.

All components were built strictly adhering to the **Integrity Mandate**:
1. **Pydantic Data Models**: Exhaustive models for scenarios (`FrameworkEnum` for all 11 frameworks, `DifficultyLevel`, `GenerateScenarioRequest`, `ScenarioResponse`), evaluations (`EvaluateSessionRequest`, `ScorecardSubscore`, `BadgeItem`, `EvaluateSessionResponse`, `JevEvaluationState`), and persistence records (`UserRecord`, `SessionRecord`, `SessionListResponse`).
2. **Gateway Protocols**: Abstract structural contracts (`GeminiGatewayProtocol`, `GroqGatewayProtocol`, `JevGatewayProtocol`, `FirestoreGatewayProtocol`) facilitating dependency inversion.
3. **Concrete Live Gateways**: Production-grade async HTTP and SDK clients for Google Gemini Flash, Groq Whisper Large-v3 STT, TypeSafe AI Jev System One, and Firebase Cloud Firestore (`theplan-9311e`).
4. **Synthetic Test Providers**: 100% offline in-memory test implementations with deterministic scenario generation, acoustic timestamp generation, genuine Jev heuristic grading enforcing the **Balanced Impact Rule** (1.0 for both qualitative operational outcomes and quantitative metrics), and thread-safe Firestore collection emulation with cursor pagination.
5. **FastAPI Dependency Injection**: `Depends()` providers with automatic synthetic fallback when `USE_SYNTHETIC_GATEWAYS=True` or when provider API credentials are unconfigured.
6. **Delivery Analytics Service**: Sub-5ms calculation of Words Per Minute ($WPM$), division-by-zero protection, 8-phrase filler word breakdown ("um", "uh", "like", "you know", "sort of", "kind of", "actually", "basically"), filler density percentage, and pause/power-pause detection ($\ge 0.5\text{s}$ and $\ge 1.5\text{s}$).

---

## 2. Component Breakdown & Architecture

### 2.1 Pydantic Models (`app/models/`)

- **`app/models/scenario.py`**:
  - `FrameworkEnum`: String enum supporting the 11 communication frameworks:
    `STAR`, `CARL`, `PAR`, `SCQA`, `SBI`, `RADICAL_CANDOR`, `STATE`, `GOTTMAN`, `VOSS`, `SPARKLINE`, `MONROE`.
  - `DifficultyLevel`: `beginner`, `intermediate`, `advanced`.
  - `GenerateScenarioRequest`: Accepts `target_framework` (aliased with `framework`), `user_domain` (min 2, max 120 chars), `difficulty_level`, and optional `focus_theme`.
  - `ScenarioResponse`: Returns structured scenario metadata including `scenario_id`, `title`, `context_background`, `prompt_question`, `key_dimensions_to_test`, and `target_duration_seconds`.
- **`app/models/evaluation.py`**:
  - `EvaluateSessionRequest`: Ingests `framework`, `speaker_role`, `scenario_prompt`, optional `scenario_context`, optional `transcript`, and optional `duration_seconds`.
  - `ScorecardSubscore`: Per-dimension scores (`dimension`, `score`, `weight`, `feedback`).
  - `BadgeItem`: Earned badges and warnings (`badge_id`, `title`, `description`, `category`).
  - `JevEvaluationState`: Context payload dispatched to TypeSafe AI Jev System One wire protocol.
  - `TranscriptionResult`: Structured speech-to-text response containing transcript, duration, and word-level timestamp intervals.
  - `EvaluateSessionResponse`: Unified client evaluation response containing score (0-100), subscores, raw Jev findings, deterministic tips, badges, and delivery metrics.
- **`app/models/session.py`**:
  - `UserRecord`: Firestore `users/{user_id}` schema (`user_id`, `email`, `display_name`, `role` in `["user", "admin"]`, `subscription_tier` in `["free", "pro"]`, `created_at`, `updated_at`).
  - `SessionRecord`: Firestore `sessions/{session_id}` schema (`session_id`, `user_id`, `framework`, `prompt`, `transcript`, `score`, `findings`, `tips`, `badges`, `delivery_metrics`, `created_at`).
  - `SessionListResponse`: Paginated session summaries with `items`, `total`, and pagination `cursor`.

### 2.2 Gateway Protocols & Concrete Implementations

- **`app/gateways/protocols.py`**:
  Defines runtime-checkable protocols:
  - `GeminiGatewayProtocol.generate_scenario(request: GenerateScenarioRequest) -> ScenarioResponse`
  - `GroqGatewayProtocol.transcribe_audio(audio_bytes: bytes, filename: str) -> TranscriptionResult`
  - `JevGatewayProtocol.evaluate_questions(state, questions) -> dict[str, Any]` and alias `evaluate`
  - `FirestoreGatewayProtocol`: `save_user`, `get_user`, `save_session`, `get_user_sessions`
- **`app/gateways/gemini.py` (`GeminiGateway`)**:
  Connects to Google Gemini Flash REST API (`generateContent`) using `httpx.AsyncClient`. Uses system instructions tailored to executive communication frameworks and parses strict JSON output. Includes 429 rate limit mapping and 503 provider unavailability handling.
- **`app/gateways/groq.py` (`GroqGateway`)**:
  Streams multipart audio payloads to Groq Whisper (`whisper-large-v3`) with `verbose_json` response formatting and `timestamp_granularities[]="word"`. Handles 25MB file size limits and returns `TranscriptionResult`.
- **`app/gateways/typesafe.py` (`TypeSafeGateway`)**:
  Executes parallel rubric evaluation against `https://api.typesafe.ai/v1/systemone` using JSON payload containing `state` context and `questions` criteria map.
- **`app/gateways/firestore.py` (`FirestoreGateway`)**:
  Initializes `firebase_admin` client for project `theplan-9311e` with support for `FIRESTORE_EMULATOR_HOST`, service account JSON, or GCP Application Default Credentials. Implements document CRUD and reverse-chronological query pagination on `sessions`.

### 2.3 Synthetic Gateways (`app/gateways/synthetic.py`)

1. **`SyntheticGeminiGateway`**: Generates high-fidelity scenarios across all 11 frameworks dynamically tailored to the user's role, domain, difficulty level, and focus theme.
2. **`SyntheticGroqGateway`**: Simulates high-speed speech-to-text with word-level start/end timestamps and acoustic pauses between sentences (0.6s) and clauses (0.3s). Supports buffer-based text injection for deterministic testing.
3. **`SyntheticJevGateway`**: Implements genuine heuristic question evaluation matching rubric criteria. Strictly enforces the **Balanced Impact Rule**:
   - Both quantitative metrics (`quantified_metric_impact`) and qualitative operational resolutions (`meaningful_qualitative_impact`) are awarded full credit (1.0).
   - Accurately scores Action agency levels (`Level 4` / `Level 5` for "I led", "I designed", "I diagnosed"; `Level 2` for passive "we" phrasing).
4. **`SyntheticFirestoreGateway`**: In-memory repository with `asyncio.Lock` thread-safety, simulating Firestore `users` and `sessions` collections with reverse-chronological ordering and cursor-based pagination. Includes a `clear()` method for test isolation.

### 2.4 Dependency Injection (`app/gateways/dependencies.py`)

FastAPI dependency functions provide instances of each gateway:
- `get_gemini_gateway(settings: Settings = Depends(get_settings))`
- `get_groq_gateway(settings: Settings = Depends(get_settings))`
- `get_jev_gateway(settings: Settings = Depends(get_settings))`
- `get_firestore_gateway(settings: Settings = Depends(get_settings))`

When `settings.USE_SYNTHETIC_GATEWAYS` is True OR when the respective provider API key/credentials are empty, the dependency provider automatically returns the shared synthetic instance. This enables 100% offline execution of all unit and integration tests without network access or API credentials.

### 2.5 Delivery Analytics Service (`app/services/analytics.py`)

Function `calculate_delivery_analytics(transcript, duration_seconds, word_timestamps)` computes:
- **`word_count`**: Total words in the clean transcript.
- **`duration_seconds`**: Non-negative speech duration.
- **`words_per_minute`**: $WPM = \frac{\text{word\_count}}{\text{duration\_seconds}} \times 60$, safely clamped to 0.0 when $\text{duration} \le 0$ or $\text{word\_count} = 0$.
- **`filler_count` & `filler_words_breakdown`**: Exact count of 8 target fillers using boundary regex:
  - Multi-word: `"you know"`, `"sort of"`, `"kind of"`
  - Single-word: `"um"`, `"uh"`, `"like"`, `"actually"`, `"basically"`
- **`filler_density_percentage`**: $\frac{\text{filler\_count}}{\text{word\_count}} \times 100$, rounded to 2 decimal places.
- **`pause_count`**: Number of inter-word silence intervals $\ge 0.5\text{s}$.
- **`power_pauses_count`**: Number of inter-word silence intervals $\ge 1.5\text{s}$.

---

## 3. Verification & Test Results

Executed commands:
```bash
uv run pytest tests/unit/test_delivery_analytics.py tests/unit/test_synthetic_gateways.py
uv run pytest
uv run ruff check app/models app/gateways app/services/analytics.py app/services/__init__.py tests/unit/test_delivery_analytics.py tests/unit/test_synthetic_gateways.py
uv run ruff format --check app/models app/gateways app/services/analytics.py app/services/__init__.py tests/unit/test_delivery_analytics.py tests/unit/test_synthetic_gateways.py
```

### Test Output Summary
- `tests/unit/test_delivery_analytics.py`: 10 passed in 0.03s
- `tests/unit/test_synthetic_gateways.py`: 15 passed in 0.15s
- Full test suite (`tests/`): 37 passed in 0.24s
- Ruff Lint: 0 violations across all owned files.
- Ruff Format: 100% compliant across all owned files.
