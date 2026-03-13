# Architecture Write-up

## Overview
This project is a Python/FastAPI proof-of-concept for VM lifecycle management against OpenStack-like operations.

## Layers
- API Layer (`app/api/routes.py`): REST endpoints, request/response mapping.
- Service Layer (`app/services/vm_service.py`): lifecycle orchestration and state transitions.
- Adapter Layer (`app/clients/openstack.py`): OpenStack client interface and mock implementation.
- Repository Layer (`app/repositories/vm_repository.py`): SQLite persistence abstraction.
- Domain Layer (`app/domain/*`): models and domain errors.
- Platform Layer (`app/security.py`, `app/observability.py`): auth and telemetry concerns.

## Key Design Choices
- Keep the API synchronous for PoC speed and readability.
- Use dependency inversion (`OpenStackClient` protocol) to decouple business logic from provider SDK.
- Use repository abstraction (`VMRepository`) so storage can evolve without changing API/service logic.
- Centralize lifecycle constraints in service methods to avoid duplicated state checks.
- Provide explicit domain exceptions mapped to stable HTTP responses (`404`, `409`).
- Add optional API key gate for protected VM endpoints.
- Add request-level telemetry (request id, timing, basic metrics).

## API Design Notes
- Versioned prefix: `/v1`.
- Resource-oriented endpoints (`/v1/vms`, `/v1/vms/{id}`).
- Action endpoints for lifecycle operations (`start`, `stop`, `reboot`).
- Health endpoint for liveness checks (`/v1/healthz`).
- Metrics endpoint for operational visibility (`/v1/metrics`).

## Non-Goals in Timebox
- No real OpenStack authentication/tenancy.
- No async job queue for long-running operations.
- No distributed metrics backend (Prometheus/OTel collector).

## Extension Path
- Replace `MockOpenStackClient` with real OpenStack SDK calls.
- Replace SQLite repository with PostgreSQL/Redis implementation.
- Move lifecycle operations to async jobs (Celery, RQ, or workflow engine).
