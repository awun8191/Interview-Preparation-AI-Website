"""SCQA Communication Framework Catalog.

Situation, Complication, Question, Answer methodology based on Barbara Minto's
Pyramid Principle and Bottom Line Up Front (BLUF) executive communication.
Enforces the Balanced Impact Rule on the Recommendation dimension.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

SCQA_QUESTIONS = [
    JevQuestionDefinition(
        id="scqa_situation_baseline",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker in `transcript` an  "
            "establishes uncontroversial, agreed-upon baseline "
            "Situation. In Minto's doctrine, the Situation must open "
            "with facts everyone in the room agrees upon "
            "to establish psychological safety and common ground before introducing friction."
        ),
        dimension="situation",
        weight_in_dimension=1.0,
        criteria={
            "uncontroversial_clear_baseline": CriteriaOption(
                score=1.0,
                description=(
                    "Opens with an objective, uncontroversial baseline state "
                    "that aligns all stakeholders."
                ),
            ),
            "controversial_or_abrupt_lead": CriteriaOption(
                score=0.3,
                description=(
                    "Opens with an aggressive, alarmist, or subjective ('Our "
                    "complaint legacy code is trash')."
                ),
            ),
            "vague_or_delayed_situation": CriteriaOption(
                score=0.3,
                description=(
                    "Context is ambiguous, delayed, or assumes unexplained background knowledge."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description=(
                    "Skips situational baseline entirely, diving straight or "
                    "into complaints solutions."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is unintelligible or cut off.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="scqa_complication_friction",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate how clearly and urgently the Complication or  "
            "introduces friction change in `transcript`. "
            "The Complication explains what broke the status quo, is "
            "why action needed now, and what the "
            "operational stakes are."
        ),
        dimension="complication",
        weight_in_dimension=1.0,
        criteria={
            "sharp_urgent_friction": CriteriaOption(
                score=1.0,
                description=(
                    "Crisply articulates what changed, the friction created, "
                    "and the acute risk of inaction."
                ),
            ),
            "vague_friction_low_stakes": CriteriaOption(
                score=0.4,
                description=(
                    "Mentions minor friction but fails to convey stakes or business urgency."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description=(
                    "No complication or tension identified; describes a "
                    "business-as-usual without problem."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="scqa_governing_question",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the Governing Question is clearly or  "
            "stated unmistakably framed in `transcript`. "
            "The Question defines the core strategic dilemma arising "
            "from the Complication (e.g. 'How do we migrate "
            "without taking downtime?')."
        ),
        dimension="question",
        weight_in_dimension=1.0,
        criteria={
            "explicitly_articulated": CriteriaOption(
                score=1.0,
                description=(
                    "Explicitly states the core dilemma or decision required "
                    "before presenting the solution."
                ),
            ),
            "clearly_implied": CriteriaOption(
                score=0.85,
                description=(
                    "The core question is not formally spoken as a question, "
                    "but is unmistakable from the setup."
                ),
            ),
            "muddled_or_missing": CriteriaOption(
                score=0.2,
                description=(
                    "Jumps from problem to solution without clarifying the "
                    "strategic decision at stake."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="scqa_bluf_efficiency",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess Bottom Line Up Front (BLUF) delivery efficiency  "
            "in `transcript`. Does the speaker deliver "
            "their core recommendation within the first 20-30 by or  "
            "seconds, supported top-down reasoning, do "
            "they bury the lede in chronological backstory?"
        ),
        dimension="bluf",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Buries Lede Completely: Chronological diary; answer is "
                    "hidden or never explicitly stated."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Weak BLUF: Delivers answer in the final seconds after heavy narrative fatigue."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Moderate Directness: Recommendation stated mid-way, by "
                    "followed supporting points."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Strong Executive BLUF: Clear answer up front, followed "
                    "by organized supporting pillars."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Masterful Minto Executive Delivery: Razor-sharp in  "
                    "recommendation opening seconds "
                    "with zero cognitive drag."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="scqa_recommendation_substance",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate the substance and actionability of the Answer  "
            "/ Recommendation in `transcript`. "
            "Under the Balanced Impact Rule, the recommendation is  "
            "scored top credit (1.0) whether supported by "
            "quantitative metrics or clear qualitative / operational "
            "benefits. Penalize non-committal hedging."
        ),
        dimension="recommendation",
        weight_in_dimension=1.0,
        criteria={
            "actionable_high_impact_solution": CriteriaOption(
                score=1.0,
                description=(
                    "Decisive, actionable path forward with concrete and "
                    "technical/operational rationale clear impact."
                ),
            ),
            "partial_hedged_solution": CriteriaOption(
                score=0.5,
                description=(
                    "Recommendation is hedged or indecisive ('we could maybe "
                    "look into a couple options')."
                ),
            ),
            "vague_non_committal": CriteriaOption(
                score=0.1,
                description=(
                    "Merely re-lists complaints without taking an executive "
                    "stance or proposing a path forward."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="scqa_structural_flow",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate overall structural discipline against the the  "
            "Minto Pyramid standard. Check whether briefing "
            "moves smoothly through logical hierarchy or devolves "
            "into rambling chronological weeds."
        ),
        dimension="flow",
        weight_in_dimension=1.0,
        criteria={
            "textbook_minto_flow": CriteriaOption(
                score=1.0,
                description=(
                    "Flawless logical progression: Uncontroversial Situation -> Complication -> "
                    "Question -> Decisive Answer."
                ),
            ),
            "inverted_bluf_flow": CriteriaOption(
                score=1.0,
                description=(
                    "Opens with the decisive Answer immediately, followed by "
                    "supporting Situation and Complication."
                ),
            ),
            "rambling_chronological_weeds": CriteriaOption(
                score=0.3,
                description=(
                    "Devolves into an unstructured chronological narrative "
                    "filled with technical trivia."
                ),
            ),
            "chaotic_disorganized": CriteriaOption(
                score=0.0,
                description=(
                    "Lacks logical structure; jumps erratically between problems and vague ideas."
                ),
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="SCQA",
    name="SCQA (Situation, Complication, Question, Answer)",
    description=(
        "Barbara Minto's Pyramid Principle and BLUF framework  "
        "for executive briefings and proposals. "
        "Emphasizes psychological safety in baseline facts, and "
        "sharp complication framing, decisive top-down answers."
    ),
    target_pacing_seconds=90,
    dimension_weights={
        "situation": 0.10,
        "complication": 0.20,
        "question": 0.10,
        "bluf": 0.30,
        "recommendation": 0.20,
        "flow": 0.10,
    },
    questions=SCQA_QUESTIONS,
    domain_rules={
        "balanced_impact_enforced": True,
        "outcome_dimension": "recommendation",
        "bluf_priority": True,
    },
)
