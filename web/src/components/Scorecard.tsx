import type { CSSProperties } from "react";
import type { Badge, EvaluateResponse } from "../lib/types";

const MARKS: Record<Badge["kind"], string> = {
  mastery: "◆",
  warning: "!",
  delivery: "◐",
  insight: "§",
};

const CLARITY_BAND_LABEL: Record<string, string> = {
  exceptional: "Exceptional",
  clear: "Clear",
  adequate: "Adequate",
  unclear: "Unclear",
  incoherent: "Incoherent",
};

const AMBIGUITY_LABEL: Record<string, string> = {
  unambiguous_and_precise: "Unambiguous & precise",
  minor_vagueness: "Minor vagueness",
  materially_ambiguous: "Materially ambiguous",
  unable_to_assess: "Unable to assess",
};

function band(score: number): { key: string; label: string } {
  if (score >= 85) return { key: "exceptional", label: "Exceptional" };
  if (score >= 70) return { key: "strong", label: "Strong" };
  if (score >= 50) return { key: "developing", label: "Developing" };
  return { key: "weak", label: "Needs work" };
}

export function Scorecard({
  result,
  onAgain,
  onNewScenario,
}: {
  result: EvaluateResponse;
  onAgain: () => void;
  onNewScenario: () => void;
}) {
  const m = result.delivery_metrics ?? {};
  const figure = (v: unknown): string =>
    typeof v === "number" ? String(Math.round(v * 10) / 10) : "—";
  const verdict = band(result.score);

  const duration = typeof m.duration_seconds === "number" ? m.duration_seconds : 0;
  const timed = duration > 0;

  const metrics: Array<[string, string]> = [
    ["Words per min", timed ? figure(m.words_per_minute) : "—"],
    ["Words", figure(m.word_count)],
    ["Fillers", figure(m.filler_count)],
    ["Pauses", timed ? figure(m.pause_count) : "—"],
  ];

  return (
    <div className="shell">
      <div className="core">
        <div className="dossier-top">
          <div>
            <span className="smallcaps">Evaluation · {result.framework}</span>
            <div className="score-block">
              <span className="score-figure">{Math.round(result.score)}</span>
              <span className="score-out">/ 100</span>
            </div>
            <span className="verdict" data-band={verdict.key}>
              {verdict.label}
            </span>
          </div>
          <div className="dossier-actions">
            <button className="btn btn--ghost" onClick={onAgain}>
              Retry
              <span className="btn-icon" aria-hidden="true">
                ↻
              </span>
            </button>
            <button className="btn btn--ghost" onClick={onNewScenario}>
              New scenario
              <span className="btn-icon" aria-hidden="true">
                →
              </span>
            </button>
          </div>
        </div>

        {result.subscores.length > 0 && (
          <>
            <span className="section-label">Dimension ledger</span>
            <div className="ledger">
              {result.subscores.map((s, i) => {
                const clarity = s.dimension === "clarity" ? result.clarity : null;
                const auxiliary = s.weight <= 0;
                return (
                  <div
                    className="ledger-row"
                    key={s.dimension}
                    data-aux={auxiliary ? "true" : undefined}
                  >
                    <div className="ledger-dim">
                      <span className="ledger-name">{s.dimension}</span>
                      <span className="ledger-bar">
                        <i
                          style={
                            {
                              "--p": Math.max(0, Math.min(1, s.score / 100)),
                              "--delay": `${140 + i * 70}ms`,
                            } as CSSProperties
                          }
                        />
                      </span>
                    </div>
                    <span className="ledger-weight">
                      {auxiliary ? "—" : `${Math.round(s.weight * 100)}%`}
                    </span>
                    <span className="ledger-score">{Math.round(s.score)}</span>
                    {clarity && (
                      <p className="ledger-detail">
                        <span className="ledger-tag">
                          {CLARITY_BAND_LABEL[clarity.level] ?? clarity.level}
                        </span>
                        <span className="ledger-sep" aria-hidden="true">
                          ·
                        </span>
                        <span
                          className="ledger-ambiguity"
                          data-flag={clarity.ambiguous ? "true" : "false"}
                        >
                          {AMBIGUITY_LABEL[clarity.ambiguity] ?? clarity.ambiguity}
                        </span>
                      </p>
                    )}
                    {clarity?.feedback && <p className="ledger-feedback">{clarity.feedback}</p>}
                    {s.feedback && <p className="ledger-feedback">{s.feedback}</p>}
                  </div>
                );
              })}
            </div>
          </>
        )}

        {result.badges.length > 0 && (
          <>
            <span className="section-label">Marks</span>
            <div className="seals">
              {result.badges.map((b) => (
                <div className="seal" key={b.id} data-kind={b.kind}>
                  <span className="seal-mark" aria-hidden="true">
                    {MARKS[b.kind]}
                  </span>
                  <div>
                    <span className="seal-kind">{b.kind}</span>
                    <span className="seal-title">{b.title}</span>
                    {b.description && <p className="seal-desc">{b.description}</p>}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {result.tips.length > 0 && (
          <>
            <span className="section-label">Coach&rsquo;s notes</span>
            <ol className="advice">
              {result.tips.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ol>
          </>
        )}

        <div className="metrics">
          {metrics.map(([label, value]) => (
            <div className="metric" key={label}>
              <span className="metric-label">{label}</span>
              <span className="metric-value">{value}</span>
            </div>
          ))}
        </div>

        {!timed && (
          <p className="metric-note">
            Pacing and pause metrics need a recorded answer — a written response carries no timing.
          </p>
        )}
      </div>
    </div>
  );
}
