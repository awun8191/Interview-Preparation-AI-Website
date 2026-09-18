"""Duarte Sparkline Presentation Framework Catalog.

Nancy Duarte's persuasive keynote and presentation structure (Resonate).
Creates compelling oratorical rhythm through dynamic oscillation between 'What Is' (current pain)
and 'What Could Be' (future vision), treating the Audience as Hero (Yoda/Mentor model),
delivering a memorable S.T.A.R. Moment, and ending on 'The New Bliss'.
"""

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)

SPARKLINE_QUESTIONS = [
    JevQuestionDefinition(
        id="sparkline_what_is_vs_could_be_contrast",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the oratorical oscillation and narrative tension in `transcript` between "
            "'What Is' "
            "(current broken reality, pain, bottlenecks) and 'What Could Be' (the transformed "
            "future, "
            "speed, freedom, success). Duarte's sparkline requires continuous rhythmic "
            "movement between both poles."
        ),
        dimension="contrast",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Flat Information Dump: Static feature list or boring status report with zero "
                    "dynamic contrast."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Unbalanced / One-Sided: Describes only current problems OR only future wishes "
                    "without oscillating tension."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Moderate Contrast: Makes a single transition from "
                    "problem to solution, but lacks "
                    "recurrent rhythm."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Strong Narrative Oscillation: Repeatedly juxtaposes present frustration with "
                    "future capability."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Masterful Duarte Cadence: Irresistible rhythmic tension pulling the listener "
                    "from current reality into transformed possibility."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="sparkline_audience_as_hero",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate whether the speaker positions the Audience as the Hero (Luke Skywalker) "
            "and the speaker as "
            "the Mentor / Guide (Yoda). Penalize speaker-centered arrogance where the "
            "presenter casts themselves as the sole hero."
        ),
        dimension="audience_hero",
        weight_in_dimension=1.0,
        criteria={
            "audience_is_the_hero": CriteriaOption(
                score=1.0,
                description=(
                    "Positions the audience as the hero of the journey; "
                    "frames the vision around what "
                    "the audience will conquer."
                ),
            ),
            "neutral_detached": CriteriaOption(
                score=0.5,
                description=(
                    "Speaks objectively about tools and metrics without "
                    "clearly casting the audience "
                    "as hero or ego."
                ),
            ),
            "speaker_centered_ego": CriteriaOption(
                score=0.1,
                description=(
                    "Ego trap: frames speaker or their company as the "
                    "sole hero and savior, treating "
                    "audience as passive spectators."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="sparkline_hook_first_30s",
        type=QuestionType.SCORE,
        prompt_instructions=(
            "Assess the power and arresting engagement of the opening hook in the first 15-30 "
            "seconds of `transcript`. "
            "Does the speaker shatter complacency with a startling metric, provocative "
            "question, or vivid story, "
            "or do they waste time on administrative throat-clearing?"
        ),
        dimension="hook",
        weight_in_dimension=1.0,
        criteria={
            "Level 1": CriteriaOption(
                score=0.2,
                description=(
                    "Boring Administrative Setup: Opens with slide logistics or pleasantries ('Hi "
                    "everyone, glad to be here...')."
                ),
            ),
            "Level 2": CriteriaOption(
                score=0.4,
                description=(
                    "Weak Opening: Starts with bland agenda items before reaching any emotional or "
                    "technical substance."
                ),
            ),
            "Level 3": CriteriaOption(
                score=0.6,
                description=(
                    "Standard Opening: Clear topic introduction, though lacks visceral emotional "
                    "punch."
                ),
            ),
            "Level 4": CriteriaOption(
                score=0.8,
                description=(
                    "Arresting Hook: Grips the room immediately with an unexpected metric, vivid "
                    "incident, or challenge."
                ),
            ),
            "Level 5": CriteriaOption(
                score=1.0,
                description=(
                    "Electrifying Opening: Immediately captures total cognitive focus, setting "
                    "immense stakes in the opening sentence."
                ),
            ),
        },
    ),
    JevQuestionDefinition(
        id="sparkline_star_moment_presence",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the presentation includes a S.T.A.R. Moment (Something They'll "
            "Always Remember)—such as "
            "a memorable dramatization, surprising statistic, unforgettable analogy, or vivid "
            "customer story."
        ),
        dimension="star_moment",
        weight_in_dimension=1.0,
        criteria={
            "star_moment_present": CriteriaOption(
                score=1.0,
                description=(
                    "Delivers an unmistakable, memorable S.T.A.R. showcase moment that anchors the "
                    "talk in memory."
                ),
            ),
            "generic_claim_only": CriteriaOption(
                score=0.4,
                description=(
                    "Presents factual data, but in an unmemorable, dry bullet-point format."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description="Zero memorable anchor; completely forgettable delivery.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="sparkline_new_bliss_vision",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Evaluate the conclusion in `transcript`. In Duarte's doctrine, talks should "
            "conclude with 'The New Bliss'—an "
            "inspiring vision of how the organization and world will operate once this "
            "mission is achieved. "
            "Penalize ending on flat administrative questions ('Any questions?')."
        ),
        dimension="new_bliss",
        weight_in_dimension=1.0,
        criteria={
            "inspiring_new_bliss": CriteriaOption(
                score=1.0,
                description=(
                    "Concludes with an inspiring, vivid vision of the transformed future state, "
                    "leaving the audience energized."
                ),
            ),
            "flat_logistical_ending": CriteriaOption(
                score=0.3,
                description=(
                    "Ends abruptly on administrative wrap-up ('That's all I have, questions?') "
                    "without an elevated vision."
                ),
            ),
            "absent_or_unresolved": CriteriaOption(
                score=0.0,
                description="Cuts off awkwardly without a formal conclusion.",
            ),
        },
    ),
    JevQuestionDefinition(
        id="sparkline_call_to_adventure",
        type=QuestionType.CHOICE,
        prompt_instructions=(
            "Determine whether the speaker issues a clear, unmistakable Call to Adventure "
            "challenging the audience "
            "to commit resources, adopt the standard, or take decisive action."
        ),
        dimension="call_to_adventure",
        weight_in_dimension=1.0,
        criteria={
            "clear_call_to_adventure": CriteriaOption(
                score=1.0,
                description=(
                    "Explicit, inspiring challenge inviting the "
                    "audience to cross the threshold and "
                    "act."
                ),
            ),
            "vague_invitation": CriteriaOption(
                score=0.4,
                description=(
                    "Mentions that 'it would be good to collaborate', "
                    "but lacks an explicit call to "
                    "action."
                ),
            ),
            "absent": CriteriaOption(
                score=0.0,
                description="Zero call to action presented.",
            ),
        },
    ),
]

CATALOG = FrameworkCatalog(
    framework="SPARKLINE",
    name="Duarte Sparkline (Presentations & Keynotes)",
    description=(
        "Nancy Duarte's persuasive presentation architecture. "
        "Structures talks around continuous contrast between 'What Is' and 'What Could Be', "
        "casting the audience as Luke Skywalker and the speaker as Yoda. Delivers "
        "memorable S.T.A.R. moments."
    ),
    target_pacing_seconds=120,
    dimension_weights={
        "contrast": 0.35,
        "hook": 0.25,
        "audience_hero": 0.15,
        "star_moment": 0.10,
        "new_bliss": 0.10,
        "call_to_adventure": 0.05,
    },
    questions=SPARKLINE_QUESTIONS,
    domain_rules={
        "contrast_weighted": True,
        "audience_hero_required": True,
    },
)
