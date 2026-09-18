"""STATE Communication Framework Catalog.

Crucial Conversations methodology (Patterson, Grenny, McMillan, Switzler).
Evaluates the 5-step protocol for high-stakes, emotionally fraught dialogue:
Share your facts, Tell your story, Ask for their path, Talk tentatively, Encourage testing.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

STATE_QUESTIONS = [
    JevQuestionDefinition(
        id="state_facts_first_sequencing",
        type=QuestionType.NOUL,
        prompt_instructions=(
            "Evaluate whether the speaker in `transcript` leads with objective, verifiable "
            "facts before stating "
            "their interpretations or emotional story. In Crucial Conversations, facts create "
            "safe common ground; "
            "leading with conclusions triggers instant defensiveness."
        ),
        dimension="facts_first",
        weight_in_dimension=1.0,
        criteria={
            "yes": CriteriaOption(
                score=1.0,
                description=(
                    "Leads with observable facts (dates, PRs, "
                    "deliverables, metrics) before sharing "
                    "interpretations."
                ),
            ),
            "no": CriteriaOption(
                score=0.0,
                description=(
                    "Leads with conclusions, accusations, or emotional "
                    "grievances before presenting "
                    "data."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="state_story_framing_awareness",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate how the speaker frames their interpretations in `transcript`. Does the "
            "speaker distinguish "
            "between facts and stories ('The story I am telling myself is...', 'My impression "
            "was...') or state "
            "their conclusions as absolute objective truth ('You clearly don't care')?"
        ),
        dimension="story_framing",
        weight_in_dimension=1.0,
        criteria={
            "properly_framed_as_story": CriteriaOption(
                score=1.0,
                description=(
                    "Explicitly frames conclusions as an interpretation or perception rather than "
                    "undisputed fact."
                ),
            ),
            "story_stated_as_absolute_truth": CriteriaOption(
                score=0.2,
                description=(
                    "States subjective interpretations and character judgments as indisputable "
                    "objective reality."
                ),
            ),
            "absent": CriteriaOption(
                score=0.1,
                description="No perspective or story shared; speaks in disjointed fragments.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="state_tentative_language_calibration",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the speaker's use of tentative language ('It seems to me', 'I'm wondering "
            "if', 'Perhaps') versus "
            "dogmatic absolutes ('Obviously', 'There is no doubt', 'You always'). Tentative "
            "language conveys "
            "intellectual humility and invites dialogue."
        ),
        dimension="tentative_language",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Rigidly Dogmatic: Heavy use of absolutes and uncompromising assertions."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Overly Certain: Asserts claims with little room "
                    "for alternative interpretations."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Moderately Tentative: Uses some softening language but slips into occasional "
                    "dogmatism."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Well-Calibrated Tentativeness: Thoughtfully frames hypotheses with genuine "
                    "humility."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Masterful Crucial Dialogue: Flawless balance of confidence in facts and "
                    "tentative openness in interpretation."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="state_mutual_purpose_safety",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the speaker establishes Mutual Purpose and psychological "
            "safety in `transcript`. "
            "Reminds the counterpart of shared team/organizational goals to prevent an "
            "adversarial 'me vs you' dynamic."
        ),
        dimension="mutual_purpose",
        weight_in_dimension=1.0,
        criteria={
            "explicit_mutual_purpose": CriteriaOption(
                score=1.0,
                description=(
                    "Explicitly states shared goals and commitments ('We both want this launch to "
                    "succeed smoothly')."
                ),
            ),
            "implied_collaborative": CriteriaOption(
                score=0.7,
                description=(
                    "Tone is collaborative and supportive, though mutual purpose is not formally "
                    "stated up front."
                ),
            ),
            "adversarial_me_vs_you": CriteriaOption(
                score=0.0,
                description=(
                    "Frames the discussion as a win/lose battle or adversarial confrontation."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="state_ask_and_encourage_testing",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate the 'Ask for their path' and 'Encourage testing' dimensions. Does the "
            "speaker genuinely "
            "invite the counterpart to share their data and challenge the speaker's "
            "conclusions ('How do you see this differently?')?"
        ),
        dimension="ask_testing",
        weight_in_dimension=1.0,
        criteria={
            "genuine_inquiry_and_testing": CriteriaOption(
                score=1.0,
                description=(
                    "Genuinely invites the other party's perspective and asks them to challenge or "
                    "correct the conclusion."
                ),
            ),
            "token_or_rhetorical_question": CriteriaOption(
                score=0.3,
                description=(
                    "Asks superficial or rhetorical questions "
                    "('Right?', 'Don't you agree?') without "
                    "real inquiry."
                ),
            ),
            "zero_inquiry_closed": CriteriaOption(
                score=0.0,
                description=(
                    "Monologues without asking a single question or inviting the counterpart to "
                    "speak."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="state_emotional_composure",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the speaker's emotional regulation and composure under high stakes. "
            "Evaluates whether the "
            "speaker maintains calm psychological safety versus fight (combative anger) or "
            "flight (timid retreat)."
        ),
        dimension="composure",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Hostile / Dysregulated: Overtly angry, defensive, sarcastic, or combative."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Visibly Agitated: Noticeable frustration, trembling urgency, or defensive "
                    "hedging."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Professionally Controlled: Controlled professional demeanor, though slightly "
                    "tense."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Calm & Grounded: Measured breathing, steady "
                    "cadence, respectful and clear under "
                    "pressure."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Exemplary Poise & Presence: Radiant psychological "
                    "safety and profound calm under "
                    "high emotional stakes."
                ),
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="STATE",
    name="STATE (Crucial Conversations)",
    description=(
        "Patterson, Grenny, McMillan & Switzler's high-stakes dialogue model. "
        "Transforms destructive arguments into constructive problem-solving by leading with facts, "
        "talking tentatively, framing conclusions as stories, and actively encouraging testing."
    ),
    target_pacing_seconds=90,
    dimension_weights={
        "facts_first": 0.20,
        "story_framing": 0.15,
        "tentative_language": 0.25,
        "mutual_purpose": 0.10,
        "ask_testing": 0.20,
        "composure": 0.10,
    },
    questions=STATE_QUESTIONS,
    domain_rules={
        "facts_first_priority": True,
        "tentative_language_weighted": True,
    },
)
