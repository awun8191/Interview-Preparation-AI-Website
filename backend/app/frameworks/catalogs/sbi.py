"""SBI Communication Framework Catalog.

Situation, Behavior, Impact methodology from the Center for Creative Leadership (CCL).
Enforces the Camera-Recordable Test for behavior, banishes the feedback sandwich,
and measures operational/relational impact.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

SBI_QUESTIONS = [
    JevQuestionDefinition(
        id="sbi_situation_anchoring",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker in `transcript` anchors feedback to a specific time "
            "and place. "
            "Under SBI, feedback must reference an exact event (date, meeting, pull request) "
            "rather than sweeping "
            "generalities ('You always do this') which trigger defensive debates."
        ),
        dimension="situation",
        weight_in_dimension=1.0,
        criteria={
            "specifically_anchored_time_place": CriteriaOption(
                score=1.0,
                description=(
                    "Anchors feedback to a specific date, meeting, incident, or pull request ('In "
                    "yesterday's sprint planning...')."
                ),
            ),
            "vague_general_anchoring": CriteriaOption(
                score=0.5,
                description=(
                    "Mentions a general timeframe ('Recently on the project...') without naming a "
                    "specific moment."
                ),
            ),
            "unanchored_sweeping_claim": CriteriaOption(
                score=0.1,
                description=(
                    "Uses sweeping absolutes ('You always do this', "
                    "'You never listen') that invite "
                    "factual disputes."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description=(
                    "No situational anchor whatsoever; jumps straight into character critiques."
                ),
            ),
            "unable_to_assess": CriteriaOption(
                score=0.0,
                description="Transcript is unintelligible or cut off.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="sbi_behavioral_camera_test",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess whether the Behavior described in `transcript` passes the Camera- "
            "Recordable Test. "
            "A valid behavioral description includes only what a video camera could see and "
            "hear (exact quoted words, "
            "physical actions, timestamps). Penalize subjective character judgments ('you "
            "were rude', 'you were lazy', "
            "'you had bad attitude') and mind-reading."
        ),
        dimension="behavior",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Mind-Reading / Character Attack: Subjective labels "
                    "('you were disrespectful and "
                    "arrogant')."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Mixed Behavior & Interpretation: Blends observable actions with motive "
                    "speculation."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Adequate Behavioral Observation: Describes what "
                    "occurred with minor subjective "
                    "coloration."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Strong Camera-Test Precision: Quotes exact words and describes observable "
                    "physical actions."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Flawless Camera-Recordable Mastery: Pristine "
                    "neutral description of observable "
                    "facts with zero character judgment."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="sbi_impact_operational_clarity",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Assess the Impact component in `transcript`. Evaluate whether the speaker "
            "clearly communicates the "
            "consequences of the behavior—either operational (delayed release, blocked squad, "
            "downtime) or relational "
            "(reduced trust, team disengagement). Both operational and relational impacts "
            "receive full credit (1.0)."
        ),
        dimension="impact",
        weight_in_dimension=1.0,
        criteria={
            "clear_operational_or_relational_impact": CriteriaOption(
                score=1.0,
                description=(
                    "Clearly explains the operational, technical, or team consequence of the "
                    "behavior."
                ),
            ),
            "vague_emotional_venting": CriteriaOption(
                score=0.4,
                description=(
                    "Vents frustration ('It really annoyed me') without "
                    "articulating organizational "
                    "impact."
                ),
            ),
            "absent_impact": CriteriaOption(
                score=0.0,
                description=(
                    "Omits impact entirely; describes behavior without explaining why it matters."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="sbi_feedback_sandwich_filter",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the speaker uses an artificial 'Feedback Sandwich' (compliment "
            "-> critique -> compliment) "
            "or delivers clean, direct, respectful candor without patronizing fluff."
        ),
        dimension="candor",
        weight_in_dimension=1.0,
        criteria={
            "clean_direct_candor": CriteriaOption(
                score=1.0,
                description=(
                    "Delivers direct, respectful, and transparent feedback without artificial "
                    "sandwich padding."
                ),
            ),
            "artificial_sandwiching_detected": CriteriaOption(
                score=0.3,
                description=(
                    "Buries critique inside forced or disingenuous compliments ('You're so great, "
                    "but...')."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="sbi_solution_co_creation",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate how the feedback concludes. Under modern leadership standards, the "
            "feedback giver does not "
            "issue a unilateral ultimatum; they invite curiosity and co-design a solution together."
        ),
        dimension="co_creation",
        weight_in_dimension=1.0,
        criteria={
            "collaborative_co_creation": CriteriaOption(
                score=1.0,
                description=(
                    "Pauses, invites counterpart's perspective, and "
                    "asks open questions to co-author "
                    "safeguards."
                ),
            ),
            "unilateral_dictate_or_threat": CriteriaOption(
                score=0.3,
                description=(
                    "Issues an authoritarian command or threat without "
                    "listening ('Fix this or you're "
                    "fired')."
                ),
            ),
            "unresolved_or_abrupt_end": CriteriaOption(
                score=0.2,
                description=(
                    "Ends abruptly after describing impact, leaving "
                    "zero next steps or collaborative "
                    "path."
                ),
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="SBI",
    name="SBI (Situation, Behavior, Impact)",
    description=(
        "Center for Creative Leadership behavioral feedback methodology. "
        "Anchors critique in concrete events, strictly enforces the Camera-Recordable Test, "
        "articulates operational/relational impact, and co-authors solutions."
    ),
    target_pacing_seconds=90,
    dimension_weights={
        "situation": 0.15,
        "behavior": 0.35,
        "impact": 0.25,
        "candor": 0.10,
        "co_creation": 0.15,
    },
    questions=SBI_QUESTIONS,
    domain_rules={
        "camera_test_enforced": True,
        "anti_sandwich_filter": True,
    },
)
