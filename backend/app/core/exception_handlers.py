"""Global exception handlers ensuring standard non-2xx error envelopes."""

import logging
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError, ErrorCode

logger = logging.getLogger(__name__)


def _get_request_id(request: Request) -> str:
    """Extract or generate request_id for tracing."""
    request_id = getattr(request.state, "request_id", None)
    if not request_id:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    return str(request_id)


def _build_error_response(
    status_code: int,
    code: str,
    message: str,
    retryable: bool,
    details: Any,
    request_id: str,
) -> JSONResponse:
    """Build standard error envelope JSONResponse."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "retryable": retryable,
                "details": details,
            },
            "request_id": request_id,
        },
        headers={"X-Request-ID": request_id},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI application."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        request_id = _get_request_id(request)
        logger.warning(
            "AppError [%s] %s (status=%d, retryable=%s) [req_id=%s]",
            exc.code,
            exc.message,
            exc.status_code,
            exc.retryable,
            request_id,
        )
        return _build_error_response(
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
            retryable=exc.retryable,
            details=exc.details,
            request_id=request_id,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = _get_request_id(request)
        formatted_details = [
            {
                "loc": [str(loc_item) for loc_item in err.get("loc", [])],
                "msg": err.get("msg", ""),
                "type": err.get("type", ""),
            }
            for err in exc.errors()
        ]
        logger.info(
            "Validation error on %s %s: %d errors [req_id=%s]",
            request.method,
            request.url.path,
            len(formatted_details),
            request_id,
        )
        return _build_error_response(
            status_code=422,
            code=ErrorCode.VALIDATION_ERROR.value,
            message="Request validation failed.",
            retryable=False,
            details=formatted_details,
            request_id=request_id,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        request_id = _get_request_id(request)
        if exc.status_code == 404:
            code = ErrorCode.NOT_FOUND.value
        elif exc.status_code == 401:
            code = ErrorCode.UNAUTHORIZED.value
        elif exc.status_code == 422:
            code = ErrorCode.VALIDATION_ERROR.value
        elif exc.status_code >= 500:
            code = ErrorCode.INTERNAL_ERROR.value
        else:
            code = "HTTP_ERROR"

        retryable = exc.status_code >= 500
        message = str(exc.detail) if exc.detail else "HTTP request error."
        return _build_error_response(
            status_code=exc.status_code,
            code=code,
            message=message,
            retryable=retryable,
            details=None,
            request_id=request_id,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = _get_request_id(request)
        logger.exception("Unhandled server exception: %s [req_id=%s]", exc, request_id)
        return _build_error_response(
            status_code=500,
            code=ErrorCode.INTERNAL_ERROR.value,
            message="An unexpected internal server error occurred.",
            retryable=False,
            details=None,
            request_id=request_id,
        )
