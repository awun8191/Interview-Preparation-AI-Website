# Handoff Report: Complete Communication Frameworks Specification Mining

**Agent:** `spec_miner_1` (Teamwork Specification Miner)  
**Date:** 2026-09-17  
**Type:** Hard (Task complete)  
**Deliverable Path:** `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/spec_miner_1/analysis.md`

---

## 1. Observation

### Source Material Observed
Directly inspected all 12 specification files in `/home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/`:
- `jev-comms.md` (lines 1–310): Tripartite cognitive architecture, Gemini generation prompt contract, Jev `/v1/systemone` parallel state/question contract, delivery analytics ($WPM$, pauses, fillers), deterministic scoring, and STAR evaluation suite.
- `star.md` (lines 1–310): STAR dimensions (S: 15%, T: 15%, A: 55%, R: 15%), 6 Jev questions (`star_situation_grounding`, `star_task_clarity`, `star_action_ownership_and_depth`, `star_result_and_impact`, `star_narrative_balance`, `star_prompt_relevance`), Balanced Impact Rule (lines 119–125 & 277–278), scoring weights (15/15/45/15/10), and badge triggers.
- `carl.md` (lines 1–251): Executive reflection & systemic learning, 4 dimensions (C: 15–20%, A: 35%, R: 15%, L: 25–30%), 6 Jev questions (`carl_context_framing`, `carl_action_ownership_and_rigor`, `carl_result_and_impact`, `carl_learning_metacognitive_depth`, `carl_narrative_balance`, `carl_vulnerability_and_humility`), non-linear scoring on Learning (Level 1: 0.0, Level 2: 0.30, Level 3: 0.65, Level 4: 0.85, Level 5: 1.0), scoring weights (15/25/15/35/10), and badge triggers.
- `par.md` (lines 1–234): Executive brevity (45–60s), 3 dimensions (Problem: 10–15s, Action: 30–35s, Result: 10–15s), 5 Jev questions (`par_problem_sharpness`, `par_action_decisiveness`, `par_result_and_impact`, `par_brevity_and_information_density`, `par_prompt_relevance`), non-linear scoring on Action (Level 1: 0.1, Level 2: 0.35, Level 3: 0.65, Level 4: 0.85, Level 5: 1.0), scoring weights (20/45/20/15), and badge triggers.
- `scqa.md` (lines 1–232): Minto Pyramid / BLUF, 4 dimensions (Situation, Complication, Question, Answer), 6 Jev questions (`scqa_situation_baseline`, `scqa_complication_friction`, `scqa_governing_question`, `scqa_bluf_efficiency`, `scqa_recommendation_substance`, `scqa_structural_flow`), scoring weights (10/20/10/30/20/10), and badge triggers.
- `sbi.md` (lines 1–221): Center for Creative Leadership feedback, Camera-Recordable Test, Banish Feedback Sandwich, 5 Jev questions (`sbi_situation_anchoring`, `sbi_behavioral_camera_test`, `sbi_impact_operational_clarity`, `sbi_feedback_sandwich_filter`, `sbi_solution_co_creation`), scoring weights (15/35/25/10/15), and badge triggers.
- `radical_candor.md` (lines 1–227): Kim Scott 2x2 Matrix (Care Personally vs Challenge Directly), 5 Jev questions (`candor_quadrant_classification`, `candor_challenge_directly_clarity`, `candor_care_personally_signals`, `candor_private_developmental_setting`, `candor_openness_to_counter_feedback`), scoring weights (30/35/25/10), and badge triggers.
- `state.md` (lines 1–238): Crucial Conversations protocol, 5 dimensions (Share facts, Tell story, Ask path, Talk tentatively, Encourage testing), 6 Jev questions (`state_facts_first_sequencing`, `state_story_framing_awareness`, `state_tentative_language_calibration`, `state_mutual_purpose_safety`, `state_ask_and_encourage_testing`, `state_emotional_composure`), scoring weights (20/15/25/10/20/10), and badge triggers.
- `gottman.md` (lines 1–267): Conflict de-escalation, Four Horsemen (Criticism, Contempt, Defensiveness, Stonewalling), 6 Jev questions (`gottman_four_horsemen_marker`, `gottman_soft_startup_presence`, `gottman_responsibility_acceptance`, `gottman_repair_attempt_usage`, `gottman_flooding_awareness_timeout`, `gottman_validation_of_counterpart`), multiplicative penalty formulation with Contempt as 0.1x failure marker, scoring weights (30/25/15/15/15), and badge triggers.
- `voss.md` (lines 1–253): Chris Voss Tactical Empathy, sensory emotion labeling without "I", calibrated questions without "Why", Ackerman bargaining, 6 Jev questions (`voss_emotion_labeling`, `voss_calibrated_questions`, `voss_no_oriented_inquiry`, `voss_vocal_tone_estimate`, `voss_reciprocal_concession_framing`, `voss_mirroring_technique`), severe penalty (0.1) for 'Why', scoring weights (25/30/25/10/5/5), and badge triggers.
- `sparkline.md` (lines 1–236): Nancy Duarte presentation geometry, "What Is" vs "What Could Be" oscillation, S.T.A.R. moment, New Bliss, 6 Jev questions (`sparkline_what_is_vs_could_be_contrast`, `sparkline_audience_as_hero`, `sparkline_hook_first_30s`, `sparkline_star_moment_presence`, `sparkline_new_bliss_vision`, `sparkline_call_to_adventure`), scoring weights (35/25/15/10/10/5), and badge triggers.
- `monroe.md` (lines 1–243): Alan Monroe 5-step motivated sequence (Attention, Need, Satisfaction, Visualization, Action), 6 Jev questions (`monroe_attention_hook`, `monroe_need_urgency`, `monroe_satisfaction_viability`, `monroe_visualization_polarity`, `monroe_action_friction_and_clarity`, `monroe_sequence_progression`), scoring weights (15/25/15/20/25/10), and badge triggers.
- `CLAUDE.md` and `AGENTS.md` (lines 1–132): Sub-second latency budget ($<1.0\text{s}$), standard error envelope specification (`error.code`, `error.message`, `retryable`), backend directory conventions (`app/gateways/`, `app/services/`).

---

## 2. Logic Chain

1. **Premise 1:** The user request requires mining all specifications in `docs/frameworks/` for 11 communication frameworks (STAR, CARL, PAR, SCQA, SBI, Radical Candor, STATE, Gottman, Voss, Sparkline, Monroe).
2. **Premise 2:** Examination of `docs/frameworks/` confirmed exactly 11 framework Markdown files plus `jev-comms.md`.
3. **Premise 3:** Each framework markdown file follows a standardized, highly rigorous structure containing:
   - Theoretical foundation & dimension breakdown.
   - Gemini scenario generation prompt contract (JSON schema, input parameters, target durations).
   - Jev System One evaluation state schema (`scenario_prompt`, `scenario_context`, `target_framework`, `speaker_role`, `transcript`, `word_count`, `duration_seconds`, `words_per_minute`).
   - 5 to 6 discrete typed questions for Jev System One (`choice`, `score`, or `noul`), with instructions and exhaustive criteria definitions (totalling 63 questions across the 11 frameworks).
   - Explicit composite score formulas ($Score_{\text{Framework}}$) with weights summing to 100% (or multiplicative penalty models like Gottman).
   - Real-time coaching triggers mapping specific Jev evaluation outputs to UI badges and actionable sentences.
4. **Premise 4:** The Balanced Impact Rule is defined in `jev-comms.md:119-125`, `star.md:216-225, 277-278`, `carl.md:47-51`, `par.md:47-51`, etc., and mandates that quantitative metrics and qualitative/operational outcomes receive equal top subscores ($1.0$).
5. **Conclusion:** All framework dimensions, question schemas, scoring rubrics, badge triggers, and architectural contracts have been completely mined and documented in `analysis.md` for deterministic backend implementation.

---

## 3. Caveats

- **No Caveats.** Every framework document in `docs/frameworks/` was read and mined in full. All 63 question primitives, rubrics, mathematical weights, and badge triggers have been cataloged without omissions.

---

## 4. Conclusion

The specification mining phase is complete. The backend implementation team has everything necessary to:
1. Construct the Pydantic schemas for Jev requests/responses and error envelopes.
2. Build the Jev gateway in `app/gateways/typesafe.py` with static, immutable question definitions for all 11 frameworks.
3. Build the deterministic scoring engine in `app/services/scoring.py` computing composite 0–100 scores and synthesizing badges/tips in $<10\text{ms}$.
4. Implement the Balanced Impact Rule across STAR, CARL, PAR, SCQA, and other outcome questions.

---

## 5. Verification Method

To independently verify the mining findings:
1. Inspect `analysis.md` at:
   `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/spec_miner_1/analysis.md`
2. Cross-reference any question ID or formula against its authoritative source in `docs/frameworks/`:
   ```bash
   grep -n "star_result_and_impact" /home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/star.md
   grep -n "carl_learning_metacognitive_depth" /home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/carl.md
   grep -n "gottman_four_horsemen_marker" /home/nasbombz/Documents/Projects/the-plan-software/docs/frameworks/gottman.md
   ```
3. Invalidation condition: If any question ID, criteria key, or scoring weight in `analysis.md` fails to match the corresponding definition in `docs/frameworks/`, the specification is invalid.
