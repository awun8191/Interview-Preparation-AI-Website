# Cross-Cutting Specification: Answer Clarity & Ambiguity

**The-Plan-Software Communication Engine: Universal Clarity Dimension & Jev Wire Catalog**

---

## 1. Executive Summary & Why Clarity Is Cross-Cutting

Every framework in the engine — STAR, CARL, PAR, SCQA, SBI, Radical Candor, STATE, Gottman,
Voss, Duarte Sparkline, and Monroe — shares one prerequisite: the listener must be able to
understand the answer. A structurally perfect STAR story delivered in a fog of undefined
referents and hedged non-claims fails as communication.

This specification defines a **cross-cutting `clarity` dimension** that is appended to **every**
framework catalog at construction time. It grades two independent things in parallel:

1. **Clarity** — how well the answer is organized and expressed.
2. **Ambiguity** — how much genuinely unresolvable meaning the answer contains.

The dimension is **auxiliary**: it is graded and reported as a subscore with a composite weight of
**$0.0$**, so it **never changes the 0–100 composite score**. It is additionally returned to clients
as a standalone `clarity` object on the evaluation response.

---

## 2. Core Evaluation Principles

### Principle 1: Clarity Is Independent of Framework Structure

A candidate can execute the STAR arc flawlessly while still being ambiguous. Clarity is judged on
the transcript's own merits — comprehensibility, ordering, precision of language — not on whether
the framework's steps are present.

* **What We Look For:** A discernible through-line, concrete nouns, specific verbs, resolved
  references.
* **What We Penalize:** Undefined `it`/`they`/`this`, contradictory claims, hedging that voids a
  claim, filler, and false starts.

### Principle 2: Ambiguity Is a Distinct, Detectable Signal

Clarity and ambiguity are correlated but measured separately. An answer can be *generally* clear
yet contain one materially ambiguous claim, and that ambiguity is worth surfacing on its own.

* **Realistic Balance:** Isolated hedging ("I think we probably should...") is common and only
  *minor* vagueness. Reserve `materially_ambiguous` for meaning the listener genuinely cannot
  recover.

### Principle 3: Never Distort the Framework Score

Clarity must inform coaching without silently re-weighting the framework rubrics. The metric is
reported as a $0.0$-weight subscore alongside the composite score, never folded into it.

---

## 3. Jev System One Wire Catalog: Cross-Cutting Clarity Suite

### 3.1 State Structure

The clarity questions use the exact same `state` payload as every other framework
(`scenario_prompt`, `scenario_context`, `target_framework`, `speaker_role`, `transcript`,
`word_count`, `duration_seconds`, `words_per_minute`). No additional state is required.

### 3.2 The Two Cross-Cutting Questions Submitted to Jev

Both questions are appended to every framework's question payload. They carry
`"dimension": "clarity"` and are flagged in code with `domain_metadata = {"cross_cutting": true}`.

#### Question 1: `clarity_of_response` (Primitive: `score`)

```json
{
  "type": "score",
  "instructions": "Assess how clearly and precisely the speaker in `transcript` expresses their answer, independent of framework structure. Judge comprehensibility, logical ordering, economical phrasing, and freedom from vague or self-contradictory language. A clear answer is easy to follow on first listen, uses concrete nouns and specific verbs, and avoids filler, hedging, and undefined references.",
  "criteria": {
    "Level 1": "Incoherent or Unintelligible: Disjointed, contradictory, or impossible to follow; the core meaning cannot be recovered.",
    "Level 2": "Fragmented or Hard to Follow: Frequent false starts, undefined references, and filler obscure the point.",
    "Level 3": "Understandable with Effort: The main point is recoverable but buried under vague phrasing, hedging, or erratic ordering.",
    "Level 4": "Clear and Well-Structured: Easy to follow on first listen with concrete language and a discernible through-line.",
    "Level 5": "Exceptionally Clear and Economical: Crisp, precise, and economical; every sentence advances an unambiguous point."
  }
}
```

#### Question 2: `ambiguity_presence` (Primitive: `choice`)

```json
{
  "type": "choice",
  "instructions": "Determine whether `transcript` contains material ambiguity that would leave a listener unsure what the speaker means. Look for vague quantifiers and placeholders ('some things', 'stuff', 'a lot'), unresolved referents (unclear 'it', 'they', or 'this'), hedging that voids a claim ('kind of', 'maybe', 'sort of'), contradictory or underspecified timeframes and scope, and equivocation that never commits to a position.",
  "criteria": {
    "unambiguous_and_precise": "No material ambiguity; claims, referents, and scope are specific and internally consistent.",
    "minor_vagueness": "Isolated vague phrasing or hedging that does not obscure the core meaning of the answer.",
    "materially_ambiguous": "Meaning is genuinely unclear: undefined referents, contradictory claims, or hedging that voids the point.",
    "unable_to_assess": "The transcript is severely garbled, unintelligible, or cut off."
  }
}
```

---

## 4. Deterministic Clarity Assessment (All Frameworks)

### 4.1 Clarity Score Formulation

Neither question carries composite weight. The standalone clarity score is the mean of the two
question credits, scaled to 0–100:

$$Score_{\text{clarity}} = \left( \frac{S_{\text{clarity}} + S_{\text{ambiguity}}}{2} \right) \times 100$$

* **Clarity of Response ($S_{\text{clarity}}$):** `Level 1` = $0.2$, `Level 2` = $0.4$,
  `Level 3` = $0.6$, `Level 4` = $0.8$, `Level 5` = $1.0$.
* **Ambiguity Presence ($S_{\text{ambiguity}}$):** `unambiguous_and_precise` = $1.0$,
  `minor_vagueness` = $0.6$, `materially_ambiguous` = $0.2$, `unable_to_assess` = $0.0$.

### 4.2 Clarity Bands

| Score Range | Band | Meaning |
| :--- | :--- | :--- |
| $\ge 90$ | `exceptional` | Exceptionally clear and economical delivery. |
| $70\text{–}89.9$ | `clear` | Clear, well-structured answer. |
| $50\text{–}69.9$ | `adequate` | Understandable but could be tightened for clarity. |
| $30\text{–}49.9$ | `unclear` | Restructure: lead with the point and cut filler. |
| $< 30$ | `incoherent` | Rebuild the answer around a single, explicit through-line. |

### 4.3 Response Field

Clarity is reported twice: as a **subscore** entry (`dimension: "clarity"`, `weight: 0.0`) in the
standard `subscores` array, and as a standalone `clarity` object:

```json
{
  "clarity": {
    "score": 90.0,
    "level": "exceptional",
    "clarity_level": "Level 4",
    "ambiguity": "unambiguous_and_precise",
    "ambiguous": false,
    "feedback": "Exceptionally clear and economical delivery."
  }
}
```

`ambiguous` is `true` only when `ambiguity == "materially_ambiguous"`. This object is also
persisted on the session record for history retrieval.

---

## 5. Real-Time Coaching Triggers (Cross-Cutting)

| Jev Evaluation Trigger | UI Badge | Deterministic Coaching Advice |
| :--- | :--- | :--- |
| `ambiguity_presence.choice == "materially_ambiguous"` | 🔴 **Vague Answer** | *"Your answer contained material ambiguity: a listener could not tell exactly what you meant. Resolve vague references (name the 'it' or 'they'), drop hedges like 'kind of' or 'maybe', and commit to specific claims."* |
| `clarity_of_response.choice >= "Level 4"` AND `ambiguity_presence.choice == "unambiguous_and_precise"` | ✅ **High Clarity** | *"Crisp, unambiguous answer that a listener can follow on the first pass."* |
| `clarity_of_response.choice <= "Level 2"` | ⚠️ **Hard to Follow** | *"Your answer was hard to follow even though the content may be sound. Lead with a single explicit point, order the supporting detail, and cut filler and false starts."* |
