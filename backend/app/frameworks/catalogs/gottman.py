"""Gottman De-escalation Framework Catalog.

Dr. John Gottman's conflict de-escalation methodology.
Identifies the Four Horsemen (Criticism, Contempt, Defensiveness, Stonewalling)
and rewards their Antidotes:
Soft Start-up, Accepting Responsibility, Emotional Validation, and Repair Attempts.
Enforces a severe multiplicative penalty (0.1x collapse) if Contempt is detected.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

GOTTMAN_QUESTIONS = [
    JevQuestionDefinition(
        id="gottman_four_horsemen_marker",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Detect whether any of Dr. John Gottman's Four Horsemen of interpersonal "
            "destruction are present in `transcript`: "
            "1. Contempt (sarcasm, eye-rolling mockery, sneering, hostile cynicism - DEADLIEST) "
            "2. Defensiveness (victim-playing, counter-attacking, excuse-making) "
            "3. Criticism (global character assassination rather than specific complaint) "
            "4. Stonewalling (cold withdrawal, monosyllabic evasion, silent abandonment). "
            "Or whether the response is completely clean and de-escalating."
        ),
        dimension="horsemen",
        weight_in_dimension=0.0,
        criteria={
            "none_clean_de_escalated": CriteriaOption(
                score=1.0,
                description=(
                    "Zero horsemen detected; calm, de-escalating, and "
                    "emotionally grounded delivery."
                ),
            ),
            "defensiveness_detected": CriteriaOption(
                score=0.6,
                description=(
                    "Defensiveness detected: plays blameless victim or deflects onto counterpart."
                ),
            ),
            "criticism_detected": CriteriaOption(
                score=0.5,
                description=(
                    "Criticism detected: attacks counterpart's personality rather than specific "
                    "behavior."
                ),
            ),
            "stonewalling_detected": CriteriaOption(
                score=0.4,
                description=(
                    "Stonewalling detected: emotional shutdown, "
                    "withdrawal, or monosyllabic refusal "
                    "to engage."
                ),
            ),
            "contempt_detected": CriteriaOption(
                score=0.1,
                description=(
                    "Contempt detected: mockery, sarcasm, superiority, sneering, or disgust "
                    "(Catastrophic Failure)."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="gottman_soft_startup_presence",
        type=QuestionType.NOUL,
        prompt_instructions=(
            "Evaluate whether the speaker uses a Gentle / Soft Start-up. Does the speaker "
            "begin gently, "
            "focusing on their own feelings and a polite request ('I feel concerned about X "
            "and would appreciate Y'), "
            "avoiding harsh blame in the opening seconds?"
        ),
        dimension="soft_startup",
        weight_in_dimension=1.0,
        criteria={
            "yes": CriteriaOption(
                score=1.0,
                description=(
                    "Employs a soft start-up: opens gently without accusations, focusing on mutual "
                    "problem-solving."
                ),
            ),
            "no": CriteriaOption(
                score=0.2,
                description="Harsh start-up: opens with blame, irritation, or sharp accusations.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="gottman_responsibility_acceptance",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess whether the speaker Accepts Responsibility for their part in the "
            "conflict. In Gottman's "
            "antidotes, de-escalation requires owning even a small portion (5%) of the "
            "breakdown ('You're right, "
            "I should have updated the ticket earlier')."
        ),
        dimension="responsibility",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Zero Ownership: Totally externalizes blame; insists they did nothing wrong."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Reluctant Hedging: Admits fault only with excuses ('I only did it because you "
                    "did X')."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description="Basic Acknowledgment: Politely acknowledges a procedural oversight.",
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Clear Vulnerable Ownership: Explicitly admits their mistake and its impact on "
                    "the counterpart."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Masterful Responsibility Acceptance: Unconditional, graceful ownership that "
                    "completely disarms defensiveness."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="gottman_repair_attempt_usage",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker introduces an active, de-escalating Repair Attempt "
            "in `transcript`. "
            "A Repair Attempt is any verbal gesture that cools emotional temperature (e.g. "
            "'Can we take a breath?', "
            "'I hear you, and you're right about that', 'Let's pause a second')."
        ),
        dimension="repair_attempt",
        weight_in_dimension=1.0,
        criteria={
            "active_repair_attempt_used": CriteriaOption(
                score=1.0,
                description=(
                    "Actively deploys an unmistakable verbal repair attempt to de-escalate tension."
                ),
            ),
            "not_applicable_steady": CriteriaOption(
                score=1.0,
                description=(
                    "Conversation remained calm enough that an emergency repair attempt was not "
                    "necessary."
                ),
            ),
            "missed_or_escalated": CriteriaOption(
                score=0.2,
                description=(
                    "Matches counterpart's anger, escalating the "
                    "conflict with heightened aggression."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="gottman_flooding_awareness_timeout",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the speaker recognizes psychological/physiological flooding "
            "and proposes a calm, "
            "structured timeout (approx. 20 minutes) with a commitment to return, or "
            "successfully de-escalates in real time."
        ),
        dimension="flooding_timeout",
        weight_in_dimension=1.0,
        criteria={
            "structured_timeout_called": CriteriaOption(
                score=1.0,
                description=(
                    "Calmly identifies high emotional arousal and "
                    "proposes a structured 15-20m break "
                    "with firm return time."
                ),
            ),
            "in_session_de_escalation": CriteriaOption(
                score=1.0,
                description=(
                    "Successfully de-escalates dialogue in real time "
                    "without needing a full timeout."
                ),
            ),
            "abrupt_stormout_or_abandonment": CriteriaOption(
                score=0.1,
                description=(
                    "Storms off or hangs up without establishing a return time (Stonewalling / "
                    "Abandonment)."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="gottman_validation_of_counterpart",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess whether the speaker validates the emotional reality and perspective of "
            "the counterpart. "
            "Validation acknowledges that feelings are understandable ('I understand why you "
            "felt blindsided') "
            "before trying to resolve logistics."
        ),
        dimension="validation",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Invalidating & Dismissive: Gaslights or mocks feelings ('You are being "
                    "completely irrational')."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Cold Logic: Ignores emotions completely, responding with detached, robotic "
                    "technical logic."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Basic Acknowledgment: Politely acknowledges their "
                    "anger, then immediately pivots "
                    "to logistics."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Strong Empathic Validation: Clearly articulates why the counterpart feels "
                    "aggrieved or stressed."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Masterful Emotional Attunement: Makes counterpart "
                    "feel completely seen, heard, "
                    "and validated before touching facts."
                ),
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="GOTTMAN",
    name="Gottman De-escalation (Four Horsemen & Antidotes)",
    description=(
        "Dr. John Gottman's conflict resolution and de-escalation science. "
        "Penalizes Criticism, Defensiveness, Stonewalling, and Contempt. "
        "Rewards Soft Start-up, Responsibility Acceptance, Repair Attempts, and Emotional "
        "Validation. "
        "Contempt triggers an immediate 0.1x score collapse."
    ),
    target_pacing_seconds=90,
    dimension_weights={
        "responsibility": 0.30,
        "validation": 0.25,
        "soft_startup": 0.15,
        "repair_attempt": 0.15,
        "flooding_timeout": 0.15,
    },
    questions=GOTTMAN_QUESTIONS,
    domain_rules={
        "multiplicative_penalty": True,
        "horsemen_penalty_question": "gottman_four_horsemen_marker",
        "contempt_collapse_factor": 0.1,
    },
)
