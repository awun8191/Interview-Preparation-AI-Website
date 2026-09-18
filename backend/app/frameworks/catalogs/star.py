"""STAR Communication Framework Catalog.

Situation, Task, Action, Result methodology for structured behavioral interviews.
Enforces the Balanced Impact Rule: equal full credit (1.0) for both quantitative metrics
and meaningful qualitative / operational achievements.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

STAR_QUESTIONS = [
    JevQuestionDefinition(
        id="star_situation_grounding",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the candidate in `transcript` anchors "
            "their response in an authentic, "
            "concrete, and identifiable Situation in response to "
            "`scenario_prompt`. A valid Situation "
            "grounds the story in real-world context (such as a specific company, project, system, "
            "team setting, scale, or timeframe). Distinguish authentic "
            "past experiences from purely "
            "theoretical or hypothetical advice where the speaker describes what one 'should' do "
            "instead of what they actually did."
        ),
        dimension="situation",
        weight_in_dimension=1.0,
        criteria={
            "well_grounded": CriteriaOption(
                score=1.0,
                description=(
                    "The speaker clearly grounds the answer in a "
                    "concrete, authentic past scenario, "
                    "identifying recognizable context such as the "
                    "organization, system, project, or timeframe."
                ),
            ),
            "partially_grounded": CriteriaOption(
                score=0.75,
                description=(
                    "The speaker mentions a scenario with minimal "
                    "context. While brief, it is clearly an "
                    "actual past event rather than theoretical philosophy."
                ),
            ),
            "hypothetical_or_generic": CriteriaOption(
                score=0.2,
                description=(
                    "The speaker answers in generic, theoretical terms "
                    "('Whenever you migrate a database...') "
                    "rather than recounting an actual past event."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description=(
                    "The speaker provides zero situational context, "
                    "jumping straight into detached actions "
                    "without explaining where, when, or why this occurred."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="The transcript is severely garbled, unintelligible, or cut off.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="star_task_clarity",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the candidate clearly isolates the "
            "specific Task, objective, or obstacle "
            "in `transcript`. The Task defines the core challenge: what "
            "needed to be achieved, what constraint "
            "made it difficult (e.g. tight deadline, zero downtime, "
            "conflicting priorities), and what the "
            "speaker was personally responsible for resolving."
        ),
        dimension="task",
        weight_in_dimension=1.0,
        criteria={
            "clearly_defined": CriteriaOption(
                score=1.0,
                description=(
                    "The specific task, core objective, technical "
                    "hurdle, or organizational challenge is "
                    "explicitly defined with clear stakes and constraints."
                ),
            ),
            "broadly_implied": CriteriaOption(
                score=0.7,
                description=(
                    "The core task is not formally stated up front, but "
                    "becomes understandable from the "
                    "context of the actions described."
                ),
            ),
            "absent_or_unclear": CriteriaOption(
                score=0.0,
                description=(
                    "The candidate skips defining the challenge or "
                    "objective entirely, jumping from context "
                    "into disjointed tasks without clarifying what problem they were solving."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is garbled or incomplete.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="star_action_ownership_and_depth",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the candidate's personal agency, ownership, and technical depth in the Action "
            "component of `transcript`. Differentiate between healthy "
            "collaboration and hiding behind a "
            "passive collective 'we' where the candidate's personal "
            "contribution is obscured. Look for "
            "first-person active verbs ('I designed', 'I diagnosed', 'I "
            "coordinated'), technical specifics, "
            "and trade-off rationale."
        ),
        dimension="action",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Zero Agency / Passive 'We': Speaks almost "
                    "exclusively in collective or passive terms."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Weak Individual Contribution: Predominantly "
                    "team-centric with minor personal tasks."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Adequate Ownership & Clear Role: Good balance of "
                    "team context and individual ownership."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Strong Leadership & Specificity: Decisive "
                    "first-person ownership and proactive execution."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Exemplary Strategic Agency & Mastery: Exceptional "
                    "leadership, trade-off analysis, "
                    "and composure under ambiguity."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="star_result_and_impact",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Assess the Result and Impact component in `transcript`. "
            "Evaluate whether the narrative concludes "
            "with tangible, meaningful impact. Crucially: DO NOT "
            "penalize candidates simply because their result "
            "is not expressed as a numerical percentage or financial "
            "figure. Both quantitative metrics AND "
            "meaningful qualitative / operational outcomes are fully "
            "valid indicators of high impact. "
            "Distinguish real impact from weak superficial filler "
            "('everything was fine') or unresolved cliffhangers."
        ),
        dimension="result",
        weight_in_dimension=1.0,
        criteria={
            "quantified_metric_impact": CriteriaOption(
                score=1.0,
                description=(
                    "Result includes concrete numerical metrics or measurable data points "
                    "(e.g. latency reduced by 65%, zero downtime, recovered in 12m)."
                ),
            ),
            "meaningful_qualitative_impact": CriteriaOption(
                score=1.0,
                description=(
                    "Result delivers clear, high-value operational, "
                    "strategic, or relational impact "
                    "without specific numbers (e.g. unblocked "
                    "cross-functional squad, prevented enterprise "
                    "churn, eliminated single point of failure)."
                ),
            ),
            "weak_or_vague_outcome": CriteriaOption(
                score=0.3,
                description=(
                    "Outcome is mentioned but superficial, clichéd, or unsubstantiated without "
                    "clear evidence of value ('everyone was happy')."
                ),
            ),
            "absent_or_unresolved": CriteriaOption(
                score=0.0,
                description=(
                    "No result or outcome provided. Candidate trails "
                    "off or leaves the narrative unresolved."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is garbled or cut off before conclusion.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="star_narrative_balance",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate narrative pacing and balance against the ideal "
            "STAR structure (approx. 15% Situation, "
            "15% Task, 55% Action, 15% Result). Check whether the "
            "speaker allocates the bulk of time to "
            "execution and actions rather than an overly long history lecture."
        ),
        dimension="balance",
        weight_in_dimension=1.0,
        criteria={
            "well_balanced_action_focus": CriteriaOption(
                score=1.0,
                description=(
                    "Well-balanced pacing reserving the majority of "
                    "response for detailed actions and outcomes."
                ),
            ),
            "context_heavy_history_lecture": CriteriaOption(
                score=0.4,
                description=(
                    "Severely unbalanced toward context; spends over "
                    "half the answer on background lore."
                ),
            ),
            "rushed_or_truncated": CriteriaOption(
                score=0.3,
                description=(
                    "Overly brief, superficial, or rushed (e.g. under "
                    "30 seconds), omitting critical steps."
                ),
            ),
            "rambling_and_disorganized": CriteriaOption(
                score=0.1,
                description="Lacks narrative structure; jumps erratically and wanders on tangents.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="star_prompt_relevance",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the candidate's answer directly answers "
            "the specific challenge posed in "
            "`scenario_prompt`."
        ),
        dimension="relevance",
        weight_in_dimension=0.0,
        criteria={
            "directly_relevant": CriteriaOption(
                score=1.0,
                description="Directly and faithfully addresses the core premise of the prompt.",
            ),
            "partially_relevant": CriteriaOption(
                score=0.7,
                description="Addresses broad theme but dodges specific constraint or conflict.",
            ),
            "tangential_or_deflected": CriteriaOption(
                score=0.2,
                description="Pivots to an unrelated topic or answers a different question.",
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="STAR",
    name="STAR (Situation, Task, Action, Result)",
    description=(
        "Standardized behavioral interview methodology (DDI / Amazon / Google). "
        "Evaluates contextual grounding, explicit mission framing, personal agency in execution, "
        "and balanced impact (quantitative or operational)."
    ),
    target_pacing_seconds=105,
    dimension_weights={
        "situation": 0.15,
        "task": 0.15,
        "action": 0.45,
        "result": 0.15,
        "balance": 0.10,
    },
    questions=STAR_QUESTIONS,
    domain_rules={
        "balanced_impact_enforced": True,
        "outcome_dimension": "result",
    },
)
