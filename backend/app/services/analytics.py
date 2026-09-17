"""Speech delivery analytics service.

Calculates speech pacing (WPM), acoustic pauses, and filler word density
from transcripts and word-level timestamp metadata.
"""

import math
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

FILLER_PHRASES = [
    "you know",
    "sort of",
    "kind of",
]

FILLER_TOKENS = [
    "um",
    "uh",
    "like",
    "actually",
    "basically",
]

ALL_TARGET_FILLERS = [
    "um",
    "uh",
    "like",
    "you know",
    "sort of",
    "kind of",
    "actually",
    "basically",
]


class DeliveryAnalyticsResult(BaseModel):
    """Structured result from speech delivery analysis."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    word_count: int = Field(..., description="Total words in transcript")
    duration_seconds: float = Field(..., description="Duration in seconds")
    words_per_minute: float = Field(..., description="Speaking pacing (WPM)")
    filler_count: int = Field(..., description="Total filler words/phrases detected")
    filler_words_breakdown: dict[str, int] = Field(
        default_factory=dict,
        description="Per-token breakdown of detected filler words",
    )
    filler_density_percentage: float = Field(
        ...,
        description="Percentage of total words that are fillers",
    )
    pause_count: int = Field(default=0, description="Total pauses detected (>= 0.5s)")
    power_pauses_count: int = Field(
        default=0,
        description="Deliberate executive power pauses (>= 1.5s)",
    )

    @property
    def filler_word_count(self) -> int:
        return self.filler_count

    @property
    def filler_density_pct(self) -> float:
        return self.filler_density_percentage

    @property
    def power_pause_count(self) -> int:
        return self.power_pauses_count


def calculate_delivery_analytics(
    transcript: str,
    duration_seconds: float,
    word_timestamps: list[dict[str, Any]] | None = None,
) -> DeliveryAnalyticsResult:
    """Analyze spoken or written transcript for pacing, filler words, and pauses.

    Args:
        transcript: Full transcript text.
        duration_seconds: Duration of the speech recording in seconds.
        word_timestamps: Optional list of word dicts with 'word', 'start', and 'end' keys.

    Returns:
        DeliveryAnalyticsResult with WPM, filler word statistics, and pause counts.
    """
    clean_text = transcript.strip()
    words = clean_text.split() if clean_text else []
    word_count = len(words)

    # Pacing: Words Per Minute
    if duration_seconds <= 0.0 or word_count == 0:
        wpm = 0.0
    else:
        wpm = round((word_count / duration_seconds) * 60.0, 2)

    # Filler word analysis
    filler_breakdown: dict[str, int] = {filler: 0 for filler in ALL_TARGET_FILLERS}

    lower_text = clean_text.lower()

    # 1. Multi-word phrases
    for phrase in FILLER_PHRASES:
        pattern = rf"\b{re.escape(phrase)}\b"
        matches = re.findall(pattern, lower_text)
        count = len(matches)
        filler_breakdown[phrase] = count

    # 2. Single-word tokens
    for token in FILLER_TOKENS:
        pattern = rf"\b{re.escape(token)}\b"
        matches = re.findall(pattern, lower_text)
        count = len(matches)
        filler_breakdown[token] = count

    total_filler_count = sum(filler_breakdown.values())

    # Filler density percentage
    filler_density = round((total_filler_count / word_count) * 100.0, 2) if word_count > 0 else 0.0

    # Pause analysis
    pause_count = 0
    power_pauses_count = 0

    valid_timestamps: list[dict[str, float]] = []
    if word_timestamps:
        for item in word_timestamps:
            if not isinstance(item, dict):
                continue
            s = item.get("start")
            e = item.get("end")
            if s is None or e is None:
                continue
            try:
                s_float = float(s)
                e_float = float(e)
                if (
                    math.isnan(s_float)
                    or math.isinf(s_float)
                    or math.isnan(e_float)
                    or math.isinf(e_float)
                ):
                    continue
                valid_timestamps.append({"start": s_float, "end": e_float})
            except (ValueError, TypeError):
                continue

    if valid_timestamps and len(valid_timestamps) > 1:
        # Sort by start time in case input is unsorted
        sorted_timestamps = sorted(
            valid_timestamps,
            key=lambda w: w["start"],
        )

        for i in range(len(sorted_timestamps) - 1):
            curr_end = sorted_timestamps[i]["end"]
            next_start = sorted_timestamps[i + 1]["start"]
            gap = next_start - curr_end

            if gap >= 0.5:
                pause_count += 1
            if gap >= 1.5:
                power_pauses_count += 1

    return DeliveryAnalyticsResult(
        word_count=word_count,
        duration_seconds=max(0.0, float(duration_seconds)),
        words_per_minute=wpm,
        filler_count=total_filler_count,
        filler_words_breakdown=filler_breakdown,
        filler_density_percentage=filler_density,
        pause_count=pause_count,
        power_pauses_count=power_pauses_count,
    )
