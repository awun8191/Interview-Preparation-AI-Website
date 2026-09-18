"""Scenario generation API endpoints."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.errors import AppError, ProviderUnavailableError
from app.gateways.dependencies import get_gemini_gateway
from app.gateways.protocols import GeminiGatewayProtocol
from app.models.scenario import GenerateScenarioRequest, ScenarioResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.post("/generate", response_model=ScenarioResponse)
@router.post("/generate/", response_model=ScenarioResponse, include_in_schema=False)
async def generate_scenario(
    request: GenerateScenarioRequest,
    gemini_gateway: Annotated[GeminiGatewayProtocol, Depends(get_gemini_gateway)],
) -> ScenarioResponse:
    """Generate authentic, role-tailored practice prompts matching framework and domain."""
    try:
        scenario = await gemini_gateway.generate_scenario(request)
        return scenario
    except AppError:
        raise
    except Exception as exc:
        logger.exception("Scenario generation gateway error: %s", exc)
        raise ProviderUnavailableError(
            message=f"Scenario generation provider failed: {exc}",
        ) from exc
