"""API v1 master router."""

from fastapi import APIRouter

from app.api.v1 import health, scenarios, sessions

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(scenarios.router)
api_v1_router.include_router(sessions.router)
