"""Deterministic Badge Engine for Communication Practice Sessions.

Evaluates Jev question responses, dimension subscores, and delivery analytics
to synthesize UI badges, achievement awards, and diagnostic alerts.
"""

from typing import Any

try:
    from app.models.evaluation import BadgeItem
except ImportError:
    from pydantic import BaseModel, Field

    class BadgeItem(BaseModel):  # type: ignore[no-redef]
        badge_id: str = Field(..., description="Unique badge code")
        title: str = Field(..., description="Display title")
        description: str = Field(..., description="Explanation")
        category: str = Field(default="mastery", description="Category")


class BadgeEngine:
    """Evaluates session findings and analytics to award badges and diagnostic flags."""

    @staticmethod
    def _extract_choice(finding: Any) -> str:
        if isinstance(finding, dict):
            return str(
                finding.get("choice") or finding.get("value") or finding.get("selected") or ""
            )
        return str(finding or "")

    @staticmethod
    def _extract_score_level(finding: Any) -> int:
        if isinstance(finding, dict):
            val = finding.get("score") or finding.get("level") or finding.get("value")
        else:
            val = finding

        if isinstance(val, int):
            return val
        s = str(val or "")
        if "Level 5" in s or s == "5":
            return 5
        if "Level 4" in s or s == "4":
            return 4
        if "Level 3" in s or s == "3":
            return 3
        if "Level 2" in s or s == "2":
            return 2
        if "Level 1" in s or s == "1":
            return 1
        return 0

    @staticmethod
    def _extract_noul_prob(finding: Any, key: str = "yes") -> float:
        if isinstance(finding, dict):
            if key in finding:
                try:
                    return float(finding[key])
                except (ValueError, TypeError):
                    pass
            if "probabilities" in finding and key in finding["probabilities"]:
                try:
                    return float(finding["probabilities"][key])
                except (ValueError, TypeError):
                    pass
            choice = str(finding.get("choice") or "")
            if choice.lower() == key.lower():
                return 1.0
        s = str(finding or "").lower()
        if s == key.lower():
            return 1.0
        return 0.0

    def evaluate_badges(
        self,
        framework: str,
        jev_findings: dict[str, Any],
        subscores: dict[str, float],
        analytics: Any = None,
    ) -> list[BadgeItem]:
        """Synthesize badges and warnings from Jev findings and delivery metrics."""
        badges: list[BadgeItem] = []
        fw = framework.upper()

        # -------------------------------------------------------------
        # 1. Framework-Specific Jev Badges
        # -------------------------------------------------------------
        if fw == "STAR":
            res = self._extract_choice(jev_findings.get("star_result_and_impact"))
            if res == "meaningful_qualitative_impact":
                badges.append(
                    BadgeItem(
                        badge_id="HIGH_IMPACT_OUTCOME",
                        title="High-Impact Outcome",
                        description=(
                            "Excellent delivery of operational impact "
                            "solving core organizational/technical "
                            "bottlenecks."
                        ),
                        category="mastery",
                    )
                )
            elif res == "quantified_metric_impact":
                badges.append(
                    BadgeItem(
                        badge_id="QUANTIFIED_MASTERY",
                        title="Quantified Mastery",
                        description=(
                            "Outstanding use of measurable data points "
                            "and concrete numbers to prove impact."
                        ),
                        category="mastery",
                    )
                )
            elif res == "weak_or_vague_outcome":
                badges.append(
                    BadgeItem(
                        badge_id="VAGUE_IMPACT",
                        title="Vague Impact",
                        description=(
                            "Result lacked clear evidence of change or operational significance."
                        ),
                        category="warning",
                    )
                )

            act_level = self._extract_score_level(
                jev_findings.get("star_action_ownership_and_depth")
            )
            if act_level >= 4:
                badges.append(
                    BadgeItem(
                        badge_id="STRONG_AGENCY",
                        title="Strong Agency & Leadership",
                        description=(
                            "Decisive first-person ownership and proactive problem-solving."
                        ),
                        category="mastery",
                    )
                )
            elif 1 <= act_level <= 2:
                badges.append(
                    BadgeItem(
                        badge_id="THE_WE_TRAP",
                        title="The 'We' Trap (Low Agency)",
                        description=(
                            "Heavy reliance on passive team phrasing "
                            "obscures personal contribution."
                        ),
                        category="warning",
                    )
                )

            sit = self._extract_choice(jev_findings.get("star_situation_grounding"))
            if sit == "hypothetical_or_generic":
                badges.append(
                    BadgeItem(
                        badge_id="HYPOTHETICAL_GENERALIZATION",
                        title="Hypothetical Generalization",
                        description=(
                            "Recounted theoretical advice instead of an authentic past situation."
                        ),
                        category="warning",
                    )
                )

            bal = self._extract_choice(jev_findings.get("star_narrative_balance"))
            if bal == "context_heavy_history_lecture":
                badges.append(
                    BadgeItem(
                        badge_id="CONTEXT_OVERLOAD",
                        title="Context Overload",
                        description=(
                            "Spent majority of time on background lore "
                            "rather than action and results."
                        ),
                        category="warning",
                    )
                )

        elif fw == "CARL":
            res = self._extract_choice(jev_findings.get("carl_result_and_impact"))
            if res == "meaningful_qualitative_impact":
                badges.append(
                    BadgeItem(
                        badge_id="HIGH_OPERATIONAL_IMPACT",
                        title="High Operational Impact",
                        description=(
                            "Clearly articulated how service stability "
                            "and team alignment were restored."
                        ),
                        category="mastery",
                    )
                )
            elif res == "quantified_metric_impact":
                badges.append(
                    BadgeItem(
                        badge_id="QUANTIFIED_MASTERY",
                        title="Quantified Mastery",
                        description="Backed results with concrete quantitative statistics.",
                        category="mastery",
                    )
                )

            learn_level = self._extract_score_level(
                jev_findings.get("carl_learning_metacognitive_depth")
            )
            if learn_level >= 4:
                badges.append(
                    BadgeItem(
                        badge_id="SYSTEMIC_WISDOM",
                        title="Systemic Wisdom",
                        description=(
                            "Demonstrated how a single failure led to "
                            "permanent, team-wide safeguards."
                        ),
                        category="mastery",
                    )
                )
            elif learn_level == 2:
                badges.append(
                    BadgeItem(
                        badge_id="SUPERFICIAL_LEARNING",
                        title="Superficial Learning",
                        description=(
                            "Learning relied on generic platitudes "
                            "rather than systemic process improvements."
                        ),
                        category="warning",
                    )
                )
            elif learn_level == 1:
                badges.append(
                    BadgeItem(
                        badge_id="DEFENSIVE_BLAME_ALERT",
                        title="Defensive Blame Alert",
                        description=(
                            "Externalized blame onto teammates or legacy tooling; zero ownership."
                        ),
                        category="warning",
                    )
                )

            bal = self._extract_choice(jev_findings.get("carl_narrative_balance"))
            if bal == "rushed_afterthought_learning":
                badges.append(
                    BadgeItem(
                        badge_id="RUSHED_REFLECTION",
                        title="Rushed Reflection",
                        description=(
                            "Rushed reflection in the final seconds "
                            "rather than treating it as the primary "
                            "climax."
                        ),
                        category="warning",
                    )
                )

        elif fw == "PAR":
            brev = self._extract_choice(jev_findings.get("par_brevity_and_information_density"))
            if brev == "crisp_executive_brevity":
                badges.append(
                    BadgeItem(
                        badge_id="EXECUTIVE_BREVITY",
                        title="Executive Brevity",
                        description=(
                            "Delivered a complete, high-impact "
                            "narrative in under 60 seconds with zero "
                            "waste."
                        ),
                        category="mastery",
                    )
                )
            elif brev == "bloated_or_rambling":
                badges.append(
                    BadgeItem(
                        badge_id="BLOAT_WARNING",
                        title="Bloat Warning (>75s)",
                        description="Exceeded time budget with excessive background lore.",
                        category="warning",
                    )
                )

            prob = self._extract_choice(jev_findings.get("par_problem_sharpness"))
            if prob == "slow_meandering_setup":
                badges.append(
                    BadgeItem(
                        badge_id="BACKSTORY_CREEP",
                        title="Backstory Creep",
                        description=(
                            "Delayed stating the friction point until late in the response."
                        ),
                        category="warning",
                    )
                )

            res = self._extract_choice(jev_findings.get("par_result_and_impact"))
            if res in ("meaningful_qualitative_impact", "quantified_metric_impact"):
                badges.append(
                    BadgeItem(
                        badge_id="HIGH_OPERATIONAL_IMPACT",
                        title="High Operational Impact",
                        description=(
                            "Decisively eliminated technical bottlenecks and established stability."
                        ),
                        category="mastery",
                    )
                )

        elif fw == "SCQA":
            bluf_level = self._extract_score_level(jev_findings.get("scqa_bluf_efficiency"))
            if bluf_level >= 4:
                badges.append(
                    BadgeItem(
                        badge_id="EXECUTIVE_BLUF",
                        title="Executive BLUF",
                        description=(
                            "Delivered a decisive recommendation up front with clear justification."
                        ),
                        category="mastery",
                    )
                )
            elif 1 <= bluf_level <= 2:
                badges.append(
                    BadgeItem(
                        badge_id="BURYING_THE_LEDE",
                        title="Burying the Lede",
                        description=(
                            "Delayed core recommendation behind extensive background narrative."
                        ),
                        category="warning",
                    )
                )

            sit = self._extract_choice(jev_findings.get("scqa_situation_baseline"))
            if sit == "controversial_or_abrupt_lead":
                badges.append(
                    BadgeItem(
                        badge_id="AGGRESSIVE_LEAD",
                        title="Aggressive Lead",
                        description=(
                            "Opened with controversial complaints "
                            "rather than uncontroversial baseline "
                            "facts."
                        ),
                        category="warning",
                    )
                )

        elif fw == "SBI":
            cam_level = self._extract_score_level(jev_findings.get("sbi_behavioral_camera_test"))
            if cam_level >= 4:
                badges.append(
                    BadgeItem(
                        badge_id="CAMERA_RECORDABLE_PRECISION",
                        title="Camera-Recordable Precision",
                        description=(
                            "Stuck entirely to observable facts and "
                            "quoted language with zero mind-reading."
                        ),
                        category="mastery",
                    )
                )
            elif 1 <= cam_level <= 2:
                badges.append(
                    BadgeItem(
                        badge_id="MIND_READING_CHARACTER_ATTACK",
                        title="Mind-Reading / Character Attack",
                        description=(
                            "Used subjective personality labels ('you "
                            "were rude') triggering defensiveness."
                        ),
                        category="warning",
                    )
                )

            sand = self._extract_choice(jev_findings.get("sbi_feedback_sandwich_filter"))
            if sand == "artificial_sandwiching_detected":
                badges.append(
                    BadgeItem(
                        badge_id="SANDWICH_DETECTED",
                        title="Sandwich Detected",
                        description=(
                            "Padded critique inside fake compliments "
                            "rather than delivering direct candor."
                        ),
                        category="warning",
                    )
                )

            co = self._extract_choice(jev_findings.get("sbi_solution_co_creation"))
            if co == "collaborative_co_creation":
                badges.append(
                    BadgeItem(
                        badge_id="CO_AUTHORED_SOLUTION",
                        title="Co-Authored Solution",
                        description=(
                            "Invited the counterpart's perspective to "
                            "co-design future behavioral safeguards."
                        ),
                        category="mastery",
                    )
                )

        elif fw == "RADICAL_CANDOR":
            quad = self._extract_choice(jev_findings.get("candor_quadrant_classification"))
            if quad == "radical_candor":
                badges.append(
                    BadgeItem(
                        badge_id="RADICAL_CANDOR_ACHIEVED",
                        title="Radical Candor Achieved",
                        description=(
                            "Spoke direct truth with unmistakable "
                            "clarity while demonstrating deep personal "
                            "care."
                        ),
                        category="mastery",
                    )
                )
            elif quad == "ruinous_empathy":
                badges.append(
                    BadgeItem(
                        badge_id="RUINOUS_EMPATHY_TRAP",
                        title="The Ruinous Empathy Trap",
                        description=(
                            "Hedged critique out of fear of hurting "
                            "feelings, failing to convey the issue."
                        ),
                        category="warning",
                    )
                )
            elif quad == "obnoxious_aggression":
                badges.append(
                    BadgeItem(
                        badge_id="OBNOXIOUS_AGGRESSION_ALERT",
                        title="Obnoxious Aggression Alert",
                        description=(
                            "Critique was harsh and dismissive without demonstrating personal care."
                        ),
                        category="warning",
                    )
                )

            openness_yes = self._extract_noul_prob(
                jev_findings.get("candor_openness_to_counter_feedback"), "yes"
            )
            if openness_yes >= 0.7:
                badges.append(
                    BadgeItem(
                        badge_id="RECIPROCAL_VULNERABILITY",
                        title="Reciprocal Vulnerability",
                        description=(
                            "Proactively solicited critique on own "
                            "leadership, building deep safety."
                        ),
                        category="mastery",
                    )
                )

        elif fw == "STATE":
            facts_yes = self._extract_noul_prob(
                jev_findings.get("state_facts_first_sequencing"), "yes"
            )
            tent_level = self._extract_score_level(
                jev_findings.get("state_tentative_language_calibration")
            )
            if facts_yes >= 0.8 and tent_level >= 4:
                badges.append(
                    BadgeItem(
                        badge_id="CRUCIAL_MASTERY",
                        title="Crucial Mastery",
                        description=(
                            "Led with undeniable facts, framed concerns "
                            "with humility, and maintained safety."
                        ),
                        category="mastery",
                    )
                )
            elif facts_yes < 0.3:
                badges.append(
                    BadgeItem(
                        badge_id="ACCUSATORY_LEAD",
                        title="Accusatory Lead",
                        description=(
                            "Led with emotional grievances rather than verifiable objective data."
                        ),
                        category="warning",
                    )
                )

            if 1 <= tent_level <= 2:
                badges.append(
                    BadgeItem(
                        badge_id="THE_DOGMATIC_TRAP",
                        title="The Dogmatic Trap",
                        description=(
                            "Used dogmatic absolutes provoking "
                            "resistance rather than tentative "
                            "exploration."
                        ),
                        category="warning",
                    )
                )

            story = self._extract_choice(jev_findings.get("state_story_framing_awareness"))
            if story == "story_stated_as_absolute_truth":
                badges.append(
                    BadgeItem(
                        badge_id="STORY_AS_FACT_ALERT",
                        title="Story as Fact Alert",
                        description="Stated subjective interpretation as indisputable fact.",
                        category="warning",
                    )
                )

        elif fw == "GOTTMAN":
            horseman = self._extract_choice(jev_findings.get("gottman_four_horsemen_marker"))
            resp_level = self._extract_score_level(
                jev_findings.get("gottman_responsibility_acceptance")
            )

            if horseman == "contempt_detected":
                badges.append(
                    BadgeItem(
                        badge_id="CONTEMPT_ALERT",
                        title="Contempt Alert",
                        description=(
                            "Detected sarcasm, sneering, or mockery—the "
                            "deadliest relationship destructor."
                        ),
                        category="warning",
                    )
                )
            elif horseman == "defensiveness_detected":
                badges.append(
                    BadgeItem(
                        badge_id="DEFENSIVE_TRAP",
                        title="Defensive Trap",
                        description=(
                            "Played blameless victim or "
                            "counter-attacked rather than accepting "
                            "ownership."
                        ),
                        category="warning",
                    )
                )
            elif horseman == "none_clean_de_escalated" and resp_level >= 4:
                badges.append(
                    BadgeItem(
                        badge_id="MASTERFUL_DE_ESCALATION",
                        title="Masterful De-escalation",
                        description=(
                            "Neutralized conflict by validating emotions and owning responsibility."
                        ),
                        category="mastery",
                    )
                )

            repair = self._extract_choice(jev_findings.get("gottman_repair_attempt_usage"))
            if repair == "active_repair_attempt_used":
                badges.append(
                    BadgeItem(
                        badge_id="REPAIR_ATTEMPT_DEPLOYED",
                        title="Repair Attempt Deployed",
                        description=(
                            "Skillfully deployed a verbal cooling gesture to keep dialogue safe."
                        ),
                        category="mastery",
                    )
                )

        elif fw in ("VOSS", "VOSS_NEGOTIATION"):
            label_yes = self._extract_noul_prob(jev_findings.get("voss_emotion_labeling"), "yes")
            if label_yes >= 0.8:
                badges.append(
                    BadgeItem(
                        badge_id="TACTICAL_EMPATHY_MASTER",
                        title="Tactical Empathy Master",
                        description=(
                            "Disarmed tension with third-person sensory "
                            "emotion labels without conceding "
                            "leverage."
                        ),
                        category="mastery",
                    )
                )

            calib = self._extract_choice(jev_findings.get("voss_calibrated_questions"))
            if calib == "accusatory_why":
                badges.append(
                    BadgeItem(
                        badge_id="THE_WHY_TRAP",
                        title="The 'Why' Trap",
                        description=(
                            "Asked an accusatory 'Why' question "
                            "triggering defensiveness and resistance."
                        ),
                        category="warning",
                    )
                )
            elif calib == "calibrated_how_what":
                badges.append(
                    BadgeItem(
                        badge_id="COGNITIVE_BURDEN_SHIFT",
                        title="Cognitive Burden Shift",
                        description=(
                            "Brilliantly passed the problem-solving "
                            "burden to counterpart with 'How'/'What'."
                        ),
                        category="mastery",
                    )
                )

            tone = self._extract_choice(jev_findings.get("voss_vocal_tone_estimate"))
            if tone == "late_night_dj_calm":
                badges.append(
                    BadgeItem(
                        badge_id="LATE_NIGHT_FM_DJ",
                        title="Late-Night FM DJ",
                        description=(
                            "Calm downward-inflecting delivery "
                            "projected quiet authority and de-escalated "
                            ""
                            "pressure."
                        ),
                        category="delivery",
                    )
                )

        elif fw in ("SPARKLINE", "DUARTE_SPARKLINE"):
            contrast_level = self._extract_score_level(
                jev_findings.get("sparkline_what_is_vs_could_be_contrast")
            )
            if contrast_level >= 4:
                badges.append(
                    BadgeItem(
                        badge_id="DUARTE_CADENCE_MASTER",
                        title="Duarte Cadence Master",
                        description=(
                            "Created compelling tension oscillating "
                            "between current reality and future "
                            "possibility."
                        ),
                        category="mastery",
                    )
                )
            elif 1 <= contrast_level <= 2:
                badges.append(
                    BadgeItem(
                        badge_id="FLAT_INFORMATION_DUMP",
                        title="Flat Information Dump",
                        description=(
                            "Presentation felt like a flat status "
                            "update with no oratorical contrast."
                        ),
                        category="warning",
                    )
                )

            hook_level = self._extract_score_level(jev_findings.get("sparkline_hook_first_30s"))
            if 1 <= hook_level <= 2:
                badges.append(
                    BadgeItem(
                        badge_id="THROAT_CLEARING_WARNING",
                        title="Throat-Clearing Warning",
                        description=(
                            "Wasted opening seconds on administrative "
                            "logistics instead of an arresting hook."
                        ),
                        category="warning",
                    )
                )

            new_bliss = self._extract_choice(jev_findings.get("sparkline_new_bliss_vision"))
            if new_bliss == "inspiring_new_bliss":
                badges.append(
                    BadgeItem(
                        badge_id="THE_NEW_BLISS_ACHIEVED",
                        title="The New Bliss Achieved",
                        description=(
                            "Concluded on an elevated vision of the transformed future state."
                        ),
                        category="mastery",
                    )
                )

        elif fw in ("MONROE", "MONROE_SEQUENCE"):
            act = self._extract_choice(jev_findings.get("monroe_action_friction_and_clarity"))
            need = self._extract_choice(jev_findings.get("monroe_need_urgency"))
            if act == "singular_frictionless_ask" and need == "acute_need_proven":
                badges.append(
                    BadgeItem(
                        badge_id="PERSUASION_MASTER",
                        title="Persuasion Master",
                        description=(
                            "Established acute urgency, proved "
                            "satisfaction, and closed with a singular "
                            "ask."
                        ),
                        category="mastery",
                    )
                )
            elif act == "vague_non_committal_close":
                badges.append(
                    BadgeItem(
                        badge_id="THE_WASTED_CLOSE",
                        title="The Wasted Close",
                        description="Built momentum but ended on an indecisive non-committal ask.",
                        category="warning",
                    )
                )

            if need == "absent":
                badges.append(
                    BadgeItem(
                        badge_id="SOLUTION_WITHOUT_NEED",
                        title="Solution Without Need",
                        description="Pitched a cure before proving that any disease existed.",
                        category="warning",
                    )
                )

        # -------------------------------------------------------------
        # 2. Cross-Cutting Clarity & Ambiguity Badges
        # -------------------------------------------------------------
        ambiguity = self._extract_choice(jev_findings.get("ambiguity_presence"))
        clarity_level = self._extract_score_level(jev_findings.get("clarity_of_response"))

        if ambiguity == "materially_ambiguous":
            badges.append(
                BadgeItem(
                    badge_id="VAGUE_ANSWER",
                    title="Vague Answer",
                    description=(
                        "Answer contained material ambiguity: undefined "
                        "referents, contradictory claims, or hedging that "
                        "voided the point."
                    ),
                    category="warning",
                )
            )
        elif clarity_level >= 4 and ambiguity == "unambiguous_and_precise":
            badges.append(
                BadgeItem(
                    badge_id="HIGH_CLARITY",
                    title="High Clarity",
                    description=(
                        "Crisp, unambiguous answer that a listener can follow on the first pass."
                    ),
                    category="mastery",
                )
            )

        # -------------------------------------------------------------
        # 3. Acoustic & Speech Analytics Badges (if analytics provided)
        # -------------------------------------------------------------
        if analytics is not None:
            wpm = getattr(analytics, "words_per_minute", None)
            if wpm is not None:
                if 130 <= wpm <= 170:
                    badges.append(
                        BadgeItem(
                            badge_id="OPTIMAL_PACE",
                            title="Optimal Pace",
                            description=(
                                "Spoke at the gold standard executive speed of 130–170 WPM."
                            ),
                            category="delivery",
                        )
                    )
                elif wpm > 185:
                    badges.append(
                        BadgeItem(
                            badge_id="FAST_PACING_WARNING",
                            title="Fast Pacing Warning",
                            description=(
                                "Cadence was hurried (>185 WPM); slow down to let key points land."
                            ),
                            category="delivery",
                        )
                    )
                elif 0 < wpm < 110:
                    badges.append(
                        BadgeItem(
                            badge_id="SLOW_PACING_WARNING",
                            title="Slow Pacing Warning",
                            description="Cadence was slow (<110 WPM); elevate vocal energy.",
                            category="delivery",
                        )
                    )

            filler_density = getattr(analytics, "filler_density_percentage", None)
            if filler_density is not None and filler_density < 2.0:
                badges.append(
                    BadgeItem(
                        badge_id="CLEAN_CADENCE",
                        title="Clean Cadence",
                        description=(
                            "Exemplary vocal discipline: filler words comprised under 2% of speech."
                        ),
                        category="delivery",
                    )
                )

            power_pauses = getattr(analytics, "power_pauses_count", 0)
            if power_pauses >= 3:
                badges.append(
                    BadgeItem(
                        badge_id="POWER_PAUSER",
                        title="Power Pauser",
                        description=(
                            "Mastered deliberate silence (>=1.5s) to emphasize strategic points."
                        ),
                        category="delivery",
                    )
                )

        return badges
