"""Synthetic in-memory gateways for 100% offline testing.

Provides genuine, deterministic mocks for Gemini scenario generation,
Groq Whisper speech-to-text, TypeSafe AI Jev System One evaluation,
and Firebase Firestore persistence.
"""

import asyncio
import re
import uuid
from datetime import UTC, datetime
from typing import Any

from app.models.evaluation import JevEvaluationState, TranscriptionResult
from app.models.scenario import (
    FrameworkEnum,
    GenerateScenarioRequest,
    ScenarioResponse,
)
from app.models.session import SessionRecord, UserRecord

# Framework-specific scenario templates
FRAMEWORK_SCENARIO_TEMPLATES: dict[FrameworkEnum, dict[str, Any]] = {
    FrameworkEnum.STAR: {
        "title": "High-Stakes Operational Execution",
        "context_background": (
            "During a high-concurrency peak event at {domain}, a critical service "
            "degraded, causing sudden transaction failures and customer escalation."
        ),
        "prompt_question": (
            "Tell me about a time you led an urgent technical intervention under high "
            "uncertainty. What specific actions did you take and what was the outcome?"
        ),
        "key_dimensions": [
            "Clear situational grounding and constraint definition",
            "Individual agency and technical ownership in actions",
            "Demonstrated outcome (operational resolution or quantified impact)",
        ],
        "target_duration": 90,
    },
    FrameworkEnum.CARL: {
        "title": "Architectural Setback & Metacognitive Learning",
        "context_background": (
            "An architectural migration you spearheaded at {domain} uncovered unexpected "
            "subsystem flaws, forcing a roll-back and retrospective review."
        ),
        "prompt_question": (
            "Describe a significant project failure or setback you experienced. What flawed "
            "assumptions did you uncover, and what permanent safeguards did you establish?"
        ),
        "key_dimensions": [
            "Psychological ownership without defensive blame",
            "Metacognitive root cause identification",
            "Permanent systemic and organizational safeguards instituted",
        ],
        "target_duration": 100,
    },
    FrameworkEnum.PAR: {
        "title": "Executive Brevity & Decisive Problem Solving",
        "context_background": (
            "Leadership required an immediate 60-second summary regarding a major roadblock "
            "threatening the quarterly delivery milestone at {domain}."
        ),
        "prompt_question": (
            "In 45 to 60 seconds, describe a high-stakes bottleneck you solved, the decisive "
            "action you executed, and the final business result."
        ),
        "key_dimensions": [
            "High information density without filler",
            "Decisive action selection under tight constraints",
            "Tangible result delivered within 60 seconds",
        ],
        "target_duration": 60,
    },
    FrameworkEnum.SCQA: {
        "title": "Strategic Recommendation & BLUF",
        "context_background": (
            "The executive committee at {domain} is evaluating two mutually exclusive "
            "infrastructure strategies with substantial capital allocation implications."
        ),
        "prompt_question": (
            "Present your recommendation for infrastructure modernization using the Minto "
            "Pyramid: set baseline, define complication, frame question, and deliver answer."
        ),
        "key_dimensions": [
            "Uncontroversial situation setup",
            "Sharp, destabilizing complication",
            "Bottom-Line-Up-Front (BLUF) answer structure",
        ],
        "target_duration": 90,
    },
    FrameworkEnum.SBI: {
        "title": "Camera-Recordable Performance Feedback",
        "context_background": (
            "A senior peer at {domain} repeatedly interrupted junior colleagues during reviews, "
            "diminishing psychological safety and stifling dissenting technical perspectives."
        ),
        "prompt_question": (
            "Deliver constructive feedback using Situation-Behavior-Impact: anchor "
            "in observable facts without character judgment."
        ),
        "key_dimensions": [
            "Camera-recordable behavior descriptions",
            "Separation of observable facts from psychological intent",
            "Direct statement of team impact",
        ],
        "target_duration": 75,
    },
    FrameworkEnum.RADICAL_CANDOR: {
        "title": "Caring Personally While Challenging Directly",
        "context_background": (
            "A high-performing staff member at {domain} has let code quality slip on a sprint, "
            "jeopardizing client SLA commitments."
        ),
        "prompt_question": (
            "Address this quality decline with empathy while holding them directly accountable "
            "to standards, avoiding ruinous empathy."
        ),
        "key_dimensions": [
            "Genuine personal care and relational investment",
            "Direct, unvarnished challenge to work output",
            "Avoidance of ruinous empathy and obnoxious aggression",
        ],
        "target_duration": 80,
    },
    FrameworkEnum.STATE: {
        "title": "Crucial Conversations Under High Stakes",
        "context_background": (
            "You suspect leadership at {domain} is rushing an unvetted release to hit targets, "
            "introducing severe regulatory and security risks."
        ),
        "prompt_question": (
            "Initiate a crucial conversation with leadership using STATE: share facts, tell "
            "your story, ask for their path, talk tentatively, and encourage testing."
        ),
        "key_dimensions": [
            "Facts-first framing before interpretation",
            "Tentative phrasing that invites dialogue",
            "Active inquiry into opposing viewpoints",
        ],
        "target_duration": 90,
    },
    FrameworkEnum.GOTTMAN: {
        "title": "Conflict De-escalation & Gentle Startup",
        "context_background": (
            "During a heated cross-functional debate at {domain}, a partner lead accused "
            "your team of negligence and poor communication."
        ),
        "prompt_question": (
            "De-escalate this friction using a Gentle Start-Up: express concern without "
            "criticism or contempt, and offer a clear repair attempt."
        ),
        "key_dimensions": [
            "Gentle start-up using 'I' statements",
            "Absence of the Four Horsemen (criticism, contempt, defensiveness, stonewalling)",
            "Constructive repair attempt to restore collaboration",
        ],
        "target_duration": 75,
    },
    FrameworkEnum.VOSS: {
        "title": "Tactical Empathy & Calibrated Negotiation",
        "context_background": (
            "A key vendor for {domain} has abruptly demanded a 40% price increase midway through "
            "contract renewal, threatening service termination within 48 hours."
        ),
        "prompt_question": (
            "Negotiate with the vendor using Chris Voss Tactical Empathy: label their emotions, "
            "use a calibrated 'How' or 'What' question, and conduct an accusations audit."
        ),
        "key_dimensions": [
            "Emotion labeling using sensory stems ('It seems like...', 'It sounds like...')",
            "Calibrated open-ended questions ('How am I supposed to do that?')",
            "Proactive accusations audit disarming counterpart resistance",
        ],
        "target_duration": 85,
    },
    FrameworkEnum.SPARKLINE: {
        "title": "Visionary Oratory: What Is vs. What Could Be",
        "context_background": (
            "You must persuade the organization at {domain} to adopt a radical AI-assisted "
            "development workflow requiring substantial habit modification."
        ),
        "prompt_question": (
            "Pitch this workflow transformation using Nancy Duarte's Sparkline: contrast "
            "the reality of 'What Is' with 'What Could Be', ending with a call to adventure."
        ),
        "key_dimensions": [
            "Dynamic rhythm alternating between current reality and ideal future",
            "Heightened contrast and emotional resonance",
            "Compelling final call to adventure",
        ],
        "target_duration": 110,
    },
    FrameworkEnum.MONROE: {
        "title": "Motivated Persuasion Sequence",
        "context_background": (
            "You are proposing that {domain} invest a significant portion of next quarter's budget "
            "into eliminating technical debt and re-architecting legacy data pipelines."
        ),
        "prompt_question": (
            "Deliver your proposal following Monroe's Motivated Sequence: Attention, Need, "
            "Satisfaction, Visualization, and Call to Action."
        ),
        "key_dimensions": [
            "Attention-grabbing opening hook",
            "Compelling articulation of existential need",
            "Concrete satisfaction plan, vivid visualization, and specific call to action",
        ],
        "target_duration": 120,
    },
}


class SyntheticGeminiGateway:
    """Synthetic generator producing authentic, framework-tailored scenarios."""

    async def generate_scenario(self, request: GenerateScenarioRequest) -> ScenarioResponse:
        framework = request.target_framework
        template = FRAMEWORK_SCENARIO_TEMPLATES.get(
            framework,
            FRAMEWORK_SCENARIO_TEMPLATES[FrameworkEnum.STAR],
        )

        domain = request.user_domain.strip() or "Enterprise Engineering"
        theme_suffix = f" — {request.focus_theme}" if request.focus_theme else ""

        title = f"{template['title']}{theme_suffix}"
        context = template["context_background"].format(domain=domain)
        if request.focus_theme:
            context += f" Focus area: {request.focus_theme}."

        raw_slug_str = f"{framework.value}-{domain}-{request.difficulty_level.value}".lower()
        slug = re.sub(r"[^a-z0-9]+", "-", raw_slug_str).strip("-")
        scenario_id = f"synthetic-{slug}"

        return ScenarioResponse(
            scenario_id=scenario_id,
            title=title,
            context_background=context,
            prompt_question=template["prompt_question"],
            key_dimensions_to_test=template["key_dimensions"],
            target_duration_seconds=template["target_duration"],
            target_framework=framework,
            difficulty_level=request.difficulty_level,
        )


class SyntheticGroqGateway:
    """In-memory STT provider returning authentic transcripts and word timestamps."""

    def __init__(self, default_transcript: str | None = None) -> None:
        self.default_transcript = default_transcript or (
            "At PaySync last November, I took full ownership of the PostgreSQL ledger migration. "
            "When query timeouts occurred, I diagnosed lock contention in the checkout funnel, "
            "isolated the offending table locks, and refactored the connection pooling. "
            "This resolved the outage in fifteen minutes and stabilized transactional latency."
        )

    async def transcribe_audio(
        self, audio_bytes: bytes, filename: str = "audio.wav"
    ) -> TranscriptionResult:
        # Check if caller passed a text payload inside audio_bytes for custom mock testing
        try:
            decoded = audio_bytes.decode("utf-8").strip()
            if len(decoded) > 10 and not decoded.startswith(("\x00", "RIFF", "\xff\xfb")):
                transcript = decoded
            else:
                transcript = self.default_transcript
        except UnicodeDecodeError:
            transcript = self.default_transcript

        words_list = transcript.split()
        word_timestamps: list[dict[str, Any]] = []
        current_time = 0.0

        for _i, word in enumerate(words_list):
            word_duration = max(0.15, len(word) * 0.05)
            start = round(current_time, 2)
            end = round(current_time + word_duration, 2)
            word_timestamps.append({"word": word, "start": start, "end": end})

            # Natural pause between sentences or clauses
            if word.endswith((".", "!", "?")):
                current_time = end + 0.6
            elif word.endswith((",", ";")):
                current_time = end + 0.3
            else:
                current_time = end + 0.05

        total_duration = round(current_time, 2)

        return TranscriptionResult(
            transcript=transcript,
            duration_seconds=total_duration,
            words=word_timestamps,
        )


class SyntheticJevGateway:
    """Mock Jev System One evaluation strictly enforcing the Balanced Impact Rule."""

    async def evaluate_questions(
        self,
        state: JevEvaluationState | dict[str, Any],
        questions: dict[str, Any],
    ) -> dict[str, Any]:
        state_dict = state.model_dump() if isinstance(state, JevEvaluationState) else state
        transcript = str(state_dict.get("transcript", "")).lower()

        results: dict[str, Any] = {}

        for q_id, q_spec in questions.items():
            q_type = q_spec.get("type", "choice")
            criteria = q_spec.get("criteria", {})

            if q_type == "score":
                # Evaluate depth and ownership heuristics
                agency_markers = [
                    "i led",
                    "i designed",
                    "i diagnosed",
                    "i owned",
                    "i refactored",
                    "my action",
                ]
                if any(m in transcript for m in agency_markers):
                    choice = (
                        "Level 5"
                        if "safeguard" in transcript or "systemic" in transcript
                        else "Level 4"
                    )
                elif "we" in transcript and "i " not in transcript:
                    choice = "Level 2"
                else:
                    choice = "Level 4"

                results[q_id] = {
                    "type": "score",
                    "level": choice,
                    "choice": choice,
                    "probabilities": {
                        "Level 1": 0.01,
                        "Level 2": 0.05,
                        "Level 3": 0.14,
                        "Level 4": 0.65 if choice == "Level 4" else 0.20,
                        "Level 5": 0.70 if choice == "Level 5" else 0.15,
                    },
                }
            else:
                criteria_keys = list(criteria.keys())
                chosen_key = criteria_keys[0] if criteria_keys else "choice_1"

                # Check for Result & Impact: The Balanced Impact Rule!
                if (
                    "quantified_metric_impact" in criteria
                    and "meaningful_qualitative_impact" in criteria
                ):
                    # Look for numerical metrics in transcript
                    has_metrics = bool(
                        re.search(
                            r"\b\d+(\.\d+)?%?|\b\d+\s*(ms|seconds|minutes|hours|dollars)\b",
                            transcript,
                        )
                    )
                    qualitative_markers = [
                        "resolved",
                        "stabilized",
                        "unblocked",
                        "prevented",
                        "eliminated",
                        "repaired",
                        "restored",
                        "mitigated",
                        "successful",
                    ]
                    has_qualitative = any(m in transcript for m in qualitative_markers)

                    if has_metrics:
                        chosen_key = "quantified_metric_impact"
                    elif has_qualitative:
                        # Full credit under Balanced Impact Rule
                        chosen_key = "meaningful_qualitative_impact"
                    elif "weak_or_vague_outcome" in criteria:
                        chosen_key = "weak_or_vague_outcome"
                elif "well_grounded" in criteria:
                    grounding_markers = ["at ", "when ", "during ", "last ", "project", "outage"]
                    if any(m in transcript for m in grounding_markers):
                        chosen_key = "well_grounded"
                    elif "hypothetical_or_generic" in criteria and (
                        "in general" in transcript or "always" in transcript
                    ):
                        chosen_key = "hypothetical_or_generic"
                elif "clearly_defined" in criteria:
                    task_markers = [
                        "challenge",
                        "problem",
                        "task",
                        "objective",
                        "timeout",
                        "incident",
                    ]
                    if any(m in transcript for m in task_markers):
                        chosen_key = "clearly_defined"
                    else:
                        chosen_key = criteria_keys[0]
                elif "materially_ambiguous" in criteria:
                    vague_markers = [
                        "kind of",
                        "sort of",
                        "maybe",
                        "stuff",
                        "things",
                        "somehow",
                        " etc",
                        "a lot",
                        "whatever",
                    ]
                    if any(m in transcript for m in vague_markers):
                        chosen_key = "materially_ambiguous"
                    else:
                        chosen_key = "unambiguous_and_precise"
                elif "directly_relevant" in criteria:
                    chosen_key = "directly_relevant"

                probabilities: dict[str, float] = {}
                for key in criteria_keys:
                    if key == chosen_key:
                        probabilities[key] = 0.90
                    else:
                        probabilities[key] = round(0.10 / max(1, len(criteria_keys) - 1), 3)

                results[q_id] = {
                    "type": "choice",
                    "choice": chosen_key,
                    "probabilities": probabilities,
                }

        return results

    async def evaluate(
        self,
        state: JevEvaluationState | dict[str, Any],
        questions: dict[str, Any],
    ) -> dict[str, Any]:
        return await self.evaluate_questions(state, questions)


class SyntheticFirestoreGateway:
    """Thread-safe in-memory Firestore repository for users and sessions."""

    def __init__(self) -> None:
        self._users: dict[str, UserRecord] = {}
        self._sessions: dict[str, SessionRecord] = {}
        self._lock = asyncio.Lock()

    def clear(self) -> None:
        """Reset repository state for clean test isolation."""
        self._users.clear()
        self._sessions.clear()

    async def save_user(self, user: UserRecord) -> None:
        async with self._lock:
            # Upsert user record
            self._users[user.user_id] = user.model_copy(update={"updated_at": datetime.now(UTC)})

    async def get_user(self, user_id: str) -> UserRecord | None:
        async with self._lock:
            record = self._users.get(user_id)
            return record.model_copy() if record else None

    async def save_session(self, session: SessionRecord) -> str:
        async with self._lock:
            session_id = session.session_id or str(uuid.uuid4())
            record = session.model_copy(update={"session_id": session_id})
            self._sessions[session_id] = record
            return session_id

    async def get_user_sessions(
        self,
        user_id: str,
        limit: int = 20,
        cursor: str | None = None,
    ) -> list[SessionRecord]:
        async with self._lock:
            user_sessions = [
                s.model_copy() for s in self._sessions.values() if s.user_id == user_id
            ]
            # Order descending by created_at
            user_sessions.sort(key=lambda s: s.created_at, reverse=True)

            start_idx = 0
            if cursor:
                for idx, s in enumerate(user_sessions):
                    if s.session_id == cursor:
                        start_idx = idx + 1
                        break

            return user_sessions[start_idx : start_idx + limit]
