# Milestone 3 Technical Analysis Report

**Agent**: `worker_m3` (Teamwork Preview Worker — Implementer, QA, Specialist)  
**Workspace**: `/home/nasbombz/Documents/Projects/the-plan-software/backend`  
**Date**: 2026-09-17  
**Status**: COMPLETE (Verified Clean)

---

## Executive Summary

Milestone 3 establishes the communication intelligence and deterministic scoring core of The Plan Software backend. It implements 11 executive and relational communication methodologies, 63 Jev System One question definitions with granular criteria rubrics, strict enforcement of the **Balanced Impact Rule**, a mathematical 0–100 deterministic scoring engine with domain-specific modifiers, a behavioral badge engine, a targeted coaching tips engine, and an automated test suite comprising 18 unit tests (55 tests across the monorepo).

---

## 1. Framework Architecture & Jev Question System

The framework layer is decoupled into core schemas (`app/frameworks/base.py`), a global registry with case-insensitive aliasing (`app/frameworks/__init__.py`), and 11 distinct catalogs (`app/frameworks/catalogs/`).

### 1.1 Core Domain Models (`app/frameworks/base.py`)
- **`QuestionType`**: `CHOICE` (discrete qualitative outcomes), `SCORE` (1–5 rubric levels), `NOUL` (binary presence/absence).
- **`CriteriaOption`**: Normalized raw score in [0.0, 1.0] and verbatim rubric description.
- **`JevQuestionDefinition`**: Unique identifier, question type, prompt instructions, dimension grouping, intra-dimension weight, and criteria mapping.
- **`FrameworkCatalog`**: Framework key, human-readable name, pedagogical description, list of questions, and dimension weights summing strictly to 1.0.

### 1.2 Catalog Inventory (63 Questions Across 11 Methodologies)

| Framework | Questions | Dimensions | Dimension Weights | Key Pedagogical Rule |
| :--- | :---: | :--- | :--- | :--- |
| **STAR** | 6 | `situation`, `task`, `action`, `result` | 15%, 15%, 45%, 25% | Balanced Impact Rule; 2:1 Action-to-Context ratio. |
| **CARL** | 6 | `context`, `action`, `result`, `learning` | 15%, 35%, 20%, 30% | Non-linear metacognitive learning scale; vulnerability. |
| **PAR** | 5 | `problem`, `action`, `result` | 20%, 55%, 25% | Executive brevity; 45–60s screening filter. |
| **SCQA** | 6 | `situation`, `complication`, `question`, `answer` | 15%, 20%, 15%, 50% | Uncontroversial baseline; BLUF answer delivery. |
| **SBI** | 5 | `situation`, `behavior`, `impact` | 20%, 50%, 30% | Camera-Recordable Test; banishes feedback sandwich. |
| **RADICAL_CANDOR** | 5 | `care_personally`, `challenge_directly`, `environment` | 40%, 40%, 20% | 2x2 quadrant classification; private setting. |
| **STATE** | 6 | `share_facts`, `tell_story`, `ask_path`, `talk_tentatively`, `encourage_testing` | 25%, 20%, 15%, 20%, 20% | Facts first; tentative language ('The story I tell myself'). |
| **GOTTMAN** | 6 | `soft_startup`, `responsibility`, `validation`, `repair_attempts`, `flooding_timeout` | 25%, 25%, 20%, 15%, 15% | 0.1x score collapse if Contempt detected. |
| **VOSS** | 6 | `labels`, `calibrated_questions`, `no_oriented`, `vocal_tone`, `concessions` | 25%, 25%, 15%, 15%, 20% | Severe penalty for accusatory 'Why'; DJ voice. |
| **SPARKLINE** | 6 | `contrast`, `hero_journey`, `star_moment`, `new_bliss`, `call_to_adventure` | 30%, 15%, 20%, 20%, 15% | Alternating What Is vs. What Could Be; audience as hero. |
| **MONROE** | 6 | `attention`, `need`, `satisfaction`, `visualization`, `action` | 15%, 25%, 25%, 20%, 15% | 5-step sequence; dual-polarity visualization. |

---

## 2. The Balanced Impact Rule

### 2.1 Principle
Traditional evaluation engines over-index on raw numerical percentages, unfairly penalizing engineering leaders and specialists whose highest-leverage work involves complex organizational, cultural, or architectural interventions that lack a neat scalar metric.

The **Balanced Impact Rule** mathematically guarantees:
Score(quantified_metric_impact) == Score(meaningful_qualitative_impact) == 1.0 (100%)

### 2.2 Concrete Catalog Rubrics
In `STAR`, `CARL`, `PAR`, and `SCQA`:
- `quantified_metric_impact` (1.0): Measured percentages, latency reductions, revenue impacts, SLA improvements.
- `meaningful_qualitative_impact` (1.0): Unblocking cross-functional squads, eliminating single points of failure, preventing enterprise client churn, resolving multi-party contract deadlocks, establishing engineering architectural standards.
- `weak_or_vague_outcome` (0.3): Generic assertions ("things got much better", "the team was happier").
- `absent_or_unresolved` (0.0): Abrupt endings or complete failure to state an outcome.

---

## 3. Deterministic Scoring Engine (`app/services/scoring.py`)

### 3.1 Mathematical Formulation
1. **Raw Choice Extraction**:
   For each question q, criteria keys are resolved to raw normalized points s_q in [0.0, 1.0]. For SCORE types, discrete Likert levels (Level 1–5) are mapped to continuous scores (0.2, 0.4, 0.6, 0.8, 1.0).
2. **Dimension Subscore**:
   For each dimension d: Subscore_d = 100 * sum(s_q * w_q for q in d)
3. **Composite Base Score**:
   BaseScore = sum(Subscore_d * W_d for d in dimensions)
4. **Domain-Specific Multipliers & Non-Linear Rubrics**:
   - **Gottman Interpersonal Collapse**:
     - Contempt detected: 0.10x (90% score destruction; mathematically reflects Gottman's empirical finding of contempt as the singular fatal relationship predictor).
     - Stonewalling detected: 0.40x
     - Criticism detected: 0.50x
     - Defensiveness detected: 0.60x
   - **Voss Calibrated Question Modifier**:
     - Accusatory 'why' detected: Calibrated questions subscore drops to 10.0 (raw 0.1).
   - **CARL Metacognition Curve**:
     - Level 5 (Systemic / Transferable Wisdom): 1.0
     - Level 4 (Tactical Self-Correction): 0.85
     - Level 3 (Basic Lesson Learned): 0.65
     - Level 2 (Superficial Realization): 0.30
     - Level 1 (Defensive External Blame): 0.00
5. **Clamping**:
   CompositeScore = min(100.0, max(0.0, Score))

---

## 4. Badge Engine (`app/services/badges.py`)

Synthesizes positive accomplishments and behavioral warning flags:
- **Positive Badges**: `High-Impact Outcome`, `Executive Brevity`, `Masterful Minto BLUF`, `Camera-Test Verified`, `Radical Candor Master`, `Crucial Dialogue Master`, `Masterful De-escalation`, `Tactical Empathy Master`, `Cognitive Burden Shift`, `Dynamic Orator`, `Persuasion Architect`, `Optimal Pace`, `Clean Cadence`, `Power Pauser`.
- **Alert / Warning Badges**: `The 'Why' Trap`, `Contempt Alert`, `Defensive Trap`, `Criticism Alert`, `Stonewalling Alert`, `Defensive Blame Alert`, `Fast Pacing Warning`, `Slow Pacing Warning`, `High Filler Density`.

---

## 5. Coaching Tips Engine (`app/services/tips.py`)

Generates behavioral coaching advice keyed to specific rubrics:
- Detects buried ledes in SCQA executive briefings.
- Highlights artificial feedback sandwiching in SBI.
- Warns against ruinous empathy and obnoxious aggression in Radical Candor.
- Flags dogmatic absolutes in STATE dialogues and provides framing stems ("The story I tell myself is...").
- Corrects accusatory "Why" questions to calibrated "What" / "How" inquiries.
- Integrates speech delivery telemetry (pacing > 185 WPM, filler words > 3.0%).

---

## 6. Verification & Quality Matrix

- `tests/unit/test_framework_catalogs.py`: 5 tests PASS (0.01s)
- `tests/unit/test_balanced_impact_rule.py`: 5 tests PASS (0.01s)
- `tests/unit/test_scoring_engine.py`: 8 tests PASS (0.01s)
- Total Milestone 3 Tests: 18 PASS (0.03s)
- Monorepo Pytest Suite: 55 PASS (0.26s)
- Ruff Lint Check (`uv run ruff check .`): 0 errors, 100% clean.
- Ruff Format Check (`uv run ruff format --check .`): 0 unformatted files, 93 files checked.
