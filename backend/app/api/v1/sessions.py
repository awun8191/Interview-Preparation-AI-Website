"""Session evaluation and history retrieval API endpoints."""

import logging
import uuid
from datetime import UTC, datetime
from typing import Annotated, Any

import pydantic
from fastapi import APIRouter, Depends, Query, Request
from fastapi.exceptions import RequestValidationError

from app.core.errors import (
    AppError,
    FirestoreError,
    GroqSTTError,
    TypeSafeUnavailableError,
    ValidationError,
)
from app.frameworks import get_framework_catalog
from app.gateways.dependencies import (
    get_firestore_gateway,
    get_groq_gateway,
    get_jev_gateway,
)
from app.gateways.protocols import (
    FirestoreGatewayProtocol,
    GroqGatewayProtocol,
    JevGatewayProtocol,
)
from app.models.evaluation import (
    EvaluateSessionRequest,
    EvaluateSessionResponse,
    JevEvaluationState,
)
from app.models.scenario import FrameworkEnum
from app.models.session import SessionListResponse, SessionRecord
from app.services.analytics import calculate_delivery_analytics
from app.services.clarity import ClarityAssessor
from app.services.scoring import ScoringEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/evaluate", response_model=EvaluateSessionResponse)
@router.post("/evaluate/", response_model=EvaluateSessionResponse, include_in_schema=False)
async def evaluate_session(
    request: Request,
    groq_gateway: Annotated[GroqGatewayProtocol, Depends(get_groq_gateway)],
    jev_gateway: Annotated[JevGatewayProtocol, Depends(get_jev_gateway)],
    firestore_gateway: Annotated[FirestoreGatewayProtocol, Depends(get_firestore_gateway)],
) -> EvaluateSessionResponse:
    """Evaluate a spoken or written practice session against communication framework rubrics."""
    content_type = request.headers.get("content-type", "").lower()

    if "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        try:
            form = await request.form()
        except Exception as exc:
            raise ValidationError(f"Failed to parse form payload: {exc}") from exc

        raw_framework = form.get("framework") or form.get("target_framework")
        if not raw_framework:
            raise ValidationError("Field 'framework' is required.")

        try:
            catalog = get_framework_catalog(str(raw_framework))
        except ValueError as val_err:
            raise ValidationError(str(val_err)) from val_err

        raw_prompt = form.get("scenario_prompt") or form.get("prompt")
        if not raw_prompt:
            raise ValidationError("Field 'scenario_prompt' is required.")
        scenario_prompt = str(raw_prompt).strip()
        if not scenario_prompt:
            raise ValidationError("Field 'scenario_prompt' cannot be empty.")

        raw_context = form.get("scenario_context") or form.get("context")
        scenario_context = str(raw_context).strip() if raw_context else None

        role_val = (
            form.get("speaker_role")
            or form.get("role")
            or form.get("user_domain")
            or "Professional"
        )
        speaker_role = str(role_val)
        user_id = str(form.get("user_id") or "anonymous")

        audio_file = form.get("audio_file") or form.get("file") or form.get("audio")
        transcript_form = form.get("transcript")
        duration_form = form.get("duration_seconds")

        transcript = ""
        duration_seconds = 0.0
        word_timestamps: list[dict[str, Any]] | None = None

        if audio_file is not None and hasattr(audio_file, "read"):
            audio_bytes = await audio_file.read()
            if audio_bytes:
                filename = getattr(audio_file, "filename", "audio.wav") or "audio.wav"
                try:
                    transcription = await groq_gateway.transcribe_audio(
                        audio_bytes=audio_bytes,
                        filename=filename,
                    )
                    transcript = transcription.transcript
                    duration_seconds = transcription.duration_seconds
                    word_timestamps = transcription.words
                except AppError:
                    raise
                except Exception as exc:
                    logger.exception("Groq speech-to-text error: %s", exc)
                    raise GroqSTTError(
                        message=f"Groq speech-to-text transcription failed: {exc}",
                    ) from exc

        if not transcript and transcript_form:
            transcript = str(transcript_form).strip()
            if duration_form is not None:
                try:
                    duration_seconds = max(0.0, float(duration_form))
                except (ValueError, TypeError):
                    duration_seconds = 0.0

        if not transcript:
            raise ValidationError("Neither audio nor text was provided for evaluation.")

    else:
        # Default: JSON request body
        try:
            body = await request.json()
        except Exception as exc:
            raise ValidationError("Invalid JSON body or missing payload.") from exc

        if not isinstance(body, dict):
            raise ValidationError("Request body must be a JSON object.")

        try:
            eval_req = EvaluateSessionRequest.model_validate(body)
        except pydantic.ValidationError as pyd_exc:
            raise RequestValidationError(pyd_exc.errors()) from pyd_exc

        framework_raw = (
            eval_req.framework.value
            if hasattr(eval_req.framework, "value")
            else str(eval_req.framework)
        )
        try:
            catalog = get_framework_catalog(framework_raw)
        except ValueError as val_err:
            raise ValidationError(str(val_err)) from val_err

        scenario_prompt = eval_req.scenario_prompt.strip()
        if not scenario_prompt:
            raise ValidationError("Field 'scenario_prompt' cannot be empty.")

        scenario_context = eval_req.scenario_context
        speaker_role = eval_req.speaker_role
        user_id = eval_req.user_id

        if not eval_req.transcript or not eval_req.transcript.strip():
            raise ValidationError("Neither audio nor text was provided for evaluation.")

        transcript = eval_req.transcript.strip()
        duration_seconds = max(0.0, float(eval_req.duration_seconds or 0.0))
        word_timestamps = None

    # 1. Delivery Analytics
    analytics = calculate_delivery_analytics(
        transcript=transcript,
        duration_seconds=duration_seconds,
        word_timestamps=word_timestamps,
    )

    # 2. Format Jev evaluation state
    state = JevEvaluationState(
        scenario_prompt=scenario_prompt,
        scenario_context=scenario_context,
        target_framework=catalog.framework,
        speaker_role=speaker_role,
        transcript=transcript,
        word_count=analytics.word_count,
        duration_seconds=analytics.duration_seconds,
        words_per_minute=analytics.words_per_minute,
    )

    # 3. Rubric questions payload
    questions = catalog.to_jev_questions_payload()

    # 4. Invoke Jev gateway for parallel evaluation
    try:
        findings = await jev_gateway.evaluate_questions(state, questions)
    except AppError:
        raise
    except Exception as exc:
        logger.exception("TypeSafe AI Jev evaluation error: %s", exc)
        raise TypeSafeUnavailableError(
            message=f"TypeSafe AI Jev System One evaluation failed: {exc}",
            details=str(exc),
        ) from exc

    # 5. Deterministic scoring, badges, and tips synthesis
    scoring_engine = ScoringEngine()
    scorecard = scoring_engine.score_session(
        framework=catalog.framework,
        jev_findings=findings,
        analytics=analytics,
    )

    # 6. Firestore Persistence
    session_id = str(uuid.uuid4())
    created_at = datetime.now(UTC)
    badge_ids = [b.badge_id for b in scorecard.badges]

    clarity = ClarityAssessor().assess(
        scorecard.details.get("question_scores"),
        findings,
    )

    record = SessionRecord(
        session_id=session_id,
        user_id=user_id,
        framework=catalog.framework,
        prompt=scenario_prompt,
        transcript=transcript,
        score=scorecard.composite_score,
        findings=findings,
        tips=scorecard.tips,
        badges=badge_ids,
        clarity=clarity.model_dump(),
        delivery_metrics=analytics.model_dump(),
        created_at=created_at,
    )

    try:
        await firestore_gateway.save_session(record)
    except AppError:
        raise
    except Exception as exc:
        logger.exception("Firestore session persistence error: %s", exc)
        raise FirestoreError(
            message=f"Failed to persist evaluation session to Firestore: {exc}",
            details={"session_id": session_id, "user_id": user_id},
        ) from exc

    try:
        framework_enum = FrameworkEnum(catalog.framework)
    except ValueError:
        framework_enum = catalog.framework  # fallback to raw string if needed

    return EvaluateSessionResponse(
        session_id=session_id,
        user_id=user_id,
        framework=framework_enum,
        score=scorecard.composite_score,
        subscores=scorecard.subscore_items,
        findings=findings,
        tips=scorecard.tips,
        badges=scorecard.badges,
        clarity=clarity,
        delivery_metrics=analytics.model_dump(),
        delivery_analytics=analytics.model_dump(),
        scorecard=scorecard.model_dump(),
        created_at=created_at,
    )


@router.get("", response_model=SessionListResponse)
@router.get("/", response_model=SessionListResponse, include_in_schema=False)
async def get_user_sessions(
    user_id: Annotated[
        str, Query(min_length=1, description="User ID to retrieve historical sessions for")
    ],
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of sessions to return")
    ] = 20,
    cursor: Annotated[str | None, Query(description="Pagination cursor from previous page")] = None,
    firestore_gateway: Annotated[FirestoreGatewayProtocol, Depends(get_firestore_gateway)] = None,
) -> SessionListResponse:
    """Retrieve historical evaluation sessions for a given user ordered by created_at desc."""
    try:
        sessions = await firestore_gateway.get_user_sessions(
            user_id=user_id,
            limit=limit,
            cursor=cursor,
        )
    except AppError:
        raise
    except Exception as exc:
        logger.exception("Firestore session query error for user %s: %s", user_id, exc)
        raise FirestoreError(
            message=f"Failed to retrieve sessions from Firestore: {exc}",
            details={"user_id": user_id},
        ) from exc

    next_cursor = sessions[-1].session_id if len(sessions) == limit and sessions else None

    return SessionListResponse(
        items=sessions,
        total=len(sessions),
        cursor=next_cursor,
    )
