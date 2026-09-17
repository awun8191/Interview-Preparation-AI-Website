export type Framework =
  | "STAR"
  | "CARL"
  | "PAR"
  | "SCQA"
  | "SBI"
  | "RADICAL_CANDOR"
  | "STATE"
  | "GOTTMAN"
  | "VOSS"
  | "SPARKLINE"
  | "MONROE";

export type Difficulty = "beginner" | "intermediate" | "advanced";

export interface FrameworkMeta {
  id: Framework;
  name: string;
  tagline: string;
  track: string;
}

export const FRAMEWORKS: FrameworkMeta[] = [
  { id: "STAR", name: "STAR", tagline: "Situation, Task, Action, Result — balanced interview stories", track: "Interviews" },
  { id: "CARL", name: "CARL", tagline: "Context, Action, Result, Learning — executive reflection", track: "Interviews" },
  { id: "PAR", name: "PAR", tagline: "Problem, Action, Result — 60-second executive brevity", track: "Interviews" },
  { id: "SCQA", name: "SCQA", tagline: "Situation, Complication, Question, Answer — BLUF structuring", track: "Executive" },
  { id: "SBI", name: "SBI", tagline: "Situation, Behavior, Impact — camera-clear feedback", track: "Executive" },
  { id: "RADICAL_CANDOR", name: "Radical Candor", tagline: "Care Personally + Challenge Directly", track: "Executive" },
  { id: "STATE", name: "STATE", tagline: "Facts-first crucial conversations under pressure", track: "Dialogue" },
  { id: "GOTTMAN", name: "Gottman", tagline: "De-escalation and repair, minus the Four Horsemen", track: "Dialogue" },
  { id: "VOSS", name: "Voss", tagline: "Tactical empathy and calibrated questions", track: "Negotiation" },
  { id: "SPARKLINE", name: "Sparkline", tagline: "What-Is vs What-Could-Be presentation rhythm", track: "Persuasion" },
  { id: "MONROE", name: "Monroe", tagline: "Five-step motivated sequence to action", track: "Persuasion" },
];

export interface Scenario {
  scenario_id: string;
  title: string;
  context_background: string;
  prompt_question: string;
  key_dimensions_to_test: string[];
  target_duration_seconds: number;
  target_framework: Framework;
  difficulty_level: Difficulty;
}

export interface Subscore {
  dimension: string;
  score: number;
  weight: number;
  feedback?: string | null;
}

export interface ClarityAssessment {
  score: number;
  level: string;
  clarity_level: string;
  ambiguity: string;
  ambiguous: boolean;
  feedback?: string | null;
}

export interface Badge {
  id: string;
  title: string;
  description: string;
  kind: "mastery" | "warning" | "delivery" | "insight";
}

export interface DeliveryMetrics {
  word_count?: number;
  duration_seconds?: number;
  words_per_minute?: number;
  filler_count?: number;
  filler_density_percentage?: number;
  pause_count?: number;
  power_pauses_count?: number;
  [key: string]: unknown;
}

export interface EvaluateResponse {
  session_id: string;
  user_id: string;
  framework: Framework;
  score: number;
  subscores: Subscore[];
  clarity?: ClarityAssessment | null;
  findings: Record<string, unknown>;
  tips: string[];
  badges: Badge[];
  delivery_metrics?: DeliveryMetrics | null;
  request_id?: string | null;
}

export class ApiError extends Error {
  code: string;
  retryable: boolean;
  requestId: string | null;
  details: unknown;

  constructor(code: string, message: string, retryable = false, requestId: string | null = null, details: unknown = null) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.retryable = retryable;
    this.requestId = requestId;
    this.details = details;
  }
}