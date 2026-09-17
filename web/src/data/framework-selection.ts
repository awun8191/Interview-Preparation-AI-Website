/**
 * Framework selection guidance.
 *
 * AUTHORED CONTENT. This is the one part of the brief that is not derived from
 * docs/frameworks/*.md, which contain no framework-selection guidance at all.
 * It is educational copy, not rubric criteria, and it does not affect scoring.
 *
 * Review or replace the wording here freely; regenerating the briefs
 * (bun run briefs) will not overwrite this file.
 */

import type { Framework } from "../lib/types";

export type SelectionGuidance = {
  reachFor: string[];
  holdOff: string[];
  pairsWith?: string;
};

export const FRAMEWORK_SELECTION: Record<Framework, SelectionGuidance> = {
  STAR: {
    reachFor: [
      "Behavioral interview rounds where you are asked to prove past execution.",
      "Any question that begins with tell me about a time.",
      "Demonstrating individual ownership inside what was a team effort.",
    ],
    holdOff: [
      "Hypothetical or forward-looking questions, which ask for a plan rather than a story.",
      "Screening calls with under a minute, where PAR carries the same evidence faster.",
      "A live disagreement, which needs de-escalation rather than a retrospective.",
    ],
    pairsWith: "CARL when the panel cares more about what you learned than what you shipped.",
  },
  CARL: {
    reachFor: [
      "Senior and leadership loops where self-awareness is part of what is being tested.",
      "Questions about failure, a decision you would reverse, or a lesson that stuck.",
      "Situations where the systemic safeguard matters more than personal credit.",
    ],
    holdOff: [
      "Early screening rounds, where the interviewer still wants evidence of execution.",
      "When you have no genuine learning to offer, because a forced lesson reads as a platitude.",
      "Rapid-fire rounds with no room for metacognition.",
    ],
    pairsWith: "STAR when the story's outcome matters more than its lesson.",
  },
  PAR: {
    reachFor: [
      "Recruiter screens and phone rounds where you have 45 to 60 seconds.",
      "Executive updates where the headline matters more than the narrative.",
      "Moments where the listener has already decided and needs the punchline.",
    ],
    holdOff: [
      "Deep technical rounds where the panel wants to probe your reasoning.",
      "Situations so complex that cutting the context makes your actions look arbitrary.",
    ],
    pairsWith: "STAR when you have 90 seconds and the panel wants the reasoning.",
  },
  SCQA: {
    reachFor: [
      "Recommending a decision to people who outrank you.",
      "Written updates and memos where the reader might stop after the first line.",
      "Steering meetings where the room needs the recommendation before the reasoning.",
    ],
    holdOff: [
      "Interview answers about your own past work, which are stories rather than arguments.",
      "Emotionally charged conversations, where leading with the conclusion reads as dismissive.",
    ],
    pairsWith: "Sparkline when the recommendation needs a story, not just a structure.",
  },
  SBI: {
    reachFor: [
      "Delivering corrective feedback to a peer or a report.",
      "Describing a behaviour you need changed without attacking the person.",
      "Any moment where you must separate an observable act from your interpretation of it.",
    ],
    holdOff: [
      "Praising someone, where a plain acknowledgement lands better than a formula.",
      "Disciplinary or contractual conversations that belong in a formal process.",
      "When you cannot name the specific behaviour, because SBI collapses without it.",
    ],
  },
  RADICAL_CANDOR: {
    reachFor: [
      "One-to-ones where you have been avoiding a hard message.",
      "Correcting a strong performer whose behaviour is costing the rest of the team.",
      "Any moment where you notice yourself softening a critique past the point of usefulness.",
    ],
    holdOff: [
      "Public settings, because critique in front of others becomes obnoxious aggression.",
      "Before the relationship exists, since challenge without demonstrated care reads as attack.",
      "Purely technical disagreements where no relationship is at risk.",
    ],
  },
  STATE: {
    reachFor: [
      "High-stakes disagreements where opinions differ and emotions are running high.",
      "Telling someone news they will not want to hear.",
      "Resetting a conversation that has turned defensive on both sides.",
    ],
    holdOff: [
      "Routine updates and low-stakes decisions, where the protocol is overkill.",
      "When the other party has no ability or appetite to change the outcome.",
      "Emergencies, which need clear direction first and dialogue second.",
    ],
    pairsWith: "Gottman when the conversation has already escalated past facts.",
  },
  GOTTMAN: {
    reachFor: [
      "A conflict that has moved from the issue onto the person.",
      "Co-founder or partner deadlocks where the relationship outlasts the disagreement.",
      "Repairing damage after you were the one who escalated.",
    ],
    holdOff: [
      "Negotiations over terms, where the goal is a settlement rather than a repaired relationship.",
      "When you are calm and thinking clearly, because a time-out then reads as avoidance.",
      "Settings where any acknowledgement of fault will be read as weakness.",
    ],
    pairsWith: "VOSS when the relationship is intact and you need to trade rather than repair.",
  },
  VOSS: {
    reachFor: [
      "Negotiating terms where you need information more than you need to be right.",
      "Breakdowns where the other side has gone quiet, emotional, or positional.",
      "Salary, vendor, and deadline conversations with a real counterpart.",
    ],
    holdOff: [
      "Internal decisions that only need a rational comparison of options.",
      "When you must issue a directive rather than discover what the other side needs.",
      "Short exchanges, where labeling every emotion reads as technique rather than conversation.",
    ],
  },
  SPARKLINE: {
    reachFor: [
      "Keynotes, all-hands, and vision talks where you are changing how people see something.",
      "Pitches where you need the audience to want the future you are describing.",
      "Any talk where the audience is comfortable with the status quo.",
    ],
    holdOff: [
      "Operational reviews and status updates, where the audience wants numbers rather than narrative.",
      "When you have under two minutes, because the oscillation needs room to land.",
      "Closing a specific decision that a direct ask would move faster.",
    ],
    pairsWith: "Monroe when the talk must end in a specific ask.",
  },
  MONROE: {
    reachFor: [
      "Sales demos and investor pitches where you need a commitment at the end.",
      "Budget requests that require an approval today.",
      "Any proposal where the audience does not yet feel the problem.",
    ],
    holdOff: [
      "Informational talks with no ask attached.",
      "Audiences who already agree with you, where establishing need wastes their patience.",
      "When there is no single clear action you can ask for.",
    ],
    pairsWith: "Sparkline when you want belief rather than a signed decision.",
  },
};
