import { useEffect, useRef, useState } from "react";
import { MAX_RECORD_SECONDS, startRecording, type Recorder } from "../lib/audio";

type Tab = "mic" | "text";

export function AnswerPanel({
  speakerRole,
  onSpeakerRole,
  submitting,
  onSubmitText,
  onSubmitAudio,
}: {
  speakerRole: string;
  onSpeakerRole: (v: string) => void;
  submitting: boolean;
  onSubmitText: (transcript: string) => void;
  onSubmitAudio: (blob: Blob, durationSeconds: number) => void;
}) {
  const [tab, setTab] = useState<Tab>("mic");
  const [text, setText] = useState("");
  const [recording, setRecording] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [recordError, setRecordError] = useState<string | null>(null);
  const recRef = useRef<Recorder | null>(null);
  const timerRef = useRef<number | null>(null);
  const startRef = useRef(0);

  useEffect(() => {
    return () => {
      if (timerRef.current) window.clearInterval(timerRef.current);
      recRef.current?.cancel();
      if (audioURL) URL.revokeObjectURL(audioURL);
    };
  }, [audioURL]);

  async function handleRecord() {
    setRecordError(null);
    try {
      const { recorder } = await startRecording();
      recRef.current = recorder;
      startRef.current = Date.now();
      setElapsed(0);
      setRecording(true);
      timerRef.current = window.setInterval(() => {
        const s = Math.floor((Date.now() - startRef.current) / 1000);
        setElapsed(s);
        if (s >= MAX_RECORD_SECONDS) void handleStop();
      }, 250);
    } catch (e) {
      setRecordError(e instanceof Error ? e.message : "Could not start recording.");
    }
  }

  async function handleStop() {
    if (timerRef.current) {
      window.clearInterval(timerRef.current);
      timerRef.current = null;
    }
    const rec = recRef.current;
    recRef.current = null;
    setRecording(false);
    if (!rec) return;
    try {
      const blob = await rec.stop();
      const secs = Math.max(1, Math.round((Date.now() - startRef.current) / 1000));
      setAudioBlob(blob);
      setAudioURL((prev) => {
        if (prev) URL.revokeObjectURL(prev);
        return URL.createObjectURL(blob);
      });
      setElapsed(secs);
    } catch {
      setRecordError("Recording failed. Try again.");
    }
  }

  const mm = String(Math.floor(elapsed / 60)).padStart(2, "0");
  const ss = String(elapsed % 60).padStart(2, "0");
  const wordCount = text.trim().split(/\s+/).filter(Boolean).length;

  return (
    <div className="shell">
      <div className="core">
        <div className="core-head">
          <div>
            <span className="smallcaps">Step two</span>
            <h2 className="core-title">Deliver your answer</h2>
          </div>
        </div>

        <div className="field field-narrow">
          <span>Speaking as</span>
          <input
            value={speakerRole}
            onChange={(e) => onSpeakerRole(e.target.value)}
            placeholder="Professional"
            maxLength={120}
          />
        </div>

        <div className="seg" role="tablist" aria-label="Answer mode">
          <button type="button" role="tab" aria-selected={tab === "mic"} onClick={() => setTab("mic")}>
            Mic
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === "text"}
            onClick={() => setTab("text")}
          >
            Text
          </button>
        </div>

        {tab === "mic" ? (
          <div>
            <div className="recorder">
              {!recording ? (
                <button className="btn btn--record" onClick={handleRecord} disabled={submitting}>
                  Record
                  <span className="btn-icon" aria-hidden="true">
                    ●
                  </span>
                </button>
              ) : (
                <button className="btn btn--primary" onClick={handleStop}>
                  Stop
                  <span className="btn-icon" aria-hidden="true">
                    ■
                  </span>
                </button>
              )}
              <span className="timer" data-live={recording}>
                <span className="timer-dot" aria-hidden="true" />
                {mm}:{ss} / {String(Math.floor(MAX_RECORD_SECONDS / 60)).padStart(2, "0")}:00
              </span>
            </div>

            {recordError && <p className="field-error">{recordError}</p>}

            {audioURL ? (
              <div className="playback">
                <audio controls src={audioURL} />
                <div>
                  <button
                    className="btn btn--primary"
                    disabled={submitting || !audioBlob}
                    onClick={() => audioBlob && onSubmitAudio(audioBlob, elapsed)}
                  >
                    {submitting ? "Scoring" : "Submit recording"}
                    <span className="btn-icon" aria-hidden="true">
                      →
                    </span>
                  </button>
                </div>
              </div>
            ) : (
              <p className="hint" style={{ marginTop: "20px" }}>
                Record up to three minutes, then submit. No microphone? Switch to text.
              </p>
            )}
          </div>
        ) : (
          <div>
            <textarea
              className="writer"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type your answer exactly as you would say it aloud…"
            />
            <div className="writer-foot">
              <span className="hint">{wordCount} words</span>
              <button
                className="btn btn--primary"
                disabled={submitting || text.trim().length === 0}
                onClick={() => onSubmitText(text.trim())}
              >
                {submitting ? "Scoring" : "Submit answer"}
                <span className="btn-icon" aria-hidden="true">
                  →
                </span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
