# CI/CD

How this repository builds, tests, and deploys. All of it runs on GitHub Actions — pushing
to `main` is the only step required to ship.

## At a glance

| Workflow | File | Trigger | Target |
| :--- | :--- | :--- | :--- |
| **CI** | `.github/workflows/ci.yml` | every push, every PR | lint, format, tests, typecheck, build |
| **Deploy API** | `.github/workflows/deploy-api.yml` | push touching `backend/**` | Google Cloud Run |
| **Deploy Web** | `.github/workflows/deploy-web.yml` | push touching `web/**` | Cloudflare Workers |

Each deploy workflow also declares `workflow_dispatch`, so it can be run by hand:

```bash
gh workflow run deploy-api.yml
gh workflow run deploy-web.yml
gh run list --limit 5
```

| Service | URL |
| :--- | :--- |
| Website | https://the-plan.raregazzetto.me |
| Website (fallback) | https://the-plan-web.nasirdaud2015.workers.dev |
| API | https://the-plan-api-480187173082.us-central1.run.app |

---

## 1. CI (`ci.yml`)

Runs on every push and pull request. Two independent jobs, so a backend failure does not hide a
frontend one. Concurrent runs on the same ref cancel each other.

**`backend`** — working directory `backend/`, Python via `astral-sh/setup-uv` (pinned to `0.12.5`):

```bash
uv sync --frozen          # fails if uv.lock is out of sync with pyproject.toml
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

**`web`** — working directory `web/`, Bun via `oven-sh/setup-bun` (pinned to `1.4.2`):

```bash
bun install --frozen-lockfile
bun run typecheck
bun run build
```

Both use committed lockfiles (`uv.lock`, `bun.lock`), so CI resolves the same versions you get
locally. **If you change a dependency, commit the updated lockfile or CI will fail.**

---

## 2. Deploy API (`deploy-api.yml`)

Triggers on pushes that touch `backend/**` (or the workflow file itself).

Cloud Build builds `backend/Dockerfile` and Cloud Run serves the result. The container installs
dependencies with `uv sync --frozen --no-dev`, then runs:

```
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
```

Cloud Run injects `PORT`; 8080 is its default and the local fallback.

### Authentication — keyless

The workflow uses **Workload Identity Federation**, so no long-lived service-account key is
stored in GitHub. It exchanges a short-lived GitHub OIDC token for Google Cloud credentials
scoped to this repository.

| Setting | Value |
| :--- | :--- |
| Project | `theplan-9311e` |
| Region | `us-central1` (co-located with the `nam5` Firestore database) |
| Service | `the-plan-api` |
| Runtime identity | `the-plan-api@theplan-9311e.iam.gserviceaccount.com` |
| Deploy identity | `the-plan-deployer@theplan-9311e.iam.gserviceaccount.com` |
| WIF provider | `projects/480187173082/locations/global/workloadIdentityPools/github/providers/github` |

The OIDC provider is constrained by `attribute-condition = assertion.repository=='awun8191/the-plan-software'`,
so no other repository can authenticate as the deployer.

### Permissions

| Principal | Role | Why |
| :--- | :--- | :--- |
| runtime SA | `roles/datastore.user` | read/write Firestore |
| deployer SA | `roles/run.admin` | deploy Cloud Run services |
| deployer SA | `roles/iam.serviceAccountUser` | attach the runtime SA to the revision |
| deployer SA | `roles/cloudbuild.builds.editor` | build the image |
| deployer SA | `roles/artifactregistry.writer` | push the image |
| deployer SA | `roles/storage.admin` | Cloud Build staging bucket |
| deployer SA | `roles/serviceusage.serviceUsageConsumer` | quota/billing project binding |

### Configuration

**Environment variables live on the Cloud Run service, not in the workflow.** The deploy passes no
`--set-env-vars`, so a redeploy preserves whatever is already configured — including
`GEMINI_API_KEY`, `GROQ_API_KEY`, `TYPESAFE_API_KEY` and `CORS_ORIGINS`.

Firestore uses Application Default Credentials from the metadata server, so no credential file is
baked into the image or mounted at runtime.

---

## 3. Deploy Web (`deploy-web.yml`)

Triggers on pushes that touch `web/**` (or the workflow file itself).

```bash
bun install --frozen-lockfile
bun run build          # rm -rf dist && bun build … && bun scripts/postbuild.ts
bunx wrangler deploy
```

The Worker is **assets-only** — `wrangler.jsonc` declares an `assets` directory with
`not_found_handling: "single-page-application"` and has no `main` entry point.

| Setting | Value |
| :--- | :--- |
| Worker | `the-plan-web` |
| Custom domain | `the-plan.raregazzetto.me` (declared in `wrangler.jsonc` `routes`) |
| Account | `fc1b39ec01d49a7e05f1ae971deb8e8f` |

### The API URL is baked in at build time

`BUN_PUBLIC_API_BASE` is set in the workflow's `env:` and **inlined into the bundle by Bun** during
`bun run build` (via `--env='BUN_PUBLIC_*'`). It is not read at runtime, so **changing it requires a
rebuild and redeploy** — editing it in the Cloudflare dashboard does nothing.

If it is missing at build time the bundle falls back to `http://127.0.0.1:8018/api/v1` on localhost
and to the `api.the-plan.example` placeholder everywhere else, which looks like a broken site.

### Wrangler version matters

`wrangler` is pinned as a `web/` devDependency (`4.124.0`). `cloudflare/wrangler-action` defaults to
wrangler **3.90.0**, which predates assets-only Workers configs and fails with
`Missing entry-point: … or the 'main' config field`. Keeping wrangler declared locally means the
action uses 4.x and local deploys match CI. Bump it deliberately, not accidentally.

---

## Repository secrets

Set with `gh secret set <NAME> --repo awun8191/the-plan-software`.

| Secret | Where it comes from |
| :--- | :--- |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/480187173082/locations/global/workloadIdentityPools/github/providers/github` |
| `GCP_SERVICE_ACCOUNT` | `the-plan-deployer@theplan-9311e.iam.gserviceaccount.com` |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare dashboard, account ID |
| `CLOUDFLARE_API_TOKEN` | Cloudflare **My Profile → API Tokens → Create Token → Custom token** |

The Cloudflare token needs exactly one permission: **Account → Workers Scripts → Edit**, scoped to
the account above. Nothing else.

Rotate it by creating a replacement in the dashboard, then re-running `gh secret set` and triggering
`deploy-web.yml`. No code change is needed.

---

## Runbooks

### Point the website at a different API

1. Add the new origin to the API's `CORS_ORIGINS` (see below) — otherwise the browser blocks it.
2. Update `BUN_PUBLIC_API_BASE` in `.github/workflows/deploy-web.yml`.
3. Push, or `gh workflow run deploy-web.yml`.

### Change the API's CORS origins

`CORS_ORIGINS` is a JSON list. `gcloud run services update --update-env-vars` splits on commas, so a
JSON list **must** go through a file:

```bash
cat > /tmp/env.yaml <<'YAML'
CORS_ORIGINS: "[\"https://the-plan.raregazzetto.me\", \"https://example.com\"]"
YAML
gcloud run services update the-plan-api --region us-central1 \
  --env-vars-file /tmp/env.yaml
```

`--env-vars-file` **replaces the entire set**, so include every variable the service needs — or use
`--update-env-vars` for a single scalar value.

### Update a provider API key

```bash
gcloud run services update the-plan-api --region us-central1 \
  --update-env-vars TYPESAFE_API_KEY=...
```

Moving these to Secret Manager is worthwhile hardening and is not done yet.

### Roll back the API

```bash
gcloud run revisions list --service the-plan-api --region us-central1
gcloud run services update-traffic the-plan-api --region us-central1 \
  --to-revisions <revision-name>=100
```

### Add another frontend origin or subdomain

Attach the domain in `wrangler.jsonc`:

```jsonc
"routes": [
  { "pattern": "the-plan.raregazzetto.me", "custom_domain": true },
  { "pattern": "another.raregazzetto.me", "custom_domain": true }
]
```

Cloudflare creates the DNS record and certificate automatically. Note that adding a custom domain
disables the `workers.dev` route unless `"workers_dev": true` is also set — which it is here, so both
URLs stay live.

---

## Troubleshooting

| Symptom | Cause |
| :--- | :--- |
| Site loads but every action fails with a network/CORS error | The origin is not in the API's `CORS_ORIGINS`. |
| Site calls `127.0.0.1:8018` or `api.the-plan.example` in production | `BUN_PUBLIC_API_BASE` was missing at build time; rebuild and redeploy. |
| `Missing entry-point: … 'main' config field` | Wrangler resolved to 3.x. Ensure `wrangler` is installed in `web/`. |
| `iam.serviceAccounts.getAccessToken denied` right after IAM changes | Propagation delay; re-run the workflow after a minute. |
| Deep link such as `/practice/` loads HTML instead of the app | Asset paths regressed to relative; `scripts/postbuild.ts` should make them absolute. |
| `uv sync --frozen` fails in CI but works locally | `uv.lock` is stale — run `uv sync` locally and commit it. |
| Web deploy fails with `CLOUDFLARE_API_TOKEN` missing | The secret is unset or the token was revoked. |
