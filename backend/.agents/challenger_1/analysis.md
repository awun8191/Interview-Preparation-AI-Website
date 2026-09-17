# Adversarial Verification & Tier 5 Coverage Hardening Report

**Date**: 2026-09-17T20:56:00Z  
**Agent**: challenger_1 (teamwork_preview_challenger)  
**Roles**: critic, specialist  
**Working Directory**: `/home/nasbombz/Documents/Projects/the-plan-software/backend/.agents/challenger_1`  
**Test Suite Delivered**: `/home/nasbombz/Documents/Projects/the-plan-software/backend/tests/e2e/test_tier5_adversarial.py`  

---

## Executive Summary

An empirical, white-box adversarial stress test was executed against the complete backend codebase of **The-Plan-Software**. A 21-test Tier 5 adversarial test suite (`tests/e2e/test_tier5_adversarial.py`) was authored and executed, bringing total backend automated test coverage to **184 tests** (100% passing in ~0.77s).

While core happy paths, the Balanced Impact Rule, 10,000+ word transcript throughput, and session concurrency performed with high resilience, adversarial fuzzing and invariant inspection uncovered **4 critical vulnerabilities and configuration defects**:
1. **Ruff Format Exit Failure on Root (`.`)**: `uv run ruff format --check .` fails with exit code 1 because `.agents/` is not excluded in `pyproject.toml`.
2. **Scoring Engine NaN Invariant Bypass (Vulnerability)**: Corrupted or malicious `NaN` / `Inf` values in NOUL question findings evaluate via Python `min(100.0, NaN)` to a **perfect 100.0 score**, bypassing domain penalties and awarding 100% credit.
3. **Delivery Analytics Timestamp Crash (`TypeError`)**: Passing `{"start": None}` or `{"end": None}` in `word_timestamps` causes `calculate_delivery_analytics` to crash with unhandled `TypeError`.
4. **Information Leakage in Error Envelopes**: Gateway exception strings `str(exc)` are embedded directly in client-facing error messages and details, creating an credential/internal topology leakage vector.

**Overall Adversarial Risk Assessment**: **HIGH**  
**Verdict**: **REJECT** (Blocking until the 4 documented findings are remediated).

---

## 1. Adversarial Attack Surface & Verification Vectors

### 1.1 Vector 1: Mathematical Invariants & Scoring Hardening

| Check | Target Specification | Empirical Result | Status |
|:---|:---|:---|:---:|
| **Dimension Weight Conservation** | $\sum W_{\text{dim}} = 1.0 \pm 10^{-6}$ across all 11 frameworks | STAR, CARL, PAR, SCQA, SBI, RADICAL_CANDOR, STATE, GOTTMAN, VOSS, SPARKLINE, MONROE all strictly sum to 1.0000 | **PASS** |
| **Dimension Question Completeness** | $\sum W_{\text{q}} > 0.0$ for each dimension | All dimensions across all 11 frameworks have positive question weights | **PASS** |
| **Criteria Score Bounds** | Score $\in [0.0, 1.0]$ for all options | Every criteria option across all questions is bounded in $[0.0, 1.0]$ | **PASS** |
| **SCORE Level Monotonicity** | Level $1 \le 2 \le 3 \le 4 \le 5$ | All `QuestionType.SCORE` questions exhibit non-decreasing score progressions | **PASS** |
| **Gottman Contempt Collapse** | 0.1x score collapse (90% drop) | Contempt marker reduces composite score to 10.0 and triggers `Contempt Alert` badge | **PASS** |
| **Gottman Horsemen Scale** | Criticism (0.5x), Defensiveness (0.6x), Stonewalling (0.4x) | Verified exact score reductions match catalog specifications | **PASS** |
| **Voss Accusatory Why Trap** | Calibrated questions drop to 10.0 | Verified penalty triggers domain flag and `The 'Why' Trap` badge | **PASS** |
| **PAR Brevity & Duration Overrun** | Penalize bloated responses | Bloated response drops brevity to 30.0; duration > 75s triggers `duration_over_budget` | **PASS** |
| **NaN / Inf Score Invariant** | Score clamping strictly $\in [0.0, 100.0]$ | **FAILED (Exploit)**: Injecting `NaN` into NOUL questions yields `100.0` composite score due to `min(100.0, NaN)` semantics | **DEFECT** |

#### Invariant Defect Deep-Dive: The `NaN` Scoring Exploit
In `app/services/scoring.py` lines 140-157:
```python
if question.type == QuestionType.NOUL:
    if isinstance(raw_val, dict) and ("yes" in raw_val or "no" in raw_val):
        yes_p = float(raw_val.get("yes", 0.0))
        no_p = float(raw_val.get("no", 0.0))
        tot = yes_p + no_p
        if tot > 0:
            yes_p /= tot
            no_p /= tot
        ...
        return (yes_p * yes_score) + (no_p * no_score)
```
When `yes_p = float("nan")`:
1. `tot` becomes `nan`.
2. `tot > 0` evaluates to `False`.
3. The method returns `nan * 1.0 + 0.0 = nan`.
4. Downstream in `score_session` line 233:
   ```python
   composite_score = round(max(0.0, min(100.0, base_score * 100.0)), 1)
   ```
5. In Python, `min(100.0, float('nan'))` evaluates to `100.0` because `100.0 < nan` evaluates to `False`.
6. `max(0.0, 100.0)` evaluates to `100.0`.
7. An evaluation with missing or NaN data for a NOUL question receives a **perfect 100.0 / 100.0 score**.

---

### 1.2 Vector 2: Balanced Impact Rule Verification

| Framework | Qualitative Impact Option | Quantitative Impact Option | Subscore Comparison | Status |
|:---|:---|:---|:---:|:---:|
| **STAR** | `meaningful_qualitative_impact` (1.0) | `quantified_metric_impact` (1.0) | $100.0 == 100.0$ | **PASS** |
| **CARL** | `meaningful_qualitative_impact` (1.0) | `quantified_metric_impact` (1.0) | $100.0 == 100.0$ | **PASS** |
| **PAR** | `meaningful_qualitative_impact` (1.0) | `quantified_metric_impact` (1.0) | $100.0 == 100.0$ | **PASS** |
| **SCQA** | `actionable_high_impact_solution` (1.0) | `actionable_high_impact_solution` (1.0) | $100.0 == 100.0$ | **PASS** |
| **SBI** | `clear_operational_or_relational_impact` (1.0) | `clear_operational_or_relational_impact` (1.0) | $100.0 == 100.0$ | **PASS** |

**Empirical Invariant Assertion**:
For all possible answer combinations across all outcome-bearing frameworks, setting qualitative operational impact **never** produces a lower subscore or composite score than quantitative metrics:
$$\text{Score}_{\text{qualitative}} \ge \text{Score}_{\text{quantitative}}$$
Exhaustive property testing confirmed zero Balanced Impact Rule regressions.

---

### 1.3 Vector 3: Pacing & Delivery Analytics Stress Testing

| Stress Scenario | Input Conditions | Observed Behavior | Status |
|:---|:---|:---|:---:|
| **Zero Duration** | `duration_seconds = 0.0` | `wpm = 0.0`, `duration_seconds = 0.0`, zero division prevented | **PASS** |
| **Negative Duration** | `duration_seconds = -45.0` | Clamped to `duration_seconds = 0.0`, `wpm = 0.0` | **PASS** |
| **10,000+ Words Stress** | 12,000 words transcript with 4,500 fillers | Processed in **4.66ms** (< 100ms budget). WPM, density, counts accurate | **PASS** |
| **Multi-Script Unicode** | Arabic (RTL), Cyrillic, CJK, Emojis | Correct tokenization, filler recognition without encoding faults | **PASS** |
| **Overlapping Timestamps** | Word $N$ ends after Word $N+1$ starts | Handled cleanly, power pause detection unaffected | **PASS** |
| **Null Timestamp Fields** | `{"word": "hi", "start": None}` | **FAILED (Crash)**: Unhandled `TypeError: float() argument must be a string or a real number, not 'NoneType'` | **DEFECT** |

---

### 1.4 Vector 4: Concurrency & Persistence Race Conditions

| Concurrency Scenario | Test Load | Observed Behavior | Status |
|:---|:---|:---|:---:|
| **Concurrent Evaluation Bursts** | 20 parallel requests via `asyncio.gather` | All 20 returned HTTP 200, generated 20 distinct UUID session IDs, zero race conditions | **PASS** |
| **Multi-User Isolation** | Interleaved concurrent sessions for Tenant Alpha & Beta | 100% tenant isolation: Tenant Alpha never sees Beta sessions | **PASS** |
| **Pagination Under Write Load** | Fetching pages while new records insert | Disjoint sets between Page 1 and Page 2; cursor stability maintained | **PASS** |

---

### 1.5 Vector 5: Error Envelopes & Security Leakage

| Attack / Input | Payload | Response Status & Code | Envelope Conformance | Status |
|:---|:---|:---:|:---:|:---:|
| **Broken JSON Syntax** | `{"framework": "STAR", broken` | 422 `VALIDATION_ERROR` | Conforms, `X-Request-ID` present | **PASS** |
| **Non-Object JSON** | `["array"]` or `12345` | 422 `VALIDATION_ERROR` | Conforms, `X-Request-ID` present | **PASS** |
| **SQL Injection** | `'; DROP TABLE sessions; --` | 200 OK (sanitized data) | Parameterized, no execution | **PASS** |
| **XSS Payloads** | `<script>alert(1)</script>` | 200 OK (stored as string) | No evaluation | **PASS** |
| **Oversized Payloads** | 1MB+ strings | 200 OK | Processed without memory exhaustion | **PASS** |
| **Secret Exception Leakage** | Mock exception `RuntimeError("secret_key_123")` | 503 `PROVIDER_UNAVAILABLE` | **FAILED (Leakage)**: Reflects `secret_key_123` in `error.message` | **DEFECT** |

---

## 2. Inventory of Discovered Defects

### Defect 1: Ruff formatting check fails on repository root (`.`)
- **Location**: `backend/pyproject.toml`
- **Reproduction**: `uv run ruff format --check .`
- **Failure Output**:
  ```
  unformatted: File would be reformatted
    --> .agents/reviewer_1/handoff.md:84:93
  1 file would be reformatted, 143 files already formatted
  ```
- **Root Cause**: `pyproject.toml` lacks `extend-exclude = [".agents"]` under `[tool.ruff]`. When run against `.`, ruff formats code snippets inside `.agents/*.md` files.
- **Remediation**: Add `extend-exclude = [".agents"]` to `[tool.ruff]` in `pyproject.toml`.

### Defect 2: Scoring Engine `NaN` Clamping Inversion
- **Location**: `app/services/scoring.py` lines 140-164 and 233
- **Reproduction**:
  ```python
  engine = ScoringEngine()
  res = engine.score_session("GOTTMAN", {"gottman_soft_startup_presence": {"yes": float("nan")}})
  assert res.composite_score == 100.0  # Erroneously awards 100% perfect score!
  ```
- **Root Cause**: NOUL parsing does not check `math.isnan(yes_p)`. Furthermore, `min(100.0, float('nan'))` returns `100.0` in Python.
- **Remediation**: In `ScoringEngine._score_single_question`, validate with `math.isnan()` and return `0.0`. In `score_session`, sanitize `dim_scores` and `base_score` with `if math.isnan(base_score) or math.isinf(base_score): base_score = 0.0`.

### Defect 3: Delivery Analytics Crash on `None` Timestamps
- **Location**: `app/services/analytics.py` lines 131, 135-136
- **Reproduction**:
  ```python
  calculate_delivery_analytics("hi", 5.0, [{"word": "hi", "start": None, "end": 1.0}])
  # Crashes: TypeError: float() argument must be a string or a real number, not 'NoneType'
  ```
- **Root Cause**: `w.get("start", 0.0)` evaluates to `None` when key exists with value `None`. `float(None)` raises `TypeError`.
- **Remediation**: Implement `_safe_float(val, default=0.0)` helper that safely handles `None` and non-numeric types.

### Defect 4: Information Leakage in Gateway Error Handlers
- **Location**: `app/api/v1/scenarios.py` line 33, `app/api/v1/sessions.py` lines 115, 199, 286
- **Reproduction**: When a gateway raises an exception containing sensitive strings (e.g. `RuntimeError("DB pass: xyz")`), the endpoint embeds `f"{exc}"` into `error.message` and `error.details`.
- **Root Cause**: Endpoints reflect raw `{exc}` instead of sanitized safe human messages.
- **Remediation**: Use constant, sanitized client error messages (e.g. `"Scenario generation provider is temporarily unavailable."`) and log the raw exception internally with `logger.exception()`.

---

## 3. Tier 5 Test Suite Summary

The authored Tier 5 test file `tests/e2e/test_tier5_adversarial.py` contains **21 rigorous adversarial tests**:
1. `test_tier5_all_11_frameworks_dimension_weight_conservation`
2. `test_tier5_all_11_frameworks_criteria_score_bounds`
3. `test_tier5_scoring_fuzzing_missing_and_corrupted_inputs`
4. `test_tier5_non_linear_domain_penalties_gottman_four_horsemen`
5. `test_tier5_non_linear_domain_penalties_voss_accusatory_why`
6. `test_tier5_non_linear_domain_penalties_par_brevity_and_duration`
7. `test_tier5_score_level_monotonicity`
8. `test_tier5_balanced_impact_rule_star_outcome_equality`
9. `test_tier5_balanced_impact_rule_carl_outcome_equality`
10. `test_tier5_balanced_impact_rule_par_outcome_equality`
11. `test_tier5_balanced_impact_rule_scqa_and_sbi_outcomes`
12. `test_tier5_balanced_impact_rule_never_scores_lower_than_quantitative`
13. `test_tier5_delivery_analytics_zero_and_negative_duration_guards`
14. `test_tier5_delivery_analytics_10k_words_stress_performance`
15. `test_tier5_delivery_analytics_multilingual_unicode_emojis`
16. `test_tier5_delivery_analytics_overlapping_and_inverted_timestamps`
17. `test_tier5_concurrent_session_evaluations_load`
18. `test_tier5_concurrent_multi_user_isolation_and_pagination`
19. `test_tier5_malformed_json_and_boundary_error_envelopes`
20. `test_tier5_injection_and_oversized_payload_handling`
21. `test_tier5_error_envelope_structure_and_no_unhandled_tracebacks`

**Overall Test Suite Performance**:
- Full suite: **184 passed in 0.77s** (`uv run pytest`)
- Code hygiene: `uv run ruff check .` passed with 0 errors.
