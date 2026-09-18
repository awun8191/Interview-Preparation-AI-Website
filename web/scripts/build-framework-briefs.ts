/**
 * Generates web/src/data/framework-briefs.generated.ts from docs/frameworks/*.md
 *
 * The specs are wildly uneven (star.md is the umbrella product spec, gottman.md
 * has every section number shifted, monroe.md has no principles section at all),
 * so extraction is driven by an explicit per-framework map rather than heuristics.
 *
 * Run: bun run briefs
 */

import { join } from "node:path";
import type { Framework } from "../src/lib/types";

const DOCS_DIR = join(import.meta.dir, "..", "..", "docs", "frameworks");
const OUT_FILE = join(import.meta.dir, "..", "src", "data", "framework-briefs.generated.ts");

export type Run = { text: string; strong?: boolean; em?: boolean };

export type ListItem = { label?: Run[]; runs: Run[]; children?: ListItem[] };

export type Block =
  | { kind: "p"; runs: Run[] }
  | { kind: "ul"; items: ListItem[] }
  | { kind: "ol"; items: ListItem[] }
  | { kind: "table"; head: Run[][]; rows: Run[][][] }
  | { kind: "group"; heading: string; blocks: Block[] };

export type BriefSection = { heading: string; blocks: Block[] };

export type FrameworkBrief = {
  id: Framework;
  fullName: string;
  origin: string | null;
  why: Block[];
  sections: BriefSection[];
};

type SourceMap = {
  file: string;
  fullName: string;
  why: string;
  anatomy: string | null;
  principles: string | null;
};

const SOURCES: Record<Framework, SourceMap> = {
  STAR: {
    file: "star.md",
    fullName: "Situation, Task, Action, Result",
    why: "3.1",
    anatomy: "STAR Sentence Stems & Language Patterns",
    principles: "Key Evaluation Principles & Realistic Nuances",
  },
  CARL: {
    file: "carl.md",
    fullName: "Context, Action, Result, Learning",
    why: "1",
    anatomy: "Key Differences Between STAR and CARL",
    principles: "Core Evaluation Principles & Realistic Nuances",
  },
  PAR: {
    file: "par.md",
    fullName: "Problem, Action, Result",
    why: "1",
    anatomy: "Framework Comparison: STAR vs. CARL vs. PAR",
    principles: "Core Evaluation Principles & Realistic Nuances",
  },
  SCQA: {
    file: "scqa.md",
    fullName: "Situation, Complication, Question, Answer",
    why: "1",
    anatomy: "Framework Comparison: Narrative (STAR) vs. Structural (SCQA)",
    principles: "Core Evaluation Principles & Realistic Nuances",
  },
  SBI: {
    file: "sbi.md",
    fullName: "Situation, Behavior, Impact",
    why: "1",
    anatomy: "Traditional Feedback vs. SBI Feedback",
    principles: "Core Evaluation Principles & Realistic Nuances",
  },
  RADICAL_CANDOR: {
    file: "radical_candor.md",
    fullName: "Care Personally, Challenge Directly",
    why: "1",
    anatomy: "The Four Quadrants",
    principles: "Core Evaluation Principles & Realistic Nuances",
  },
  STATE: {
    file: "state.md",
    fullName: "Share facts, Tell your story, Ask, Talk tentatively, Encourage testing",
    why: "1",
    anatomy: "The 5 Elements of STATE",
    principles: "Core Evaluation Principles & Realistic Nuances",
  },
  GOTTMAN: {
    file: "gottman.md",
    fullName: "De-escalation and the Four Horsemen",
    why: "1",
    anatomy: "The Four Horsemen and Their Antidotes",
    principles: "Core Principles & Realistic Nuances",
  },
  VOSS: {
    file: "voss.md",
    fullName: "Tactical Empathy and Calibrated Questions",
    why: "1",
    anatomy: null,
    principles: "Core Negotiation Principles & Behavioral Nuances",
  },
  SPARKLINE: {
    file: "sparkline.md",
    fullName: "What Is against What Could Be",
    why: "1",
    anatomy: "The 5 Structural Pillars of Duarte's Sparkline",
    principles: "Core Presentation Principles & Realistic Nuances",
  },
  MONROE: {
    file: "monroe.md",
    fullName: "The Five Step Motivated Sequence",
    why: "1",
    anatomy: "The Five Steps of Monroe's Motivated Sequence",
    principles: null,
  },
};

type Heading = { level: number; title: string; index: number };

function stripCodeFences(lines: string[]): (string | null)[] {
  let insideFence = false;
  return lines.map((line) => {
    if (line.trimStart().startsWith("```")) {
      insideFence = !insideFence;
      return null;
    }
    return insideFence ? null : line;
  });
}

function deLatex(input: string): string {
  return input
    .replace(/\$\$/g, "")
    .replace(/\$/g, "")
    .replace(/\\rightarrow/g, "→")
    .replace(/\\leftarrow/g, "←")
    .replace(/\\Rightarrow/g, "⇒")
    .replace(/\\leq?\b/g, "≤")
    .replace(/\\geq?\b/g, "≥")
    .replace(/\\times/g, "×")
    .replace(/\\text\{([^}]*)\}/g, "$1")
    .replace(/\\[a-zA-Z]+/g, "")
    .replace(/[{}]/g, "");
}

function cleanText(input: string): string {
  return deLatex(input)
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function parseRuns(input: string): Run[] {
  const text = cleanText(input);
  const runs: Run[] = [];
  const pattern = /\*\*(.+?)\*\*|\*(.+?)\*/g;
  let cursor = 0;
  let match: RegExpExecArray | null;

  while ((match = pattern.exec(text)) !== null) {
    if (match.index > cursor) runs.push({ text: text.slice(cursor, match.index) });
    if (match[1] !== undefined) runs.push({ text: match[1], strong: true });
    else if (match[2] !== undefined) runs.push({ text: match[2], em: true });
    cursor = pattern.lastIndex;
  }
  if (cursor < text.length) runs.push({ text: text.slice(cursor) });

  return runs.filter((run) => run.text.length > 0);
}

function runsToText(runs: Run[]): string {
  return runs.map((run) => run.text).join("");
}

function splitLabel(text: string): { label?: Run[]; body: Run[] } {
  const bold = text.match(/^\*\*(.+?):\*\*\s*(.*)$/);
  if (bold) return { label: parseRuns(bold[1] ?? ""), body: parseRuns(bold[2] ?? "") };
  const italic = text.match(/^\*(.+?):\*\s*(.*)$/);
  if (italic) return { label: parseRuns(italic[1] ?? ""), body: parseRuns(italic[2] ?? "") };
  return { body: parseRuns(text) };
}

function parseBlocks(lines: (string | null)[]): Block[] {
  const blocks: Block[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    if (line == null || line.trim() === "" || /^-{3,}$/.test(line.trim())) {
      i += 1;
      continue;
    }

    const heading = line.match(/^(#{2,6})\s+(.*)$/);
    if (heading) {
      let j = i + 1;
      while (
        j < lines.length &&
        !(lines[j] !== null && /^(#{2,6})\s+/.test(lines[j]!))
      ) {
        j += 1;
      }
      const inner = parseBlocks(lines.slice(i + 1, j));
      blocks.push({
        kind: "group",
        heading: baseTitle(cleanText(heading[2]!)),
        blocks: inner,
      });
      i = j;
      continue;
    }

    if (line.trimStart().startsWith("|")) {
      const rows: Run[][][] = [];
      while (i < lines.length && lines[i] !== null && lines[i]!.trimStart().startsWith("|")) {
        const rawCells = lines[i]!
          .trim()
          .replace(/^\|/, "")
          .replace(/\|$/, "")
          .split("|")
          .map((cell) => cell.trim());
        if (!rawCells.every((cell) => /^:?-{2,}:?$/.test(cell) || cell === "")) {
          rows.push(rawCells.map((cell) => parseRuns(cell)));
        }
        i += 1;
      }
      if (rows.length > 0) {
        const [head, ...body] = rows;
        blocks.push({ kind: "table", head: head ?? [], rows: body });
      }
      continue;
    }

    const bullet = line.match(/^(\s*)[*+-]\s+(.*)$/);
    const numbered = line.match(/^(\s*)(\d+)\.\s+(.*)$/);

    if (bullet || numbered) {
      const ordered = Boolean(numbered);
      const items: ListItem[] = [];
      let current: ListItem | null = null;

      const memberPattern = ordered ? /^(\s*)\d+\.\s+(.*)$/ : /^(\s*)[*+-]\s+(.*)$/;
      const anyListPattern = /^(\s*)(?:\d+\.|[*+-])\s+(.*)$/;

      while (i < lines.length) {
        const candidate = lines[i];
        if (candidate == null) break;

        const member = candidate.match(memberPattern);
        const anyList = candidate.match(anyListPattern);
        if (!member) {
          const nestedIndent = anyList ? (anyList[1] ?? "").length : 0;
          if (!anyList || nestedIndent < 2) break;
        }

        const chosen = member ?? anyList!;
        const isNested = (chosen[1] ?? "").length >= 2;
        const parsed = splitLabel(chosen[2] ?? "");

        if (isNested && current) {
          current.children = current.children ?? [];
          current.children.push({ label: parsed.label, runs: parsed.body });
        } else {
          current = { label: parsed.label, runs: parsed.body };
          items.push(current);
        }
        i += 1;
      }

      blocks.push({ kind: ordered ? "ol" : "ul", items });
      continue;
    }

    const paragraph: string[] = [];
    while (
      i < lines.length &&
      lines[i] != null &&
      lines[i]!.trim() !== "" &&
      !lines[i]!.trimStart().startsWith("|") &&
      !/^\s*[*+-]\s+/.test(lines[i]!) &&
      !/^\s*\d+\.\s+/.test(lines[i]!) &&
      !/^-{3,}$/.test(lines[i]!.trim())
    ) {
      paragraph.push(lines[i]!.trim());
      i += 1;
    }
    if (paragraph.length > 0) {
      blocks.push({ kind: "p", runs: parseRuns(paragraph.join(" ")) });
    }
  }

  return blocks.filter((block) => {
    if (block.kind === "p") return block.runs.length > 0;
    if (block.kind === "table") return block.head.length > 0;
    if (block.kind === "group") return block.blocks.length > 0;
    return block.items.length > 0;
  });
}

function findHeadings(lines: (string | null)[]): Heading[] {
  const headings: Heading[] = [];
  lines.forEach((line, index) => {
    if (line === null) return;
    const match = line.match(/^(#{2,4})\s+(.*)$/);
    if (match) headings.push({ level: match[1]!.length, title: cleanText(match[2]!), index });
  });
  return headings;
}

function isNumbered(key: string): boolean {
  return /^\d+(\.\d+)*$/.test(key);
}

function baseTitle(title: string): string {
  return title.replace(/^\d+(?:\.\d+)*\.?\s*/, "").trim();
}

function matchesKey(heading: Heading, key: string): boolean {
  if (isNumbered(key)) {
    const number = heading.title.match(/^(\d+(?:\.\d+)*)(?:\.|\s|$)/);
    return number?.[1] === key;
  }
  const base = baseTitle(heading.title);
  return base === key || base.startsWith(key);
}

function sliceSection(lines: (string | null)[], headings: Heading[], key: string): (string | null)[] {
  const start = headings.find((heading) => matchesKey(heading, key));
  if (!start) throw new Error(`Section not found: ${key}`);
  const after = headings.filter((heading) => heading.index > start.index);
  const next = after.find((heading) => heading.level <= start.level);
  const end = next ? next.index : lines.length;
  return lines.slice(start.index + 1, end);
}

function leadContent(lines: (string | null)[], headings: Heading[], key: string): (string | null)[] {
  const start = headings.find((heading) => matchesKey(heading, key));
  if (!start) throw new Error(`Section not found: ${key}`);
  const next = headings.find((heading) => heading.index > start.index);
  const end = next ? next.index : lines.length;
  return lines.slice(start.index + 1, end);
}

function hasHeading(lines: (string | null)[], headings: Heading[], key: string): boolean {
  return headings.some((heading) => matchesKey(heading, key));
}

const ORIGIN_PATTERN =
  /\b(?:was|were|is)\s+(?:developed|formulated|created|introduced|published|devised)\s+by\b|developed\s+by\s+/i;

function isFullNameLabel(label: Run[] | undefined): boolean {
  if (!label) return false;
  return /^full name$/i.test(runsToText(label).trim());
}

function isOriginLabel(label: Run[] | undefined): boolean {
  if (!label) return false;
  return /^(origin|developed by|attribution)$/i.test(runsToText(label).trim());
}

function harvestOrigin(blocks: Block[]): { origin: string | null; remaining: Block[] } {
  let origin: string | null = null;
  const remaining: Block[] = [];

  for (const block of blocks) {
    if (block.kind === "p" && !origin && ORIGIN_PATTERN.test(runsToText(block.runs))) {
      origin = runsToText(block.runs);
      continue;
    }

    if (block.kind === "ul" || block.kind === "ol") {
      const kept: ListItem[] = [];
      for (const item of block.items) {
        if (!origin && isOriginLabel(item.label)) {
          origin = runsToText(item.runs);
          continue;
        }
        if (isFullNameLabel(item.label)) continue;
        kept.push(item);
      }
      if (kept.length > 0) remaining.push({ ...block, items: kept });
      continue;
    }

    remaining.push(block);
  }

  return { origin, remaining };
}

function collectText(blocks: Block[]): string {
  const parts: string[] = [];
  for (const block of blocks) {
    if (block.kind === "p") parts.push(runsToText(block.runs));
    else if (block.kind === "table") {
      parts.push(
        ...block.head.map(runsToText),
        ...block.rows.flat().map(runsToText),
      );
    } else if (block.kind === "group") {
      parts.push(block.heading, collectText(block.blocks));
    } else {
      for (const item of block.items) {
        parts.push(runsToText(item.runs));
        for (const child of item.children ?? []) parts.push(runsToText(child.runs));
      }
    }
  }
  return parts.join(" \n ");
}

const FORBIDDEN = [
  /mermaid/i,
  /flowchart\s+TD/i,
  /graph\s+TD/i,
  /```/,
  /\$\$/,
  /\\text\{/,
  /\bscenario_id\b/,
  /"prompt_question"/,
  /#{1,6}\s+\w/,
];

async function buildBrief(id: Framework, map: SourceMap): Promise<FrameworkBrief> {
  const raw = await Bun.file(join(DOCS_DIR, map.file)).text();
  const lines = stripCodeFences(raw.split(/\r?\n/));
  const headings = findHeadings(lines);

  const whyBlocks = parseBlocks(leadContent(lines, headings, map.why));
  const { origin, remaining } = harvestOrigin(whyBlocks);

  const sections: BriefSection[] = [];
  const wanted: Array<[string | null, string]> = [
    [map.anatomy, "anatomy"],
    [map.principles, "principles"],
  ];

  for (const [key, role] of wanted) {
    if (!key) continue;
    if (!hasHeading(lines, headings, key)) {
      throw new Error(`${id}: mapped ${role} section not found -> "${key}"`);
    }
    const heading = headings.find((entry) => matchesKey(entry, key))!;
    const blocks = parseBlocks(sliceSection(lines, headings, key));
    if (blocks.length > 0) sections.push({ heading: titleFor(heading.title), blocks });
  }

  if (remaining.length === 0) throw new Error(`${id}: no "why" content extracted`);
  if (sections.length === 0) throw new Error(`${id}: no sections extracted`);

  const allText = collectText(remaining) + " " + sections.map((s) => collectText(s.blocks)).join(" ");
  for (const pattern of FORBIDDEN) {
    if (pattern.test(allText)) {
      throw new Error(`${id}: extraction leaked markup matching ${pattern}`);
    }
  }

  return {
    id,
    fullName: map.fullName,
    origin,
    why: remaining,
    sections,
  };
}

function titleFor(raw: string): string {
  return baseTitle(raw);
}

const briefs: Record<string, FrameworkBrief> = {};
for (const [id, map] of Object.entries(SOURCES) as Array<[Framework, SourceMap]>) {
  briefs[id] = await buildBrief(id, map);
}

const header = `/**
 * GENERATED FILE. Do not edit by hand.
 * Source: docs/frameworks/*.md
 * Regenerate with: bun run briefs
 */

import type { Framework } from "../lib/types";

export type Run = { text: string; strong?: boolean; em?: boolean };
export type ListItem = { label?: Run[]; runs: Run[]; children?: ListItem[] };
export type Block =
  | { kind: "p"; runs: Run[] }
  | { kind: "ul"; items: ListItem[] }
  | { kind: "ol"; items: ListItem[] }
  | { kind: "table"; head: Run[][]; rows: Run[][][] }
  | { kind: "group"; heading: string; blocks: Block[] };
export type BriefSection = { heading: string; blocks: Block[] };
export type FrameworkBrief = {
  id: Framework;
  fullName: string;
  origin: string | null;
  why: Block[];
  sections: BriefSection[];
};

export const FRAMEWORK_BRIEFS: Record<Framework, FrameworkBrief> = `;

await Bun.write(OUT_FILE, header + JSON.stringify(briefs, null, 2) + ";\n");

const summary = Object.values(briefs)
  .map((brief) => `${brief.id.padEnd(15)} origin:${brief.origin ? "y" : "n"} sections:[${brief.sections.map((s) => s.heading).join(" | ")}]`)
  .join("\n");
console.log(`Generated ${Object.keys(briefs).length} briefs -> ${OUT_FILE}\n${summary}`);
