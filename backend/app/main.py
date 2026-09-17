"""FastAPI application factory and entry point."""

import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.api.v1.router import api_v1_router
from app.core.config import Settings, get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import setup_logging


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware to propagate or generate X-Request-ID header and request state."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for startup and shutdown events."""
    settings = get_settings()
    setup_logging(level="DEBUG" if settings.DEBUG else "INFO")
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory configuring middleware, exception handlers, and routes."""
    current_settings = settings or get_settings()

    app = FastAPI(
        title=current_settings.PROJECT_NAME,
        debug=current_settings.DEBUG,
        lifespan=lifespan,
    )

    # Mount CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=current_settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # Mount Request ID middleware
    app.add_middleware(RequestIdMiddleware)

    # Register standardized error handlers
    register_exception_handlers(app)

    # Mount API v1 router
    app.include_router(api_v1_router, prefix=current_settings.API_V1_STR)

    return app


app = create_app()
