import { FRAMEWORKS } from "../lib/types";
import { linkProps } from "../lib/router";
import { Reveal } from "./Reveal";

const TRACK_NOTES: Record<string, string> = {
  Interviews: "Answer the question that was asked, with evidence.",
  Executive: "Structure the message before the room structures it for you.",
  Dialogue: "Hold the conversation when the stakes stop being polite.",
  Negotiation: "Trade on understanding rather than on volume.",
  Persuasion: "Move an audience to where they need to be, not where they are.",
};

const PROCESS = [
  {
    title: "Choose a methodology",
    body: "Eleven frameworks across five disciplines. Pick the one that matches the room you are about to walk into, then set the stakes with a role and a difficulty.",
  },
  {
    title: "Deliver the answer",
    body: "Speak it aloud or write it out. Audio is transcribed with word-level timestamps, so pacing, pauses and filler words are measured rather than guessed.",
  },
  {
    title: "Read the dossier",
    body: "A typed rubric scores every dimension against the framework's own criteria — a composite score, a dimension ledger, marks and specific corrections. Under a second, start to finish.",
  },
];

const CLAIMS = [
  { value: "Eleven", label: "Empirically validated communication methodologies" },
  { value: "< 1s", label: "From your last spoken word to a finished scorecard" },
  { value: "Zero", label: "Invented criteria — every score traces to a rubric" },
];

export function Landing() {
  const tracks = [...new Set(FRAMEWORKS.map((f) => f.track))];

  return (
    <>
      <Reveal className="hero">
        <div>
          <span className="eyebrow">Executive communication practice</span>
          <h1>Rehearse the room before you walk into it.</h1>
        </div>
        <div className="hero-aside">
          <p className="lede">
            The answer you give under pressure is the answer you practised. Eleven methodologies,
            scored against a typed rubric in under a second.
          </p>
          <div className="hero-cta">
            <a className="btn btn--primary" {...linkProps("/practice")}>
              Start practising
              <span className="btn-icon" aria-hidden="true">
                →
              </span>
            </a>
            <span className="hint">No account required.</span>
          </div>
        </div>
      </Reveal>

      <Reveal delay={120} className="claims">
        {CLAIMS.map((c) => (
          <div className="claim" key={c.value}>
            <span className="claim-value">{c.value}</span>
            <span className="claim-label">{c.label}</span>
          </div>
        ))}
      </Reveal>

      <Reveal className="section">
        <div className="section-head">
          <span className="eyebrow">The library</span>
          <h2 className="section-title">Eleven ways to say the thing that matters.</h2>
          <p className="section-note">Pick a discipline. Pick a framework. Start talking.</p>
        </div>

        <div className="fw-grid fw-grid--display">
          {tracks.map((track) => (
            <section className="fw-cat" key={track}>
              <span className="fw-cat-name">{track}</span>
              <p className="fw-cat-note">{TRACK_NOTES[track]}</p>
              <div className="fw-cat-items">
                {FRAMEWORKS.filter((f) => f.track === track).map((f) => (
                  <a
                    key={f.id}
                    className="fw-item"
                    {...linkProps(`/practice?framework=${f.id}`)}
                  >
                    <span className="fw-item-name">{f.name}</span>
                    <span className="fw-item-tag">{f.tagline}</span>
                  </a>
                ))}
              </div>
            </section>
          ))}
        </div>
      </Reveal>

      <Reveal className="section section--split">
        <div className="section-head">
          <span className="eyebrow">How it works</span>
          <h2 className="section-title">Three steps, one scorecard.</h2>
        </div>
        <ol className="process">
          {PROCESS.map((p) => (
            <li key={p.title}>
              <div>
                <span className="process-title">{p.title}</span>
                <p className="process-body">{p.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </Reveal>

      <Reveal className="closing">
        <h2>The room is already booked. Are you ready for it?</h2>
        <a className="btn btn--primary" {...linkProps("/practice")}>
          Start practising
          <span className="btn-icon" aria-hidden="true">
            →
          </span>
        </a>
      </Reveal>
    </>
  );
}
