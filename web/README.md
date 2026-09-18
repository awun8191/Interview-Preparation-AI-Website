# bun-react-template

To install dependencies:

```bash
bun install
```

To start a development server:

```bash
bun dev
```

To run for production:

```bash
bun start
```

This project was created using `bun init` in bun v1.4.0. [Bun](https://bun.com) is a fast all-in-one JavaScript runtime.

## Deployment

Deployed as a static SPA on Cloudflare Workers (static assets) via Wrangler. Config: `wrangler.jsonc`.

Live at:
- **https://the-plan.raregazzetto.me** (custom domain, declared in `wrangler.jsonc` `routes`)
- https://the-plan-web.nasirdaud2015.workers.dev (kept enabled via `workers_dev: true`)

```bash
bun run deploy                                              # build + wrangler deploy
BUN_PUBLIC_API_BASE="https://<api-host>/api/v1" bun run deploy   # point at a live API
```

`BUN_PUBLIC_API_BASE` is inlined at **build** time by Bun (`--env='BUN_PUBLIC_*'`), so it must be set when
`bun run build` runs — changing it requires a rebuild and redeploy. When unset, the bundle falls back to
`http://127.0.0.1:8018/api/v1` on localhost and to the `api.the-plan.example` placeholder everywhere else.

Current production value:

```bash
BUN_PUBLIC_API_BASE="https://the-plan-api-480187173082.us-central1.run.app/api/v1" bun run deploy
```

Adding an origin here means also allowing it in the API's `CORS_ORIGINS` (see `backend/README.md`), or the
browser will block the requests.

`bun scripts/postbuild.ts` rewrites asset references in `dist/index.html` to absolute paths, so deep links
such as `/practice/` resolve their JS/CSS correctly under the SPA fallback.

## Versioning

`bun scripts/version.ts` stamps each build into `dist/version.json` (version from `package.json`,
plus commit, branch and build time). The Worker serves it at `/version.json`:

```bash
curl -s https://the-plan.raregazzetto.me/version.json | jq
```

Bumping `version` in `package.json` is what cuts a release — the `Deploy Web` workflow verifies the
live commit and then tags `web-v<version>` with generated release notes. See
[../CI-CD.md](../CI-CD.md).
