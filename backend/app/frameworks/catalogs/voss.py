"""Voss Tactical Empathy Negotiation Framework Catalog.

Chris Voss's FBI hostage negotiation methodology (Never Split the Difference).
Evaluates Emotion Labeling (sensory stems, banishing 'I'), Calibrated Questions ('How' / 'What',
banishing accusatory 'Why'), No-Oriented Questions, Late-Night FM DJ Voice,
and Reciprocal Concessions.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

VOSS_QUESTIONS = [
    JevQuestionDefinition(
        id="voss_emotion_labeling",
        type=QuestionType.NOUL,
        prompt_instructions=(
            "Evaluate whether the speaker uses an Emotion Label using sensory stems ('It "
            "sounds like...', "
            "'It seems like...', 'It looks like...'). Strict Voss rule: sensory stems must "
            "NOT use the first person 'I' "
            "('I understand how you feel' is NOT an emotion label; it centers the speaker). "
            "Labels must address "
            "underlying emotional dynamics or pressures."
        ),
        dimension="emotion_labeling",
        weight_in_dimension=1.0,
        criteria={
            "yes": CriteriaOption(
                score=1.0,
                description=(
                    "Uses sensory stems ('It sounds like / seems like') targeting counterpart's "
                    "emotions without 'I'."
                ),
            ),
            "no": CriteriaOption(
                score=0.2,
                description=(
                    "Fails to use sensory stems; uses self-centered 'I understand' or ignores "
                    "emotions entirely."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="voss_calibrated_questions",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Assess whether the speaker uses Calibrated Open-Ended Questions starting with "
            "'How' or 'What' "
            "('How am I supposed to do that?', 'What is the biggest obstacle we're facing?'). "
            "Severe penalty for Accusatory 'Why' questions ('Why did you do that?'), which "
            "trigger defensiveness."
        ),
        dimension="calibrated_questions",
        weight_in_dimension=1.0,
        criteria={
            "calibrated_how_what": CriteriaOption(
                score=1.0,
                description=(
                    "Asks calibrated open-ended questions using 'How' or 'What' to pass cognitive "
                    "burden to counterpart."
                ),
            ),
            "closed_interrogation": CriteriaOption(
                score=0.5,
                description=(
                    "Asks closed, leading, or yes/no questions that elicit terse resistance."
                ),
            ),
            "no_questions_asked": CriteriaOption(
                score=0.3,
                description="Makes demands or monologues without asking questions.",
            ),
            "accusatory_why": CriteriaOption(
                score=0.1,
                description=(
                    "Uses accusatory 'Why' questions ('Why did you change the terms?') triggering "
                    "instant defensiveness (Severe Penalty)."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="voss_no_oriented_inquiry",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker frames questions to elicit 'No' to preserve "
            "counterpart autonomy "
            "('Have you given up on this project?', 'Is it a bad idea to...?'). In Voss's "
            "doctrine, 'No' protects safety."
        ),
        dimension="no_oriented_inquiry",
        weight_in_dimension=1.0,
        criteria={
            "no_oriented_question_present": CriteriaOption(
                score=1.0,
                description=(
                    "Skillfully deploys a No-oriented question giving counterpart psychological "
                    "safety and control."
                ),
            ),
            "standard_neutral_phrasing": CriteriaOption(
                score=0.7,
                description="Uses neutral conversational phrasing without forcing or tricking.",
            ),
            "forcing_yes_manipulation": CriteriaOption(
                score=0.2,
                description=(
                    "Attempts manipulative yes-momentum traps ('Do you want to save money?') "
                    "provoking resistance."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="voss_vocal_tone_estimate",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Assess psychological stance and implied vocal delivery. Does the negotiator "
            "embody the 'Late-Night FM DJ Voice' "
            "(calm, slow, reassuring, downward-inflecting) versus aggressive combativeness or "
            "submissive pleading?"
        ),
        dimension="vocal_tone",
        weight_in_dimension=1.0,
        criteria={
            "late_night_dj_calm": CriteriaOption(
                score=1.0,
                description=(
                    "Measured, calm, downward-inflecting, non-reactive delivery conveying quiet "
                    "authority and empathy."
                ),
            ),
            "assertive_professional": CriteriaOption(
                score=0.75,
                description=(
                    "Direct, polite, and transactional; effective though lacks tactical warmth."
                ),
            ),
            "submissive_apologetic": CriteriaOption(
                score=0.3,
                description=(
                    "Overly timid or apologetic, conceding leverage "
                    "unnecessarily without trade-offs."
                ),
            ),
            "aggressive_combative": CriteriaOption(
                score=0.1,
                description="Combative, demanding, issuing ultimatums, or expressing irritation.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="voss_reciprocal_concession_framing",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess how the speaker handles bargaining and concessions. Does the speaker "
            "adhere to Reciprocal Concessions "
            "('If I agree to X, what can you do for Y?') or fall into the trap of splitting "
            "the difference or unilateral caving?"
        ),
        dimension="reciprocal_concessions",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Unilateral Surrender / Caving: Immediately concedes to demands without asking "
                    "for anything in return."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Splitting the Difference: Offers a lazy 50/50 compromise leaving value on the "
                    "table."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Basic Resistance: Pushes back politely but does not propose structured trade- "
                    "offs."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Structured Reciprocity: Clearly ties any potential concession to an explicit "
                    "reciprocal concession."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Masterful Deal Architecture: Trades low-cost high-value non-monetary items, "
                    "framing proposals so counterpart feels victorious."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="voss_mirroring_technique",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker uses Mirroring (repeating the last 1 to 3 critical "
            "words with rising or "
            "neutral intonation to prompt the counterpart to elaborate)."
        ),
        dimension="mirroring",
        weight_in_dimension=1.0,
        criteria={
            "mirror_used_effectively": CriteriaOption(
                score=1.0,
                description=(
                    "Repeats critical 1–3 words seamlessly to draw out "
                    "context without confrontation."
                ),
            ),
            "mirror_not_used_or_unnecessary": CriteriaOption(
                score=0.8,
                description=(
                    "Mirroring was not explicitly used, but conversational flow remained "
                    "collaborative."
                ),
            ),
            "awkward_parroting": CriteriaOption(
                score=0.3,
                description="Repeats phrases unnaturally, sounding robotic or mocking.",
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="VOSS",
    name="Chris Voss Tactical Empathy (Negotiation)",
    description=(
        "FBI hostage negotiation methodology adapted for executive dealmaking. "
        "Leverages sensory emotion labels, calibrated open-ended questions, No-oriented framing, "
        "the Late-Night FM DJ delivery, and reciprocal concession bargaining. Penalizes "
        "accusatory 'Why'."
    ),
    target_pacing_seconds=90,
    dimension_weights={
        "emotion_labeling": 0.25,
        "calibrated_questions": 0.30,
        "reciprocal_concessions": 0.25,
        "vocal_tone": 0.10,
        "no_oriented_inquiry": 0.05,
        "mirroring": 0.05,
    },
    questions=VOSS_QUESTIONS,
    domain_rules={
        "accusatory_why_penalty": 0.1,
        "sensory_stems_required": True,
    },
)
