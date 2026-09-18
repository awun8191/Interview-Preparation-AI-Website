# E2E Test Infra: The-Plan-Software Backend

## Test Philosophy
- Opaque-box, requirement-driven test suite derived from `ORIGINAL_REQUEST.md`, `CLAUDE.md`, and `docs/frameworks/`.
- Zero live external API key requirement: Test suite must run 100% synthetically via abstract gateway dependency injection or synthetic providers in < 1 second.
- Methodology: Category-Partition + Boundary Value Analysis (BVA) + Pairwise Combinations + Real-World Workload Testing.

## Feature Inventory & Test Mapping
| # | Feature | Requirement Source | Tier 1 (Min 5) | Tier 2 (Min 5) | Tier 3 (Pairwise) | Tier 4 (Scenario) |
|---|---------|-------------------|:--------------:|:--------------:|:-----------------:|:-----------------:|
| 1 | Health Check (`GET /api/v1/health`) | `ORIGINAL_REQUEST.md §1` | 5 | 5 | ✓ | ✓ |
| 2 | Scenario Gen (`POST /api/v1/scenarios/generate`) | `ORIGINAL_REQUEST.md §1` | 5 | 5 | ✓ | ✓ |
| 3 | Audio Session Eval (`POST /api/v1/sessions/evaluate`) | `ORIGINAL_REQUEST.md §1` | 5 | 5 | ✓ | ✓ |
| 4 | Text Session Eval (`POST /api/v1/sessions/evaluate`) | `ORIGINAL_REQUEST.md §1` | 5 | 5 | ✓ | ✓ |
| 5 | Session History (`GET /api/v1/sessions`) | `ORIGINAL_REQUEST.md §1` | 5 | 5 | ✓ | ✓ |
| 6 | Standardized Error Envelope | `ORIGINAL_REQUEST.md Acceptance` | 5 | 5 | ✓ | ✓ |
| 7 | Balanced Impact Rule | `ORIGINAL_REQUEST.md Acceptance` | 5 | 5 | ✓ | ✓ |
| 8 | 11 Frameworks Scoring Math | `ORIGINAL_REQUEST.md §1` | 11 | 11 | ✓ | ✓ |
| 9 | Firestore Persistence (`users`, `sessions`) | `ORIGINAL_REQUEST.md §2` | 5 | 5 | ✓ | ✓ |

## Test Architecture
- Test Runner: `uv run pytest`
- Location: `backend/tests/`
- Test Fixtures & Synthetic Gateway Injection: `backend/tests/conftest.py`
- Pass/Fail semantics: All tests pass with exit code 0; zero ruff lint errors (`uv run ruff check .`); zero ruff format errors (`uv run ruff format --check .`).

## Coverage Thresholds
- Tier 1: Feature Coverage (>=5 test cases per core feature/endpoint)
- Tier 2: Boundary & Corner Cases (>=5 test cases covering invalid payloads, empty strings, corrupt audio, extremes, division by zero)
- Tier 3: Cross-Feature Combinations (Pairwise coverage of frameworks × audio/text × roles × outcome types)
- Tier 4: Real-World Executive Coaching Scenarios (>=6 complex real-world scenarios: STAR behavioral interview, CARL executive retro, PAR quick pitch, SCQA executive board briefing, SBI camera-test feedback, Gottman de-escalation with contempt penalty)
- **Total Minimum Target:** > 60 tests across unit, integration, and E2E suites.
