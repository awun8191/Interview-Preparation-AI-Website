# Handoff Report: Reviewer 2 (Frameworks, Rubrics & Scoring Math)

**Author**: reviewer_2  
**Role**: Objective Reviewer & Adversarial Critic  
**Working Directory**: `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/reviewer_2`  
**Date**: 2026-09-17T20:51:40Z  
**Verdict**: **REQUEST_CHANGES**

---

## 1. Observation

1. **Verification Commands**:
   - `uv run pytest` executed cleanly:
     ```
     ============================= 163 passed in 0.74s ==============================
     ```
   - `uv run ruff check .` executed cleanly:
     ```
     All checks passed!
     ```
   - `uv run ruff format --check .` failed with exit code 1:
     ```
     unformatted: File would be reformatted
       --> .agents/worker_remediation/analysis.md:27:23
        |
     26 |     "choice": choice,
        -     "probabilities": { ... },
     27 +     "probabilities": {...},
     28 | }
        |

     1 file would be reformatted, 136 files already formatted
     ```
     In `backend/pyproject.toml:38-46`, `[tool.ruff]` defines `target-version = "py313"` and `line-length = 100`, but lacks `extend-exclude = [".agents"]`.

2. **Framework Catalogs (`app/frameworks/catalogs/`)**:
   - All 11 catalogs exist: `star.py`, `carl.py`, `par.py`, `scqa.py`, `sbi.py`, `radical_candor.py`, `state.py`, `gottman.py`, `voss.py`, `sparkline.py`, `monroe.py`.
   - Question count across all 11 catalogs is exactly 63:
     `STAR: 6, CARL: 6, PAR: 5, SCQA: 6, SBI: 5, RADICAL_CANDOR: 5, STATE: 6, GOTTMAN: 6, VOSS: 6, SPARKLINE: 6, MONROE: 6` (sum = 63).
   - Dimension weights in each of the 11 catalogs sum strictly to 1.00:
     - STAR: 0.15 + 0.15 + 0.45 + 0.15 + 0.10 = 1.00
     - CARL: 0.15 + 0.25 + 0.15 + 0.35 + 0.10 = 1.00
     - PAR: 0.20 + 0.45 + 0.20 + 0.15 = 1.00
     - SCQA: 0.10 + 0.20 + 0.10 + 0.30 + 0.20 + 0.10 = 1.00
     - SBI: 0.15 + 0.35 + 0.25 + 0.10 + 0.15 = 1.00
     - RADICAL_CANDOR: 0.30 + 0.35 + 0.25 + 0.10 = 1.00
     - STATE: 0.20 + 0.15 + 0.25 + 0.10 + 0.20 + 0.10 = 1.00
     - GOTTMAN: 0.30 + 0.25 + 0.15 + 0.15 + 0.15 = 1.00
     - VOSS: 0.25 + 0.30 + 0.25 + 0.10 + 0.05 + 0.05 = 1.00
     - SPARKLINE: 0.35 + 0.25 + 0.15 + 0.10 + 0.10 + 0.05 = 1.00
     - MONROE: 0.10 + 0.25 + 0.10 + 0.20 + 0.25 + 0.10 = 1.00

3. **Deterministic Scoring Engine (`app/services/scoring.py`)**:
   - Balanced Impact Rule: Full 1.0 credit awarded to `meaningful_qualitative_impact` and `quantified_metric_impact` across STAR, CARL, PAR, SCQA, and SBI.
   - Gottman Contempt Collapse: `gottman_four_horsemen_marker == "contempt_detected"` multiplies base score by 0.1 (lines 204-214).
   - Voss Calibrated Questions: `accusatory_why` incurs score 0.1 on the 0.30 weighted dimension and sets `domain_penalties["accusatory_why_used"] = True`.
   - CARL Metacognitive Learning: Non-linear scale Level 1: 0.0, Level 2: 0.30, Level 3: 0.65, Level 4: 0.85, Level 5: 1.0.
   - PAR Brevity: Penalizes duration > 75s and `bloated_or_rambling`.
   - Adversarial Regex Finding: Lines 130-136 in `scoring.py`:
     ```python
     m = re.search(r"([1-5])", lvl_str)
     if m:
         lvl_int = int(m.group(1))
         opt2 = question.criteria.get(f"Level {lvl_int}")
         if opt2:
             return opt2.score
         return lvl_int / 5.0
     ```
     Observed execution: Passing `{"star_action_ownership_and_depth": -5}` returns `100.0` action subscore because `re.search(r"([1-5])", "-5")` matches `'5'`, awarding maximum score to negative integers.

4. **Firestore Data Models (`app/models/session.py` & `app/gateways/firestore.py`)**:
   - `UserRecord`: fields `user_id`, `email`, `display_name`, `role`, `subscription_tier`, `created_at`.
   - `SessionRecord`: fields `session_id`, `user_id`, `framework`, `prompt`, `transcript`, `score` (bounded 0.0-100.0), `findings`, `tips`, `badges`, `delivery_metrics`, `created_at`.
   - Validation correctly rejects out-of-range scores and unapproved roles/tiers.

---

## 2. Logic Chain

1. From Observation 1, the user acceptance criteria in `ORIGINAL_REQUEST.md` state:
   "`uv run ruff check .` and `uv run ruff format --check .` pass with zero errors."
2. `uv run ruff format --check .` exits with code 1 because `.agents/worker_remediation/analysis.md` contains unformatted code blocks, and `pyproject.toml` does not exclude `.agents/` from formatting.
3. Therefore, the verification criterion for `ruff format --check .` is currently failing.
4. From Observation 3, `_score_single_question` in `scoring.py` uses `re.search(r"([1-5])", lvl_str)` without guarding against negative numbers or requiring word boundaries. Passing an input of `-5` causes the regex to capture `5`, awarding a 100% score to an adversarial negative input.
5. In accordance with reviewer responsibilities to stress-test failure modes and enforce acceptance criteria without modifying implementation code ourselves, these findings must be addressed by remediation.
6. Consequently, the review verdict must be `REQUEST_CHANGES`.

---

## 3. Caveats

- In-memory synthetic gateways (`SyntheticFirestoreGateway`, `SyntheticJevGateway`) were used for offline verification, matching the requirement that no external API keys are required during the test suite.
- Production Firestore integration against live Google Cloud project `theplan-9311e` was verified via client configuration and mock tests, but not connected live over the network due to offline test isolation rules.
- No other caveats.

---

## 4. Conclusion

**Verdict: REQUEST_CHANGES**

The framework catalogs, scoring formulas, Balanced Impact Rule, and Firestore models are well-architected, highly faithful to the domain specifications, and functionally sound. However, changes are requested to address two concrete issues:
1. **[Critical] Fix Ruff Format Check Failure**:
   Add `extend-exclude = [".agents"]` to `backend/pyproject.toml` under `[tool.ruff]` (or format `.agents/worker_remediation/analysis.md`) so that `uv run ruff format --check .` passes with zero errors.
2. **[Major] Harden Regex in `app/services/scoring.py:130-136`**:
   Prevent negative integer inputs (e.g. `-5`) from falsely matching digit `5` and receiving maximum credit.

---

## 5. Verification Method

1. Run `uv run pytest` from `backend/` to verify test suite health:
   ```bash
   uv run pytest
   ```
2. Run `uv run ruff check .` to verify linting:
   ```bash
   uv run ruff check .
   ```
3. Run `uv run ruff format --check .` to verify formatting:
   ```bash
   uv run ruff format --check .
   ```
4. Verify negative input handling in `ScoringEngine`:
   ```bash
   uv run python -c "from app.services.scoring import ScoringEngine; e = ScoringEngine(); res = e.score_session('STAR', {'star_action_ownership_and_depth': -5}); print(res.subscores['action'])"
   ```
   (Must output `0.0`, not `100.0`).
