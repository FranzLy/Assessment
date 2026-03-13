# OpenStack VM Lifecycle API (PoC)

This repository provides a time-boxed proof-of-concept REST API for managing OpenStack VM lifecycle operations.
It is designed to demonstrate API design, Python engineering fundamentals, SDLC thinking, and clear technical documentation.

## Objective
- Build REST endpoints for VM lifecycle operations.
- Deliver a working Python prototype with engineering best practices.
- Provide design and architecture write-up.
- Include a roadmap/backlog beyond the 2-4 hour timebox.

## Scope Implemented
- VM lifecycle APIs:
  - Create VM
  - List/Get VM
  - Start VM
  - Stop VM
  - Reboot VM
  - Delete VM
- Health check endpoint.
- In-memory state store for PoC.
- OpenStack adapter abstraction with mock implementation.
- Basic automated tests.

## Project Structure
```text
.
├── app
│   ├── api
│   │   └── routes.py
│   ├── clients
│   │   └── openstack.py
│   ├── domain
│   │   ├── errors.py
│   │   └── models.py
│   ├── services
│   │   └── vm_service.py
│   ├── config.py
│   ├── logging_config.py
│   └── main.py
├── docs
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
├── tests
│   ├── conftest.py
│   └── test_vm_api.py
├── .env.example
├── Makefile
└── pyproject.toml
```

## Quick Start
### 1) Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
make install
```

### 3) Run API
```bash
make run
```

API base URL: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

### 4) Run tests
```bash
make test
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/v1/healthz` | Service health check |
| POST | `/v1/vms` | Create VM |
| GET | `/v1/vms` | List VMs |
| GET | `/v1/vms/{vm_id}` | Get VM detail |
| POST | `/v1/vms/{vm_id}/start` | Start VM |
| POST | `/v1/vms/{vm_id}/stop` | Stop VM |
| POST | `/v1/vms/{vm_id}/reboot` | Reboot VM |
| DELETE | `/v1/vms/{vm_id}` | Delete VM |

## Example Calls
### Create VM
```bash
curl -X POST http://localhost:8000/v1/vms \
  -H "Content-Type: application/json" \
  -d '{
    "name": "vm-1",
    "image_id": "img-ubuntu-22",
    "flavor_id": "m1.small",
    "network_id": "net-001",
    "metadata": {"owner": "assessment"}
  }'
```

### Start VM
```bash
curl -X POST http://localhost:8000/v1/vms/<vm_id>/start
```

## Error Handling
- `404 Not Found`: VM does not exist.
- `409 Conflict`: invalid lifecycle transition for current VM state.

## Design Decisions
- Synchronous REST API for faster PoC delivery and easier demonstration.
- Domain/service separation to isolate lifecycle rules.
- Adapter pattern for OpenStack integration to keep vendor-specific code isolated.
- In-memory storage for timeboxed delivery; planned upgrade to persistent store.

Detailed architecture notes are in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).  
Backlog and roadmap are in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## SDLC Notes
- Timebox-oriented MVP first (working endpoints + tests + docs).
- Explicitly document non-goals and follow-up plan.
- Keep code small, testable, and ready for incremental hardening.

## Limitations (PoC)
- No real OpenStack auth or tenant scoping.
- No async orchestration for long-running operations.
- No durable persistence across service restarts.

## Next Steps
- Integrate real OpenStack SDK calls in `app/clients/openstack.py`.
- Add persistence and migration strategy.
- Add authN/authZ and production observability.
