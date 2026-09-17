## 2026-09-17T18:27:28Z
You are explorer_2, a teamwork_preview_explorer.
Your working directory is: /home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2
Workspace root: /home/nasbombz/Documents/Projects/the-plan-software/backend
Monorepo root: /home/nasbombz/Documents/Projects/the-plan-software

MANDATORY: Read the original user request first at:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/ORIGINAL_REQUEST.md

Also read:
- /home/nasbombz/Documents/Projects/the-plan-software/CLAUDE.md
- /home/nasbombz/Documents/Projects/the-plan-software/AGENTS.md

YOUR TASK:
Investigate and design external integrations, data models, and API contracts for the backend:
1. Cognitive Orchestration Endpoints:
   - POST /api/v1/scenarios/generate: input/output schema, Gemini Flash prompt engineering, role-tailored scenarios.
   - POST /api/v1/sessions/evaluate: input (audio multipart vs text JSON), Groq Whisper STT invocation (model, audio format handling), Jev gateway dispatch format (state + questions dict matching frameworks), scoring math (composite 0-100), coaching tips generation, badge triggering.
   - GET /api/v1/sessions: query params (user_id, pagination/limit), response schema.
   - GET /api/v1/health: liveness check schema.
2. Firebase Firestore Integration:
   - Project: `theplan-9311e`.
   - `firebase-admin` initialization (credentials handling via env/file vs default app, emulator/mocking for tests).
   - Data model specifications:
     - `users/{user_id}`: email, display_name, role (user | admin), subscription_tier (free | pro), created_at.
     - `sessions/{session_id}`: user_id, framework, prompt, transcript, score (0-100), findings (Jev map), tips (list of strings), created_at.
3. Standardized Error Handling:
   - Pydantic validation error envelopes and API error envelope format: `{ "error": { "code": "...", "message": "...", "retryable": bool } }`.
4. Testing & Gateway abstraction strategy:
   - How to architect gateways so `uv run pytest` runs purely with synthetic fixtures/mocks with no live API keys needed.

DELIVERABLE:
Write your design and analysis to:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2/analysis.md
and handoff report to:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2/handoff.md
Update your progress in:
/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/explorer_2/progress.md

Do NOT modify files outside your working directory.
When done, send a message to orchestrator with your findings and file paths.
