"""CARL Communication Framework Catalog.

Context, Action, Result, Learning methodology for senior / executive reflection.
Prioritizes metacognition, intellectual humility, and systemic organizational safeguards.
Enforces the Balanced Impact Rule on the Result dimension.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

CARL_QUESTIONS = [
    JevQuestionDefinition(
        id="carl_context_framing",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker in `transcript` establishes a concrete, credible Context "
            "for the scenario in response to `scenario_prompt`. The "
            "Context must set the stage: identifying "
            "the organizational setting, technical or business goal, "
            "initial premise/assumption, and stakes."
        ),
        dimension="context",
        weight_in_dimension=1.0,
        criteria={
            "well_framed_context": CriteriaOption(
                score=1.0,
                description=(
                    "Clearly grounds the narrative in an authentic past context with organization, "
                    "system, and baseline assumptions."
                ),
            ),
            "partially_framed": CriteriaOption(
                score=0.75,
                description=(
                    "Establishes a real past scenario with minimal "
                    "details, though baseline context is clear."
                ),
            ),
            "hypothetical_or_generic": CriteriaOption(
                score=0.2,
                description=(
                    "Answers in theoretical terms ('When building microservices, people often...') "
                    "rather than an authentic past event."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description=(
                    "Provides zero context, launching into actions or "
                    "lessons with no explanation of where or why."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is severely garbled, corrupt, or unintelligible.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="carl_action_ownership_and_rigor",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the candidate's personal ownership, agency, and technical depth in the Action "
            "component of `transcript`. Evaluate what the candidate "
            "personally investigated, decided, "
            "designed, or executed when the complication or failure emerged."
        ),
        dimension="action",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Passive / Obscured Contribution: Uses passive or "
                    "collective language exclusively."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Weak Ownership: Narrative is predominantly "
                    "team-centric with minor incidental participation."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Adequate Ownership & Clear Action: Clear "
                    "separation between team responsibilities and "
                    "personal actions."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Strong Problem-Solving & Technical Depth: Decisive "
                    "first-person ownership and proactive triage."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Exemplary Leadership & Composure: Outstanding "
                    "execution, stakeholder stabilization, "
                    "and technical remediation under pressure."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="carl_result_and_impact",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Assess the Result component in `transcript`. Evaluate "
            "whether the response details a tangible, "
            "identifiable outcome. Crucially: DO NOT penalize the "
            "candidate if the result is not expressed "
            "as a numeric percentage. Both quantitative metrics AND "
            "meaningful qualitative / operational "
            "outcomes are fully valid representations of impact."
        ),
        dimension="result",
        weight_in_dimension=1.0,
        criteria={
            "quantified_metric_impact": CriteriaOption(
                score=1.0,
                description=(
                    "Result includes concrete numerical data points "
                    "(e.g. recovered service in 14m, reduced memory footprint by 40%)."
                ),
            ),
            "meaningful_qualitative_impact": CriteriaOption(
                score=1.0,
                description=(
                    "Result delivers clear operational, strategic, or "
                    "relational impact without numbers "
                    "(e.g. stabilized cluster, unblocked launch, salvaged enterprise customer)."
                ),
            ),
            "weak_or_vague_outcome": CriteriaOption(
                score=0.3,
                description=(
                    "Outcome is mentioned but superficial or "
                    "unsubstantiated without clear evidence of value."
                ),
            ),
            "absent_or_unresolved": CriteriaOption(
                score=0.0,
                description=(
                    "No result is provided; jumps directly from actions "
                    "to lessons without stating what happened."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is garbled or cut off.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="carl_learning_metacognitive_depth",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Evaluate the Learning component in `transcript`—the "
            "defining climax of the CARL framework. "
            "Assess metacognition, intellectual maturity, and systemic "
            "growth. Does the speaker identify "
            "an underlying flawed assumption, explain how mental models "
            "evolved, and describe concrete, "
            "lasting systemic safeguards (e.g. automated canary gates, "
            "RFC templates, runbooks) instituted across the team?"
        ),
        dimension="learning",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.0,
                description=(
                    "Defensive / Externalized Blame: Blames juniors, "
                    "tooling, or deadlines; zero psychological "
                    "ownership."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.30,
                description=(
                    "Superficial Platitudes: Offers shallow clichés "
                    "('communication is key', 'always double check')."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.65,
                description=(
                    "Individual Tactical Takeaway: Identifies a "
                    "personal mistake and articulates individual "
                    "changes."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.85,
                description=(
                    "Systemic Process & Engineering Improvement: "
                    "Upgraded team-wide engineering gates, "
                    "tooling, or protocols."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Transformational Organizational Wisdom: Profound "
                    "metacognitive depth, cultural resilience, "
                    "and org-wide learning."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="carl_narrative_balance",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate narrative pacing and balance against the CARL standard (approx. 20% Context, "
            "35% Action, 15% Result, 30% Learning). In CARL, the "
            "Learning is the primary deliverable: "
            "check whether the speaker allocated sufficient time and "
            "depth (~25-30%) to meaningful reflection, "
            "or whether they rushed through the learning in the final 5 seconds as an afterthought."
        ),
        dimension="balance",
        weight_in_dimension=1.0,
        criteria={
            "rich_learning_climax": CriteriaOption(
                score=1.0,
                description=(
                    "Well-balanced pacing with deep reflection "
                    "reserving ~25-30% for systemic improvements."
                ),
            ),
            "rushed_afterthought_learning": CriteriaOption(
                score=0.4,
                description=(
                    "Spends 90% of time on narrative, cramming learning "
                    "into a single hurried closing sentence."
                ),
            ),
            "context_heavy_history_lecture": CriteriaOption(
                score=0.3,
                description=(
                    "Spends over half the time on backstory lore, "
                    "leaving little time for actions and learning."
                ),
            ),
            "disorganized_or_rambling": CriteriaOption(
                score=0.1,
                description="Lacks structural flow, jumping erratically between timelines.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="carl_vulnerability_and_humility",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Assess the psychological stance and emotional maturity of "
            "the speaker. Evaluates candid ownership "
            "of mistakes versus an infallible, defensive, or guarded persona."
        ),
        dimension="vulnerability",
        weight_in_dimension=0.0,
        criteria={
            "authentic_humility_and_ownership": CriteriaOption(
                score=1.0,
                description=(
                    "Candid, balanced, and calm ownership of "
                    "misjudgments without defensive excuse-making."
                ),
            ),
            "guarded_or_reluctant": CriteriaOption(
                score=0.5,
                description=(
                    "Hedges answers to avoid admitting a "
                    "genuine mistake ('I only did it "
                    "because...')."
                ),
            ),
            "defensive_or_arrogant": CriteriaOption(
                score=0.1,
                description="Exhibits hostility or arrogance, minimizing real failures.",
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="CARL",
    name="CARL (Context, Action, Result, Learning)",
    description=(
        "Executive reflection and metacognition framework emphasizing systemic takeaways, "
        "architectural safeguards, and psychological maturity. Heaviest weight placed on Learning."
    ),
    target_pacing_seconds=115,
    dimension_weights={
        "context": 0.15,
        "action": 0.25,
        "result": 0.15,
        "learning": 0.35,
        "balance": 0.10,
    },
    questions=CARL_QUESTIONS,
    domain_rules={
        "balanced_impact_enforced": True,
        "outcome_dimension": "result",
        "non_linear_learning": True,
    },
)
