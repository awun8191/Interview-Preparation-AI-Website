"""Radical Candor Communication Framework Catalog.

Kim Scott's 2x2 framework balancing Care Personally and Challenge Directly.
Classifies responses into Radical Candor, Ruinous Empathy, Obnoxious Aggression,
and Manipulative Insincerity, while testing for private developmental setting
and reciprocal feedback.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

RADICAL_CANDOR_QUESTIONS = [
    JevQuestionDefinition(
        id="candor_quadrant_classification",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Classify the overall feedback delivered in `transcript` into Kim Scott's 2x2 matrix: "
            "1. Radical Candor (High Care + High Challenge) "
            "2. Ruinous Empathy (High Care + Low Challenge / soft hedging) "
            "3. Obnoxious Aggression (Low Care + High Challenge / brutal assault) "
            "4. Manipulative Insincerity (Low Care + Low Challenge / passive aggressive)."
        ),
        dimension="quadrant",
        weight_in_dimension=1.0,
        criteria={
            "radical_candor": CriteriaOption(
                score=1.0,
                description=(
                    "High Care Personally + High Challenge Directly: speaks the hard truth with "
                    "compassion and clarity."
                ),
            ),
            "ruinous_empathy": CriteriaOption(
                score=0.4,
                description=(
                    "High Care Personally + Low Challenge Directly: "
                    "soft-pedals or hides critique out "
                    "of fear of hurting feelings."
                ),
            ),
            "obnoxious_aggression": CriteriaOption(
                score=0.2,
                description=(
                    "Low Care Personally + High Challenge Directly: brutally blunt, mocking, or "
                    "dismissive without supporting growth."
                ),
            ),
            "manipulative_insincerity": CriteriaOption(
                score=0.0,
                description=(
                    "Low Care Personally + Low Challenge Directly: "
                    "backstabbing, dishonest flattery, "
                    "or passive-aggressive posture."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="candor_challenge_directly_clarity",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the clarity, directness, and specificity of the critique in `transcript`. "
            "Does the recipient "
            "leave the conversation with zero doubt about what standard was missed and what "
            "specific actions must change?"
        ),
        dimension="challenge_directly",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Zero Directness: Critiques are so veiled or absent "
                    "that the recipient is unaware "
                    "there is an issue."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Weak / Confusing: Hints at a problem but hedges so "
                    "heavily that the urgency is "
                    "lost."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Moderate Clarity: Identifies the issue, though "
                    "performance expectations remain "
                    "somewhat broad."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Direct & Unambiguous: States the standard, names the gap, and provides clear "
                    "corrective direction."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Exemplary Direct Challenge: Pristine clarity on "
                    "standards, business impact, and "
                    "non-negotiable next steps."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="candor_care_personally_signals",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess signals of personal care, empathy, and genuine investment in the "
            "counterpart's growth in `transcript`. "
            "Radical candor requires connecting on a human level before correcting."
        ),
        dimension="care_personally",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Cold / Transactional: Purely punitive or bureaucratic with zero human empathy."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Perfunctory Politeness: Polite words without authentic emotional investment."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Clear Human Respect: Acknowledges them as a person "
                    "and validates their dignity."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Active Compassion: Expresses explicit commitment to helping them succeed and "
                    "overcome blockers."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Profound Personal Investment: Deep psychological safety, warmth, and "
                    "unmistakable belief in their potential."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="candor_private_developmental_setting",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the feedback is delivered in a private, developmental setting "
            "or framed respectfully, "
            "adhering to Kim Scott's rule: Praise in public, criticize in private."
        ),
        dimension="environment",
        weight_in_dimension=0.5,
        criteria={
            "private_developmental_frame": CriteriaOption(
                score=1.0,
                description=(
                    "Framed as a confidential, 1-on-1 developmental conversation focused on growth."
                ),
            ),
            "inappropriate_public_tone": CriteriaOption(
                score=0.0,
                description="Uses public shaming or humiliation in front of peers.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="candor_openness_to_counter_feedback",
        type=QuestionType.NOUL,
        prompt_instructions=(
            "Determine whether the speaker invites feedback on their own leadership or asks "
            "curiosity questions "
            "to uncover their own blind spots ('What could I be doing better to support you?')."
        ),
        dimension="environment",
        weight_in_dimension=0.5,
        criteria={
            "yes": CriteriaOption(
                score=1.0,
                description=(
                    "Explicitly invites reciprocal feedback on their "
                    "own leadership or asks what they "
                    "can do to remove blockers."
                ),
            ),
            "no": CriteriaOption(
                score=0.0,
                description=(
                    "Solely delivers one-way feedback and asks zero "
                    "reciprocal questions about their "
                    "own role."
                ),
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="RADICAL_CANDOR",
    name="Radical Candor (Care Personally & Challenge Directly)",
    description=(
        "Kim Scott's high-performance leadership model. Drives breakthrough performance by pairing "
        "relentless direct challenge with profound personal care and reciprocal feedback "
        "solicitation."
    ),
    target_pacing_seconds=90,
    dimension_weights={
        "quadrant": 0.30,
        "challenge_directly": 0.35,
        "care_personally": 0.25,
        "environment": 0.10,
    },
    questions=RADICAL_CANDOR_QUESTIONS,
    domain_rules={
        "quadrant_matrix": True,
        "reciprocal_openness_bonus": True,
    },
)
