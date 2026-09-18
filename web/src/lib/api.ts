import {
  ApiError,
  type Badge,
  type Difficulty,
  type EvaluateResponse,
  type Framework,
  type Scenario,
} from "./types";
import { getUserId } from "./identity";

const DEV_API_BASE = "http://127.0.0.1:8018/api/v1";

// Reserved TLD (RFC 2606), so this deliberately never resolves. It stands in
// until the Cloud Run API is live and BUN_PUBLIC_API_BASE is supplied at build.
const PLACEHOLDER_API_BASE = "https://api.the-plan.example/api/v1";

function injectedApiBase(): string | undefined {
  try {
    // Bun statically replaces this at build time (see --env='BUN_PUBLIC_*' in
    // the build script). When the variable is absent the reference survives
    // un-replaced, so the try/catch keeps browsers from throwing on `process`.
    return process.env.BUN_PUBLIC_API_BASE;
  } catch {
    return undefined;
  }
}

export function apiBase(): string {
  const injected = injectedApiBase()?.trim();
  if (injected) return injected.replace(/\/$/, "");

  if (typeof window !== "undefined") {
    const { hostname } = window.location;
    if (hostname === "localhost" || hostname === "127.0.0.1" || hostname === "[::1]") {
      return DEV_API_BASE;
    }
  }

  return PLACEHOLDER_API_BASE;
}

function newRequestId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID();
  return `req-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
}

async function parseError(res: Response, requestId: string | null): Promise<never> {
  let code = `HTTP_${res.status}`;
  let message = `Request failed with status ${res.status}`;
  let retryable = res.status >= 500;
  let details: unknown = null;
  let rid = requestId ?? res.headers.get("X-Request-ID");
  try {
    const body = await res.json();
    if (body && typeof body === "object" && "error" in body) {
      const err = (body as { error: { code?: string; message?: string; retryable?: boolean; details?: unknown }; request_id?: string }).error;
      if (err?.code) code = String(err.code);
      if (err?.message) message = String(err.message);
      if (typeof err?.retryable === "boolean") retryable = err.retryable;
      if ("details" in err) details = err.details;
      if ((body as { request_id?: string }).request_id) rid = String((body as { request_id?: string }).request_id);
    }
  } catch {
    // fall through with defaults
  }
  throw new ApiError(code, message, retryable, rid, details);
}

async function fetchJson<T>(path: string, init: RequestInit, requestId: string): Promise<{ data: T; requestId: string | null }> {
  const res = await fetch(`${apiBase()}${path}`, {
    ...init,
    headers: {
      "X-Request-ID": requestId,
      ...(init.headers ?? {}),
    },
  });
  const rid = res.headers.get("X-Request-ID") ?? requestId;
  if (!res.ok) await parseError(res, rid);
  const data = (await res.json()) as T;
  return { data, requestId: rid };
}

export interface GenerateScenarioInput {
  framework: Framework;
  userDomain: string;
  difficulty: Difficulty;
  focusTheme?: string;
}

export async function generateScenario(input: GenerateScenarioInput): Promise<Scenario> {
  const { data } = await fetchJson<Scenario>(
    "/scenarios/generate",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        target_framework: input.framework,
        user_domain: input.userDomain,
        difficulty_level: input.difficulty,
        ...(input.focusTheme ? { focus_theme: input.focusTheme } : {}),
      }),
    },
    newRequestId(),
  );
  return data;
}

export function normalizeBadges(raw: unknown): Badge[] {
  if (!Array.isArray(raw)) return [];
  return raw.flatMap((b): Badge[] => {
    if (typeof b === "string") {
      return [{ id: b, title: b, description: "", kind: "insight" as const }];
    }
    if (b && typeof b === "object") {
      const obj = b as Record<string, unknown>;
      const id = String(obj.badge_id ?? obj.id ?? "BADGE");
      return [
        {
          id,
          title: String(obj.title ?? id),
          description: String(obj.description ?? ""),
          kind: (["mastery", "warning", "delivery", "insight"] as const).includes(obj.category as Badge["kind"])
            ? (obj.category as Badge["kind"])
            : "insight",
        },
      ];
    }
    return [];
  });
}

interface RawEvaluate {
  session_id: string;
  user_id: string;
  framework: Framework;
  score: number;
  subscores?: EvaluateResponse["subscores"];
  clarity?: EvaluateResponse["clarity"];
  findings?: Record<string, unknown>;
  tips?: string[];
  badges?: unknown;
  delivery_metrics?: EvaluateResponse["delivery_metrics"];
  delivery_analytics?: EvaluateResponse["delivery_metrics"];
}

function toEvaluateResponse(raw: RawEvaluate, requestId: string | null): EvaluateResponse {
  return {
    session_id: raw.session_id,
    user_id: raw.user_id,
    framework: raw.framework,
    score: raw.score,
    subscores: raw.subscores ?? [],
    clarity: raw.clarity ?? null,
    findings: raw.findings ?? {},
    tips: raw.tips ?? [],
    badges: normalizeBadges(raw.badges),
    delivery_metrics: raw.delivery_metrics ?? raw.delivery_analytics ?? null,
    request_id: requestId,
  };
}

export interface AnswerInput {
  framework: Framework;
  scenarioPrompt: string;
  scenarioContext?: string;
  speakerRole?: string;
  durationSeconds?: number;
}

export async function evaluateText(transcript: string, input: AnswerInput): Promise<EvaluateResponse> {
  const requestId = newRequestId();
  const { data } = await fetchJson<RawEvaluate>(
    "/sessions/evaluate",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        framework: input.framework,
        scenario_prompt: input.scenarioPrompt,
        transcript,
        speaker_role: input.speakerRole || "Professional",
        ...(input.scenarioContext ? { scenario_context: input.scenarioContext } : {}),
        ...(typeof input.durationSeconds === "number" ? { duration_seconds: input.durationSeconds } : {}),
        user_id: getUserId(),
      }),
    },
    requestId,
  );
  return toEvaluateResponse(data, requestId);
}

export async function evaluateAudio(audio: Blob, input: AnswerInput): Promise<EvaluateResponse> {
  const requestId = newRequestId();
  const form = new FormData();
  const ext = audio.type.includes("wav") ? "wav" : audio.type.includes("mp4") ? "m4a" : "webm";
  form.append("audio_file", audio, `answer.${ext}`);
  form.append("framework", input.framework);
  form.append("scenario_prompt", input.scenarioPrompt);
  form.append("speaker_role", input.speakerRole || "Professional");
  form.append("user_id", getUserId());
  if (input.scenarioContext) form.append("scenario_context", input.scenarioContext);
  const { data } = await fetchJson<RawEvaluate>("/sessions/evaluate", { method: "POST", body: form }, requestId);
  return toEvaluateResponse(data, requestId);
}
