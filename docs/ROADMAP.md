# Roadmap / Backlog

## Phase 1 (Next 1-2 days)
- Integrate real OpenStack SDK/client with auth and project scoping.
- Add request correlation IDs and structured JSON logs.
- Add richer validation (name uniqueness, flavor/image checks).

## Phase 2 (Next 1 week)
- Introduce persistent storage (PostgreSQL) with migrations.
- Add async task processing for lifecycle operations.
- Add API authN/authZ (JWT or service-to-service token).
- Add OpenAPI examples and contract tests.

## Phase 3 (Next 2-3 weeks)
- Add observability (metrics, tracing, dashboards, alerting).
- Add quota and policy engine (per tenant limits).
- Add retry/circuit-breaker strategy around OpenStack calls.
- Add CI pipeline (lint, tests, security scan, build artifact).

## Deferred / Nice to Have
- Webhook callbacks for lifecycle completion.
- Bulk operations and filters for VM fleet management.
- Soft-delete retention and audit history endpoint.
