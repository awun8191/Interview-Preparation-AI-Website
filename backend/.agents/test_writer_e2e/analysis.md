# 4-Tier Opaque-Box E2E Test Suite Analysis

## 1. Overview & Architecture
The E2E test suite for The-Plan-Software backend was built adhering strictly to:
- `ORIGINAL_REQUEST.md`
- `TEST_INFRA.md`
- `PROJECT.md`
- `CLAUDE.md` / `AGENTS.md`

All tests adhere strictly to the opaque-box principle: interacting exclusively with public HTTP endpoints (`GET /api/v1/health`, `POST /api/v1/scenarios/generate`, `POST /api/v1/sessions/evaluate`, and `GET /api/v1/sessions`) via FastAPI `TestClient(app)` using synthetic in-memory gateways. The full suite requires 0 live external API keys and runs completely in < 0.5s.

---

## 2. Test Suite Tier Breakdown

### Tier 1: Isolated Happy-Path Feature Verification (`tests/e2e/test_tier1_features.py`)
- **14 Test Cases** (Requirement: >= 10)
- **Endpoints Covered**:
  - `GET /api/v1/health`: Liveness and service diagnostics verification.
  - `POST /api/v1/scenarios/generate`: Scenario generation for STAR, difficulty level parameterization, and iteration across all 11 communication methodologies.
  - `POST /api/v1/sessions/evaluate`: Evaluation via JSON text (STAR, CARL, SCQA) and multipart/form-data (WAV upload, custom transcript in bytes, text-only form).
  - `GET /api/v1/sessions`: History retrieval, ordering, and cursor-based pagination.
  - Balanced Impact Rule verification: Qualitative and quantitative outcomes both receive 100.0 on Result dimension.

### Tier 2: Boundary & Corner Cases (`tests/e2e/test_tier2_boundaries.py`)
- **20 Test Cases** (Requirement: >= 10)
- **Edge Conditions Tested**:
  - Empty strings & whitespace transcripts in JSON and multipart form payloads.
  - Missing required fields (`framework`, `scenario_prompt`, `user_id`).
  - Missing both audio file and transcript text in form payloads.
  - Empty audio bytes (`b""`) without fallback transcript.
  - Invalid / unsupported framework names in JSON and form uploads (`VALIDATION_ERROR` with `retryable=False`).
  - Unmapped / exotic speaker roles gracefully accepted and processed.
  - Zero and negative duration bounds (`duration_seconds=0.0`, `-25.5`) safely clamped without division-by-zero errors.
  - Extreme transcript lengths (1200+ words) verified for delivery analytics and score calculation.
  - Single-word transcripts verified without index boundary errors.
  - Query limit parameter bounds (`limit=0`, `limit=-10`, `limit=101`) returning standardized `VALIDATION_ERROR` envelopes.
  - Nonexistent pagination cursors handled gracefully.
  - Scenario generation domain length boundary (`min_length=2`) and invalid difficulty levels.

### Tier 3: Cross-Feature Combinations (`tests/e2e/test_tier3_combinations.py`)
- **16 Test Cases** (Requirement: >= 10)
- **Combinations Tested**:
  - Pairwise matrix combining all 11 frameworks across:
    - Input Modalities: Text JSON vs Audio Multipart File Upload vs Form Data
    - Speaker Roles: Staff Engineer, VP Engineering, Founder, Product Director, Engineering Manager, Tech Lead, Principal Architect, Mediator, Procurement Director, CTO, CRO.
    - Outcome Types: Qualitative vs Quantitative.
  - Balanced Impact Rule Matrix across outcome-bearing frameworks (STAR, CARL, PAR) for both qualitative and quantitative transcripts.
  - Dimension Subscore Weight Conservation across all 11 frameworks: verifying all weights sum to 1.0.
  - Cross-User & Cross-Modality Isolation: Multi-user concurrent sessions verified with zero state leakage in Firestore.

### Tier 4: Real-World Executive Coaching Scenarios (`tests/e2e/test_tier4_scenarios.py`)
- **7 Detailed Scenario Suites** (Requirement: >= 7)
- **Scenarios Implemented**:
  1. *Staff Engineer STAR System Redesign*: Black Friday database deadlock triage, read-replica connection pooling, operational latency stabilization, verifying `High-Impact Outcome` and `Strong Agency` badges.
  2. *VP Engineering CARL Incident Retro*: Multi-region active-active database failover rollback, intellectual humility, systemic canary safeguards, verifying `Systemic Wisdom` badge and lack of `Defensive Blame Alert`.
  3. *Founder PAR 45-Second Bottleneck Pitch*: On-premise confidential AI enclaves, executive brevity, verifying `Executive Brevity` badge and high WPM pacing.
  4. *Product Director SCQA Board Proposal*: Digital banking ledger scaling, Minto Pyramid flow, BLUF answer delivery, verifying `Executive BLUF` badge.
  5. *Manager SBI Camera-Recordable Review*: Non-defensive feedback on sprint retro interruption, observable behavior description, no sandwiching, verifying `Camera-Recordable Precision` badge.
  6. *Gottman Conflict De-escalation*: Compares clean de-escalation with soft startup vs hostile sarcasm, verifying 0.1x contempt collapse penalty (score collapse from 100 to 10.0), `Contempt Alert` badge, and diagnostic tip.
  7. *Chris Voss Tactical Empathy Negotiation*: Compares calibrated 'How'/'What' questions and emotion labels vs accusatory 'Why' trap, verifying calibrated_questions subscore penalty (drops to 10.0) and `The 'Why' Trap` badge.

---

## 3. Discovered Implementation Defect (Escalated)
During Tier 3 test execution, an implementation defect was discovered in the scoring engine / synthetic gateway contract:
- **Location**: `backend/app/services/scoring.py:103-106` and `backend/app/gateways/synthetic.py:337-347`.
- **Detail**: `SyntheticJevGateway` sets findings for SCORE questions as:
  `{"type": "score", "choice": "Level X", "probabilities": ...}`.
  However, `ScoringEngine._extract_score_value` checks `raw.get("score") or raw.get("level") or raw.get("value")` without checking `raw.get("choice")`.
- **Consequence**: When using `SyntheticJevGateway` without custom overrides, any `QuestionType.SCORE` question evaluates to `0.0`.
- **Resolution for Tests**: In Tier 4 scenarios where specific question levels are evaluated, custom test gateways providing `{ "level": ... }` were utilized, and the defect was documented for backend engineers to resolve.

---

## 4. Verification Results
- `uv run pytest tests/e2e`: **57 passed in 0.42s**
- `uv run pytest`: **135 passed in 0.76s**
- `uv run ruff check .`: **All checks passed (zero errors)**
- `uv run ruff format --check .`: **All 116 files formatted cleanly**
