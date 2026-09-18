# Handoff Report: Adversarial Verification & Tier 5 Coverage Hardening

## Verdict: REJECT

**Date**: 2026-09-17T20:56:00Z  
**Agent**: challenger_1 (teamwork_preview_challenger)  
**Roles**: critic, specialist  
**Working Directory**: `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/challenger_1`  

---

## 1. Observation

### 1.1 Test Execution Commands & Results
- **Full Test Suite Execution**:
  Command: `uv run pytest`
  Output:
  ```
  ============================= 184 passed in 0.77s ==============================
  ```
  All 184 automated tests (including 21 newly authored Tier 5 tests in `tests/e2e/test_tier5_adversarial.py`) passed cleanly.

- **Ruff Lint Check**:
  Command: `uv run ruff check .`
  Output:
  ```
  All checks passed!
  ```

- **Ruff Format Check on Source & Tests**:
  Command: `uv run ruff format --check app tests`
  Output:
  ```
  65 files already formatted
  ```

- **Ruff Format Check on Root (`.`) Failure**:
  Command: `uv run ruff format --check .`
  Output:
  ```
  unformatted: File would be reformatted
    --> .agents/reviewer_1/handoff.md:84:93
     |
  83 |    ```python
     -    firestore_gateway: Annotated[FirestoreGatewayProtocol, Depends(get_firestore_gateway)] = None,
  84 +    firestore_gateway: Annotated[FirestoreGatewayProtocol, Depends(get_firestore_gateway)] = (None,)
  85 |    ```
     |
  1 file would be reformatted, 143 files already formatted
  ```
  Exit code: `1`.

### 1.2 Mathematical Vulnerability: `NaN` Invariant Bypass in `ScoringEngine`
- **File**: `/home/nasbombz/Documents/Projects/the-plan-software/backend/app/services/scoring.py` (lines 140-157, 233)
- **Observation**:
  In `_score_single_question`, when a NOUL finding is passed as `{"yes": float("nan")}`, `tot = yes_p + no_p` evaluates to `nan`. `tot > 0` evaluates to `False`. The function returns `(nan * 1.0) + (0.0 * 0.0) = nan`.
  In `score_session` line 233:
  ```python
  composite_score = round(max(0.0, min(100.0, base_score * 100.0)), 1)
  ```
  In Python, `min(100.0, float("nan"))` evaluates to `100.0`. `max(0.0, 100.0)` evaluates to `100.0`.
- **Empirical Execution**:
  ```bash
  uv run python -c "
  from app.services.scoring import ScoringEngine
  engine = ScoringEngine()
  p = {'gottman_soft_startup_presence': {'yes': float('nan')}}
  res = engine.score_session('GOTTMAN', p)
  print('composite_score:', res.composite_score)
  assert res.composite_score == 100.0
  "
  ```
  Output: `composite_score: 100.0`.
  A payload containing `NaN` bypasses all scoring logic and awards a perfect 100.0% score.

### 1.3 Delivery Analytics Crash (`TypeError`) on Null Timestamps
- **File**: `/home/nasbombz/Documents/Projects/the-plan-software/backend/app/services/analytics.py` (line 131)
- **Observation**:
  ```python
  sorted_timestamps = sorted(
      word_timestamps,
      key=lambda w: float(w.get("start", 0.0)),
  )
  ```
  When `word_timestamps = [{"word": "hello", "start": None, "end": 1.0}]`, `w.get("start", 0.0)` returns `None` because `"start"` key is present in the dict with value `None`.
  Executing `float(None)` raises:
  `TypeError: float() argument must be a string or a real number, not 'NoneType'`.

### 1.4 Raw Exception Leakage in Error Envelopes
- **Files**:
  - `app/api/v1/scenarios.py` (line 33): `message=f"Scenario generation provider failed: {exc}"`
  - `app/api/v1/sessions.py` (line 115): `message=f"Groq speech-to-text transcription failed: {exc}"`
  - `app/api/v1/sessions.py` (line 199): `message=f"TypeSafe AI Jev System One evaluation failed: {exc}"`, `details=str(exc)`
  - `app/api/v1/sessions.py` (line 286): `message=f"Failed to retrieve sessions from Firestore: {exc}"`
- **Observation**:
  When a gateway throws an exception with credentials or connection strings (e.g. `RuntimeError("Mock connection string: postgres://user:pass@internal-db:5432")`), the endpoint reflects `str(exc)` back to the HTTP client inside the `error.message` and `error.details` fields.

---

## 2. Logic Chain

1. **Step 1 (Root Format Check Failure)**: Observation 1.1 confirms that running the mandated repository check `uv run ruff format --check .` exits with code 1. Because `pyproject.toml` omitted `extend-exclude = [".agents"]`, markdown code fences in `.agents/reviewer_1/handoff.md` cause ruff formatting check to fail.
2. **Step 2 (Scoring Invariant Breach)**: Observation 1.2 empirically proves that `ScoringEngine` fails the mathematical clamping invariant: corrupted or malicious `NaN` inputs in NOUL questions evaluate via Python's `min(100.0, NaN)` to a full 100.0 score. This breaches the requirement that scoring must be robust against arbitrary inputs.
3. **Step 3 (Service Crash Vulnerability)**: Observation 1.3 shows that `calculate_delivery_analytics` crashes with unhandled `TypeError` when word timestamps contain `None`. If the speech-to-text provider returns null timestamps for unvoiced tokens, the endpoint will crash instead of completing analysis.
4. **Step 4 (Information Disclosure Risk)**: Observation 1.4 confirms that unhandled gateway exceptions reflect `str(exc)` into the client response envelope. In production, this can leak internal database URIs, API keys, or network hostnames, violating AGENTS.md Rule 4.
5. **Step 5 (Verdict Deduction)**: While 184 tests pass and Tier 5 coverage was successfully delivered, the presence of an invariant exploit (Defect 2), an unhandled service crash (Defect 3), potential credential leakage (Defect 4), and a failing `uv run ruff format --check .` command (Defect 1) requires an empirical verdict of **REJECT** until these 4 items are remediated.

---

## 3. Caveats

- **No Caveats on Tested Vectors**: Scoring math across all 11 frameworks, Balanced Impact Rule equality, 10,000+ words delivery analytics, multi-script Unicode processing, concurrent session persistence (20 concurrent requests), and basic malformed JSON error envelopes were empirically tested and confirmed passing.
- **Scope Limitation**: Challenger agents operate under the "Review-only — do NOT modify implementation code" constraint. The 4 defects are documented with precise reproduction code and recommended fixes for worker remediation.

---

## 4. Conclusion

**Verdict: REJECT**

The backend architecture is near production-ready, achieving 184/184 passing tests and sub-second execution speeds. However, approval is blocked until the following 4 items are remediated:
1. **Fix `pyproject.toml`**: Add `extend-exclude = [".agents"]` under `[tool.ruff]` so that `uv run ruff format --check .` passes cleanly.
2. **Fix `app/services/scoring.py`**: Sanitize `NaN` / `Inf` values in `_score_single_question` and guard `composite_score` against `math.isnan(base_score)`.
3. **Fix `app/services/analytics.py`**: Add safe float parsing for `word_timestamps` to handle `None` values without raising `TypeError`.
4. **Fix Gateway Exception Envelopes**: In `app/api/v1/scenarios.py` and `app/api/v1/sessions.py`, replace `f"...: {exc}"` with sanitized static client messages and do not reflect raw exception strings in `details`.

---

## 5. Verification Method

To independently reproduce the findings and verify remediation:

1. **Verify Root Ruff Format Failure**:
   ```bash
   uv run ruff format --check .
   ```
   *Current Result: Exits with code 1 due to unexcluded `.agents/`.*  
   *Expected Post-Fix: Exits with code 0.*

2. **Verify Full Test Suite (184 Tests including Tier 5)**:
   ```bash
   uv run pytest tests/e2e/test_tier5_adversarial.py -v
   uv run pytest
   ```
   *Expected Result: 184 passed in < 1.0s.*

3. **Verify NaN Scoring Exploit**:
   ```bash
   uv run python -c "
   from app.services.scoring import ScoringEngine
   engine = ScoringEngine()
   p = {'gottman_soft_startup_presence': {'yes': float('nan')}}
   res = engine.score_session('GOTTMAN', p)
   print('Score:', res.composite_score)
   assert res.composite_score == 100.0, 'Bug reproduced: NaN yields 100% score'
   "
   ```
   *Post-Fix Invalidation Condition*: `res.composite_score` must evaluate to `0.0`.

4. **Verify Timestamp Null Crash**:
   ```bash
   uv run python -c "
   from app.services.analytics import calculate_delivery_analytics
   calculate_delivery_analytics('hi', 5.0, [{'word': 'hi', 'start': None, 'end': 1.0}])
   "
   ```
   *Post-Fix Invalidation Condition*: Completes successfully without `TypeError`.
