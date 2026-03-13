from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.clients.openstack import MockOpenStackClient
from app.config import Settings
from app.domain.errors import InvalidStateTransitionError, VMNotFoundError
from app.logging_config import setup_logging
from app.services.vm_service import VMService


def create_app() -> FastAPI:
    settings = Settings.from_env()
    setup_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="REST API PoC for OpenStack VM lifecycle management",
    )
    app.state.vm_service = VMService(MockOpenStackClient())

    @app.exception_handler(VMNotFoundError)
    async def not_found_handler(_: Request, exc: VMNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidStateTransitionError)
    async def state_error_handler(_: Request, exc: InvalidStateTransitionError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    app.include_router(router)
    return app


app = create_app()
