/**
 * Stamps the build with what it actually is.
 *
 * Writes `dist/version.json`, which the Worker serves at `/version.json` — the
 * quickest way to answer "what is live right now?" without shipping any
 * telemetry into the app itself.
 *
 * The version comes from `package.json`; the commit prefers the CI-provided
 * `GITHUB_SHA` and falls back to reading git locally.
 */

const distDir = new URL("../dist", import.meta.url).pathname;

function run(cmd: string[]): string | null {
  try {
    const proc = Bun.spawnSync(cmd, { stdout: "pipe", stderr: "ignore" });
    if (proc.exitCode !== 0) return null;
    return proc.stdout.toString().trim() || null;
  } catch {
    return null;
  }
}

async function main(): Promise<void> {
  const pkg = (await Bun.file(new URL("../package.json", import.meta.url)).json()) as {
    name: string;
    version: string;
  };

  const commit =
    process.env.GITHUB_SHA?.slice(0, 12) ??
    run(["git", "rev-parse", "--short=12", "HEAD"]) ??
    "unknown";

  const branch =
    process.env.GITHUB_REF_NAME ??
    run(["git", "rev-parse", "--abbrev-ref", "HEAD"]) ??
    "unknown";

  const version = {
    name: pkg.name,
    version: pkg.version,
    commit,
    branch,
    builtAt: new Date().toISOString(),
  };

  await Bun.write(`${distDir}/version.json`, `${JSON.stringify(version, null, 2)}\n`);
  console.log(`version.json → ${version.name} v${version.version} (${commit} on ${branch})`);
}

await main();
