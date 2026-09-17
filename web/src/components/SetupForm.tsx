import type { Difficulty, Framework } from "../lib/types";
import { FrameworkPicker } from "./FrameworkPicker";

export function SetupForm({
  framework,
  onFramework,
  role,
  onRole,
  difficulty,
  onDifficulty,
  theme,
  onTheme,
  loading,
  onSubmit,
}: {
  framework: Framework;
  onFramework: (f: Framework, trigger: HTMLElement) => void;
  role: string;
  onRole: (v: string) => void;
  difficulty: Difficulty;
  onDifficulty: (d: Difficulty) => void;
  theme: string;
  onTheme: (v: string) => void;
  loading: boolean;
  onSubmit: () => void;
}) {
  return (
    <div className="shell">
      <div className="core">
        <div className="core-head">
          <div>
            <span className="smallcaps">Step one</span>
            <h2 className="core-title">Choose your arena</h2>
          </div>
        </div>

        <FrameworkPicker value={framework} onChange={onFramework} />

        <div className="fields" style={{ marginTop: "34px" }}>
          <label className="field">
            <span>Your role or domain</span>
            <input
              value={role}
              onChange={(e) => onRole(e.target.value)}
              placeholder="Staff Backend Engineer"
              maxLength={120}
            />
          </label>
          <label className="field">
            <span>Difficulty</span>
            <select value={difficulty} onChange={(e) => onDifficulty(e.target.value as Difficulty)}>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>
          <label className="field">
            <span>Focus theme — optional</span>
            <input
              value={theme}
              onChange={(e) => onTheme(e.target.value)}
              placeholder="Production Outage"
              maxLength={160}
            />
          </label>
        </div>

        <div className="field-action">
          <button
            className="btn btn--primary"
            onClick={onSubmit}
            disabled={loading || role.trim().length < 2}
          >
            {loading ? "Composing scenario" : "Generate scenario"}
            <span className="btn-icon" aria-hidden="true">
              →
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}
