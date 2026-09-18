"""Unit tests for Framework Catalogs and Jev System One question definitions."""

import pytest

from app.frameworks import (
    ALL_CATALOGS,
    FrameworkCatalog,
    QuestionType,
    get_framework_catalog,
    list_framework_catalogs,
    list_supported_frameworks,
)

EXPECTED_FRAMEWORKS = [
    "STAR",
    "CARL",
    "PAR",
    "SCQA",
    "SBI",
    "RADICAL_CANDOR",
    "STATE",
    "GOTTMAN",
    "VOSS",
    "SPARKLINE",
    "MONROE",
]

EXPECTED_QUESTION_COUNTS = {
    "STAR": 8,
    "CARL": 8,
    "PAR": 7,
    "SCQA": 8,
    "SBI": 7,
    "RADICAL_CANDOR": 7,
    "STATE": 8,
    "GOTTMAN": 8,
    "VOSS": 8,
    "SPARKLINE": 8,
    "MONROE": 8,
}


def test_all_11_frameworks_registered():
    """Verify that all 11 communication methodologies are registered and loadable."""
    assert len(ALL_CATALOGS) == 11
    catalogs = list_framework_catalogs()
    assert len(catalogs) == 11

    supported = list_supported_frameworks()
    assert set(supported) == set(EXPECTED_FRAMEWORKS)

    for fw in EXPECTED_FRAMEWORKS:
        cat = get_framework_catalog(fw)
        assert isinstance(cat, FrameworkCatalog)
        assert cat.framework == fw
        assert len(cat.name) > 0
        assert len(cat.description) > 0


def test_framework_catalog_weights_sum_to_one():
    """Verify that dimension weights for each of the 11 catalogs sum strictly to 1.0."""
    from app.frameworks.cross_cutting import CLARITY_DIMENSION

    for cat in ALL_CATALOGS:
        total_weight = sum(cat.dimension_weights.values())
        assert pytest.approx(total_weight, rel=1e-5) == 1.0, (
            f"Framework {cat.framework} dimension weights sum to {total_weight}, expected 1.0"
        )
        # All framework dimensions carry positive weight; only the auxiliary
        # clarity dimension is allowed to be 0.0 (reported but not scored).
        assert cat.dimension_weights[CLARITY_DIMENSION] == 0.0, cat.framework
        for dim, weight in cat.dimension_weights.items():
            if dim == CLARITY_DIMENSION:
                continue
            assert weight > 0.0, (
                f"Framework {cat.framework} dimension '{dim}' has non-positive weight"
            )


def test_question_counts_and_types():
    """Verify total question count (85 across monorepo) and valid question properties."""
    total_questions = sum(len(cat.questions) for cat in ALL_CATALOGS)
    assert total_questions == 85, (
        f"Expected exactly 85 questions across 11 frameworks, got {total_questions}"
    )

    for cat in ALL_CATALOGS:
        expected_count = EXPECTED_QUESTION_COUNTS[cat.framework]
        assert len(cat.questions) == expected_count, (
            f"{cat.framework} has {len(cat.questions)} questions, expected {expected_count}"
        )

        for q in cat.questions:
            assert q.id.startswith(cat.framework.lower()) or "_" in q.id
            assert q.type in (QuestionType.CHOICE, QuestionType.SCORE, QuestionType.NOUL)
            assert len(q.prompt_instructions) > 20
            assert len(q.criteria) >= 2, f"Question {q.id} must have at least 2 criteria options"

            for opt_key, opt_val in q.criteria.items():
                assert 0.0 <= opt_val.score <= 1.0, (
                    f"Score for {q.id}:{opt_key} out of range [0, 1]"
                )
                assert len(opt_val.description) > 0, (
                    f"Description for {q.id}:{opt_key} must not be empty"
                )


def test_wire_payload_serialization():
    """Verify that to_jev_questions_payload produces valid Jev System One wire format."""
    for cat in ALL_CATALOGS:
        payload = cat.to_jev_questions_payload()
        assert isinstance(payload, dict)
        assert len(payload) == len(cat.questions)

        for _q_id, q_wire in payload.items():
            assert "type" in q_wire
            assert "instructions" in q_wire
            assert "criteria" in q_wire
            assert isinstance(q_wire["criteria"], dict)
            # Criteria in wire dict maps option key to string description
            for k, desc in q_wire["criteria"].items():
                assert isinstance(k, str)
                assert isinstance(desc, str)
                assert len(desc) > 0


def test_cross_cutting_clarity_questions_injected_into_all_catalogs():
    """Every catalog carries the two clarity questions in an auxiliary dimension."""
    from app.frameworks.cross_cutting import (
        AMBIGUITY_QUESTION_ID,
        CLARITY_DIMENSION,
        CLARITY_SCORE_QUESTION_ID,
    )

    for cat in ALL_CATALOGS:
        ids = {q.id for q in cat.questions}
        assert CLARITY_SCORE_QUESTION_ID in ids, cat.framework
        assert AMBIGUITY_QUESTION_ID in ids, cat.framework

        clarity_questions = cat.questions_by_dimension(CLARITY_DIMENSION)
        assert len(clarity_questions) == 2, cat.framework
        assert all(q.domain_metadata.get("cross_cutting") is True for q in clarity_questions)

        # Auxiliary dimension: reported as a 0-weight subscore, never composite-affecting.
        assert cat.dimension_weights[CLARITY_DIMENSION] == 0.0, cat.framework


def test_get_framework_catalog_aliases_and_casing():
    """Verify case insensitivity, hyphens, and wire aliases."""
    assert get_framework_catalog("star").framework == "STAR"
    assert get_framework_catalog("Star").framework == "STAR"
    assert get_framework_catalog("radical-candor").framework == "RADICAL_CANDOR"
    assert get_framework_catalog("radical candor").framework == "RADICAL_CANDOR"
    assert get_framework_catalog("VOSS_NEGOTIATION").framework == "VOSS"
    assert get_framework_catalog("DUARTE_SPARKLINE").framework == "SPARKLINE"
    assert get_framework_catalog("MONROE_SEQUENCE").framework == "MONROE"

    with pytest.raises(ValueError, match="Unsupported framework 'NONEXISTENT'"):
        get_framework_catalog("NONEXISTENT")
