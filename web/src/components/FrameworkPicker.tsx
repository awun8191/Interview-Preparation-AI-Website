import { FRAMEWORKS, type Framework } from "../lib/types";

export function FrameworkPicker({
  value,
  onChange,
}: {
  value: Framework;
  onChange: (f: Framework, trigger: HTMLElement) => void;
}) {
  const tracks = [...new Set(FRAMEWORKS.map((f) => f.track))];
  return (
    <div className="fw-grid">
      {tracks.map((track) => (
        <section className="fw-cat" key={track}>
          <span className="fw-cat-name">{track}</span>
          <div className="fw-cat-items">
            {FRAMEWORKS.filter((f) => f.track === track).map((f) => (
              <button
                key={f.id}
                type="button"
                className="fw-item"
                aria-pressed={value === f.id}
                onClick={(event) => onChange(f.id, event.currentTarget)}
              >
                <span className="fw-item-name">{f.name}</span>
                <span className="fw-item-tag">{f.tagline}</span>
              </button>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
