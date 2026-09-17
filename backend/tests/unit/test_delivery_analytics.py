"""Unit tests for speech delivery analytics."""

import pytest

from app.services.analytics import (
    ALL_TARGET_FILLERS,
    calculate_delivery_analytics,
)


def test_wpm_normal_speech() -> None:
    """Test standard WPM calculation with valid duration and words."""
    # 150 words in 60 seconds = 150 WPM
    words = "word " * 150
    result = calculate_delivery_analytics(transcript=words, duration_seconds=60.0)

    assert result.word_count == 150
    assert result.duration_seconds == 60.0
    assert result.words_per_minute == 150.0


def test_wpm_fractional_duration() -> None:
    """Test WPM with non-integer duration."""
    # 75 words in 30.5 seconds -> (75 / 30.5) * 60 = 147.54 WPM
    words = "test " * 75
    result = calculate_delivery_analytics(transcript=words, duration_seconds=30.5)

    assert result.word_count == 75
    assert result.words_per_minute == pytest.approx(147.54, abs=0.05)


def test_division_by_zero_protection() -> None:
    """Test that zero or negative duration returns 0 WPM without raising an exception."""
    result_zero = calculate_delivery_analytics(
        transcript="Some spoken words here",
        duration_seconds=0.0,
    )
    assert result_zero.words_per_minute == 0.0
    assert result_zero.duration_seconds == 0.0

    result_negative = calculate_delivery_analytics(
        transcript="Some spoken words here",
        duration_seconds=-15.0,
    )
    assert result_negative.words_per_minute == 0.0
    assert result_negative.duration_seconds == 0.0


def test_empty_transcript() -> None:
    """Test empty and whitespace-only transcripts."""
    result_empty = calculate_delivery_analytics(transcript="", duration_seconds=45.0)
    assert result_empty.word_count == 0
    assert result_empty.words_per_minute == 0.0
    assert result_empty.filler_count == 0
    assert result_empty.filler_density_percentage == 0.0
    assert result_empty.pause_count == 0
    assert result_empty.power_pauses_count == 0

    result_whitespace = calculate_delivery_analytics(transcript="   \n\t  ", duration_seconds=30.0)
    assert result_whitespace.word_count == 0
    assert result_whitespace.words_per_minute == 0.0


def test_filler_word_detection_all_tokens() -> None:
    """Test detection of all target single-word and multi-word filler phrases."""
    # Target fillers: um, uh, like, you know, sort of, kind of, actually, basically
    sample_text = (
        "Um, I was uh thinking that like we should you know migrate the database. "
        "It was sort of tricky and kind of risky, but actually it basically worked."
    )
    result = calculate_delivery_analytics(transcript=sample_text, duration_seconds=20.0)

    # Verify all 8 categories exist in breakdown
    for filler in ALL_TARGET_FILLERS:
        assert filler in result.filler_words_breakdown

    assert result.filler_words_breakdown["um"] == 1
    assert result.filler_words_breakdown["uh"] == 1
    assert result.filler_words_breakdown["like"] == 1
    assert result.filler_words_breakdown["you know"] == 1
    assert result.filler_words_breakdown["sort of"] == 1
    assert result.filler_words_breakdown["kind of"] == 1
    assert result.filler_words_breakdown["actually"] == 1
    assert result.filler_words_breakdown["basically"] == 1

    assert result.filler_count == 8
    # Total word count in sample_text
    expected_word_count = len(sample_text.split())
    assert result.word_count == expected_word_count
    # Density: (8 / expected_word_count) * 100
    expected_density = round((8 / expected_word_count) * 100.0, 2)
    assert result.filler_density_percentage == expected_density


def test_filler_case_insensitivity() -> None:
    """Test that filler detection ignores case."""
    text = "UM, this was ACTUALLY Kind Of unexpected, Basically LIKE that."
    result = calculate_delivery_analytics(transcript=text, duration_seconds=10.0)

    assert result.filler_words_breakdown["um"] == 1
    assert result.filler_words_breakdown["actually"] == 1
    assert result.filler_words_breakdown["kind of"] == 1
    assert result.filler_words_breakdown["basically"] == 1
    assert result.filler_words_breakdown["like"] == 1
    assert result.filler_count == 5


def test_filler_word_boundary_precision() -> None:
    """Ensure substrings like 'umbrella' or 'alike' are not counted as fillers."""
    text = "The umbrella was alike to a human kidney, not humdrum."
    result = calculate_delivery_analytics(transcript=text, duration_seconds=10.0)

    assert result.filler_words_breakdown["um"] == 0
    assert result.filler_words_breakdown["like"] == 0
    assert result.filler_count == 0
    assert result.filler_density_percentage == 0.0


def test_pause_and_power_pause_detection() -> None:
    """Test pause and power pause detection from word timestamps."""
    word_timestamps = [
        {"word": "First", "start": 0.0, "end": 0.5},
        # Gap = 1.0 - 0.5 = 0.5s -> pause (>= 0.5s)
        {"word": "second", "start": 1.0, "end": 1.4},
        # Gap = 1.6 - 1.4 = 0.2s -> normal speech gap (< 0.5s)
        {"word": "third", "start": 1.6, "end": 2.0},
        # Gap = 3.8 - 2.0 = 1.8s -> power pause (>= 1.5s) and pause (>= 0.5s)
        {"word": "fourth", "start": 3.8, "end": 4.5},
        # Gap = 6.0 - 4.5 = 1.5s -> exactly 1.5s power pause and pause
        {"word": "fifth", "start": 6.0, "end": 6.8},
    ]

    result = calculate_delivery_analytics(
        transcript="First second third fourth fifth",
        duration_seconds=7.0,
        word_timestamps=word_timestamps,
    )

    # 3 pauses total: 0.5s gap, 1.8s gap, 1.5s gap
    assert result.pause_count == 3
    # 2 power pauses: 1.8s gap, 1.5s gap
    assert result.power_pauses_count == 2


def test_unordered_word_timestamps() -> None:
    """Ensure word timestamps passed in out-of-order are sorted before calculating pauses."""
    unordered_timestamps = [
        {"word": "second", "start": 2.5, "end": 3.0},
        {"word": "first", "start": 0.0, "end": 0.5},
    ]
    # Gap between end=0.5 and start=2.5 is 2.0s -> 1 pause, 1 power pause
    result = calculate_delivery_analytics(
        transcript="first second",
        duration_seconds=4.0,
        word_timestamps=unordered_timestamps,
    )

    assert result.pause_count == 1
    assert result.power_pauses_count == 1


def test_convenience_property_aliases() -> None:
    """Test that property aliases work for backward and frontend compatibility."""
    result = calculate_delivery_analytics(
        transcript="Um hello world",
        duration_seconds=5.0,
        word_timestamps=[
            {"word": "Um", "start": 0.0, "end": 0.3},
            {"word": "hello", "start": 2.0, "end": 2.5},
            {"word": "world", "start": 2.6, "end": 3.0},
        ],
    )
    assert result.filler_word_count == result.filler_count
    assert result.filler_density_pct == result.filler_density_percentage
    assert result.power_pause_count == result.power_pauses_count


def test_word_timestamps_null_and_invalid_values() -> None:
    """Verify calculate_delivery_analytics gracefully handles None, NaN, and invalid timestamps."""
    # Timestamps with None start/end
    none_timestamps = [
        {"word": "hello", "start": None, "end": 1.0},
        {"word": "world", "start": 1.5, "end": None},
        {"word": "valid1", "start": 2.0, "end": 2.5},
        {"word": "valid2", "start": 4.5, "end": 5.0},  # gap: 2.0s -> 1 pause, 1 power pause
    ]
    res = calculate_delivery_analytics(
        transcript="hello world valid1 valid2",
        duration_seconds=5.0,
        word_timestamps=none_timestamps,
    )
    assert res.pause_count == 1
    assert res.power_pauses_count == 1

    # Completely invalid timestamps
    corrupted_timestamps = [
        {"word": "a", "start": float("nan"), "end": 1.0},
        {"word": "b", "start": 1.0, "end": float("inf")},
        {"word": "c", "start": "bad", "end": "data"},
        "not-a-dict",  # type: ignore[list-item]
    ]
    res_corrupted = calculate_delivery_analytics(
        transcript="a b c",
        duration_seconds=3.0,
        word_timestamps=corrupted_timestamps,
    )
    assert res_corrupted.pause_count == 0
    assert res_corrupted.power_pauses_count == 0
