# The-Plan-Software Backend

FastAPI service for the communication coaching engine (Gemini scenarios, Groq Whisper STT,
TypeSafe Jev evaluation, deterministic scoring, Firestore persistence).

## Local development

```bash
uv sync
uv run uvicorn app.main:app --host 127.0.0.1 --port 8018 --reload
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

## Deployment (Google Cloud Run)

Project `theplan-9311e`, region `us-central1` — co-located with the `nam5` Firestore database.

```bash
# From backend/
gcloud run deploy the-plan-api \
  --source . \
  --project theplan-9311e \
  --region us-central1
```

Cloud Build builds the `Dockerfile` and pushes to Artifact Registry. The container listens on
`$PORT` (Cloud Run's default is 8080) via:

```
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
```

### Runtime configuration

- **Identity:** `the-plan-api@theplan-9311e.iam.gserviceaccount.com`, granted
  `roles/datastore.user`. Firestore authenticates with Application Default Credentials from the
  metadata server, so no service-account key is baked into the image or mounted at runtime.
- **Environment variables** live on the service. Update them with:

  ```bash
  gcloud run services update the-plan-api --region us-central1 --update-env-vars KEY=value
  ```

  Provider keys (`GEMINI_API_KEY`, `GROQ_API_KEY`, `TYPESAFE_API_KEY`) are currently plain env
  vars. Moving them to Secret Manager is worthwhile hardening.
- **CORS:** `CORS_ORIGINS` is pinned to the deployed frontend origins
  (`https://the-plan.raregazzetto.me` and `https://the-plan-web.nasirdaud2015.workers.dev`). Adding a
  domain requires updating it and redeploying:

  ```bash
  gcloud run services update the-plan-api --region us-central1 \
    --update-env-vars 'CORS_ORIGINS=...'
  ```

  Note: `--update-env-vars` splits on commas, so a JSON list must be applied with `--env-vars-file`.
- **Custom domain:** the API intentionally serves on its default `run.app` URL. Mapping
  `the-plan-api.raregazzetto.me` would require `gcloud domains verify` first.

Live service: https://the-plan-api-480187173082.us-central1.run.app
