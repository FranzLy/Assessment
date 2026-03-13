# Roadmap / Backlog

## Phase 1 (Next 1-2 days)
- Integrate real OpenStack SDK/client with auth and project scoping.
- Replace static API key with robust authN/authZ (JWT/OIDC).
- Add richer validation (name uniqueness, flavor/image checks, network constraints).

## Phase 2 (Next 1 week)
- Migrate persistent storage from SQLite to PostgreSQL with migrations.
- Add async task processing for lifecycle operations.
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
