# Handoff Report — explorer_1

**Date:** 2026-09-17  
**From:** `explorer_1` (teamwork_preview_explorer)  
**To:** `orchestrator_1` (teamwork_preview_orchestrator)  
**Working Directory:** `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_1`  
**Handoff Type:** Hard (Survey Task Complete)  

---

## 1. Observation

Direct observations made during codebase and environment inspection:

1. **Backend Directory Contents & Greenfield State:**
   - Command: `ls -la /home/nasbombz/Documents/Projects/the-plan-software/backend`
   - Observed files: `.git`, `.gitignore`, `.python-version`, `ORIGINAL_REQUEST.md`, `README.md` (0 bytes), `pyproject.toml` (347 bytes), `src/backend/__init__.py` (53 bytes).
   - `src/backend/__init__.py` content:
     ```python
     def main() -> None:
         print("Hello from backend!")
     ```
   - `pyproject.toml` content:
     ```toml
     [project]
     name = "backend"
     version = "0.1.0"
     description = "Add your description here"
     readme = "README.md"
     authors = [
         { name = "Dauda", email = "awun8191@gmail.com" }
     ]
     requires-python = ">=3.13"
     dependencies = []

     [project.scripts]
     backend = "backend:main"

     [build-system]
     requires = ["uv_build>=0.12.5,<0.13.0"]
     build-backend = "uv_build"
     ```
   - `backend/.gitignore` content: ignores `__pycache__/`, `*.py[oc]`, `build/`, `dist/`, `wheels/`, `*.egg-info`, `.venv`. Does not yet ignore `.env*`, `.pytest_cache/`, `.ruff_cache/`, or `.coverage`.

2. **Git Repository Status:**
   - Command in `backend/`: `git status`
   - Output: `On branch main, No commits yet. Untracked files: .agents/, .gitignore, .python-version, ORIGINAL_REQUEST.md, README.md, pyproject.toml, src/`
   - Command in monorepo root `/home/nasbombz/Documents/Projects/the-plan-software`: `git status`
   - Output: `fatal: not a git repository (or any of the parent directories): .git`

3. **Runtime & Toolchain Detection:**
   - Command: `which uv` $\rightarrow$ `/home/nasbombz/.local/bin/uv` (version `uv 0.12.5 (x86_64-unknown-linux-gnu)`).
   - Command: `uv python list` $\rightarrow$ `cpython-3.13.13-linux-x86_64-gnu` is installed at `/home/nasbombz/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13`.
   - `.python-version` content: `3.13`.
   - Command: `uv run python --version` $\rightarrow$ `Python 3.13.13` (uv created `.venv` on demand).
   - Command: `which ruff` $\rightarrow$ `which: no ruff in (...)`. Ruff and pytest must be added to `pyproject.toml` dev dependencies.

4. **Monorepo Guidelines & Architecture Standards:**
   - In `CLAUDE.md` (lines 35–53):
     - Server start command: `uv run uvicorn app.main:app --host 127.0.0.1 --port 8017 --reload`
     - Test command: `uv run pytest`
     - Lint & format command: `uv run ruff check .` and `uv run ruff format .` (and `uv run ruff format --check .`)
     - Gateway & service responsibilities explicitly placed under `app/`: `app/gateways/gemini.py`, `app/gateways/groq.py`, `app/gateways/typesafe.py`, `app/services/analytics.py`, `app/services/scoring.py`.
   - In `CLAUDE.md` (lines 108–132):
     - End-to-end feedback latency budget $< 1.0\text{s}$ (Audio $\rightarrow$ Groq $\sim 350\text{ms}$ $\rightarrow$ Jev $\sim 200\text{ms}$ $\rightarrow$ Scoring $\sim 5\text{ms}$).
     - Never invent rubric criteria (all defined in `docs/frameworks/`).
     - Balanced Impact Standard: full credit (1.0 weight) for qualitative/operational outcomes as well as quantitative metrics.
     - Standardized error envelope: `{"error": {"code": "...", "message": "...", "retryable": bool}, "request_id": "..."}`.
     - Zero stack trace or credential leakage.

5. **Framework Knowledge Base:**
   - Directory `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/` contains 12 comprehensive files (`carl.md`, `gottman.md`, `jev-comms.md`, `monroe.md`, `par.md`, `radical_candor.md`, `sbi.md`, `scqa.md`, `sparkline.md`, `star.md`, `state.md`, `voss.md`).
   - Every framework defines complete Jev wire catalogs (`choice`, `score`, `noul`), instructions, criteria maps, composite scoring weights, and coaching badge triggers.

6. **Agent Collaboration Scope:**
   - `explorer_2` is actively analyzing API contracts, external gateway request/response models, and Firestore data persistence.
   - `spec_miner_1` is actively extracting all 11 framework rubrics and question schemas from `docs/frameworks/`.

---

## 2. Logic Chain

1. **Premise:** Observations 1 and 2 establish that the backend directory contains solely an uncommitted initial scaffold created by `uv init` with no business logic or dependencies installed.
   - **Inference:** Greenfield setup is required; there is no existing code or legacy structure to preserve.

2. **Premise:** Observation 3 confirms that `uv 0.12.5` and Python 3.13 (`cpython-3.13.13`) are installed and functional.
   - **Inference:** The toolchain completely meets the monorepo requirements. All project management must strictly use `uv`.

3. **Premise:** Observation 4 shows `CLAUDE.md` mandates `uv run uvicorn app.main:app --host 127.0.0.1 --port 8017 --reload` and places responsibilities in `app/gateways/` and `app/services/`.
   - **Inference:** The default `uv init` structure (`src/backend`) does not align with the mandated `app.main:app` module path. The root backend package should be refactored to a top-level `app/` directory (`backend/app/...`) packaged via `hatchling` in `pyproject.toml`.

4. **Premise:** Observation 4 mandates that `uv run pytest` must pass cleanly with synthetic fixtures without external API keys.
   - **Inference:** Gateways (`GeminiGateway`, `GroqGateway`, `TypeSafeGateway`, `FirestoreGateway`) must adhere to abstract base interfaces or protocols, instantiated via FastAPI dependency injection (`app/api/deps.py`), allowing seamless synthetic mocking in `tests/conftest.py`.

5. **Premise:** Observation 4 and 5 define the Balanced Impact Rule, sub-second latency SLA, deterministic scoring math, and standardized non-2xx error envelopes.
   - **Inference:** Domain models must specify `ErrorEnvelope` with Pydantic; `app/core/handlers.py` must register global exception handlers for validation, gateway errors, and unexpected exceptions; and `app/services/scoring.py` must implement exact mathematical formulas and trigger rules without calling LLMs during scoring.

---

## 3. Caveats

1. **Live External API Keys:** No active `.env` file exists in the repository. Synthetic mocks are mandatory for test execution and local validation until live credentials (`TYPESAFE_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY`, Firebase service account) are supplied.
2. **Monorepo Git Root:** The root `/home/nasbombz/Documents/Projects/the-plan-software` is not a git repository; git is only initialized inside `backend/`. Any git commands executed by agents must run inside `backend/`.
3. **Web & Mobile Integration:** Both `mobile/` and `web/` are in early scaffold states and do not yet call backend endpoints. Backend contracts must adhere directly to `CLAUDE.md` and `docs/frameworks/`.

---

## 4. Conclusion

1. **Codebase Status:** Confirmed greenfield status. Pristine slate ready for full FastAPI backend implementation.
2. **Recommended Package & Directory Structure:**
   - Top-level `app/` structure: `app/main.py`, `app/api/v1/` (`health.py`, `scenarios.py`, `sessions.py`, `router.py`), `app/core/` (`config.py`, `handlers.py`, `exceptions.py`), `app/models/` (`common.py`, `scenario.py`, `session.py`, `user.py`, `jev.py`), `app/services/` (`analytics.py`, `scoring.py`, `persistence.py`, `scenario_service.py`, `evaluation_service.py`), and `app/gateways/` (`base.py`, `gemini.py`, `groq.py`, `typesafe.py`, `firestore.py`).
   - Co-located `tests/` directory with `unit/`, `integration/`, and `fixtures/`.
3. **Packaging Strategy:**
   - Update `pyproject.toml` with `build-backend = "hatchling.build"` exposing `packages = ["app"]`.
   - Add core dependencies: `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `httpx`, `firebase-admin`, `google-genai`, `python-multipart`, `python-dotenv`.
   - Add dev dependencies: `pytest`, `pytest-asyncio`, `pytest-mock`, `ruff`, `coverage`.
4. **Deliverable Reference:** Complete architectural details and configuration templates are recorded in `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_1/analysis.md`.

---

## 5. Verification Method

Once the implementation agent applies the proposed configuration and files:

1. **Verify Python & uv Environment:**
   ```bash
   cd /home/nasbombz/Documents/Projects/the-plan-software/backend
   uv --version
   uv run python --version
   # Expected: Python 3.13.x
   ```
2. **Verify Dependency Resolution & Sync:**
   ```bash
   uv sync
   # Expected: Installs fastapi, uvicorn, pydantic, ruff, pytest without conflicts
   ```
3. **Verify Linting & Formatting Compliance:**
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   # Expected: 0 errors, 0 warnings
   ```
4. **Verify Automated Test Suite:**
   ```bash
   uv run pytest
   # Expected: All synthetic unit and integration tests pass without network access
   ```
5. **Verify Server Execution & Liveness Probe:**
   ```bash
   uv run uvicorn app.main:app --host 127.0.0.1 --port 8017 &
   PID=$!
   sleep 2
   curl -s http://127.0.0.1:8017/api/v1/health
   # Expected: {"status": "ok", "version": "0.1.0", "environment": "development"}
   kill $PID
   ```
6. **Invalidation Conditions:**
   - Any dependency on Python $< 3.13.
   - Use of raw `pip` instead of `uv`.
   - Failure to return the standard error envelope on invalid requests.
   - Score penalties applied to qualitative/operational outcomes under the Balanced Impact Rule.
