# Architecture Write-up

## Overview
This project is a Python/FastAPI proof-of-concept for VM lifecycle management against OpenStack-like operations.

## Layers
- API Layer (`app/api/routes.py`): REST endpoints, request/response mapping.
- Service Layer (`app/services/vm_service.py`): lifecycle orchestration and state transitions.
- Adapter Layer (`app/clients/openstack.py`): OpenStack client interface and mock implementation.
- Domain Layer (`app/domain/*`): models and domain errors.

## Key Design Choices
- Keep the API synchronous for PoC speed and readability.
- Use dependency inversion (`OpenStackClient` protocol) to decouple business logic from provider SDK.
- Centralize lifecycle constraints in service methods to avoid duplicated state checks.
- Provide explicit domain exceptions mapped to stable HTTP responses (`404`, `409`).

## API Design Notes
- Versioned prefix: `/v1`.
- Resource-oriented endpoints (`/v1/vms`, `/v1/vms/{id}`).
- Action endpoints for lifecycle operations (`start`, `stop`, `reboot`).
- Health endpoint for liveness checks (`/v1/healthz`).

## Non-Goals in Timebox
- No real OpenStack authentication/tenancy.
- No async job queue for long-running operations.
- No persistent DB storage (in-memory only).

## Extension Path
- Replace `MockOpenStackClient` with real OpenStack SDK calls.
- Add repository layer for PostgreSQL/Redis.
- Move lifecycle operations to async jobs (Celery, RQ, or workflow engine).
