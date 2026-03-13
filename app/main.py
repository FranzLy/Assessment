from __future__ import annotations

import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.clients.openstack import MockOpenStackClient
from app.config import Settings
from app.domain.errors import InvalidStateTransitionError, VMNotFoundError
from app.logging_config import setup_logging
from app.observability import MetricsCollector
from app.repositories.vm_repository import SQLiteVMRepository
from app.services.vm_service import VMService

logger = logging.getLogger(__name__)


def _route_label(request: Request) -> str:
    route = request.scope.get("route")
    if route and hasattr(route, "path"):
        return route.path
    return request.url.path


def create_app() -> FastAPI:
    settings = Settings.from_env()
    if settings.auth_enabled and not settings.api_key:
        raise ValueError("APP_API_KEY is required when APP_AUTH_ENABLED=true")
    setup_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="REST API PoC for OpenStack VM lifecycle management",
    )
    app.state.settings = settings
    app.state.metrics = MetricsCollector()
    app.state.vm_service = VMService(
        MockOpenStackClient(),
        SQLiteVMRepository(settings.db_path),
    )

    @app.middleware("http")
    async def request_observability(request: Request, call_next):
        start = perf_counter()
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            duration_ms = (perf_counter() - start) * 1000
            route = _route_label(request)
            app.state.metrics.record(request.method, route, 500, duration_ms)
            logger.exception(
                "request.failed request_id=%s method=%s path=%s duration_ms=%.2f",
                request_id,
                request.method,
                route,
                duration_ms,
            )
            raise
        duration_ms = (perf_counter() - start) * 1000
        route = _route_label(request)
        app.state.metrics.record(request.method, route, status_code, duration_ms)
        logger.info(
            "request.completed request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
            request_id,
            request.method,
            route,
            status_code,
            duration_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(VMNotFoundError)
    async def not_found_handler(_: Request, exc: VMNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidStateTransitionError)
    async def state_error_handler(_: Request, exc: InvalidStateTransitionError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    app.include_router(router)
    return app


app = create_app()
