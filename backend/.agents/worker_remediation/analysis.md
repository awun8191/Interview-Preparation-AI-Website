# Defect Remediation Analysis Report: QuestionType.SCORE Evaluation

## Executive Summary
This remediation addresses the defect identified in `TEST_READY.md § 6` regarding `QuestionType.SCORE` extraction in `ScoringEngine._extract_score_value` and population in `SyntheticJevGateway`. The discrepancy caused SCORE-type questions evaluated through the default synthetic gateway contract to extract as `None` and fail to match rubric criteria (producing subscores of `0.0`).

The defect was resolved cleanly through surgical, minimal modifications to both the extraction engine and the synthetic gateway, backed by comprehensive unit tests spanning all supported representation formats.

---

## 1. Problem Analysis & Root Cause

### 1.1 Root Cause in `ScoringEngine`
In `app/services/scoring.py`, `_extract_score_value` previously inspected:
```python
if isinstance(raw, dict):
    return raw.get("score") or raw.get("level") or raw.get("value")
return raw
```
When findings dictionaries contained `"choice": "Level X"` (matching the standard Jev findings schema for choice and score representations), `_extract_score_value` returned `None`. In `_score_single_question`, this resulted in `lvl_str = ""`, finding no criteria match and returning `0.0`.

### 1.2 Root Cause in `SyntheticJevGateway`
In `app/gateways/synthetic.py` (lines 337-347), `SyntheticJevGateway` populated findings for `score`-type questions as:
```python
results[q_id] = {
    "type": "score",
    "choice": choice,
    "probabilities": {...},
}
```
It omitted `"level": choice`, meaning downstream consumers expecting explicit `"level"` keys had to handle fallback extraction or received missing values.

---

## 2. Implementation Changes

### 2.1 `app/services/scoring.py`
Updated `ScoringEngine._extract_score_value` with signature `(raw: Any) -> str | None`:
- Checks `raw.get("score") or raw.get("level") or raw.get("value") or raw.get("choice")` in priority sequence.
- Safely converts non-None values to string representation for unified downstream criteria lookup and regex extraction.
- Handles raw strings, integers, dictionaries, empty dictionaries, and `None` safely.

### 2.2 `app/gateways/synthetic.py`
Updated `SyntheticJevGateway.evaluate_questions` for `q_type == "score"`:
- Populates both `"level": choice` and `"choice": choice` alongside `"type": "score"` and `"probabilities"`.
- Preserves full backward compatibility with any tests expecting `"choice"` while fulfilling contracts expecting `"level"`.

### 2.3 `tests/unit/test_scoring_engine.py`
Added Section 6 containing:
1. `test_score_question_representation_formats`: Parameterized test across 26 representation variations (dictionaries with `"choice"`, `"level"`, `"score"`, `"value"`, integers, strings, and full Jev findings payloads) verifying deterministic subscore computation (e.g. 80.0 for Level 4, 100.0 for Level 5 in STAR `action`).
2. `test_extract_score_value_direct`: Verifies extraction fallbacks, type normalization, and resolution priority (`score` -> `level` -> `value` -> `choice`).
3. `test_synthetic_jev_gateway_score_question_integration`: End-to-end unit test validating that `SyntheticJevGateway` populates both `"level"` and `"choice"`, and `ScoringEngine` processes the resulting finding into a valid non-zero subscore.

---

## 3. Verification & Quality Assurance

- **Unit, Integration, and E2E Tests**:
  `uv run pytest` -> **163 passed in 0.78s** (increased from 135 to 163 tests, zero regressions).
- **Linter**:
  `uv run ruff check .` -> **Passed cleanly (0 errors)**.
- **Formatter**:
  `uv run ruff format --check .` -> **All 122 files cleanly formatted**.
