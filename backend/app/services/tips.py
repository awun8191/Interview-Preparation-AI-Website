"""Actionable Coaching Tips Generator for Communication Sessions.

Generates targeted, high-leverage feedback tips based on Jev System One question triggers,
subscore deficits, and speech analytics.
"""

from typing import Any


class CoachingTipsEngine:
    """Produces actionable, deterministic coaching feedback."""

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

    def generate_tips(
        self,
        framework: str,
        jev_findings: dict[str, Any],
        subscores: dict[str, float],
        analytics: Any = None,
    ) -> list[str]:
        """Produce a list of actionable coaching recommendations."""
        tips: list[str] = []
        fw = framework.upper()

        # -------------------------------------------------------------
        # 1. Framework Specific Triggers
        # -------------------------------------------------------------
        if fw == "STAR":
            res = self._extract_choice(jev_findings.get("star_result_and_impact"))
            if res == "weak_or_vague_outcome":
                tips.append(
                    "Your result was descriptive ('everything went "
                    "fine') but lacked clear evidence "
                    "of impact. "
                    "Clarify what actually changed: did it unblock "
                    "a squad, prevent client churn, or "
                    "improve system stability?"
                )
            elif res == "absent_or_unresolved":
                tips.append(
                    "You concluded your story without stating the "
                    "final outcome. Always finish your "
                    "narrative arc with "
                    "a clear statement of resolution or operational impact."
                )

            act = self._extract_score_level(jev_findings.get("star_action_ownership_and_depth"))
            if 1 <= act <= 2:
                tips.append(
                    "You leaned heavily on passive team phrasing ('we did', 'we migrated'). "
                    "Interviewers want to know "
                    "YOUR individual contribution. Rephrase using: "
                    "'I designed', 'I diagnosed', or "
                    "'My specific ownership was X'."
                )

            sit = self._extract_choice(jev_findings.get("star_situation_grounding"))
            if sit == "hypothetical_or_generic":
                tips.append(
                    "You answered in theoretical terms ('When "
                    "building systems, you should...') "
                    "rather than recounting "
                    "an authentic past event. Ground your answer in "
                    "a specific company, system, or "
                    "project."
                )

            bal = self._extract_choice(jev_findings.get("star_narrative_balance"))
            if bal == "context_heavy_history_lecture":
                tips.append(
                    "You spent over half your response setting up "
                    "backstory and background. Condense "
                    "your Situation "
                    "to 2–3 sentences so you have adequate time to showcase your actions and "
                    "decisions."
                )

            task = self._extract_choice(jev_findings.get("star_task_clarity"))
            if task == "absent_or_unclear":
                tips.append(
                    "You jumped from background into tasks without "
                    "clearly framing the obstacle. "
                    "State the core challenge "
                    "up front: what specific constraint, deadline, or failure were you solving?"
                )

        elif fw == "CARL":
            learn = self._extract_score_level(jev_findings.get("carl_learning_metacognitive_depth"))
            if learn == 2:
                tips.append(
                    "Your learning was clichéd ('communication is "
                    "key'). Senior interviewers look for "
                    "systemic takeaways: "
                    "what specific engineering gate, runbook, or architectural rule did you "
                    "institute?"
                )
            elif learn == 1:
                tips.append(
                    "You externalized blame onto teammates or "
                    "legacy tooling. Executive maturity "
                    "requires psychological "
                    "ownership: clearly state what assumption YOU personally got wrong."
                )

            bal = self._extract_choice(jev_findings.get("carl_narrative_balance"))
            if bal == "rushed_afterthought_learning":
                tips.append(
                    "You spent 90% of your time on the story and "
                    "rushed the learning in the final "
                    "seconds. In the CARL "
                    "framework, reserve the final 30–45 seconds exclusively for reflection and "
                    "takeaways."
                )

            res = self._extract_choice(jev_findings.get("carl_result_and_impact"))
            if res in ("weak_or_vague_outcome", "absent_or_unresolved"):
                tips.append(
                    "Do not skip the immediate outcome before "
                    "reflecting on learnings. State the "
                    "technical resolution first "
                    "(e.g. cluster stabilized, clients migrated) so "
                    "the learning has a concrete "
                    "baseline."
                )

        elif fw == "PAR":
            prob = self._extract_choice(jev_findings.get("par_problem_sharpness"))
            if prob == "slow_meandering_setup":
                tips.append(
                    "You spent over 20 seconds on setup before stating the problem. In the PAR "
                    "format, state the friction "
                    "point in your very first sentence: 'The challenge was X'."
                )

            brev = self._extract_choice(jev_findings.get("par_brevity_and_information_density"))
            if brev == "bloated_or_rambling":
                tips.append(
                    "Your response exceeded 75 seconds. In fast "
                    "screening rounds, aim for 45–60 "
                    "seconds by eliminating "
                    "background lore and focusing strictly on the high-leverage move you made."
                )

            act = self._extract_score_level(jev_findings.get("par_action_decisiveness"))
            if 1 <= act <= 2:
                tips.append(
                    "Highlight individual action verbs ('I "
                    "deployed', 'I inspected') rather than "
                    "passive team summaries."
                )

        elif fw == "SCQA":
            bluf = self._extract_score_level(jev_findings.get("scqa_bluf_efficiency"))
            if 1 <= bluf <= 2:
                tips.append(
                    "You spent too much time on background narrative before delivering your "
                    "recommendation. In executive "
                    "briefings, state the Answer in the first 20–30 seconds, then support it."
                )

            sit = self._extract_choice(jev_findings.get("scqa_situation_baseline"))
            if sit == "controversial_or_abrupt_lead":
                tips.append(
                    "You opened with a controversial claim or alarmist statement. In Minto's "
                    "doctrine, open with an "
                    "uncontroversial fact everyone agrees on to "
                    "establish psychological safety before "
                    "introducing friction."
                )

            rec = self._extract_choice(jev_findings.get("scqa_recommendation_substance"))
            if rec == "vague_non_committal":
                tips.append(
                    "Your recommendation was indecisive ('we could "
                    "look into things'). Executives "
                    "expect a point of view: "
                    "state an explicit recommendation with clear next steps."
                )

        elif fw == "SBI":
            cam = self._extract_score_level(jev_findings.get("sbi_behavioral_camera_test"))
            if 1 <= cam <= 2:
                tips.append(
                    "You used subjective personality labels ('you "
                    "were rude / unprofessional'). That "
                    "triggers instant defensiveness. "
                    "Describe only what a video camera could record: exact words and specific "
                    "physical actions."
                )

            sit = self._extract_choice(jev_findings.get("sbi_situation_anchoring"))
            if sit == "unanchored_sweeping_claim":
                tips.append(
                    "You used sweeping absolutes ('You always do "
                    "this'). This triggers fact-checking "
                    "debates. Anchor your "
                    "feedback to a single specific date, meeting, or pull request."
                )

            sand = self._extract_choice(jev_findings.get("sbi_feedback_sandwich_filter"))
            if sand == "artificial_sandwiching_detected":
                tips.append(
                    "Avoid hiding hard critique inside fake "
                    "compliments. Leaders value clean, direct, "
                    "and respectful transparency."
                )

        elif fw == "RADICAL_CANDOR":
            quad = self._extract_choice(jev_findings.get("candor_quadrant_classification"))
            if quad == "ruinous_empathy":
                tips.append(
                    "You were too soft and hedged your critique. "
                    "Out of fear of hurting feelings, you "
                    "failed to communicate "
                    "the gravity of the problem. Remember: 'Clarity "
                    "is kindness'. Be direct about the "
                    "standard."
                )
            elif quad == "obnoxious_aggression":
                tips.append(
                    "Your critique was harsh and dismissive. "
                    "Challenging directly without personal "
                    "care creates defensiveness "
                    "and fear. Acknowledge their dignity and offer genuine support."
                )

            chal = self._extract_score_level(jev_findings.get("candor_challenge_directly_clarity"))
            if 1 <= chal <= 2:
                tips.append(
                    "The recipient leaves this conversation without "
                    "knowing exactly what must change. "
                    "Be specific: name the "
                    "exact deliverables, dates, and non-negotiable standards."
                )

        elif fw == "STATE":
            facts = self._extract_noul_prob(jev_findings.get("state_facts_first_sequencing"), "yes")
            if facts < 0.3:
                tips.append(
                    "You led with your emotional conclusion or "
                    "grievance rather than data. In high- "
                    "stakes disputes, state "
                    "observable facts first (dates, PRs, metrics) before sharing your story."
                )

            tent = self._extract_score_level(
                jev_findings.get("state_tentative_language_calibration")
            )
            if 1 <= tent <= 2:
                tips.append(
                    "You used dogmatic absolutes ('You always', "
                    "'Obviously', 'There is no question'). "
                    "Absolutes provoke "
                    "instant resistance. Soften your delivery: 'It "
                    "appears to me', 'My concern is "
                    "that'."
                )

            story = self._extract_choice(jev_findings.get("state_story_framing_awareness"))
            if story == "story_stated_as_absolute_truth":
                tips.append(
                    "You stated your interpretation as an "
                    "incontrovertible fact. Remember: facts are "
                    "verifiable; stories are "
                    "mental models. Frame your conclusion as: 'The story I'm telling myself is...'."
                )

        elif fw == "GOTTMAN":
            horseman = self._extract_choice(jev_findings.get("gottman_four_horsemen_marker"))
            if horseman == "contempt_detected":
                tips.append(
                    "Detected sarcasm, mocking, or sneering "
                    "language. In Gottman's research, Contempt "
                    "is the #1 predictor of "
                    "partnership destruction. Banish all sarcasm and address the problem as equals."
                )
            elif horseman == "defensiveness_detected":
                tips.append(
                    "You played the blameless victim or counter-attacked ('Don't blame me!'). "
                    "Defensiveness escalates anger. "
                    "Neutralize it by owning even 5% of the fault: "
                    "'You're right, I should have "
                    "flagged that earlier'."
                )

            val = self._extract_score_level(jev_findings.get("gottman_validation_of_counterpart"))
            if 1 <= val <= 2:
                tips.append(
                    "You dismissed their feelings ('You're overreacting'). People cannot solve "
                    "problems logically until they feel "
                    "heard. Validate their emotion first: 'I understand why you are so upset'."
                )

        elif fw in ("VOSS", "VOSS_NEGOTIATION"):
            calib = self._extract_choice(jev_findings.get("voss_calibrated_questions"))
            if calib == "accusatory_why":
                tips.append(
                    "You asked a 'Why' question ('Why did you raise "
                    "the rates?'). 'Why' triggers "
                    "defensiveness in negotiation. "
                    "Rephrase to a calibrated 'What': 'What led to this change in pricing?'"
                )

            label = self._extract_noul_prob(jev_findings.get("voss_emotion_labeling"), "yes")
            if label < 0.4:
                tips.append(
                    "You jumped straight into counter-arguments "
                    "without labeling their emotion. "
                    "Always diffuse negative tension "
                    "first: 'It sounds like your hands are tied by corporate leadership'."
                )

            conc = self._extract_score_level(jev_findings.get("voss_reciprocal_concession_framing"))
            if 1 <= conc <= 2:
                tips.append(
                    "You compromised too easily or offered to split "
                    "the difference. In high-stakes "
                    "negotiation, never concede "
                    "without asking for something in return: 'If I "
                    "agree to X, what can you do for "
                    "Y?'"
                )

        elif fw in ("SPARKLINE", "DUARTE_SPARKLINE"):
            contrast = self._extract_score_level(
                jev_findings.get("sparkline_what_is_vs_could_be_contrast")
            )
            if 1 <= contrast <= 2:
                tips.append(
                    "Your presentation felt like a flat feature "
                    "list. Build dynamic contrast: show "
                    "what is broken or painful "
                    "today, then contrast it directly with what could be."
                )

            hook = self._extract_score_level(jev_findings.get("sparkline_hook_first_30s"))
            if 1 <= hook <= 2:
                tips.append(
                    "You opened with boring pleasantries or "
                    "administrative setup. In high-stakes "
                    "talks, grab the room in the "
                    "first 15 seconds: open with a startling "
                    "metric, provocative question, or vivid "
                    "story."
                )

        elif fw in ("MONROE", "MONROE_SEQUENCE"):
            need = self._extract_choice(jev_findings.get("monroe_need_urgency"))
            if need == "absent":
                tips.append(
                    "You pitched your solution before the audience "
                    "felt the pain. People do not buy "
                    "cures for diseases they "
                    "don't have. Develop the Need and consequence of inaction first."
                )

            act = self._extract_choice(jev_findings.get("monroe_action_friction_and_clarity"))
            if act == "vague_non_committal_close":
                tips.append(
                    "You built great momentum but ended with a "
                    "weak, non-committal ask ('Think about "
                    "it and let me know'). "
                    "Always close with a specific physical step: "
                    "'Sign here for the 30-day pilot "
                    "today'."
                )

        # -------------------------------------------------------------
        # 2. Cross-Cutting Clarity & Ambiguity Guidance
        # -------------------------------------------------------------
        ambiguity = self._extract_choice(jev_findings.get("ambiguity_presence"))
        clarity_level = self._extract_score_level(jev_findings.get("clarity_of_response"))

        if ambiguity == "materially_ambiguous":
            tips.append(
                "Your answer contained material ambiguity: a listener could "
                "not tell exactly what you meant. Resolve vague references "
                "(name the 'it' or 'they'), drop hedges like 'kind of' or "
                "'maybe', and commit to specific claims."
            )
        elif clarity_level and clarity_level <= 2:
            tips.append(
                "Your answer was hard to follow even though the content may "
                "be sound. Lead with a single explicit point, order the "
                "supporting detail, and cut filler and false starts."
            )

        # -------------------------------------------------------------
        # 3. General Subscore Deficit Guidance (if subscore < 60)
        # -------------------------------------------------------------
        for dim, score in subscores.items():
            if score < 50.0 and len(tips) < 3:
                clean_dim = dim.replace("_", " ").title()
                fallback_tip = (
                    f"Focus on elevating your {clean_dim} "
                    f"component (scored {score:.0f}/100) with "
                    f"more concrete specifics and structured "
                    f"framing."
                )
                if fallback_tip not in tips:
                    tips.append(fallback_tip)

        # -------------------------------------------------------------
        # 3. Delivery Analytics Guidance
        # -------------------------------------------------------------
        if analytics is not None:
            wpm = getattr(analytics, "words_per_minute", None)
            if wpm is not None and wpm > 185:
                tips.append(
                    f"Your speaking rate was {wpm:.0f} WPM (above the "
                    f"recommended 130–170 WPM). Slow down and use "
                    "deliberate pauses so your listener has time to absorb complex points."
                )
            elif wpm is not None and 0 < wpm < 110:
                tips.append(
                    f"Your speaking rate was {wpm:.0f} WPM (below 110 "
                    f"WPM). Pick up your cadence to maintain audience "
                    f"engagement."
                )

            density = getattr(analytics, "filler_density_percentage", None)
            if density is not None and density > 5.0:
                tips.append(
                    f"Filler word density was {density:.1f}% of your "
                    f"spoken words. Replace filler phrases with silent "
                    f"pauses."
                )

        return tips
