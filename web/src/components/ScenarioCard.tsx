import type { Scenario } from "../lib/types";

export function ScenarioCard({
  scenario,
  onRegenerate,
  regenerating,
}: {
  scenario: Scenario;
  onRegenerate: () => void;
  regenerating: boolean;
}) {
  return (
    <div className="shell">
      <div className="core">
        <div className="core-head">
          <div>
            <div className="scenario-meta">
              <span className="meta-bit">{scenario.target_framework}</span>
              <span className="meta-bit">{scenario.difficulty_level}</span>
              <span className="meta-bit">Target {scenario.target_duration_seconds}s</span>
            </div>
            <h2 className="core-title core-title--lg">{scenario.title}</h2>
          </div>
          <button className="btn btn--ghost" onClick={onRegenerate} disabled={regenerating}>
            {regenerating ? "Composing" : "Regenerate"}
            <span className="btn-icon" aria-hidden="true">
              ↻
            </span>
          </button>
        </div>

        <p className="context">{scenario.context_background}</p>

        <blockquote className="pullquote">“{scenario.prompt_question}”</blockquote>

        {scenario.key_dimensions_to_test.length > 0 && (
          <div className="chips">
            {scenario.key_dimensions_to_test.map((d) => (
              <span key={d} className="chip">
                {d}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
