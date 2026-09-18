"""Monroe's Motivated Sequence Framework Catalog.

Alan H. Monroe's 5-step sequential persuasion model:
Attention -> Need -> Satisfaction -> Visualization -> Action.
Evaluates emotional escalation, dual-polarity visualization, and singular
frictionless closing calls to action.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

MONROE_QUESTIONS = [
    JevQuestionDefinition(
        id="monroe_attention_hook",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the power of the Attention step in the first 15 seconds of `transcript`. "
            "Does the speaker "
            "arrest complacency with an unexpected statistic, vivid story, or acute dilemma, "
            "or do they open "
            "with sluggish pleasantries?"
        ),
        dimension="attention",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Sluggish / Boring: Starts with administrative logistics or rambling "
                    "pleasantries."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Weak Lead: Mentions the topic politely without "
                    "establishing emotional friction."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Clear Lead: Competently introduces the subject matter with moderate interest."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Compelling Attention: Shatters complacency quickly "
                    "with an engaging incident or "
                    "stat."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Electrifying Attention Hook: Grips the listener's focus completely within the "
                    "opening sentence."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="monroe_need_urgency",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker proves an acute, urgent Need before offering a "
            "cure. People do not buy cures "
            "for diseases they don't have. Does the speaker detail the cost of inaction, "
            "systemic breakdown, or escalating risk?"
        ),
        dimension="need",
        weight_in_dimension=1.0,
        criteria={
            "acute_need_proven": CriteriaOption(
                score=1.0,
                description=(
                    "Thoroughly proves an acute operational, technical, "
                    "or financial problem and the "
                    "mounting cost of inaction."
                ),
            ),
            "vague_need_low_urgency": CriteriaOption(
                score=0.4,
                description=(
                    "Identifies a problem, but fails to make the "
                    "listener feel the urgent necessity "
                    "for change."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description=(
                    "Pitches a solution without first demonstrating why any change is needed "
                    "(Solution looking for a problem)."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="monroe_satisfaction_viability",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate the Satisfaction step in `transcript`. Does the speaker present a "
            "concrete, viable solution "
            "that directly resolves the Need and proves how it will work?"
        ),
        dimension="satisfaction",
        weight_in_dimension=1.0,
        criteria={
            "concrete_viable_solution": CriteriaOption(
                score=1.0,
                description=(
                    "Presents an explicit, viable solution showing exactly how it satisfies every "
                    "facet of the identified need."
                ),
            ),
            "vague_or_incomplete_solution": CriteriaOption(
                score=0.4,
                description=(
                    "Proposes general ideas without detailing how they "
                    "will realistically solve the "
                    "problem."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description="Fails to articulate a concrete plan or solution.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="monroe_visualization_polarity",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the Visualization step in `transcript`. Evaluates whether the speaker "
            "creates vivid dual-polarity "
            "contrast: painting both the positive relief of adoption (relief, speed, profit) "
            "and the painful reality "
            "of doing nothing."
        ),
        dimension="visualization",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Zero Visualization: Jumps straight from the solution to the ask with zero "
                    "sensory projection."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Weak / Dry: Mentions abstract benefits without "
                    "evoking visceral relief or risk."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Single-Sided Visualization: Paints only the "
                    "positive future OR only the negative "
                    "consequence."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Strong Dual-Polarity Contrast: Vividly juxtaposes "
                    "the relief of success with the "
                    "danger of inaction."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Masterful Sensory Immersion: Electrifying "
                    "projection; listener viscerally feels "
                    "both the danger and relief."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="monroe_action_friction_and_clarity",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate the final Action step in `transcript`. In Monroe's Motivated Sequence, "
            "the closing call to action "
            "must be SINGULAR, SPECIFIC, and FRICTIONLESS. It tells the listener exactly what "
            "physical move to make today. "
            "Strictly penalize asking for vague or burdensome laundry lists of tasks."
        ),
        dimension="action",
        weight_in_dimension=1.0,
        criteria={
            "singular_frictionless_ask": CriteriaOption(
                score=1.0,
                description=(
                    "Singular, razor-sharp, low-friction ask ('Authorize this 30-day staging pilot "
                    "today', 'Sign here for access')."
                ),
            ),
            "burdensome_or_multiple_asks": CriteriaOption(
                score=0.4,
                description=(
                    "Overwhelms the decision-maker with a laundry list of complex, high-effort "
                    "requests."
                ),
            ),
            "vague_non_committal_close": CriteriaOption(
                score=0.2,
                description=(
                    "Ends weakly without a concrete ask ('So think "
                    "about it and let me know', 'We can "
                    "talk sometime')."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description="Zero call to action provided.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="monroe_sequence_progression",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate overall sequence integrity against Monroe's 5-step model: "
            "Attention -> Need -> Satisfaction -> Visualization -> Action."
        ),
        dimension="progression",
        weight_in_dimension=1.0,
        criteria={
            "flawless_five_step_progression": CriteriaOption(
                score=1.0,
                description=(
                    "Flows seamlessly through all five sequential "
                    "psychological stages with natural "
                    "momentum."
                ),
            ),
            "minor_step_omission": CriteriaOption(
                score=0.6,
                description=(
                    "Follows general structure but slightly rushes or skips one step (e.g. weak "
                    "visualization)."
                ),
            ),
            "disordered_or_jumbled": CriteriaOption(
                score=0.2,
                description=(
                    "Jumbles sequence (e.g. asking for action before explaining need; proposing "
                    "solutions without problem)."
                ),
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="MONROE",
    name="Monroe's Motivated Sequence (Persuasion)",
    description=(
        "Alan H. Monroe's 5-step psychological escalation sequence for high-conversion persuasion: "
        "Attention -> Need -> Satisfaction -> Visualization -> Action. "
        "Heaviest weight on proving acute Need and demanding a singular, frictionless Action."
    ),
    target_pacing_seconds=120,
    dimension_weights={
        "attention": 0.10,
        "need": 0.25,
        "satisfaction": 0.10,
        "visualization": 0.20,
        "action": 0.25,
        "progression": 0.10,
    },
    questions=MONROE_QUESTIONS,
    domain_rules={
        "sequential_escalation": True,
        "singular_ask_required": True,
    },
)
