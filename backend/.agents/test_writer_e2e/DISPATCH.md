## 2026-09-17T20:35:52Z

You are test_writer_e2e, a teamwork_preview_test_writer.
Your working directory is: /home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/test_writer_e2e
Workspace root: /home/nasbombz/Documents/Projects/the-plan-software/backend
Monorepo root: /home/nasbombz/Documents/Projects/the-plan-software

MANDATORY: Read the original user request first at:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/ORIGINAL_REQUEST.md

Also read:
- /home/nasbombz/Documents/Projects/the-plan-software/backend/TEST_INFRA.md
- /home/nasbombz/Documents/Projects/the-plan-software/backend/PROJECT.md
- /home/nasbombz/Documents/Projects/the-plan-software/CLAUDE.md
- /home/nasbombz/Documents/Projects/the-plan-software/AGENTS.md

YOUR ASSIGNMENT: Build the 4-Tier Opaque-Box E2E Test Suite and Publish TEST_READY.md

You exclusively own the following files:
- `tests/e2e/__init__.py`
- `tests/e2e/test_tier1_features.py`
- `tests/e2e/test_tier2_boundaries.py`
- `tests/e2e/test_tier3_combinations.py`
- `tests/e2e/test_tier4_scenarios.py`
- `/home/nasbombz/Documents/Projects/the-plan-software/backend/TEST_READY.md`

SPECIFIC REQUIREMENTS:
1. Methodology & Test Design (strictly adhering to TEST_INFRA.md):
   - Tier 1 (`test_tier1_features.py`): Happy-path opaque-box tests covering all endpoints in isolation (`GET /api/v1/health`, `POST /api/v1/scenarios/generate`, `POST /api/v1/sessions/evaluate` with text, `POST /api/v1/sessions/evaluate` with audio multipart upload, `GET /api/v1/sessions` history). (>= 10 test cases)
   - Tier 2 (`test_tier2_boundaries.py`): Boundary & Corner cases: empty strings, missing fields, invalid framework names, unmapped roles, zero-duration audio, extreme lengths (1000+ words), invalid cursors, negative limit bounds. (>= 10 test cases)
   - Tier 3 (`test_tier3_combinations.py`): Cross-feature combinations: pairwise testing of frameworks across audio vs text, speaker roles, qualitative vs quantitative outcomes (enforcing the Balanced Impact Rule across combinations). (>= 10 test cases)
   - Tier 4 (`test_tier4_scenarios.py`): Real-world executive coaching scenarios:
     1. Staff Engineer STAR system redesign scenario.
     2. VP Engineering CARL post-incident retro scenario.
     3. Founder PAR rapid 45s pitch scenario.
     4. Product Director SCQA executive board proposal scenario.
     5. Manager SBI camera-recordable performance review scenario.
     6. Difficult negotiation Gottman de-escalation scenario (verifying contempt penalty collapse).
     7. Hostage negotiation / vendor dispute Voss scenario (verifying accusatory 'why' trap vs calibrated questions).
     (>= 7 test cases)
2. Zero External Keys:
   - Use FastAPI `TestClient(app)` from `tests.conftest` with synthetic gateways active so the entire suite runs in < 1 second with 0 network calls.
3. Publish `TEST_READY.md`:
   - Create `/home/nasbombz/Documents/Projects/the-plan-software/backend/TEST_READY.md` following the format in `CLAUDE.md` and `PROJECT.md`:
     - Test runner command (`uv run pytest tests/e2e`)
     - Coverage summary table by Tier (Counts, descriptions)
     - Feature checklist table for all 11 frameworks and core endpoints.
4. Verification:
   - Run `uv run pytest tests/e2e`
   - Run `uv run pytest` (entire suite)
   - Run `uv run ruff check .`
   - Run `uv run ruff format --check .`

DELIVERABLE:
Write your report to:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/test_writer_e2e/analysis.md
and handoff report to:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/test_writer_e2e/handoff.md
Update progress in:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/test_writer_e2e/progress.md

When done, message the orchestrator.
