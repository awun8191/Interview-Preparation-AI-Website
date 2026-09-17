# Comprehensive Communication Frameworks Specification Report

**Author:** `spec_miner_1` (Teamwork Specification Miner)  
**Date:** 2026-09-17  
**Authority Sources:**
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/jev-comms.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/star.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/carl.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/par.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/scqa.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/sbi.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/radical_candor.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/state.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/gottman.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/voss.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/sparkline.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/monroe.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/CLAUDE.md` & `AGENTS.md`
- `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/ORIGINAL_REQUEST.md`

---

## 1. Executive Summary

This report establishes the authoritative specification mined from the framework encyclopedia at `docs/frameworks/` for implementation in The-Plan-Software backend. The coaching engine implements a tripartite cognitive architecture:
1. **Generative Scenario Engine (Gemini Flash):** Pre-session scenario generation conditioned on framework, domain, difficulty, and theme.
2. **Perception Engine (Groq Whisper Large-v3):** High-accuracy STT delivering transcript, word count, timestamps, and delivery metrics ($WPM$).
3. **Judgment Engine (TypeSafe AI Jev System One):** Deterministic, typed decision primitives (`choice`, `score`, `noul`) evaluated in parallel over HTTP POST to `https://api.typesafe.ai/v1/systemone` in $\sim 120\text{--}280\text{ ms}$.
4. **Deterministic Feedback Synthesis:** Zero-streaming-delay mathematical scoring (0--100) and instant UI badge/tip synthesis in $<10\text{ ms}$.

A central requirement is the **Balanced Impact Rule**, which strictly prohibits penalizing responses that deliver meaningful qualitative/operational outcomes instead of numerical figures.

---

## 2. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Architecture | Tripartite Pipeline | Generation (Gemini) $\rightarrow$ Perception (Groq) $\rightarrow$ Judgment (Jev) $\rightarrow$ Deterministic Scoring | User prompt + Audio / text | Complete scorecard + tips + badges | Standard error envelope (`PROVIDER_UNAVAILABLE`, retryable) | `jev-comms.md:14-53`, `CLAUDE.md:10-15` |
| 2 | Scenario Gen | Gemini Scenario Engine | Dynamic generation of role-specific scenarios per framework | `target_framework`, `user_domain`, `difficulty_level`, `focus_theme` | Strict JSON: `scenario_id`, `title`, `context_background`, `prompt_question`, `key_dimensions_to_test`, `target_duration_seconds` | Fallback / non-2xx error envelope | `jev-comms.md:60-94`, `carl.md:58-85`, etc. |
| 3 | STT Perception | Groq Whisper Large-v3 | Sub-second audio transcription & word count | Multipart audio | Transcript string, duration, word timestamps | Error envelope (`GROQ_STT_FAILED`) | `CLAUDE.md:45-49` |
| 4 | Delivery Analytics | Delivery Metrics Engine | Real-time speech speed & cadence metrics | Transcript, word count, duration | Words Per Minute ($WPM$), pauses, filler word counts | Clamped to 0 when duration $\le 0$ | `jev-comms.md:25`, `CLAUDE.md:47` |
| 5 | Grading Gateway | Jev System One Gateway | Typed evaluation dispatching questions in parallel | `state` object + `questions` dictionary | Dictionary mapping question IDs to typed responses | Standard error envelope (`TYPESAFE_UNAVAILABLE`) | `jev-comms.md:28-36`, `CLAUDE.md:46` |
| 6 | Grading Primitive | Jev `choice` Primitive | Categorical option selection from predefined criteria | Instructions + criteria map | Choice string matching one key in criteria | `unable_to_assess` on corrupt/garbled audio | `jev-comms.md:169-181` |
| 7 | Grading Primitive | Jev `score` Primitive | 1 to 5 descriptive rubric evaluation | Instructions + criteria map (Level 1 to Level 5) | `Level 1` through `Level 5` | Mapped to lowest level or `Level 1` | `jev-comms.md:198-210` |
| 8 | Grading Primitive | Jev `noul` Primitive | Binary probabilistic assessment | Instructions + criteria (yes/no) | Object with `{"yes": float, "no": float}` | Mapped to 0.0 probability | `radical_candor.md:184-194`, `state.md:129-138` |
| 9 | Scoring Rule | Balanced Impact Rule | Grants full credit (1.0) for qualitative/operational outcomes as well as quantitative metrics | Outcome evaluation choice | Subscore = 1.0 for both types of impact | Vague outcomes receive 0.3, absent 0.0 | `jev-comms.md:119-125`, `star.md:216-225`, `carl.md:47-51` |
| 10 | Framework 1 | STAR Suite | Evaluates Situation, Task, Action, Result | 6 Jev questions (`star_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `star.md:148-300` |
| 11 | Framework 2 | CARL Suite | Evaluates Context, Action, Result, Learning | 6 Jev questions (`carl_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `carl.md:96-250` |
| 12 | Framework 3 | PAR Suite | Evaluates Problem, Action, Result for 45-60s brevity | 5 Jev questions (`par_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `par.md:102-234` |
| 13 | Framework 4 | SCQA Suite | Evaluates Situation, Complication, Question, Answer (BLUF) | 6 Jev questions (`scqa_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `scqa.md:98-232` |
| 14 | Framework 5 | SBI Suite | Evaluates Situation, Behavior (Camera-Test), Impact | 5 Jev questions (`sbi_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `sbi.md:103-221` |
| 15 | Framework 6 | Radical Candor Suite | Evaluates Care Personally & Challenge Directly 2x2 matrix | 5 Jev questions (`candor_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `radical_candor.md:106-227` |
| 16 | Framework 7 | STATE Suite | Evaluates Crucial Conversations 5-step dialogue protocol | 6 Jev questions (`state_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `state.md:106-238` |
| 17 | Framework 8 | Gottman Suite | Evaluates Four Horsemen & Antidotes De-escalation | 6 Jev questions (`gottman_*`) | Composite score (0-100), badges, tips | Multiplicative penalty for Contempt | `gottman.md:128-267` |
| 18 | Framework 9 | Voss Negotiation Suite | Evaluates Tactical Empathy, Calibrated Questions, Labels | 6 Jev questions (`voss_*`) | Composite score (0-100), badges, tips | Severe penalty for 'Why' | `voss.md:120-253` |
| 19 | Framework 10 | Duarte Sparkline Suite | Evaluates "What Is" vs "What Could Be" oratorical cadence | 6 Jev questions (`sparkline_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `sparkline.md:104-236` |
| 20 | Framework 11 | Monroe Sequence Suite | Evaluates Monroe's 5-step motivated persuasion sequence | 6 Jev questions (`monroe_*`) | Composite score (0-100), badges, tips | Safe default score on failure | `monroe.md:109-243` |
| 21 | Persistence | Firestore Storage | Persists user profiles and evaluated practice sessions | `user_id`, session payload | Firestore document reference | Retryable error envelope on database failure | `ORIGINAL_REQUEST.md:29-32` |

---

## 3. Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Jev Primitive Evaluation | Garbled / inaudible speech transcript | Criteria explicitly specifies `"unable_to_assess"` across choice questions (`star_situation_grounding`, `star_task_clarity`, `star_result_and_impact`, `carl_context_framing`, `par_problem_sharpness`, etc.). Scoring engine maps this to 0.0 without crash. |
| 2 | Balanced Impact Rule | Candidate provides zero numbers but describes unblocking a team or preventing enterprise churn | Question criteria categorizes as `meaningful_qualitative_impact` and assigns identical top weight ($1.0$) as `quantified_metric_impact`. UI assigns ✅ **High-Impact Outcome** badge instead of penalizing. |
| 3 | Gottman Scoring | User uses sarcasm or sneering language (`contempt_detected`) | Multiplicative penalty multiplier collapses total score by $0.1\times$ (a 90% penalty) regardless of other scores. Triggers 🚨 **Contempt Alert** badge. |
| 4 | Voss Calibrated Questions | User asks "Why did you raise the price?" (`accusatory_why`) | `accusatory_why` drops calibrated question subscore to $0.1$ (severe penalty) and triggers ⚠️ **The 'Why' Trap** tip. |
| 5 | Voss Emotion Labeling | User says "I understand how you feel" | Criteria explicitly specifies that first-person ("I") phrases are NOT emotion labels and must be evaluated as `no` ($0.2$ subscore) because labels must use sensory stems ("It sounds/seems like"). |
| 6 | SBI Behavioral Component | User says "You were arrogant and disrespectful in the meeting" | Fails Camera-Recordable Test; classified as `Level 1` ($0.2$) due to subjective character attack / mind-reading. Triggers 🚨 **Mind-Reading / Character Attack** badge. |
| 7 | SCQA Baseline Situation | User opens with "Our legacy stack is complete garbage" | Evaluated as `controversial_or_abrupt_lead` ($0.3$ subscore). Triggers 🔴 **Aggressive Lead** badge. Minto requires an uncontroversial baseline fact. |
| 8 | PAR Brevity | User answers for 95 seconds with extensive company history | `par_brevity_and_information_density` yields `bloated_or_rambling` ($0.3$), `par_problem_sharpness` yields `slow_meandering_setup` ($0.5$). Triggers ⏱️ **Bloat Warning (>75s)** and ⚠️ **Backstory Creep**. |
| 9 | CARL Metacognition | User provides generic cliché ("I learned that communication is key") | `carl_learning_metacognitive_depth` evaluates to `Level 2` ($0.30$ non-linear subscore). Triggers ⚠️ **Superficial Learning** badge. |
| 10 | Delivery Analytics | Audio duration is zero or negative | Math engine must guard against division by zero: if `duration_seconds <= 0`, `words_per_minute = 0`. |

---

## 4. Jev System One Wire Catalog & Core Protocols

### 4.1 Evaluation State Schema
Every call to Jev (`POST https://api.typesafe.ai/v1/systemone`) supplies a state JSON object with exact keys:
```json
{
  "scenario_prompt": "string: The prompt or challenge question presented to the user",
  "scenario_context": "string: Operational setting, background stakes, and constraints",
  "target_framework": "STAR | CARL | PAR | SCQA | SBI | RADICAL_CANDOR | STATE | GOTTMAN | VOSS_NEGOTIATION | DUARTE_SPARKLINE | MONROE_SEQUENCE",
  "speaker_role": "string: User role (e.g. 'Staff Backend Engineer', 'Founder', 'Tech Lead')",
  "transcript": "string: Full speech-to-text transcript of user's spoken answer",
  "word_count": 284,
  "duration_seconds": 112,
  "words_per_minute": 152
}
```

### 4.2 Jev Question Primitives
Each question in the `questions` dict is typed:
1. `choice`: Multi-class categorical decision where criteria defines exhaustive mutually exclusive states.
2. `score`: 5-level ordinal grading (`Level 1` to `Level 5`).
3. `noul`: Binary decision returning probabilities for `yes` and `no` summing to 1.0.

### 4.3 Parallel Dispatch & Scoring Contract
All questions for a framework are sent in a single parallel payload to `https://api.typesafe.ai/v1/systemone`. The returned JSON map contains typed decisions that are parsed by the deterministic scoring engine.

---

## 5. The Balanced Impact Rule Specification

### Definition:
Across all outcome-focused frameworks (STAR, CARL, PAR, SCQA, etc.), **results do NOT need to be numeric percentages or financial statistics to receive top scores**. Forcing artificial numbers causes hallucinated or disingenuous answers in professional coaching.

### Enforcement:
1. **Equal Top Scoring:** In Jev question rubrics:
   - `quantified_metric_impact`: $1.0$ (100% credit)
   - `meaningful_qualitative_impact`: **$1.0$ (100% credit - Full Credit!)**
2. **Valid Qualitative / Operational Impact criteria:**
   - Unblocking cross-functional squads or release gates.
   - Preventing client churn or resolving enterprise contract deadlocks.
   - Establishing architectural patterns or reusable service templates adopted across squads.
   - Eliminating dangerous single points of failure.
   - Preventing data corruption or maintaining system continuity during an incident.
3. **Penalized Formats:**
   - `weak_or_vague_outcome`: $0.3$ (e.g., "things went fine", "everyone was happy").
   - `absent_or_unresolved`: $0.0$ (trailing off with no resolution).
4. **Badge Synthesis:**
   - `meaningful_qualitative_impact` triggers ✅ **High-Impact Outcome** / **High Operational Impact**.
   - `quantified_metric_impact` triggers 🌟 **Quantified Mastery**.

---

## 6. Framework-by-Framework Comprehensive Catalog

---

### Framework 1: STAR (Situation, Task, Action, Result)

#### Dimensions & Timing
- **Pacing Budget:** 90--120 seconds.
- **Proportional Allocation:** Situation ($\sim 15\%$), Task ($\sim 15\%$), Action ($\sim 55\%$), Result ($\sim 15\%$).
- **Target Framework Wire Key:** `"STAR"`

#### Jev System One Questions (6 Total)
1. `star_situation_grounding` (`choice`)
   - `well_grounded`: $1.0$
   - `partially_grounded`: $0.75$
   - `hypothetical_or_generic`: $0.2$
   - `absent`: $0.0$
   - `unable_to_assess`: $0.0$
2. `star_task_clarity` (`choice`)
   - `clearly_defined`: $1.0$
   - `broadly_implied`: $0.7$
   - `absent_or_unclear`: $0.0$
   - `unable_to_assess`: $0.0$
3. `star_action_ownership_and_depth` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
4. `star_result_and_impact` (`choice`) — *Balanced Impact Enforced*
   - `quantified_metric_impact`: $1.0$
   - `meaningful_qualitative_impact`: $1.0$ (Full credit)
   - `weak_or_vague_outcome`: $0.3$
   - `absent_or_unresolved`: $0.0$
   - `unable_to_assess`: $0.0$
5. `star_narrative_balance` (`choice`)
   - `well_balanced_action_focus`: $1.0$
   - `context_heavy_history_lecture`: $0.4$
   - `rushed_or_truncated`: $0.3$
   - `rambling_and_disorganized`: $0.1$
6. `star_prompt_relevance` (`choice`)
   - `directly_relevant`, `partially_relevant`, `tangential_or_deflected`.

#### Scoring Weights
$$Score_{\text{STAR}} = 0.15 P_S + 0.15 P_T + 0.45 S_A + 0.15 P_R + 0.10 P_B$$
- Situation ($W_S = 15\%$)
- Task ($W_T = 15\%$)
- Action ($W_A = 45\%$)
- Result ($W_R = 15\%$)
- Narrative Balance ($W_B = 10\%$)

#### Badges & Coaching Tips
- `star_result_and_impact == "meaningful_qualitative_impact"`: ✅ **High-Impact Outcome** | *"Excellent delivery of operational impact. You clearly articulated how your actions solved the core organizational/technical bottleneck."*
- `star_result_and_impact == "quantified_metric_impact"`: 🌟 **Quantified Mastery** | *"Outstanding use of measurable data. Backing your results with concrete numbers reinforces credibility and precision."*
- `star_result_and_impact == "weak_or_vague_outcome"`: ⚠️ **Vague Impact** | *"Your result was descriptive ('everything went fine') but lacked clear evidence of impact. Clarify what actually changed: did it unblock a squad, prevent client churn, or improve system stability?"*
- `star_action_ownership_and_depth <= "Level 2"`: ⚠️ **The 'We' Trap (Low Agency)** | *"You leaned heavily on passive team phrasing ('we did', 'we migrated'). Interviewers want to know YOUR individual contribution. Rephrase using: 'I designed', 'I diagnosed', or 'My specific ownership was X'."*
- `star_situation_grounding == "hypothetical_or_generic"`: 🔴 **Hypothetical Generalization** | *"You answered in theoretical terms ('When building systems, you should...') rather than recounting an authentic past event. Ground your answer in a specific company, system, or project."*
- `star_narrative_balance == "context_heavy_history_lecture"`: ⏱️ **Context Overload** | *"You spent over half your response setting up backstory and background. Condense your Situation to 2–3 sentences so you have adequate time to showcase your actions and decisions."*
- `star_task_clarity == "absent_or_unclear"`: ⚠️ **Unclear Mission** | *"You jumped from background into tasks without clearly framing the obstacle. State the core challenge up front: what specific constraint, deadline, or failure were you solving?"*

---

### Framework 2: CARL (Context, Action, Result, Learning)

#### Dimensions & Timing
- **Pacing Budget:** 100--130 seconds.
- **Proportional Allocation:** Context ($15\text{--}20\%$), Action ($35\%$), Result ($15\%$), **Learning ($25\text{--}30\%$)**.
- **Target Framework Wire Key:** `"CARL"`

#### Jev System One Questions (6 Total)
1. `carl_context_framing` (`choice`)
   - `well_framed_context`: $1.0$, `partially_framed`: $0.75$, `hypothetical_or_generic`: $0.2$, `absent`: $0.0$, `unable_to_assess`: $0.0$.
2. `carl_action_ownership_and_rigor` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
3. `carl_result_and_impact` (`choice`) — *Balanced Impact Enforced*
   - `quantified_metric_impact`: $1.0$
   - `meaningful_qualitative_impact`: $1.0$ (Full credit)
   - `weak_or_vague_outcome`: $0.3$
   - `absent_or_unresolved`: $0.0$
   - `unable_to_assess`: $0.0$
4. `carl_learning_metacognitive_depth` (`score`) — *Non-linear Rubric*
   - Level 5: $1.0$ (Transformational Organizational Wisdom)
   - Level 4: $0.85$ (Systemic Process & Engineering Improvement)
   - Level 3: $0.65$ (Individual Tactical Takeaway)
   - Level 2: $0.30$ (Superficial Platitudes)
   - Level 1: $0.0$ (Defensive / Externalized Blame)
5. `carl_narrative_balance` (`choice`)
   - `rich_learning_climax`: $1.0$
   - `rushed_afterthought_learning`: $0.4$
   - `context_heavy_history_lecture`: $0.3$
   - `disorganized_or_rambling`: $0.1$
6. `carl_vulnerability_and_humility` (`choice`)
   - `authentic_humility_and_ownership`, `guarded_or_reluctant`, `defensive_or_arrogant`.

#### Scoring Weights
$$Score_{\text{CARL}} = 0.15 P_C + 0.25 S_A + 0.15 P_R + 0.35 S_L + 0.10 P_B$$
- Context ($W_C = 15\%$)
- Action ($W_A = 25\%$)
- Result ($W_R = 15\%$)
- Learning ($W_L = 35\%$ — Heaviest Weight)
- Narrative Balance ($W_B = 10\%$)

#### Badges & Coaching Tips
- `carl_learning_metacognitive_depth >= "Level 4"`: 🌟 **Systemic Wisdom** | *"Outstanding executive reflection. You demonstrated how a single failure led to permanent, team-wide safeguards and architectural improvements."*
- `carl_learning_metacognitive_depth == "Level 2"`: ⚠️ **Superficial Learning** | *"Your learning was clichéd ('communication is key'). Senior interviewers look for systemic takeaways: what specific engineering gate, runbook, or architectural rule did you institute?"*
- `carl_learning_metacognitive_depth == "Level 1"`: 🚨 **Defensive Blame Alert** | *"You externalized blame onto teammates or legacy tooling. Executive maturity requires psychological ownership: clearly state what assumption YOU personally got wrong."*
- `carl_narrative_balance == "rushed_afterthought_learning"`: ⏱️ **Rushed Reflection** | *"You spent 90% of your time on the story and rushed the learning in the final seconds. In the CARL framework, reserve the final 30–45 seconds exclusively for reflection and takeaways."*
- `carl_vulnerability_and_humility == "guarded_or_reluctant"`: 🛡️ **Guarded Persona** | *"You hedged your answers to avoid admitting a mistake. Frame the setback as a valuable investment in your technical maturity."*
- `carl_result_and_impact == "meaningful_qualitative_impact"`: ✅ **High Operational Impact** | *"Great articulation of qualitative impact. You clearly showed how service stability and team alignment were restored."*

---

### Framework 3: PAR (Problem, Action, Result)

#### Dimensions & Timing
- **Pacing Budget:** strictly 45--60 seconds ($<65\text{s}$).
- **Proportional Allocation:** Problem ($10\text{--}15\text{s}$, $<20\%$), Action ($30\text{--}35\text{s}$), Result ($10\text{--}15\text{s}$).
- **Target Framework Wire Key:** `"PAR"`

#### Jev System One Questions (5 Total)
1. `par_problem_sharpness` (`choice`)
   - `sharp_and_immediate`: $1.0$, `slow_meandering_setup`: $0.5$, `vague_or_unclear`: $0.2$, `absent`: $0.0$, `unable_to_assess`: $0.0$.
2. `par_action_decisiveness` (`score`) — *Non-linear Rubric*
   - Level 5: $1.0$
   - Level 4: $0.85$
   - Level 3: $0.65$
   - Level 2: $0.35$
   - Level 1: $0.10$
3. `par_result_and_impact` (`choice`) — *Balanced Impact Enforced*
   - `quantified_metric_impact`: $1.0$
   - `meaningful_qualitative_impact`: $1.0$ (Full credit)
   - `weak_or_vague_outcome`: $0.3$
   - `absent_or_trailing_off`: $0.0$
   - `unable_to_assess`: $0.0$
4. `par_brevity_and_information_density` (`choice`)
   - `crisp_executive_brevity`: $1.0$, `acceptable_pacing`: $0.8$, `bloated_or_rambling`: $0.3$, `too_brief_incomplete`: $0.2$.
5. `par_prompt_relevance` (`choice`)
   - `directly_relevant`, `partially_relevant`, `tangential_or_deflected`.

#### Scoring Weights
$$Score_{\text{PAR}} = 0.20 P_P + 0.45 S_A + 0.20 P_R + 0.15 P_B$$
- Problem ($W_P = 20\%$)
- Action ($W_A = 45\%$)
- Result ($W_R = 20\%$)
- Brevity & Density ($W_B = 15\%$)

#### Badges & Coaching Tips
- `par_brevity_and_information_density == "crisp_executive_brevity"`: ⚡ **Executive Brevity** | *"Outstanding information density. You delivered a complete, high-impact story in under 60 seconds with zero wasted words."*
- `par_problem_sharpness == "slow_meandering_setup"`: ⚠️ **Backstory Creep** | *"You spent over 20 seconds on setup before stating the problem. In the PAR format, state the friction point in your very first sentence: 'The challenge was X'."*
- `par_action_decisiveness <= "Level 2"`: ⚠️ **Low Agency ("We")** | *"You leaned heavily on 'we'. In rapid-fire screening rounds, recruiters score personal ownership. Use active verbs: 'I investigated', 'I patched', 'I coordinated'."*
- `par_result_and_impact == "meaningful_qualitative_impact"`: ✅ **High Operational Impact** | *"Great delivery of operational impact. You clearly articulated how your actions eliminated the bottleneck and restored system stability."*
- `par_brevity_and_information_density == "bloated_or_rambling"`: ⏱️ **Bloat Warning (>75s)** | *"Your response exceeded 75 seconds. In fast screening rounds, aim for 45–60 seconds by eliminating background lore and focusing strictly on the move you made."*

---

### Framework 4: SCQA (Situation, Complication, Question, Answer)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 90$ seconds.
- **Philosophy:** Barbara Minto's Pyramid Principle / BLUF (Bottom Line Up Front).
- **Target Framework Wire Key:** `"SCQA"`

#### Jev System One Questions (6 Total)
1. `scqa_situation_baseline` (`choice`)
   - `uncontroversial_clear_baseline`: $1.0$, `controversial_or_abrupt_lead`: $0.3$, `vague_or_delayed_situation`: $0.3$, `absent`: $0.0$, `unable_to_assess`: $0.0$.
2. `scqa_complication_friction` (`choice`)
   - `sharp_urgent_friction`: $1.0$, `vague_friction_low_stakes`: $0.4$, `absent`: $0.0$.
3. `scqa_governing_question` (`choice`)
   - `explicitly_articulated`: $1.0$, `clearly_implied`: $0.85$, `muddled_or_missing`: $0.2$.
4. `scqa_bluf_efficiency` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
5. `scqa_recommendation_substance` (`choice`)
   - `actionable_high_impact_solution`: $1.0$ (Full credit for both quantitative & operational outcomes)
   - `partial_hedged_solution`: $0.5$
   - `vague_non_committal`: $0.1$
6. `scqa_structural_flow` (`choice`)
   - `textbook_minto_flow`: $1.0$, `inverted_bluf_flow`: $1.0$, `rambling_chronological_weeds`: $0.3$, `chaotic_disorganized`: $0.0$.

#### Scoring Weights
$$Score_{\text{SCQA}} = 0.10 P_S + 0.20 P_C + 0.10 P_Q + 0.30 S_{\text{BLUF}} + 0.20 P_R + 0.10 P_F$$
- Situation ($W_S = 10\%$)
- Complication ($W_C = 20\%$)
- Question ($W_Q = 10\%$)
- BLUF Efficiency ($W_{\text{BLUF}} = 30\%$ — Heaviest Weight)
- Recommendation Substance ($W_R = 20\%$)
- Structural Flow ($W_F = 10\%$)

#### Badges & Coaching Tips
- `scqa_bluf_efficiency >= "Level 4"`: ⚡ **Executive BLUF** | *"Masterful executive delivery. You delivered a decisive recommendation supported by clear business and technical justification with zero cognitive drag."*
- `scqa_bluf_efficiency <= "Level 2"`: ⚠️ **Burying the Lede** | *"You spent too much time on background narrative before delivering your recommendation. In executive briefings, state the Answer in the first 20–30 seconds, then support it."*
- `scqa_situation_baseline == "controversial_or_abrupt_lead"`: 🔴 **Aggressive Lead** | *"You opened with a controversial claim or alarmist statement. In Minto's doctrine, open with an uncontroversial fact everyone agrees on to establish psychological safety before introducing friction."*
- `scqa_complication_friction == "vague_friction_low_stakes"`: ⚠️ **Low-Stakes Complication** | *"Your Complication lacked urgency. Clearly articulate what broke and the operational stakes of inaction: will it cause downtime, cost overruns, or compliance violations?"*
- `scqa_recommendation_substance == "vague_non_committal"`: 🛡️ **Non-Committal Answer** | *"Your recommendation was indecisive ('we could look into things'). Executives expect a point of view: state an explicit recommendation with clear next steps."*
- `scqa_structural_flow == "rambling_chronological_weeds"`: ⏱️ **Chronological Weeds** | *"You structured your update as a chronological diary. Re-order into top-down structure: Situation $\rightarrow$ Complication $\rightarrow$ Decisive Recommendation."*

---

### Framework 5: SBI (Situation, Behavior, Impact)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 90$ seconds.
- **Philosophy:** Center for Creative Leadership (CCL); Camera-Recordable Test; Banish the Feedback Sandwich.
- **Target Framework Wire Key:** `"SBI"`

#### Jev System One Questions (5 Total)
1. `sbi_situation_anchoring` (`choice`)
   - `specifically_anchored_time_place`: $1.0$, `vague_general_anchoring`: $0.5$, `unanchored_sweeping_claim`: $0.1$, `absent`: $0.0$, `unable_to_assess`: $0.0$.
2. `sbi_behavioral_camera_test` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
3. `sbi_impact_operational_clarity` (`choice`)
   - `clear_operational_or_relational_impact`: $1.0$ (Full credit for operational or team safety impact)
   - `vague_emotional_venting`: $0.4$
   - `absent_impact`: $0.0$
4. `sbi_feedback_sandwich_filter` (`choice`)
   - `clean_direct_candor`: $1.0$
   - `artificial_sandwiching_detected`: $0.3$
5. `sbi_solution_co_creation` (`choice`)
   - `collaborative_co_creation`: $1.0$, `unilateral_dictate_or_threat`: $0.3$, `unresolved_or_abrupt_end`: $0.2$.

#### Scoring Weights
$$Score_{\text{SBI}} = 0.15 P_S + 0.35 S_B + 0.25 P_I + 0.10 P_F + 0.15 P_C$$
- Situation ($W_S = 15\%$)
- Camera-Recordable Behavior ($W_B = 35\%$ — Heaviest Weight)
- Impact Clarity ($W_I = 25\%$)
- Feedback Sandwich Filter ($W_F = 10\%$)
- Solution Co-Creation ($W_C = 15\%$)

#### Badges & Coaching Tips
- `sbi_behavioral_camera_test >= "Level 4"`: 📹 **Camera-Recordable Precision** | *"Flawless behavioral feedback. You stuck entirely to observable facts and quoted language, eliminating defensive friction."*
- `sbi_behavioral_camera_test <= "Level 2"`: 🚨 **Mind-Reading / Character Attack** | *"You used subjective personality labels ('you were rude / unprofessional'). That triggers instant defensiveness. Describe only what a video camera could record: exact words and specific physical actions."*
- `sbi_situation_anchoring == "unanchored_sweeping_claim"`: ⚠️ **The 'Always / Never' Trap** | *"You used sweeping absolutes ('You always do this'). This triggers fact-checking debates. Anchor your feedback to a single specific date, meeting, or pull request."*
- `sbi_impact_operational_clarity == "absent_impact"`: ⚠️ **Missing Impact** | *"You described the behavior but never explained why it matters. Articulate the operational or team consequence: did it cause delay, demoralize colleagues, or risk client trust?"*
- `sbi_feedback_sandwich_filter == "artificial_sandwiching_detected"`: 🥪 **Sandwich Detected** | *"Avoid hiding hard critique inside fake compliments. Leaders value clean, direct, and respectful transparency."*
- `sbi_solution_co_creation == "collaborative_co_creation"`: 🤝 **Co-Authored Solution** | *"Excellent transition to curiosity. Inviting their perspective transforms critique into a collaborative coaching moment."*

---

### Framework 6: Radical Candor (Care Personally & Challenge Directly)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 90$ seconds.
- **Philosophy:** Kim Scott; 2x2 Matrix (Care Personally vs Challenge Directly); Praise in Public, Criticize in Private; Solicit Feedback.
- **Target Framework Wire Key:** `"RADICAL_CANDOR"`

#### Jev System One Questions (5 Total)
1. `candor_quadrant_classification` (`choice`)
   - `radical_candor`: $1.0$
   - `ruinous_empathy`: $0.4$
   - `obnoxious_aggression`: $0.2$
   - `manipulative_insincerity`: $0.0$
2. `candor_challenge_directly_clarity` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
3. `candor_care_personally_signals` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
4. `candor_private_developmental_setting` (`choice`)
   - `private_developmental_frame`: $1.0$, `inappropriate_public_tone`: $0.0$.
5. `candor_openness_to_counter_feedback` (`noul`)
   - `yes`: $1.0$, `no`: $0.0$.

#### Scoring Weights
$$Score_{\text{RC}} = 0.30 P_Q + 0.35 S_D + 0.25 S_C + 0.10 P_F$$
- Quadrant ($W_Q = 30\%$)
- Challenge Directly ($W_D = 35\%$)
- Care Personally ($W_C = 25\%$)
- Private Frame & Reciprocal Openness ($W_F = 10\%$)

#### Badges & Coaching Tips
- `candor_quadrant_classification == "radical_candor"`: 🌟 **Radical Candor Achieved** | *"Exemplary leadership. You spoke the hard, necessary truth with unmistakable clarity while demonstrating deep personal care and investment in their growth."*
- `candor_quadrant_classification == "ruinous_empathy"`: ⚠️ **The Ruinous Empathy Trap** | *"You were too soft and hedged your critique. Out of fear of hurting feelings, you failed to communicate the gravity of the problem. Remember: 'Clarity is kindness'. Be direct about the standard."*
- `candor_quadrant_classification == "obnoxious_aggression"`: 🚨 **Obnoxious Aggression Alert** | *"Your critique was harsh and dismissive. Challenging directly without personal care creates defensiveness and fear. Acknowledge their dignity and offer genuine support."*
- `candor_challenge_directly_clarity <= "Level 2"`: ⚠️ **Vague Guidance** | *"The recipient leaves this conversation without knowing exactly what must change. Be specific: name the exact deliverables, dates, and non-negotiable standards."*
- `candor_care_personally_signals <= "Level 2"`: ❄️ **Cold / Transactional Tone** | *"Your tone was sterile and transactional. Connect before you correct: affirm their value to the team and express a genuine desire to see them succeed."*
- `candor_openness_to_counter_feedback.yes >= 0.7`: 🤝 **Reciprocal Vulnerability** | *"Great leadership practice. Inviting feedback on your own management builds deep psychological safety and trust."*

---

### Framework 7: STATE (Crucial Conversations)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 90$ seconds.
- **Philosophy:** Patterson, Grenny, McMillan, Switzler; Share your facts, Tell your story, Ask for their path, Talk tentatively, Encourage testing.
- **Target Framework Wire Key:** `"STATE"`

#### Jev System One Questions (6 Total)
1. `state_facts_first_sequencing` (`noul`)
   - `yes`: $1.0$, `no`: $0.0$.
2. `state_story_framing_awareness` (`choice`)
   - `properly_framed_as_story`: $1.0$, `story_stated_as_absolute_truth`: $0.2$, `absent`: $0.1$.
3. `state_tentative_language_calibration` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
4. `state_mutual_purpose_safety` (`choice`)
   - `explicit_mutual_purpose`: $1.0$, `implied_collaborative`: $0.7$, `adversarial_me_vs_you`: $0.0$.
5. `state_ask_and_encourage_testing` (`choice`)
   - `genuine_inquiry_and_testing`: $1.0$, `token_or_rhetorical_question`: $0.3$, `zero_inquiry_closed`: $0.0$.
6. `state_emotional_composure` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).

#### Scoring Weights
$$Score_{\text{STATE}} = 0.20 P_F + 0.15 P_S + 0.25 S_T + 0.10 P_M + 0.20 P_A + 0.10 S_C$$
- Facts-First Sequencing ($W_F = 20\%$)
- Story Framing ($W_S = 15\%$)
- Tentative Language ($W_T = 25\%$)
- Mutual Purpose ($W_M = 10\%$)
- Ask & Encourage Testing ($W_A = 20\%$)
- Emotional Composure ($W_C = 10\%$)

#### Badges & Coaching Tips
- `state_facts_first_sequencing.yes >= 0.8` AND `state_tentative_language_calibration >= "Level 4"`: 🛡️ **Crucial Mastery** | *"Exemplary high-stakes dialogue. You led with undeniable facts, framed your concerns with intellectual humility, and preserved psychological safety."*
- `state_facts_first_sequencing.yes < 0.3`: 🔴 **Accusatory Lead** | *"You led with your emotional conclusion or grievance rather than data. In high-stakes disputes, state observable facts first (dates, PRs, metrics) before sharing your story."*
- `state_tentative_language_calibration <= "Level 2"`: ⚠️ **The Dogmatic Trap** | *"You used dogmatic absolutes ('You always', 'Obviously', 'There is no question'). Absolutes provoke instant resistance. Soften your delivery: 'It appears to me', 'My concern is that'."*
- `state_story_framing_awareness == "story_stated_as_absolute_truth"`: ⚠️ **Story as Fact Alert** | *"You stated your interpretation as an incontrovertible fact. Remember: facts are verifiable; stories are mental models. Frame your conclusion as: 'The story I'm telling myself is...'."*
- `state_ask_and_encourage_testing != "genuine_inquiry_and_testing"`: 🤐 **Monologue Warning** | *"You failed to genuinely invite the other party's perspective. In Crucial Conversations, dialogue requires inquiry: ask 'How do you see this differently?'."*
- `state_mutual_purpose_safety == "adversarial_me_vs_you"`: ⚔️ **Adversarial Framing** | *"You framed the disagreement as me-vs-you. Establish Mutual Purpose first: remind them of your shared goal (e.g., 'We both want this launch to succeed')."*

---

### Framework 8: Gottman De-escalation (The Four Horsemen & Antidotes)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 90$ seconds.
- **Philosophy:** Dr. John Gottman; Four Horsemen (Criticism, Contempt, Defensiveness, Stonewalling); Gentle Start-up; Repair Attempts; Physiological Reset.
- **Target Framework Wire Key:** `"GOTTMAN"`

#### Jev System One Questions (6 Total)
1. `gottman_four_horsemen_marker` (`choice`)
   - `none_clean_de_escalated`: $1.0$ (Penalty = 1.0)
   - `defensiveness_detected`: $0.6$
   - `criticism_detected`: $0.5$
   - `stonewalling_detected`: $0.4$
   - `contempt_detected`: **$0.1$ (Catastrophic Failure Marker)**
2. `gottman_soft_startup_presence` (`noul`)
   - `yes`: $1.0$, `no`: $0.2$.
3. `gottman_responsibility_acceptance` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
4. `gottman_repair_attempt_usage` (`choice`)
   - `active_repair_attempt_used`: $1.0$, `not_applicable_steady`: $1.0$, `missed_or_escalated`: $0.2$.
5. `gottman_flooding_awareness_timeout` (`choice`)
   - `structured_timeout_called`: $1.0$, `in_session_de_escalation`: $1.0$, `abrupt_stormout_or_abandonment`: $0.1$.
6. `gottman_validation_of_counterpart` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).

#### Scoring Formulation (Multiplicative Penalty Model)
$$Score_{\text{Gottman}} = \text{Penalty}_{\text{Horsemen}} \times \left[ 0.30 S_R + 0.25 S_V + 0.15 P_S + 0.15 P_A + 0.15 P_T \right]$$
- Responsibility Acceptance ($W_R = 30\%$)
- Validation of Counterpart ($W_V = 25\%$)
- Soft Start-up ($W_S = 15\%$)
- Repair Attempt ($W_A = 15\%$)
- Flooding / Timeout Management ($W_T = 15\%$)

#### Badges & Coaching Tips
- `gottman_four_horsemen_marker == "none_clean_de_escalated"` AND `gottman_responsibility_acceptance >= "Level 4"`: 🕊️ **Masterful De-escalation** | *"Exemplary emotional leadership. You neutralized a volatile crisis by validating their frustration and owning your piece of the breakdown without defensiveness."*
- `gottman_four_horsemen_marker == "contempt_detected"`: 🚨 **Contempt Alert (Deadliest Marker)** | *"Detected sarcasm, mocking, or sneering language. In Gottman's research, Contempt is the #1 predictor of partnership destruction. Banish all sarcasm and address the problem as equals."*
- `gottman_four_horsemen_marker == "defensiveness_detected"`: ⚠️ **Defensive Trap** | *"You played the blameless victim or counter-attacked ('Don't blame me!'). Defensiveness escalates anger. Neutralize it by owning even 5% of the fault: 'You're right, I should have flagged that earlier'."*
- `gottman_repair_attempt_usage == "active_repair_attempt_used"`: 🧯 **Repair Attempt Deployed** | *"Great use of an active de-escalation gesture ('Can we take a breath?', 'Can I take that back?'). Repair attempts prevent arguments from spiraling."*
- `gottman_validation_of_counterpart <= "Level 2"`: ❄️ **Emotional Invalidation** | *"You dismissed their feelings ('You're overreacting'). People cannot solve problems logically until they feel heard. Validate their emotion first: 'I understand why you are so upset'."*
- `gottman_flooding_awareness_timeout == "structured_timeout_called"`: ⏱️ **Flooding Timeout Called** | *"Excellent nervous system regulation. When heart rate spikes, adrenaline prevents logic. A structured 20-minute break protects the partnership."*

---

### Framework 9: Voss Tactical Empathy (Negotiation)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 90$ seconds.
- **Philosophy:** Chris Voss; Emotion Labeling (sensory stems, banish "I"); Calibrated Questions (How/What, banish "Why"); No-Oriented Questions; Late-Night FM DJ Voice; Reciprocal Concessions (Ackerman).
- **Target Framework Wire Key:** `"VOSS_NEGOTIATION"`

#### Jev System One Questions (6 Total)
1. `voss_emotion_labeling` (`noul`)
   - `yes`: $1.0$, `no`: $0.2$. (Strict Voss rule: sensory stems without "I").
2. `voss_calibrated_questions` (`choice`)
   - `calibrated_how_what`: $1.0$, `closed_interrogation`: $0.5$, `no_questions_asked`: $0.3$, `accusatory_why`: **$0.1$ (Severe Penalty)**.
3. `voss_no_oriented_inquiry` (`choice`)
   - `no_oriented_question_present`: $1.0$, `standard_neutral_phrasing`: $0.7$, `forcing_yes_manipulation`: $0.2$.
4. `voss_vocal_tone_estimate` (`choice`)
   - `late_night_dj_calm`: $1.0$, `assertive_professional`: $0.75$, `submissive_apologetic`: $0.3$, `aggressive_combative`: $0.1$.
5. `voss_reciprocal_concession_framing` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
6. `voss_mirroring_technique` (`choice`)
   - `mirror_used_effectively`: $1.0$, `mirror_not_used_or_unnecessary`: $0.8$, `awkward_parroting`: $0.3$.

#### Scoring Weights
$$Score_{\text{Voss}} = 0.25 P_L + 0.30 P_Q + 0.25 S_C + 0.10 P_T + 0.05 P_N + 0.05 P_M$$
- Emotion Labeling ($W_L = 25\%$)
- Calibrated Questions ($W_Q = 30\%$ — Heaviest Weight)
- Reciprocal Concessions ($W_C = 25\%$)
- Vocal Tone ($W_T = 10\%$)
- No-Oriented Question ($W_N = 5\%$)
- Mirroring ($W_M = 5\%$)

#### Badges & Coaching Tips
- `voss_emotion_labeling.yes >= 0.8`: 🏷️ **Tactical Empathy Master** | *"Flawless emotion labeling. By starting with 'It sounds like / It seems like', you disarmed tension and made the counterpart feel heard without conceding leverage."*
- `voss_calibrated_questions == "accusatory_why"`: ⚠️ **The 'Why' Trap** | *"You asked a 'Why' question ('Why did you raise the rates?'). 'Why' triggers defensiveness in negotiation. Rephrase to a calibrated 'What': 'What led to this change in pricing?'"*
- `voss_emotion_labeling.no >= 0.8`: ❄️ **Missing Emotion Label** | *"You jumped straight into counter-arguments without labeling their emotion. Always diffuse negative tension first: 'It sounds like your hands are tied by corporate leadership'."*
- `voss_calibrated_questions == "calibrated_how_what"`: 🧠 **Cognitive Burden Shift** | *"Brilliant calibrated question ('How am I supposed to do that?'). You passed the burden of solving the pricing dilemma to the counterpart without being aggressive."*
- `voss_reciprocal_concession_framing <= "Level 2"`: 💸 **Unreciprocated Concession** | *"You compromised too easily or offered to split the difference. In high-stakes negotiation, never concede without asking for something in return: 'If I agree to X, what can you do for Y?'"*
- `voss_vocal_tone_estimate == "late_night_dj_calm"`: 🎙️ **Late-Night FM DJ** | *"Exceptional vocal poise. Your calm, downward-inflecting delivery projected quiet authority and de-escalated tension."*

---

### Framework 10: Duarte Sparkline (Presentations & Keynotes)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 120$ seconds.
- **Philosophy:** Nancy Duarte; Audience is the Hero (Mentor/Yoda); "What Is" vs "What Could Be" Oscillation; S.T.A.R. Moment; The New Bliss.
- **Target Framework Wire Key:** `"DUARTE_SPARKLINE"`

#### Jev System One Questions (6 Total)
1. `sparkline_what_is_vs_could_be_contrast` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
2. `sparkline_audience_as_hero` (`choice`)
   - `audience_is_the_hero`: $1.0$, `neutral_detached`: $0.5$, `speaker_centered_ego`: $0.1$.
3. `sparkline_hook_first_30s` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
4. `sparkline_star_moment_presence` (`choice`)
   - `star_moment_present`: $1.0$, `generic_claim_only`: $0.4$, `absent`: $0.0$.
5. `sparkline_new_bliss_vision` (`choice`)
   - `inspiring_new_bliss`: $1.0$, `flat_logistical_ending`: $0.3$, `absent_or_unresolved`: $0.0$.
6. `sparkline_call_to_adventure` (`choice`)
   - `clear_call_to_adventure`: $1.0$, `vague_invitation`: $0.4$, `absent`: $0.0$.

#### Scoring Weights
$$Score_{\text{Sparkline}} = 0.35 S_C + 0.25 S_H + 0.15 P_A + 0.10 P_S + 0.10 P_N + 0.05 P_T$$
- Contrast Engine ($W_C = 35\%$ — Heaviest Weight)
- Opening Hook ($W_H = 25\%$)
- Audience as Hero ($W_A = 15\%$)
- S.T.A.R. Moment ($W_S = 10\%$)
- The New Bliss ($W_N = 10\%$)
- Call to Adventure ($W_T = 5\%$)

#### Badges & Coaching Tips
- `sparkline_what_is_vs_could_be_contrast >= "Level 4"`: ⚡ **Duarte Cadence Master** | *"Outstanding oratorical rhythm. You created compelling narrative tension by continuously oscillating between the pain of current reality and the promise of the future."*
- `sparkline_hook_first_30s <= "Level 2"`: 🥱 **Throat-Clearing Warning** | *"You opened with boring pleasantries or administrative setup. In high-stakes talks, grab the room in the first 15 seconds: open with a startling metric, provocative question, or vivid story."*
- `sparkline_what_is_vs_could_be_contrast <= "Level 2"`: 📉 **Flat Information Dump** | *"Your presentation felt like a flat feature list. Build dynamic contrast: show what is broken or painful today, then contrast it directly with what could be."*
- `sparkline_audience_as_hero == "speaker_centered_ego"`: 👑 **Ego Trap Alert** | *"You framed yourself or your company as the sole hero. In Duarte's doctrine, the audience is Luke Skywalker; you are Yoda. Show how adopting your idea makes THEM triumphant."*
- `sparkline_star_moment_presence == "star_moment_present"`: 🌟 **S.T.A.R. Moment Delivered** | *"Great job including a memorable showcase moment. Unforgettable proof points and vivid case studies stick in the audience's memory long after the talk."*
- `sparkline_new_bliss_vision == "inspiring_new_bliss"`: 🌅 **The New Bliss Achieved** | *"Inspiring conclusion. You ended not on logistics, but on an elevated vision of how the world will operate once this mission is accomplished."*

---

### Framework 11: Monroe's Motivated Sequence (Persuasion)

#### Dimensions & Architecture
- **Pacing Budget:** $\sim 120$ seconds.
- **Philosophy:** Alan H. Monroe; Linear 5-step psychological escalation: Attention $\rightarrow$ Need $\rightarrow$ Satisfaction $\rightarrow$ Visualization $\rightarrow$ Action.
- **Target Framework Wire Key:** `"MONROE_SEQUENCE"`

#### Jev System One Questions (6 Total)
1. `monroe_attention_hook` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
2. `monroe_need_urgency` (`choice`)
   - `acute_need_proven`: $1.0$, `vague_need_low_urgency`: $0.4$, `absent`: $0.0$.
3. `monroe_satisfaction_viability` (`choice`)
   - `concrete_viable_solution`: $1.0$, `vague_or_incomplete_solution`: $0.4$, `absent`: $0.0$.
4. `monroe_visualization_polarity` (`score`)
   - Levels 1--5 normalized: Level 5 ($1.0$), Level 4 ($0.8$), Level 3 ($0.6$), Level 2 ($0.4$), Level 1 ($0.2$).
5. `monroe_action_friction_and_clarity` (`choice`)
   - `singular_frictionless_ask`: $1.0$, `burdensome_or_multiple_asks`: $0.4$, `vague_non_committal_close`: $0.2$, `absent`: $0.0$.
6. `monroe_sequence_progression` (`choice`)
   - `flawless_five_step_progression`: $1.0$, `minor_step_omission`: $0.6$, `disordered_or_jumbled`: $0.2$.

#### Scoring Weights
$$Score_{\text{Monroe}} = 0.15 S_H + 0.25 P_N + 0.15 P_S + 0.20 S_V + 0.25 P_A + 0.10 P_P$$
- Attention Hook ($W_H = 15\%$)
- Need Urgency ($W_N = 25\%$)
- Satisfaction Solution ($W_S = 15\%$)
- Visualization Polarity ($W_V = 20\%$)
- Action Clarity & Friction ($W_A = 25\%$ — Crucial Persuasive Pivot)
- Sequence Progression ($W_P = 10\%$)

#### Badges & Coaching Tips
- `monroe_action_friction_and_clarity == "singular_frictionless_ask"` AND `monroe_need_urgency == "acute_need_proven"`: 🎯 **Persuasion Master** | *"Flawless execution of Monroe's Sequence. You established acute urgency, proved the solution, and closed with a razor-sharp, frictionless call to action."*
- `monroe_action_friction_and_clarity == "vague_non_committal_close"`: ⚠️ **The Wasted Close** | *"You built great momentum but ended with a weak, non-committal ask ('Think about it and let me know'). Always close with a specific physical step: 'Sign here for the 30-day pilot today'."*
- `monroe_need_urgency == "absent"`: 🚨 **Solution Without Need** | *"You pitched your solution before the audience felt the pain. People do not buy cures for diseases they don't have. Develop the Need and consequence of inaction first."*
- `monroe_visualization_polarity <= "Level 2"`: 🌫️ **Missing Visualization** | *"You omitted the Visualization step. People buy on emotion and justify with logic: paint a vivid picture of the relief of success versus the disaster of doing nothing."*
- `monroe_action_friction_and_clarity == "burdensome_or_multiple_asks"`: 🛑 **Decision Fatigue Warning** | *"You overwhelmed the decision-maker with too many requests. Narrow your ask to a single, frictionless next step."*
- `monroe_attention_hook <= "Level 2"`: 🥱 **Weak Opening Hook** | *"Your opening lacked punch. Cut pleasantries: open with an arresting metric or incident that shatters complacency in the first 15 seconds."*

---

## 7. Master Framework Registry & Architecture Blueprint

### 7.1 Framework Identifier Constants
To ensure zero divergence across backend gateways and schemas, the following string identifiers must be used:
```python
class FrameworkKey(str, Enum):
    STAR = "STAR"
    CARL = "CARL"
    PAR = "PAR"
    SCQA = "SCQA"
    SBI = "SBI"
    RADICAL_CANDOR = "RADICAL_CANDOR"
    STATE = "STATE"
    GOTTMAN = "GOTTMAN"
    VOSS_NEGOTIATION = "VOSS_NEGOTIATION"
    DUARTE_SPARKLINE = "DUARTE_SPARKLINE"
    MONROE_SEQUENCE = "MONROE_SEQUENCE"
```

### 7.2 Total Question Count Summary
- STAR: 6 questions
- CARL: 6 questions
- PAR: 5 questions
- SCQA: 6 questions
- SBI: 5 questions
- RADICAL_CANDOR: 5 questions
- STATE: 6 questions
- GOTTMAN: 6 questions
- VOSS_NEGOTIATION: 6 questions
- DUARTE_SPARKLINE: 6 questions
- MONROE_SEQUENCE: 6 questions
- **Total Defined Jev Questions Across Monorepo:** 63 questions.

### 7.3 Jev Wire Templates (JSON Definitions Ready for Implementation)
Every single question's instructions and criteria are verbatim extracted from the authoritative markdown files in `docs/frameworks/` and are directly importable into `app/gateways/typesafe.py` or a dedicated framework definitions registry.

---
