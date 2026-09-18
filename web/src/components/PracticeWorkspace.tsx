import { useCallback, useRef, useState } from "react";
import { AnswerPanel } from "./AnswerPanel";
import { ErrorBanner } from "./ErrorBanner";
import { FrameworkBrief } from "./FrameworkBrief";
import { Reveal } from "./Reveal";
import { ScenarioCard } from "./ScenarioCard";
import { Scorecard } from "./Scorecard";
import { SetupForm } from "./SetupForm";
import { evaluateAudio, evaluateText, generateScenario } from "../lib/api";
import { FRAMEWORKS, type Difficulty, type EvaluateResponse, type Framework, type Scenario } from "../lib/types";

type Step = "setup" | "answer" | "result";

const STEPS: Array<{ id: Step; n: string; label: string }> = [
  { id: "setup", n: "01", label: "Choose framework" },
  { id: "answer", n: "02", label: "Deliver answer" },
  { id: "result", n: "03", label: "Review scorecard" },
];

export function PracticeWorkspace({ initialFramework }: { initialFramework?: Framework | null }) {
  const [step, setStep] = useState<Step>("setup");
  const [framework, setFramework] = useState<Framework>(initialFramework ?? "STAR");
  const [role, setRole] = useState("");
  const [speakerRole, setSpeakerRole] = useState("");
  const [difficulty, setDifficulty] = useState<Difficulty>("intermediate");
  const [theme, setTheme] = useState("");
  const [scenario, setScenario] = useState<Scenario | null>(null);
  const [result, setResult] = useState<EvaluateResponse | null>(null);
  const [generating, setGenerating] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [lastAction, setLastAction] = useState<(() => void) | null>(null);
  const [briefOpen, setBriefOpen] = useState(false);
  const briefTriggerRef = useRef<HTMLElement | null>(null);
  const railBriefRef = useRef<HTMLButtonElement>(null);

  const openBriefFrom = useCallback((trigger: HTMLElement | null) => {
    briefTriggerRef.current = trigger;
    setBriefOpen(true);
  }, []);

  const handleFramework = useCallback(
    (id: Framework, trigger: HTMLElement) => {
      setFramework(id);
      openBriefFrom(trigger);
    },
    [openBriefFrom],
  );

  const fail = useCallback((e: unknown, retry?: () => void) => {
    setError(e instanceof Error ? e : new Error("Something went wrong."));
    setLastAction(retry ? () => retry : null);
    setGenerating(false);
    setSubmitting(false);
  }, []);

  const handleGenerate = useCallback(async () => {
    if (role.trim().length < 2) return;
    setGenerating(true);
    setError(null);
    try {
      const s = await generateScenario({
        framework,
        userDomain: role.trim(),
        difficulty,
        ...(theme.trim() ? { focusTheme: theme.trim() } : {}),
      });
      setScenario(s);
      setResult(null);
      setSpeakerRole((prev) => prev || role.trim());
      setStep("answer");
    } catch (e) {
      fail(e, handleGenerate);
    } finally {
      setGenerating(false);
    }
  }, [framework, role, difficulty, theme, fail]);

  const submitText = useCallback(
    async (transcript: string) => {
      if (!scenario) return;
      setSubmitting(true);
      setError(null);
      try {
        const r = await evaluateText(transcript, {
          framework: scenario.target_framework,
          scenarioPrompt: scenario.prompt_question,
          scenarioContext: scenario.context_background,
          speakerRole: speakerRole.trim() || "Professional",
        });
        setResult(r);
        setStep("result");
      } catch (e) {
        fail(e);
      } finally {
        setSubmitting(false);
      }
    },
    [scenario, speakerRole, fail],
  );

  const submitAudio = useCallback(
    async (blob: Blob, durationSeconds: number) => {
      if (!scenario) return;
      setSubmitting(true);
      setError(null);
      try {
        const r = await evaluateAudio(blob, {
          framework: scenario.target_framework,
          scenarioPrompt: scenario.prompt_question,
          scenarioContext: scenario.context_background,
          speakerRole: speakerRole.trim() || "Professional",
          durationSeconds,
        });
        setResult(r);
        setStep("result");
      } catch (e) {
        fail(e);
      } finally {
        setSubmitting(false);
      }
    },
    [scenario, speakerRole, fail],
  );

  const activeFramework = FRAMEWORKS.find((f) => f.id === (scenario?.target_framework ?? framework));

  return (
    <>
      {step === "setup" && (
        <Reveal className="page-head">
          <span className="eyebrow">New run</span>
          <h1 className="page-title">Pick a methodology, then make your case.</h1>
        </Reveal>
      )}

      <main className="stage">
        <Reveal className="rail" delay={40}>
          <ol className="steps">
            {STEPS.map((s) => (
              <li key={s.id} className="step" data-active={s.id === step}>
                <span className="step-num">{s.n}</span>
                <span className="step-label">{s.label}</span>
              </li>
            ))}
          </ol>
          {scenario && (
            <div className="rail-note">
              <span className="smallcaps">Now practising</span>
              <span className="rail-framework">{activeFramework?.name}</span>
              <button
                type="button"
                className="rail-brief"
                ref={railBriefRef}
                onClick={() => openBriefFrom(railBriefRef.current)}
              >
                Read the brief
              </button>
            </div>
          )}
        </Reveal>

        <div className="panel">
          {error && (
            <Reveal>
              <ErrorBanner
                error={error}
                onRetry={lastAction ?? undefined}
                onDismiss={() => {
                  setError(null);
                  setLastAction(null);
                }}
              />
            </Reveal>
          )}

          {step === "setup" && (
            <Reveal delay={90}>
              <SetupForm
                framework={framework}
                onFramework={handleFramework}
                role={role}
                onRole={setRole}
                difficulty={difficulty}
                onDifficulty={setDifficulty}
                theme={theme}
                onTheme={setTheme}
                loading={generating}
                onSubmit={handleGenerate}
              />
            </Reveal>
          )}

          {step !== "setup" && scenario && (
            <Reveal delay={70}>
              <ScenarioCard
                scenario={scenario}
                onRegenerate={handleGenerate}
                regenerating={generating}
              />
            </Reveal>
          )}

          {step === "answer" && scenario && (
            <Reveal delay={150}>
              <AnswerPanel
                speakerRole={speakerRole}
                onSpeakerRole={setSpeakerRole}
                submitting={submitting}
                onSubmitText={submitText}
                onSubmitAudio={submitAudio}
              />
            </Reveal>
          )}

          {step === "result" && result && (
            <Reveal delay={90}>
              <Scorecard
                result={result}
                onAgain={() => {
                  setResult(null);
                  setStep("answer");
                }}
                onNewScenario={() => {
                  setResult(null);
                  setScenario(null);
                  setStep("setup");
                }}
              />
            </Reveal>
          )}
        </div>
      </main>

      <FrameworkBrief
        framework={scenario?.target_framework ?? framework}
        open={briefOpen}
        onClose={() => setBriefOpen(false)}
        triggerRef={briefTriggerRef}
      />
    </>
  );
}
