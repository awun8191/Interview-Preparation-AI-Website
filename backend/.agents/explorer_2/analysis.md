# Technical Architecture, Data Models & API Contracts Specification
**The-Plan-Software: Production FastAPI Backend Engine**
**Author:** explorer_2 (Teamwork Explorer)  
**Target Project:** `theplan-9311e` | **Environment:** Python >= 3.13 (`uv`)

---

## 1. Executive Summary & Cognitive Architecture

The-Plan-Software backend is an executive-grade communication intelligence platform designed to evaluate spoken and written responses against 11 empirically validated communication methodologies derived from *The Plan: Life as an Engineering System*.

The backend operates on a **tripartite cognitive architecture**:
```
                        [User Client: Web / Flutter Mobile]
                                      │
          ┌───────────────────────────┴───────────────────────────┐
          │ (1) Scenario Generation                               │ (2) Session Evaluation
          ▼                                                       ▼
┌──────────────────┐                                   ┌──────────────────────┐
│  Gemini Flash    │                                   │ Audio Multipart /    │
│  (REST Gateway)  │                                   │ Text JSON Request    │
│  ~600-900ms      │                                   └──────────┬───────────┘
└─────────┬────────┘                                              │
          │ Scenario Prompt                                       │ (Audio Stream)
          ▼                                                       ▼
┌──────────────────┐                                   ┌──────────────────────┐
│ Practice Screen  │                                   │ Groq Whisper Large   │
│ Client Display   │                                   │ (~250-400ms)         │
└──────────────────┘                                   └──────────┬───────────┘
                                                                  │ Transcript + Words
                                                                  ▼
                                                       ┌──────────────────────┐
                                                       │ Delivery Analytics   │
                                                       │ (WPM, Fillers, Pause)│
                                                       │ (< 5ms)              │
                                                       └──────────┬───────────┘
                                                                  │ State + Questions
                                                                  ▼
                                                       ┌──────────────────────┐
                                                       │ TypeSafe AI Jev      │
                                                       │ System One Wire      │
                                                       │ (~150-280ms)         │
                                                       └──────────┬───────────┘
                                                                  │ Typed Choices/Scores
                                                                  ▼
                                                       ┌──────────────────────┐
                                                       │ Deterministic Rules  │
                                                       │ Composite 0-100,     │
                                                       │ Badges, Tips (< 5ms) │
                                                       └──────────┬───────────┘
                                                                  │
                                                       ┌──────────┴───────────┐
                                                       │                      │
                                                       ▼                      ▼
                                            ┌──────────────────┐   ┌──────────────────┐
                                            │ Instant Scorecard│   │ Cloud Firestore  │
                                            │ Client Response  │   │ Persistence      │
                                            │ (< 1000ms E2E)   │   │ (theplan-9311e)  │
                                            └──────────────────┘   └──────────────────┘
```

### Sub-Second Latency Budget
To maintain executive immersion, the critical evaluation loop completes in **$< 1000\text{ms}$**:
- **Groq Whisper Large-v3 STT:** $\sim 300 - 450\text{ms}$
- **Delivery Analytics (Python):** $< 5\text{ms}$
- **TypeSafe AI (Jev System One):** $\sim 150 - 280\text{ms}$
- **Deterministic Scoring & Badge Assembly:** $< 5\text{ms}$
- **Firestore Persistence (Background or Async Task):** Non-blocking client response

---

## 2. Cognitive Orchestration Endpoints & Wire Schemas

### 2.1 Endpoint: `POST /api/v1/scenarios/generate`
Generates authentic, role-tailored practice prompts matching target frameworks and seniority levels via Google Gemini Flash.

#### 2.1.1 Request Specification (`GenerateScenarioRequest`)
```python
from enum import StrEnum
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class FrameworkEnum(StrEnum):
    STAR = "STAR"
    CARL = "CARL"
    PAR = "PAR"
    SCQA = "SCQA"
    SBI = "SBI"
    RADICAL_CANDOR = "RADICAL_CANDOR"
    STATE = "STATE"
    GOTTMAN = "GOTTMAN"
    VOSS = "VOSS"
    SPARKLINE = "SPARKLINE"
    MONROE = "MONROE"


class DifficultyLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class GenerateScenarioRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_framework: FrameworkEnum = Field(
        ..., description="Target communication methodology from the 11 cataloged frameworks."
    )
    user_domain: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=[
            "Staff Backend Engineer",
            "Fintech Founder",
            "Engineering Manager",
            "Technical Product Manager",
        ],
        description="Professional domain, functional discipline, or role title.",
    )
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.INTERMEDIATE,
        description="Difficulty setting calibrating scenario friction and trade-off complexity.",
    )
    focus_theme: str | None = Field(
        default=None,
        max_length=120,
        examples=[
            "Production Outage",
            "Challenging Leadership",
            "Cross-Functional Friction",
            "Resource Constraints",
        ],
        description="Optional thematic focus or operational context.",
    )
```

#### 2.1.2 Response Specification (`ScenarioResponse`)
```python
class ScenarioResponse(BaseModel):
    scenario_id: str = Field(
        ...,
        description="Kebab-case slug or identifier uniquely identifying the scenario.",
        examples=["staff-be-db-migration-outage"],
    )
    title: str = Field(
        ...,
        description="Concise 3-5 word headline for the scenario.",
        examples=["PostgreSQL Migration Ledger Failure"],
    )
    context_background: str = Field(
        ...,
        description="2-3 sentences setting up the organizational context, stakes, timeline, and friction.",
        examples=[
            "At PaySync, you are migrating the primary transactional ledger from MySQL to PostgreSQL under live traffic. Lock contention causes sudden query timeouts across the checkout funnel."
        ],
    )
    prompt_question: str = Field(
        ...,
        description="The exact question spoken by the interviewer, executive, or counterpart.",
        examples=[
            "Tell me about a time you led a complex technical migration that encountered severe unexpected failures."
        ],
    )
    key_dimensions_to_test: list[str] = Field(
        ...,
        description="Core behavioral and technical competencies evaluated in this scenario.",
        examples=[
            "Personal ownership of technical decisions under pressure",
            "Evidence of tangible impact (quantitative metrics or operational resolution)",
        ],
    )
    target_duration_seconds: int = Field(
        ..., description="Target answer duration budget in seconds.", examples=[90]
    )
    target_framework: FrameworkEnum = Field(..., description="The framework being tested.")
    difficulty_level: DifficultyLevel = Field(..., description="The calibrated difficulty.")
```

#### 2.1.3 Gemini Flash Prompt Engineering & Structured Outputs
- **Model:** `gemini-2.5-flash` (or `gemini-1.5-flash`).
- **REST URL:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}`
- **System Instruction:**
```text
You are the Scenario Architect for an executive-grade communication training platform.
Your objective is to generate authentic, high-stakes workplace and interview scenarios designed specifically to test the user's mastery of the target communication framework.

Target Framework: {target_framework}
User Domain: {user_domain}
Difficulty: {difficulty_level}
Focus Theme: {focus_theme}

Framework Design Rules:
1. STAR: Test past execution, individual agency under pressure, and tangible outcomes.
2. CARL: Test metacognition, failure recovery, flawed assumptions, and permanent systemic/architectural safeguards.
3. PAR: Test 45-60s executive brevity, high information density, and decisive problem-solving.
4. SCQA: Test Barbara Minto's BLUF—uncontroversial baseline, destabilizing complication, governing question, and structured recommendation.
5. SBI: Test Center for Creative Leadership camera-recordable behavior, observable impact, and peer feedback.
6. RADICAL_CANDOR: Test caring personally while challenging directly without falling into Ruinous Empathy or Obnoxious Aggression.
7. STATE: Test Crucial Conversations facts-first delivery, storytelling, tentative language, and path inquiry.
8. GOTTMAN: Test de-escalation, gentle start-up, equal standing, avoiding the Four Horsemen, and repair attempts.
9. VOSS: Test Chris Voss Tactical Empathy, emotion labeling (sensory stems 'It sounds like...'), calibrated questions ('How'/'What'), and accusations audit.
10. SPARKLINE: Test Nancy Duarte oratorical rhythm contrasting 'What Is' vs 'What Could Be'.
11. MONROE: Test Monroe's 5-step motivated sequence: Attention, Need, Satisfaction, Visualization, Action.

Operational Constraints:
- Ground scenarios in authentic domain trade-offs (e.g. latency vs cost, feature velocity vs tech debt, customer churn vs compliance risk).
- For 'intermediate' and 'advanced' difficulty, introduce conflicting priorities.
- CRITICAL: Never embed coaching hints, answers, or framework labels inside the prompt_question itself.
- Return ONLY a strictly formatted JSON object matching the requested schema.
```

- **Enforced JSON Schema:**
```json
{
  "type": "object",
  "properties": {
    "scenario_id": {"type": "string"},
    "title": {"type": "string"},
    "context_background": {"type": "string"},
    "prompt_question": {"type": "string"},
    "key_dimensions_to_test": {
      "type": "array",
      "items": {"type": "string"}
    },
    "target_duration_seconds": {"type": "integer"}
  },
  "required": ["scenario_id", "title", "context_background", "prompt_question", "key_dimensions_to_test", "target_duration_seconds"]
}
```

---

### 2.2 Endpoint: `POST /api/v1/sessions/evaluate`
The core evaluation engine. Handles dual input modes (multipart audio file upload OR text JSON payload), calls Groq Whisper STT (if audio), extracts delivery metrics, queries TypeSafe AI Jev System One, computes deterministic scores & badges, and persists to Firestore.

#### 2.2.1 Input Schemas: Dual Ingestion Architecture
To provide seamless support for both native mobile/web audio recordings and pre-transcribed text testing:
1. **JSON Payload Mode (`application/json`):**
```python
class EvaluateTextRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="Firebase Auth UID of the user")
    framework: FrameworkEnum = Field(..., description="Framework under evaluation")
    prompt: str = Field(..., min_length=5, description="Scenario prompt text")
    transcript: str = Field(..., min_length=5, description="Spoken or typed response transcript")
    scenario_context: str | None = Field(default=None, description="Optional background context")
    speaker_role: str | None = Field(default="Professional", description="Candidate's role title")
    duration_seconds: float | None = Field(
        default=None, ge=0.0, description="Optional audio duration if known"
    )
```

2. **Multipart Form Mode (`multipart/form-data`):**
- Field `audio`: Binary file upload (`UploadFile`). Supported MIME types: `audio/wav`, `audio/mpeg`, `audio/mp3`, `audio/m4a`, `audio/ogg`, `audio/webm`, `audio/flac`.
- Field `user_id`: Form field string.
- Field `framework`: Form field string matching `FrameworkEnum`.
- Field `prompt`: Form field string.
- Field `scenario_context`: Form field string (optional).
- Field `speaker_role`: Form field string (optional, defaults to "Professional").

*Routing Strategy:*
A unified endpoint handles `POST /api/v1/sessions/evaluate`. If the incoming `Content-Type` starts with `multipart/form-data`, it extracts the audio file and form fields. If it is `application/json`, it validates `EvaluateTextRequest`.

#### 2.2.2 Groq Whisper STT Invocation Pipeline
- **API Endpoint:** `https://api.groq.com/openai/v1/audio/transcriptions`
- **Authentication:** `Bearer {GROQ_API_KEY}`
- **Model:** `whisper-large-v3`
- **Parameters:**
  - `file`: `(filename, file_bytes, content_type)`
  - `model`: `"whisper-large-v3"`
  - `response_format`: `"verbose_json"`
  - `temperature`: `0.0`
  - `timestamp_granularities[]`: `"word"`
- **Audio Validation Rules:**
  - Maximum upload size: $25\text{MB}$ ($26,214,400\text{ bytes}$). Rejections return HTTP 400 `FILE_TOO_LARGE`.
  - Extension whitelist: `.mp3`, `.wav`, `.m4a`, `.ogg`, `.webm`, `.flac`, `.mp4`. Rejections return HTTP 415 `UNSUPPORTED_MEDIA_TYPE`.
- **Delivery Analytics Extraction:**
  - Word Count $N$: Total words in transcript.
  - Duration $D$: Duration in seconds from Groq verbose response `duration`.
  - Words Per Minute:
    $$\text{WPM} = \begin{cases} \left(\frac{N}{D}\right) \times 60 & \text{if } D > 0 \\ 0 & \text{otherwise} \end{cases}$$
  - Filler Words Analysis:
    - Target tokens: `\b(um|uh|er|ah|like|you know|basically|actually|literally)\b` (case-insensitive regex).
    - Filler count $F$, Filler density $\% = \left(\frac{F}{N}\right) \times 100$.
  - Power Pauses: Count intervals between word timestamps where $(\text{start}_{i+1} - \text{end}_i) \ge 1.5\text{s}$.

#### 2.2.3 TypeSafe AI Jev Gateway Dispatch Format
- **Endpoint:** `https://api.typesafe.ai/v1/systemone`
- **Headers:** `Authorization: Bearer {TYPESAFE_API_KEY}`, `Content-Type: application/json`
- **Payload Structure:**
```json
{
  "state": {
    "scenario_prompt": "Tell me about a time you led a complex technical migration that encountered severe unexpected failures.",
    "scenario_context": "Staff Backend Engineer at high-throughput fintech; MySQL to PostgreSQL migration; live payment traffic.",
    "target_framework": "STAR",
    "speaker_role": "Staff Backend Engineer",
    "transcript": "At PaySync last November, we were migrating our primary transactional ledger from MySQL to Postgres...",
    "word_count": 284,
    "duration_seconds": 112.4,
    "words_per_minute": 151.6
  },
  "questions": {
    "star_situation_grounding": {
      "type": "choice",
      "instructions": "Evaluate whether the candidate in `transcript` anchors their response in an authentic, concrete, and identifiable Situation...",
      "criteria": {
        "well_grounded": "The speaker clearly grounds the answer in a concrete, authentic past scenario...",
        "partially_grounded": "The speaker mentions a scenario with minimal context...",
        "hypothetical_or_generic": "The speaker answers in generic, theoretical terms...",
        "absent": "The speaker provides zero situational context...",
        "unable_to_assess": "The transcript is severely garbled..."
      }
    },
    "star_task_clarity": {
      "type": "choice",
      "instructions": "Evaluate whether the candidate clearly isolates the specific Task, objective, or obstacle...",
      "criteria": {
        "clearly_defined": "The specific task, core objective, technical hurdle, or organizational challenge is explicitly defined...",
        "broadly_implied": "The core task is not formally stated up front, but becomes clearly understandable...",
        "absent_or_unclear": "The candidate skips defining the challenge...",
        "unable_to_assess": "Transcript is garbled or incomplete."
      }
    },
    "star_action_ownership_and_depth": {
      "type": "score",
      "instructions": "Assess the candidate's personal agency, ownership, and technical depth in the Action component...",
      "criteria": {
        "Level 1": "Zero Agency / Passive 'We'...",
        "Level 2": "Weak Individual Contribution...",
        "Level 3": "Adequate Ownership & Clear Role...",
        "Level 4": "Strong Leadership & Technical Specificity...",
        "Level 5": "Exemplary Strategic Agency & Mastery..."
      }
    },
    "star_result_and_impact": {
      "type": "choice",
      "instructions": "Assess the Result and Impact component... DO NOT penalize candidates simply because their result is not expressed as a numerical percentage. Both quantitative metrics AND qualitative/operational/strategic outcomes are fully valid...",
      "criteria": {
        "quantified_metric_impact": "Result includes concrete numerical metrics or measurable data points...",
        "meaningful_qualitative_impact": "Result delivers clear, high-value operational, strategic, technical, or relational impact without specific numbers...",
        "weak_or_vague_outcome": "An outcome is mentioned, but it is superficial or unsubstantiated...",
        "absent_or_unresolved": "No result or outcome is provided...",
        "unable_to_assess": "Transcript is garbled."
      }
    },
    "star_narrative_balance": {
      "type": "choice",
      "instructions": "Evaluate the narrative pacing and proportional balance against ideal STAR structure...",
      "criteria": {
        "well_balanced_action_focus": "Well-balanced pacing. Setup is concise, majority on actions and outcome.",
        "context_heavy_history_lecture": "Severely unbalanced toward context.",
        "rushed_or_truncated": "The answer is overly brief or rushed.",
        "rambling_and_disorganized": "Lacks narrative structure."
      }
    },
    "star_prompt_relevance": {
      "type": "choice",
      "instructions": "Determine whether the candidate's answer directly answers the specific question posed...",
      "criteria": {
        "directly_relevant": "The response directly addresses scenario_prompt.",
        "partially_relevant": "The response addresses the broad theme, but dodges specific friction.",
        "tangential_or_deflected": "The response evades the question entirely."
      }
    }
  }
}
```

- **Jev Wire Response Format:**
```json
{
  "star_situation_grounding": {
    "type": "choice",
    "choice": "well_grounded",
    "probabilities": {
      "well_grounded": 0.94,
      "partially_grounded": 0.05,
      "hypothetical_or_generic": 0.01,
      "absent": 0.00,
      "unable_to_assess": 0.00
    }
  },
  "star_task_clarity": {
    "type": "choice",
    "choice": "clearly_defined",
    "probabilities": { "clearly_defined": 0.91, "broadly_implied": 0.08, "absent_or_unclear": 0.01 }
  },
  "star_action_ownership_and_depth": {
    "type": "score",
    "choice": "Level 4",
    "probabilities": { "Level 1": 0.01, "Level 2": 0.03, "Level 3": 0.12, "Level 4": 0.78, "Level 5": 0.06 }
  },
  "star_result_and_impact": {
    "type": "choice",
    "choice": "meaningful_qualitative_impact",
    "probabilities": { "quantified_metric_impact": 0.08, "meaningful_qualitative_impact": 0.88, "weak_or_vague_outcome": 0.04, "absent_or_unresolved": 0.00 }
  },
  "star_narrative_balance": {
    "type": "choice",
    "choice": "well_balanced_action_focus",
    "probabilities": { "well_balanced_action_focus": 0.92, "context_heavy_history_lecture": 0.05, "rushed_or_truncated": 0.02, "rambling_and_disorganized": 0.01 }
  },
  "star_prompt_relevance": {
    "type": "choice",
    "choice": "directly_relevant",
    "probabilities": { "directly_relevant": 0.96, "partially_relevant": 0.03, "tangential_or_deflected": 0.01 }
  }
}
```

---

### 2.3 Mathematical Scoring Formulations

Scores are deterministic, reproducible, computed in $< 5\text{ms}$, and normalized strictly to the interval $[0, 100]$.

#### 2.3.1 STAR Composite Score Formula
$$Score_{\text{STAR}} = 100 \times \Big[ (0.15 \times P_S) + (0.15 \times P_T) + (0.45 \times S_A) + (0.15 \times P_R) + (0.10 \times P_B) \Big]$$

Where:
- **Situation Grounding ($W_S = 0.15$):**
  - `well_grounded` $= 1.0$
  - `partially_grounded` $= 0.75$
  - `hypothetical_or_generic` $= 0.20$
  - `absent` $= 0.00$
- **Task Clarity ($W_T = 0.15$):**
  - `clearly_defined` $= 1.0$
  - `broadly_implied` $= 0.70$
  - `absent_or_unclear` $= 0.00$
- **Action Ownership & Depth ($W_A = 0.45$):**
  - Normalized Score: $\frac{\text{Level}}{5.0}$ (Level 5 $= 1.0$, Level 4 $= 0.8$, Level 3 $= 0.6$, Level 2 $= 0.4$, Level 1 $= 0.2$)
- **Result & Impact ($W_R = 0.15$ — The Balanced Impact Rule):**
  - `quantified_metric_impact` $= 1.0$
  - `meaningful_qualitative_impact` $= \mathbf{1.0}$ *(Full Credit for Real Operational / Strategic Impact!)*
  - `weak_or_vague_outcome` $= 0.30$
  - `absent_or_unresolved` $= 0.00$
- **Narrative Balance ($W_B = 0.10$):**
  - `well_balanced_action_focus` $= 1.0$
  - `context_heavy_history_lecture` $= 0.40$
  - `rushed_or_truncated` $= 0.30$
  - `rambling_and_disorganized` $= 0.10$
- **Relevance Penalty Multiplier ($M_{\text{rel}}$):**
  - `directly_relevant` $= 1.0$
  - `partially_relevant` $= 0.85$
  - `tangential_or_deflected` $= 0.40$
- Final Score: $Score_{\text{final}} = \text{round}(Score_{\text{STAR}} \times M_{\text{rel}}, 1)$, clamped to $[0.0, 100.0]$.

#### 2.3.2 CARL Composite Score Formula
$$Score_{\text{CARL}} = 100 \times \Big[ (0.15 \times P_C) + (0.25 \times S_A) + (0.15 \times P_R) + (0.35 \times S_L) + (0.10 \times P_B) \Big]$$

Where:
- **Metacognitive Learning Depth ($W_L = 0.35$ — Heaviest Weight):**
  - Level 5 $= 1.00$, Level 4 $= 0.85$, Level 3 $= 0.65$, Level 2 $= 0.30$, Level 1 $= 0.00$
- **Action Ownership ($W_A = 0.25$):** $\frac{\text{Level}}{5.0}$
- **Result ($W_R = 0.15$):** `quantified_metric_impact` $= 1.0$, `meaningful_qualitative_impact` $= \mathbf{1.0}$, `weak_or_vague_outcome` $= 0.30$, `absent` $= 0.0$
- **Context Framing ($W_C = 0.15$):** `well_framed_context` $= 1.0$, `partially_framed` $= 0.75$, `hypothetical` $= 0.20$, `absent` $= 0.0$
- **Narrative Balance ($W_B = 0.10$):** `rich_learning_climax` $= 1.0$, `rushed_afterthought` $= 0.40$, `history_lecture` $= 0.30$, `rambling` $= 0.10$.

#### 2.3.3 Coaching Tips & Badge Triggering Engine
Coaching tips and badges are evaluated deterministically from Jev's reported choices:

| Framework | Trigger Condition | Badge Identifier | Deterministic Coaching Advice String |
| :--- | :--- | :--- | :--- |
| **STAR** | `star_result_and_impact == "meaningful_qualitative_impact"` | `HIGH_IMPACT_OUTCOME` | "Excellent delivery of operational impact. You clearly articulated how your actions solved the core technical bottleneck." |
| **STAR** | `star_result_and_impact == "quantified_metric_impact"` | `QUANTIFIED_MASTERY` | "Outstanding use of measurable data. Backing your results with concrete numbers reinforces credibility and precision." |
| **STAR** | `star_result_and_impact == "weak_or_vague_outcome"` | `VAGUE_IMPACT_WARNING` | "Your result was descriptive ('everything went fine') but lacked evidence of impact. Clarify what actually changed: did it unblock a squad or improve stability?" |
| **STAR** | `star_action_ownership_and_depth <= "Level 2"` | `PASSIVE_WE_ALERT` | "You leaned heavily on passive team phrasing ('we did', 'we migrated'). Interviewers want to know YOUR individual contribution. Rephrase using: 'I designed', 'I diagnosed', or 'My ownership was X'." |
| **STAR** | `star_situation_grounding == "hypothetical_or_generic"` | `HYPOTHETICAL_ALERT` | "You answered in theoretical terms ('When building systems, you should...') rather than recounting an authentic past event. Ground your answer in a specific company or project." |
| **STAR** | `star_narrative_balance == "context_heavy_history_lecture"` | `CONTEXT_OVERLOAD` | "You spent over half your response setting up backstory. Condense your Situation to 2-3 sentences so you have adequate time to showcase your actions." |
| **STAR** | `star_task_clarity == "absent_or_unclear"` | `UNCLEAR_MISSION` | "You jumped from background into tasks without framing the obstacle. State the core challenge up front: what specific constraint or failure were you solving?" |
| **CARL** | `carl_learning_metacognitive_depth >= "Level 4"` | `SYSTEMIC_WISDOM` | "Outstanding executive reflection. You demonstrated how a single setback led to permanent, team-wide safeguards and architectural improvements." |
| **CARL** | `carl_learning_metacognitive_depth == "Level 1"` | `DEFENSIVE_BLAME_ALERT`| "You externalized blame onto teammates or legacy tooling. Executive maturity requires psychological ownership: clearly state what assumption YOU personally got wrong." |

---

### 2.4 Evaluated Session Response Schema (`SessionDetailResponse`)
```python
from datetime import datetime


class DeliveryMetrics(BaseModel):
    word_count: int = Field(..., description="Total word count in transcript")
    duration_seconds: float = Field(..., description="Audio duration in seconds")
    words_per_minute: float = Field(..., description="Speaking pacing (WPM)")
    filler_word_count: int = Field(..., description="Detected filler words")
    filler_density_pct: float = Field(..., description="Filler words as % of total words")
    power_pause_count: int = Field(..., description="Gaps >= 1.5s between words")


class SessionDetailResponse(BaseModel):
    session_id: str = Field(..., description="Unique UUID for this evaluation session")
    user_id: str = Field(..., description="Firebase Auth UID of the user")
    framework: FrameworkEnum = Field(..., description="Framework evaluated")
    prompt: str = Field(..., description="The prompt question")
    transcript: str = Field(..., description="Transcribed or submitted text")
    score: float = Field(..., ge=0.0, le=100.0, description="Normalized score 0-100")
    findings: dict[str, Any] = Field(
        ..., description="Jev System One raw question choices and scores"
    )
    tips: list[str] = Field(..., description="Deterministic coaching advice items")
    badges: list[str] = Field(..., description="Badges earned or warnings triggered")
    delivery_metrics: DeliveryMetrics | None = Field(
        default=None, description="Pacing and acoustic delivery metrics"
    )
    created_at: datetime = Field(..., description="Timestamp of evaluation")
```

---

### 2.5 Endpoint: `GET /api/v1/sessions`
Retrieves paginated historical sessions for a user from Firestore.

#### 2.5.1 Query Parameters
- `user_id`: `str` (required query parameter)
- `limit`: `int = Query(default=20, ge=1, le=100)`
- `start_after`: `str | None = Query(default=None)` (Session ID or cursor token for pagination)
- `framework`: `FrameworkEnum | None = Query(default=None)` (Optional filter)

#### 2.5.2 Response Specification (`SessionListResponse`)
```python
class SessionSummaryResponse(BaseModel):
    session_id: str
    user_id: str
    framework: FrameworkEnum
    prompt: str
    score: float
    badges: list[str]
    created_at: datetime


class SessionListResponse(BaseModel):
    items: list[SessionSummaryResponse]
    total_count: int = Field(..., description="Number of items returned in current page")
    has_more: bool = Field(..., description="Whether additional records exist beyond cursor")
    next_cursor: str | None = Field(default=None, description="Cursor for the next page")
```

---

### 2.6 Endpoint: `GET /api/v1/health`
Liveness and readiness probe for orchestration platforms (Cloud Run / Docker / Kubernetes).

#### 2.6.1 Health Response Schema (`HealthResponse`)
```python
class ServiceStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    MOCKED = "mocked"
    UNAVAILABLE = "unavailable"


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded", "unhealthy"]
    version: str = "0.1.0"
    timestamp: datetime
    environment: str = Field(..., examples=["development", "testing", "production"])
    services: dict[str, ServiceStatus] = Field(
        ...,
        examples=[
            {"gemini": "healthy", "groq": "healthy", "typesafe": "healthy", "firestore": "healthy"}
        ],
    )
```

---

## 3. Firebase Firestore Integration

### 3.1 Project Details & Target
- **Firebase Project ID:** `theplan-9311e`
- **SDK:** `firebase-admin` (v6+)

### 3.2 SDK Initialization & Credential Resolution Hierarchy
To ensure zero deployment friction across local development, Docker, GCP Cloud Run, and CI/CD tests:

```python
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client as FirestoreClient


def initialize_firebase_app() -> FirestoreClient:
    """
    Initializes firebase_admin with multi-tier fallback:
    1. Direct credentials JSON string in FIREBASE_CREDENTIALS_JSON.
    2. File path in GOOGLE_APPLICATION_CREDENTIALS.
    3. Firestore Emulator (FIRESTORE_EMULATOR_HOST).
    4. Google Application Default Credentials (ADC).
    """
    if not firebase_admin._apps:
        project_id = os.environ.get("FIREBASE_PROJECT_ID", "theplan-9311e")
        emulator_host = os.environ.get("FIRESTORE_EMULATOR_HOST")

        if emulator_host:
            # Running against local emulator: credentials are not verified
            firebase_admin.initialize_app(options={"projectId": project_id})
        elif raw_json := os.environ.get("FIREBASE_CREDENTIALS_JSON"):
            cred_dict = json.loads(raw_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, options={"projectId": project_id})
        elif cred_path := os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, options={"projectId": project_id})
        else:
            # Fallback to Application Default Credentials on GCP
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, options={"projectId": project_id})

    return firestore.client()
```

### 3.3 Data Models Specification

#### 3.3.1 Collection: `users/{user_id}`
Document ID matches the Firebase Authentication UID (`request.auth.uid`).

| Field Name | Type | Firestore Type | Constraints / Validation | Description |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `str` | String | Primary Key (Doc ID) | Firebase Auth UID |
| `email` | `str` | String | Valid email regex | User's registered email |
| `display_name` | `str` | String | Min 1, Max 100 chars | Display or preferred name |
| `role` | `str` | String | `"user" \| "admin"` | Access control level |
| `subscription_tier` | `str` | String | `"free" \| "pro"` | Monetization & quota tier |
| `created_at` | `datetime` | Timestamp | Server timestamp | Account creation instant |
| `updated_at` | `datetime` | Timestamp | Server timestamp | Last profile update instant |

#### 3.3.2 Collection: `sessions/{session_id}`
Document ID is a cryptographically secure UUIDv4.

| Field Name | Type | Firestore Type | Constraints / Description |
| :--- | :--- | :--- | :--- |
| `session_id` | `str` | String | Doc ID (UUIDv4) |
| `user_id` | `str` | String | Foreign key to `users/{user_id}` |
| `framework` | `str` | String | Framework enum string (`"STAR"`, `"CARL"`, etc.) |
| `prompt` | `str` | String | Full text of scenario prompt presented to user |
| `transcript` | `str` | String | Evaluated transcript |
| `score` | `float` | Number (Double)| Composite normalized score ($0.0 - 100.0$) |
| `findings` | `dict` | Map | Jev System One questions dict (choices, scores, probabilities) |
| `tips` | `list[str]` | Array | Deterministic coaching tips |
| `badges` | `list[str]` | Array | Earned badges or triggered warnings |
| `delivery_metrics` | `dict` | Map | Optional pacing map: `{ "wpm": float, "duration_seconds": float, ... }` |
| `created_at` | `datetime` | Timestamp | Server timestamp of session creation |

#### 3.3.3 Indexing Requirements
To support fast pagination on `GET /api/v1/sessions`:
- **Composite Index:**
  - Collection: `sessions`
  - Fields:
    1. `user_id` (Ascending)
    2. `created_at` (Descending)
- **Filtered Composite Index:**
  - Collection: `sessions`
  - Fields:
    1. `user_id` (Ascending)
    2. `framework` (Ascending)
    3. `created_at` (Descending)

---

## 4. Standardized Error Handling Architecture

### 4.1 Standard Error Envelope Contract
Per `CLAUDE.md` and repository standards, all non-2xx responses MUST strictly adhere to this envelope:

```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "The audio file format is not supported. Supported formats: .mp3, .wav, .m4a, .ogg, .webm, .flac.",
    "retryable": false,
    "details": null
  },
  "request_id": "req_01h8abc123"
}
```

### 4.2 Error Code Catalog

| HTTP Status | Error Code (`code`) | Retryable | Description |
| :--- | :--- | :--- | :--- |
| **400** | `BAD_REQUEST` | `false` | Malformed body, missing required parameters, audio file > 25MB. |
| **401** | `UNAUTHORIZED` | `false` | Missing or invalid authentication token. |
| **403** | `FORBIDDEN` | `false` | Quota exhausted or insufficient role permissions. |
| **404** | `NOT_FOUND` | `false` | Requested session or user document does not exist. |
| **415** | `UNSUPPORTED_MEDIA_TYPE` | `false` | Uploaded audio file has an unsupported extension or MIME type. |
| **422** | `VALIDATION_ERROR` | `false` | Pydantic payload validation failure (includes field-level details). |
| **429** | `RATE_LIMITED` | `true` | Upstream provider (Gemini, Groq, Jev) rate limit exceeded. |
| **503** | `PROVIDER_UNAVAILABLE` | `true` | Upstream provider connection timeout or 5xx outage. |
| **500** | `INTERNAL_SERVER_ERROR`| `false` | Unhandled server error (sanitized safe message; no stack trace leaked).|

### 4.3 Pydantic & FastAPI Exception Handlers

```python
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uuid


class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        retryable: bool = False,
        details: Any = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.retryable = retryable
        self.details = details
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "retryable": exc.retryable,
                    "details": exc.details,
                },
                "request_id": request_id,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        formatted_errors = [
            {"field": " -> ".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request parameters or body.",
                    "retryable": False,
                    "details": formatted_errors,
                },
                "request_id": request_id,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        # In production: log exc with request_id privately. Never leak internal trace to client.
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred. Please try again later.",
                    "retryable": False,
                    "details": None,
                },
                "request_id": request_id,
            },
        )
```

---

## 5. Testing & Gateway Abstraction Strategy

### 5.1 Gateway Protocols & Inversion of Control
Every external dependency (Gemini, Groq, Jev, Firestore) is hidden behind an explicit `Protocol` (structural interface). The FastAPI router depends solely on these protocols via FastAPI's `Depends()` dependency injection system.

```
                    ┌─────────────────────────┐
                    │ FastAPI Route Handlers  │
                    └────────────┬────────────┘
                                 │ Depends()
                                 ▼
      ┌─────────────────────────────────────────────────────────┐
      │                   Gateway Protocols                     │
      │  - GeminiGateway      - GroqGateway                     │
      │  - JevGateway         - FirestoreRepository             │
      └────────────┬────────────────────────────┬───────────────┘
                   │ Production                 │ Unit & Integration Tests
                   ▼                            ▼
      ┌──────────────────────────┐   ┌──────────────────────────┐
      │ Live Gateway Clients     │   │ Mock Synthetic Gateways  │
      │ - HttpGeminiGateway      │   │ - MockGeminiGateway      │
      │ - HttpGroqGateway        │   │ - MockGroqGateway        │
      │ - HttpJevGateway         │   │ - MockJevGateway         │
      │ - FirebaseFirestoreRepo  │   │ - InMemoryFirestoreRepo  │
      └──────────────────────────┘   └──────────────────────────┘
```

### 5.2 Protocol Definitions
```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class GeminiGateway(Protocol):
    async def generate_scenario(self, request: GenerateScenarioRequest) -> ScenarioResponse: ...


@runtime_checkable
class GroqGateway(Protocol):
    async def transcribe_audio(self, audio_bytes: bytes, filename: str) -> dict[str, Any]: ...


@runtime_checkable
class JevGateway(Protocol):
    async def evaluate(
        self, state: dict[str, Any], questions: dict[str, Any]
    ) -> dict[str, Any]: ...


@runtime_checkable
class FirestoreRepository(Protocol):
    async def save_session(self, session_data: dict[str, Any]) -> None: ...
    async def get_sessions(
        self, user_id: str, limit: int = 20, start_after: str | None = None
    ) -> list[dict[str, Any]]: ...
    async def get_user(self, user_id: str) -> dict[str, Any] | None: ...
    async def save_user(self, user_data: dict[str, Any]) -> None: ...
```

### 5.3 Synthetic Mock Gateways
The mock gateways produce high-fidelity, deterministic responses instantly without any external network calls:

```python
class MockGeminiGateway:
    async def generate_scenario(self, request: GenerateScenarioRequest) -> ScenarioResponse:
        return ScenarioResponse(
            scenario_id=f"synthetic-{request.target_framework.lower()}-test",
            title=f"Synthetic {request.target_framework} Practice Scenario",
            context_background="A simulated production incident requiring immediate architectural resolution.",
            prompt_question=f"Describe how you handled a critical challenge testing {request.target_framework}.",
            key_dimensions_to_test=["Individual agency", "Impact delivery"],
            target_duration_seconds=90,
            target_framework=request.target_framework,
            difficulty_level=request.difficulty_level,
        )


class MockGroqGateway:
    async def transcribe_audio(self, audio_bytes: bytes, filename: str) -> dict[str, Any]:
        return {
            "text": "At PaySync last November, I took ownership of the caching layer and reduced latency by 45%.",
            "duration": 45.2,
            "words": [
                {"word": "At", "start": 0.0, "end": 0.2},
                {"word": "PaySync", "start": 0.2, "end": 0.8},
                # ...
            ],
        }


class MockJevGateway:
    async def evaluate(self, state: dict[str, Any], questions: dict[str, Any]) -> dict[str, Any]:
        # Return pre-baked, schema-accurate choices for all requested questions
        results = {}
        for q_id, q_spec in questions.items():
            if q_spec["type"] == "score":
                results[q_id] = {
                    "type": "score",
                    "choice": "Level 4",
                    "probabilities": {"Level 4": 0.9},
                }
            else:
                first_choice = list(q_spec["criteria"].keys())[0]
                results[q_id] = {
                    "type": "choice",
                    "choice": first_choice,
                    "probabilities": {first_choice: 0.95},
                }
        return results


class InMemoryFirestoreRepository:
    def __init__(self) -> None:
        self.users: dict[str, dict[str, Any]] = {}
        self.sessions: dict[str, dict[str, Any]] = {}

    async def save_session(self, session_data: dict[str, Any]) -> None:
        self.sessions[session_data["session_id"]] = session_data

    async def get_sessions(
        self, user_id: str, limit: int = 20, start_after: str | None = None
    ) -> list[dict[str, Any]]:
        user_sessions = [s for s in self.sessions.values() if s.get("user_id") == user_id]
        user_sessions.sort(key=lambda s: s.get("created_at"), reverse=True)
        return user_sessions[:limit]

    async def get_user(self, user_id: str) -> dict[str, Any] | None:
        return self.users.get(user_id)

    async def save_user(self, user_data: dict[str, Any]) -> None:
        self.users[user_data["user_id"]] = user_data
```

### 5.4 Pytest Harness & Dependency Injection
In `tests/conftest.py`, pytest overrides the app dependencies:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import (
    get_gemini_gateway,
    get_groq_gateway,
    get_jev_gateway,
    get_firestore_repo,
)


@pytest.fixture
def test_app():
    mock_gemini = MockGeminiGateway()
    mock_groq = MockGroqGateway()
    mock_jev = MockJevGateway()
    mock_firestore = InMemoryFirestoreRepository()

    app.dependency_overrides[get_gemini_gateway] = lambda: mock_gemini
    app.dependency_overrides[get_groq_gateway] = lambda: mock_groq
    app.dependency_overrides[get_jev_gateway] = lambda: mock_jev
    app.dependency_overrides[get_firestore_repo] = lambda: mock_firestore

    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as client:
        yield client
```

#### Verification Guarantee
- Executing `uv run pytest` requires **zero environment variables or API keys**.
- Network calls are strictly intercepted at the gateway interface.
- Complete test suite finishes in under **500ms**.

---

## 6. Recommended File Layout & Dependency Roadmap

### 6.1 Backend Directory Architecture
```
backend/
├── pyproject.toml
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py                  # FastAPI instantiation, middleware, routers, handlers
│       ├── config.py                # Pydantic Settings (API keys, project ID, env)
│       ├── dependencies.py          # Gateway DI providers (get_gemini_gateway, etc.)
│       ├── middleware/
│       │   ├── __init__.py
│       │   └── request_id.py        # RequestID tracing middleware
│       ├── models/
│       │   ├── __init__.py
│       │   ├── enums.py             # FrameworkEnum, DifficultyLevel
│       │   ├── errors.py            # Error envelope and custom exceptions
│       │   ├── scenarios.py         # GenerateScenarioRequest, ScenarioResponse
│       │   ├── sessions.py          # EvaluateRequest, SessionDetailResponse, DeliveryMetrics
│       │   └── users.py             # User models
│       ├── gateways/
│       │   ├── __init__.py
│       │   ├── protocols.py         # Gateway Protocols
│       │   ├── gemini.py            # HttpGeminiGateway
│       │   ├── groq.py              # HttpGroqGateway
│       │   ├── typesafe.py          # HttpJevGateway
│       │   └── firestore.py         # FirebaseFirestoreRepository
│       ├── services/
│       │   ├── __init__.py
│       │   ├── analytics.py         # WPM, pause, filler word regex engine
│       │   ├── scoring.py           # Composite math, balanced impact rule, badges
│       │   └── frameworks_catalog.py# Rubric wire loader from docs/frameworks/
│       └── routers/
│           ├── __init__.py
│           ├── health.py            # GET /api/v1/health
│           ├── scenarios.py         # POST /api/v1/scenarios/generate
│           └── sessions.py          # POST evaluate, GET sessions
└── tests/
    ├── conftest.py                  # Pytest fixtures and dependency overrides
    ├── mocks/
    │   ├── __init__.py
    │   └── synthetic_gateways.py   # Mock gateways and in-memory DB
    ├── test_health.py
    ├── test_scenarios.py
    ├── test_evaluate.py
    ├── test_scoring_math.py         # Balanced Impact Rule unit tests
    └── test_error_envelopes.py
```

### 6.2 Recommended `pyproject.toml` Dependencies
```toml
[project]
name = "backend"
version = "0.1.0"
description = "The-Plan-Software Cognitive Orchestration Engine"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "httpx>=0.28.0",
    "python-multipart>=0.0.18",
    "firebase-admin>=6.6.0",
]

[dependency-groups]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-mock>=3.14.0",
    "ruff>=0.8.0",
]
```
