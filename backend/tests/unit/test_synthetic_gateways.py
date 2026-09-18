"""Unit tests for synthetic gateways and dependency injection."""

from datetime import UTC, datetime, timedelta

import pytest

from app.core.config import Settings
from app.gateways.dependencies import (
    get_firestore_gateway,
    get_gemini_gateway,
    get_groq_gateway,
    get_jev_gateway,
    get_synthetic_firestore,
)
from app.gateways.protocols import (
    FirestoreGatewayProtocol,
    GeminiGatewayProtocol,
    GroqGatewayProtocol,
    JevGatewayProtocol,
)
from app.gateways.synthetic import (
    SyntheticFirestoreGateway,
    SyntheticGeminiGateway,
    SyntheticGroqGateway,
    SyntheticJevGateway,
)
from app.models.evaluation import JevEvaluationState
from app.models.scenario import (
    DifficultyLevel,
    FrameworkEnum,
    GenerateScenarioRequest,
)
from app.models.session import SessionRecord, UserRecord


# ---------------------------------------------------------------------------
# 1. SyntheticGeminiGateway Tests
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_synthetic_gemini_protocol_conformance() -> None:
    """Verify SyntheticGeminiGateway conforms to GeminiGatewayProtocol."""
    gateway = SyntheticGeminiGateway()
    assert isinstance(gateway, GeminiGatewayProtocol)


@pytest.mark.asyncio
async def test_synthetic_gemini_generates_authentic_scenarios() -> None:
    """Test scenario generation across multiple frameworks and domains."""
    gateway = SyntheticGeminiGateway()

    # Test STAR framework
    star_req = GenerateScenarioRequest(
        target_framework=FrameworkEnum.STAR,
        user_domain="Staff Backend Engineer",
        difficulty_level=DifficultyLevel.ADVANCED,
        focus_theme="Database Failover",
    )
    star_res = await gateway.generate_scenario(star_req)

    assert star_res.target_framework == FrameworkEnum.STAR
    assert star_res.difficulty_level == DifficultyLevel.ADVANCED
    assert "Staff Backend Engineer" in star_res.context_background
    assert "Database Failover" in star_res.context_background
    assert len(star_res.prompt_question) > 20
    assert len(star_res.key_dimensions_to_test) >= 2
    assert star_res.target_duration_seconds > 0
    assert star_res.scenario_id.startswith("synthetic-star-")

    # Test CARL framework
    carl_req = GenerateScenarioRequest(
        target_framework=FrameworkEnum.CARL,
        user_domain="Engineering Manager",
        difficulty_level=DifficultyLevel.INTERMEDIATE,
    )
    carl_res = await gateway.generate_scenario(carl_req)

    assert carl_res.target_framework == FrameworkEnum.CARL
    assert "Engineering Manager" in carl_res.context_background
    assert "learning" in carl_res.title.lower() or "setback" in carl_res.title.lower()

    # Test VOSS negotiation framework
    voss_req = GenerateScenarioRequest(
        target_framework=FrameworkEnum.VOSS,
        user_domain="Technical Founder",
        difficulty_level=DifficultyLevel.BEGINNER,
    )
    voss_res = await gateway.generate_scenario(voss_req)

    assert voss_res.target_framework == FrameworkEnum.VOSS
    assert "Technical Founder" in voss_res.context_background
    assert "negotiat" in voss_res.prompt_question.lower() or "empathy" in voss_res.title.lower()


# ---------------------------------------------------------------------------
# 2. SyntheticGroqGateway Tests
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_synthetic_groq_protocol_conformance() -> None:
    """Verify SyntheticGroqGateway conforms to GroqGatewayProtocol."""
    gateway = SyntheticGroqGateway()
    assert isinstance(gateway, GroqGatewayProtocol)


@pytest.mark.asyncio
async def test_synthetic_groq_default_transcription() -> None:
    """Test STT transcription with realistic simulated audio bytes."""
    gateway = SyntheticGroqGateway()
    # Pass dummy binary audio bytes
    result = await gateway.transcribe_audio(b"\x00\x01\x02\x03", filename="test.wav")

    assert len(result.transcript) > 0
    assert result.duration_seconds > 0.0
    assert len(result.words) > 0

    # Verify word timing structure
    first_word = result.words[0]
    assert "word" in first_word
    assert "start" in first_word
    assert "end" in first_word
    assert first_word["start"] <= first_word["end"]


@pytest.mark.asyncio
async def test_synthetic_groq_custom_buffer_transcription() -> None:
    """Test STT transcription accepting synthetic text payload."""
    gateway = SyntheticGroqGateway()
    custom_text = (
        "I architected a distributed streaming pipeline that ingested 50k events per second."
    )
    result = await gateway.transcribe_audio(custom_text.encode("utf-8"), filename="test.wav")

    assert result.transcript == custom_text
    assert len(result.words) == len(custom_text.split())
    assert result.duration_seconds > 0.0


# ---------------------------------------------------------------------------
# 3. SyntheticJevGateway & Balanced Impact Rule Tests
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_synthetic_jev_protocol_conformance() -> None:
    """Verify SyntheticJevGateway conforms to JevGatewayProtocol."""
    gateway = SyntheticJevGateway()
    assert isinstance(gateway, JevGatewayProtocol)


@pytest.mark.asyncio
async def test_synthetic_jev_balanced_impact_rule_quantitative() -> None:
    """Ensure candidate with quantified metrics receives full impact credit."""
    gateway = SyntheticJevGateway()
    questions = {
        "star_result_and_impact": {
            "type": "choice",
            "criteria": {
                "quantified_metric_impact": "Result includes concrete numerical metrics.",
                "meaningful_qualitative_impact": "Result delivers clear operational impact.",
                "weak_or_vague_outcome": "Outcome is descriptive but superficial.",
                "absent_or_unresolved": "No outcome provided.",
            },
        },
    }

    state = JevEvaluationState(
        scenario_prompt="Describe a technical migration.",
        target_framework="STAR",
        transcript=(
            "I led the database migration, reducing p99 query latency by 45% and saving 120ms."
        ),
    )

    findings = await gateway.evaluate_questions(state, questions)
    res = findings["star_result_and_impact"]

    assert res["choice"] == "quantified_metric_impact"
    assert res["probabilities"]["quantified_metric_impact"] >= 0.85


@pytest.mark.asyncio
async def test_synthetic_jev_balanced_impact_rule_qualitative() -> None:
    """Ensure candidate with qualitative outcome receives full credit (Balanced Impact Rule)."""
    gateway = SyntheticJevGateway()
    questions = {
        "star_result_and_impact": {
            "type": "choice",
            "criteria": {
                "quantified_metric_impact": "Result includes concrete numerical metrics.",
                "meaningful_qualitative_impact": "Result delivers clear operational impact.",
                "weak_or_vague_outcome": "Outcome is descriptive but superficial.",
                "absent_or_unresolved": "No outcome provided.",
            },
        },
    }

    # Qualitative resolution without numerical percentages or metrics
    state = JevEvaluationState(
        scenario_prompt="Describe an outage resolution.",
        target_framework="STAR",
        transcript=(
            "I diagnosed the deadlock, unblocked the payments queue, and stabilized production."
        ),
    )

    findings = await gateway.evaluate(state, questions)
    res = findings["star_result_and_impact"]

    # Must grant meaningful_qualitative_impact under Balanced Impact Rule
    assert res["choice"] == "meaningful_qualitative_impact"
    assert res["probabilities"]["meaningful_qualitative_impact"] >= 0.85


@pytest.mark.asyncio
async def test_synthetic_jev_action_agency_scoring() -> None:
    """Test heuristic scoring of Action ownership based on agency markers."""
    gateway = SyntheticJevGateway()
    questions = {
        "star_action_ownership": {
            "type": "score",
            "criteria": {
                "Level 1": "Passive / zero agency",
                "Level 2": "Weak contribution",
                "Level 3": "Adequate ownership",
                "Level 4": "Strong leadership & specificity",
                "Level 5": "Exemplary strategic agency",
            },
        },
    }

    # Strong individual ownership
    strong_state = {
        "transcript": "I designed the schema, I diagnosed the issue, and I owned the deployment.",
        "target_framework": "STAR",
        "scenario_prompt": "Incident response",
    }
    strong_findings = await gateway.evaluate_questions(strong_state, questions)
    assert strong_findings["star_action_ownership"]["choice"] in ["Level 4", "Level 5"]

    # Passive 'we' phrasing
    passive_state = {
        "transcript": "We had a meeting and we decided that maybe we should look into it.",
        "target_framework": "STAR",
        "scenario_prompt": "Incident response",
    }
    passive_findings = await gateway.evaluate_questions(passive_state, questions)
    assert passive_findings["star_action_ownership"]["choice"] == "Level 2"


# ---------------------------------------------------------------------------
# 4. SyntheticFirestoreGateway Tests
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_synthetic_firestore_protocol_conformance() -> None:
    """Verify SyntheticFirestoreGateway conforms to FirestoreGatewayProtocol."""
    repo = SyntheticFirestoreGateway()
    assert isinstance(repo, FirestoreGatewayProtocol)


@pytest.mark.asyncio
async def test_synthetic_firestore_user_crud() -> None:
    """Test saving and retrieving user records."""
    repo = SyntheticFirestoreGateway()
    repo.clear()

    user = UserRecord(
        user_id="usr_test_123",
        email="eng@example.com",
        display_name="Senior Engineer",
        role="user",
        subscription_tier="pro",
    )

    # Initial get should return None
    assert await repo.get_user("usr_test_123") is None

    # Save user
    await repo.save_user(user)

    # Retrieve user
    retrieved = await repo.get_user("usr_test_123")
    assert retrieved is not None
    assert retrieved.user_id == "usr_test_123"
    assert retrieved.email == "eng@example.com"
    assert retrieved.display_name == "Senior Engineer"
    assert retrieved.subscription_tier == "pro"
    assert retrieved.updated_at is not None


@pytest.mark.asyncio
async def test_synthetic_firestore_sessions_ordering_and_pagination() -> None:
    """Test session saving, reverse-chronological ordering, and cursor pagination."""
    repo = SyntheticFirestoreGateway()
    repo.clear()

    user_id = "usr_session_tester"
    base_time = datetime.now(UTC)

    # Create 5 sessions with distinct timestamps
    sessions = []
    for i in range(5):
        s = SessionRecord(
            session_id=f"ses_00{i}",
            user_id=user_id,
            framework="STAR",
            prompt=f"Prompt {i}",
            transcript=f"Transcript {i}",
            score=80.0 + i,
            findings={"star_situation": {"choice": "well_grounded"}},
            tips=["Be more concise."],
            created_at=base_time + timedelta(minutes=i),
        )
        sessions.append(s)
        await repo.save_session(s)

    # Fetch page 1 with limit 2
    page_1 = await repo.get_user_sessions(user_id=user_id, limit=2)
    assert len(page_1) == 2
    # Should be ordered descending: ses_004 (latest), then ses_003
    assert page_1[0].session_id == "ses_004"
    assert page_1[1].session_id == "ses_003"

    # Fetch page 2 using cursor of last item from page 1
    cursor = page_1[-1].session_id
    page_2 = await repo.get_user_sessions(user_id=user_id, limit=2, cursor=cursor)
    assert len(page_2) == 2
    assert page_2[0].session_id == "ses_002"
    assert page_2[1].session_id == "ses_001"

    # Fetch remaining page
    cursor_2 = page_2[-1].session_id
    page_3 = await repo.get_user_sessions(user_id=user_id, limit=2, cursor=cursor_2)
    assert len(page_3) == 1
    assert page_3[0].session_id == "ses_000"


# ---------------------------------------------------------------------------
# 5. Dependency Injection Tests
# ---------------------------------------------------------------------------
def test_gateway_dependencies_inject_synthetic_by_default() -> None:
    """Verify that dependencies inject synthetic instances when unconfigured."""
    empty_settings = Settings(
        _env_file=None,
        GEMINI_API_KEY="",
        GROQ_API_KEY="",
        TYPESAFE_API_KEY="",
        FIREBASE_CREDENTIALS_PATH=None,
        FIRESTORE_EMULATOR_HOST=None,
        USE_SYNTHETIC_GATEWAYS=False,
    )

    gemini = get_gemini_gateway(settings=empty_settings)
    assert isinstance(gemini, SyntheticGeminiGateway)

    groq = get_groq_gateway(settings=empty_settings)
    assert isinstance(groq, SyntheticGroqGateway)

    jev = get_jev_gateway(settings=empty_settings)
    assert isinstance(jev, SyntheticJevGateway)

    firestore_gw = get_firestore_gateway(settings=empty_settings)
    assert isinstance(firestore_gw, SyntheticFirestoreGateway)


def test_gateway_dependencies_with_use_synthetic_flag() -> None:
    """Verify USE_SYNTHETIC_GATEWAYS=True forces synthetic gateways even with dummy keys."""
    synthetic_settings = Settings(
        GEMINI_API_KEY="dummy_gemini_key",
        GROQ_API_KEY="dummy_groq_key",
        TYPESAFE_API_KEY="dummy_typesafe_key",
        USE_SYNTHETIC_GATEWAYS=True,
    )

    assert isinstance(get_gemini_gateway(settings=synthetic_settings), SyntheticGeminiGateway)
    assert isinstance(get_groq_gateway(settings=synthetic_settings), SyntheticGroqGateway)
    assert isinstance(get_jev_gateway(settings=synthetic_settings), SyntheticJevGateway)
    assert isinstance(get_firestore_gateway(settings=synthetic_settings), SyntheticFirestoreGateway)


def test_shared_synthetic_firestore_singleton() -> None:
    """Verify that get_synthetic_firestore() returns the singleton instance."""
    gw_from_fn = get_synthetic_firestore()
    gw_from_dep = get_firestore_gateway()

    assert gw_from_fn is gw_from_dep
