# The-Plan-Software: AI Agent Guidelines & Architecture Manual
**Repository Standard for AI Coding Agents across Backend, Mobile, Web, and Docs**

---

## 1. Project Overview & Mission

**The-Plan-Software** is an executive-grade communication and interview coaching system. It evaluates spoken answers against 11 empirically validated communication methodologies (e.g., STAR, CARL, PAR, SCQA, SBI, Radical Candor, STATE, Gottman, Voss Tactical Empathy, Duarte Sparkline, Monroe's Motivated Sequence) derived from *The Plan: Life as an Engineering System*.

The platform operates on a **tripartite cognitive architecture**:
1. **Generation (Gemini Flash):** Crafts dynamic, authentic practice prompts tailored to the user's role and target framework.
2. **Perception (Groq Whisper Large-v3):** High-speed speech-to-text ($<400\text{ms}$) with word timestamps, $WPM$, pause detection, and filler word density.
3. **Judgment (TypeSafe AI Jev System One):** Fast, non-generative, typed rubric evaluation ($<250\text{ms}$) using `choice`, `score`, and `noul` primitives.
4. **Instant Scorecard (Deterministic Rules):** Pure mathematical scoring and badge synthesis ($<10\text{ms}$)—zero token-streaming delay.

---

## 2. Monorepo Directory Structure

```
the-plan-software/
├── backend/            # Python 3.13+ API (uv, FastAPI, Gemini, Groq, Jev)
├── mobile/             # Flutter / Dart Cross-Platform Mobile Client (Android & iOS)
├── web/                # Bun + TypeScript / React Web Client
├── docs/
│   └── frameworks/     # Source-of-truth specifications & Jev wire catalogs
├── AGENTS.md           # Master Agent Guidelines (This Document)
└── CLAUDE.md           # Root agent configuration
```

---

## 3. Subsystem Guides & Toolchains

### 3.1 `backend/` (Python API & Orchestration Engine)
* **Environment & Tools:** Python $\ge 3.13$ managed strictly with **`uv`**. Never use raw `pip` or global environments.
* **Key Commands:**
  * Sync dependencies: `uv sync`
  * Add dependencies: `uv add <package>`
  * Run server: `uv run uvicorn app.main:app --host 127.0.0.1 --port 8018 --reload`
  * Run tests: `uv run pytest`
  * Linting & Formatting: `uv run ruff check .` and `uv run ruff format .`
* **Responsibilities:**
  * `app/gateways/gemini.py`: Prompt generation service using Gemini Flash API.
  * `app/gateways/groq.py`: Audio multipart upload to Groq Whisper (`whisper-large-v3`).
  * `app/gateways/typesafe.py`: Parallel evaluation gateway to TypeSafe AI endpoint (`https://api.typesafe.ai/v1/systemone`).
  * `app/services/analytics.py`: Pacing ($WPM$), filler density, and power pause calculations.
  * `app/services/scoring.py`: Deterministic scorecards and coaching badges.
* **Environment Variables (`backend/.env`):**
  * `TYPESAFE_API_KEY`: Secret API credential for Jev.
  * `GROQ_API_KEY`: Secret API credential for Groq Whisper.
  * `GEMINI_API_KEY`: Secret API credential for Google Gemini.

---

### 3.2 `mobile/` (Flutter Cross-Platform Client)
* **Environment & Tools:** Flutter 3.x / Dart $\ge 3.13.2$.
* **Key Commands:**
  * Fetch packages: `flutter pub get`
  * Run analyzer: `dart analyze`
  * Run unit & widget tests: `flutter test`
  * Run debug app: `flutter run`
* **Core Responsibilities:**
  * Audio recording and live waveform visualization (`record` or `flutter_sound`).
  * Educational drawer displaying framework philosophy, sentence stems, and failure modes from `docs/frameworks/`.
  * Audio playback and real-time scorecard presentation.
* **Architecture Rules:**
  * Follow layered architecture: `data/` (repositories, API clients), `domain/` (models, state), `presentation/` (widgets, screens, providers/bloc).
  * Always request mic permissions cleanly using `permission_handler`.

---

### 3.3 `web/` (Bun + TypeScript Client)
* **Environment & Tools:** **Bun** is the mandatory runtime and package manager. **Never use Node.js, npm, yarn, or pnpm.**
* **Key Commands:**
  * Install dependencies: `bun install`
  * Run tests: `bun test`
  * Run development server: `bun run dev` (or `bun --hot index.ts`)
  * Build for production: `bun run build`
* **Conventions:**
  * Use `Bun.serve()` for backend/SSR endpoints when needed.
  * Use built-in `Bun.file` and `bun:sqlite` if local caching is required.
  * TypeScript with strict type-checking (`bun run typecheck`).

---

### 3.4 `docs/frameworks/` (Source of Truth for Communication Knowledge)
Every agent working on evaluation logic or UI copy **must read the corresponding specification** before writing code:
* **Track 1 (Interviews):**
  * [`star.md`](docs/frameworks/star.md): Situation, Task, Action, Result (balanced quantitative & qualitative impact).
  * [`carl.md`](docs/frameworks/carl.md): Context, Action, Result, Learning (executive metacognition & systemic safeguards).
  * [`par.md`](docs/frameworks/par.md): Problem, Action, Result (45–60s executive brevity).
* **Track 2 (Executive Communication):**
  * [`scqa.md`](docs/frameworks/scqa.md): Barbara Minto's Pyramid Principle / BLUF.
  * [`sbi.md`](docs/frameworks/sbi.md): Center for Creative Leadership feedback (camera-recordable behaviors).
  * [`radical_candor.md`](docs/frameworks/radical_candor.md): Care Personally + Challenge Directly 2×2 matrix.
* **Track 3 (High-Stakes Dialogue & Conflict):**
  * [`state.md`](docs/frameworks/state.md): Crucial Conversations (facts-first, tentative language).
  * [`gottman.md`](docs/frameworks/gottman.md): De-escalation, Four Horsemen countermeasures, repair attempts.
* **Track 4 (Negotiation):**
  * [`voss.md`](docs/frameworks/voss.md): Tactical Empathy, calibrated questions, emotion labeling, Ackerman bargaining.
* **Track 5 (Presentations & Persuasion):**
  * [`sparkline.md`](docs/frameworks/sparkline.md): Nancy Duarte's "What Is" vs. "What Could Be" oratorical rhythm.
  * [`monroe.md`](docs/frameworks/monroe.md): Monroe's 5-step motivated persuasion sequence.

---

## 4. Universal Rules for AI Agents

1. **Sub-Second Latency Budget:**
   * Audio Upload $\rightarrow$ Groq STT ($\sim 350\text{ms}$) $\rightarrow$ Jev System One ($\sim 200\text{ms}$) $\rightarrow$ Deterministic Scorecard ($\sim 5\text{ms}$).
   * The total end-to-end feedback loop must complete in **$< 1.0\text{ second}$**. Do not inject slow, heavy autoregressive LLMs into the grading critical path.
2. **Never Invent Rubric Criteria:**
   * Jev questions, primitives (`choice`, `score`, `noul`), instructions, and criteria options are strictly defined in `docs/frameworks/`. Do not alter question IDs or criteria keys without updating the specifications.
3. **Balanced Impact Standard:**
   * Never require strictly numerical metrics for high scores. Both quantitative data AND meaningful qualitative/operational outcomes receive full credit.
4. **Clean API & Envelope Contracts:**
   * Every non-2xx response must adhere to the standard error envelope:
     ```json
     {
       "error": {
         "code": "PROVIDER_UNAVAILABLE",
         "message": "Human-readable safe explanation.",
         "retryable": true
       },
       "request_id": "req_uuid"
     }
     ```
   * Never leak raw server stack traces, API keys, or provider tokens to clients.
5. **No Hallucinated Scores:**
   * Ratings and scores must be derived strictly from Jev's reported choices, levels, or probabilities. Never fabricate a synthetic score.
