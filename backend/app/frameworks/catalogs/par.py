"""PAR Communication Framework Catalog.

Problem, Action, Result methodology optimized for rapid-fire screening rounds
and executive brevity (45-60s).
Enforces the Balanced Impact Rule on the Result dimension.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

PAR_QUESTIONS = [
    JevQuestionDefinition(
        id="par_problem_sharpness",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate how immediately and sharply the candidate "
            "articulates the core friction point in `transcript`. "
            "In PAR, the speaker should cut straight to the chase "
            "within 10-15 seconds rather than delivering "
            "a rambling history setup."
        ),
        dimension="problem",
        weight_in_dimension=1.0,
        criteria={
            "sharp_and_immediate": CriteriaOption(
                score=1.0,
                description=(
                    "Immediately frames the obstacle, friction, "
                    "or crisis in the first 1–2 sentences."
                ),
            ),
            "slow_meandering_setup": CriteriaOption(
                score=0.5,
                description=(
                    "Spends over 20 seconds on background lore "
                    "before clearly stating the core problem."
                ),
            ),
            "vague_or_unclear": CriteriaOption(
                score=0.2,
                description=(
                    "Mentions that things were 'hectic' without clearly isolating the technical "
                    "or operational bottleneck."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description=(
                    "Skips stating the problem entirely, launching directly into activities."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is unintelligible or cut off.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="par_action_decisiveness",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the speed, decisiveness, and individual agency "
            "demonstrated in the Action component of `transcript`. "
            "In rapid screening, recruiters look for crisp ownership "
            "and technical execution without hesitation."
        ),
        dimension="action",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.10,
                description=(
                    "Passive / Indecisive: Completely unclear "
                    "what the speaker personally drove or "
                    "decided."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.35,
                description=(
                    "Weak Agency: Heavily collective 'we'; minor personal troubleshooting details."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.65,
                description=(
                    "Clear Tactical Action: Good ownership of "
                    "individual tasks, though trade-offs are "
                    "brief."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.85,
                description=(
                    "Decisive Executive Move: Articulates high-leverage "
                    "diagnosis, specific tools, and swift execution."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Flawless Crisis Leadership: Rapid triage, decisive "
                    "trade-offs, and authoritative "
                    "personal ownership under strict constraints."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="par_result_and_impact",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Assess the Result component in `transcript`. Evaluate "
            "whether the response delivers tangible impact. "
            "Crucially: DO NOT penalize the candidate if the result is "
            "not numeric. Both quantitative metrics AND "
            "meaningful qualitative / operational outcomes (e.g. "
            "unblocking a deployment gate, preventing client churn, "
            "eliminating architectural bottlenecks) receive equal full credit (1.0)."
        ),
        dimension="result",
        weight_in_dimension=1.0,
        criteria={
            "quantified_metric_impact": CriteriaOption(
                score=1.0,
                description=(
                    "Result includes concrete numeric statistics "
                    "(e.g. 50% speedup, zero data loss, recovered in 5m)."
                ),
            ),
            "meaningful_qualitative_impact": CriteriaOption(
                score=1.0,
                description=(
                    "Result delivers clear, high-value operational or "
                    "technical impact without numbers "
                    "(e.g. unblocked release gate, resolved vendor deadlock)."
                ),
            ),
            "weak_or_vague_outcome": CriteriaOption(
                score=0.3,
                description=(
                    "Outcome is descriptive but weak or unsubstantiated ('everything went well')."
                ),
            ),
            "absent_or_trailing_off": CriteriaOption(
                score=0.0,
                description="Candidate trails off or ends abruptly without stating the outcome.",
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is garbled or cut off.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="par_brevity_and_information_density",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether `transcript` satisfies the strict 45-60s "
            "brevity standard for PAR. Penalize "
            "responses exceeding 75 seconds or bloated with filler and administrative fluff."
        ),
        dimension="brevity",
        weight_in_dimension=1.0,
        criteria={
            "crisp_executive_brevity": CriteriaOption(
                score=1.0,
                description=(
                    "High information density delivered cleanly within "
                    "45–60 seconds with zero wasted filler."
                ),
            ),
            "acceptable_pacing": CriteriaOption(
                score=0.8,
                description="Solid delivery between 60–75 seconds with minor fluff.",
            ),
            "bloated_or_rambling": CriteriaOption(
                score=0.3,
                description=(
                    "Exceeds 75 seconds, filled with excessive backstory lore and digressions."
                ),
            ),
            "too_brief_incomplete": CriteriaOption(
                score=0.2,
                description="Under 25 seconds; omits key steps and context entirely.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="par_prompt_relevance",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the candidate's answer directly answers "
            "the exact friction point posed in `scenario_prompt`."
        ),
        dimension="relevance",
        weight_in_dimension=0.0,
        criteria={
            "directly_relevant": CriteriaOption(
                score=1.0,
                description="Directly addresses the exact challenge posed in the prompt.",
            ),
            "partially_relevant": CriteriaOption(
                score=0.7,
                description="Touches on the topic but avoids the high-pressure dilemma.",
            ),
            "tangential_or_deflected": CriteriaOption(
                score=0.2,
                description="Answers an unrelated question or deflects entirely.",
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="PAR",
    name="PAR (Problem, Action, Result)",
    description=(
        "Rapid-fire screening and executive briefing framework strictly "
        "budgeted for 45–60 seconds. "
        "Prioritizes immediate problem definition, decisive personal action, and punchy impact."
    ),
    target_pacing_seconds=55,
    dimension_weights={
        "problem": 0.20,
        "action": 0.45,
        "result": 0.20,
        "brevity": 0.15,
    },
    questions=PAR_QUESTIONS,
    domain_rules={
        "balanced_impact_enforced": True,
        "outcome_dimension": "result",
        "brevity_cap_seconds": 65,
    },
)
