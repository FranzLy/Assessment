from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def _create_vm(client, headers=None):
    payload = {
        "name": "vm-1",
        "image_id": "img-ubuntu-22",
        "flavor_id": "m1.small",
        "network_id": "net-001",
        "metadata": {"owner": "assessment"},
    }
    response = client.post("/v1/vms", json=payload, headers=headers)
    assert response.status_code == 201
    return response.json()


def test_healthcheck(client):
    response = client.get("/v1/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "X-Request-ID" in response.headers


def test_vm_lifecycle_happy_path(client):
    vm = _create_vm(client)
    vm_id = vm["id"]
    assert vm["status"] == "STOPPED"

    started = client.post(f"/v1/vms/{vm_id}/start")
    assert started.status_code == 200
    assert started.json()["status"] == "RUNNING"

    rebooted = client.post(f"/v1/vms/{vm_id}/reboot")
    assert rebooted.status_code == 200
    assert rebooted.json()["status"] == "RUNNING"

    stopped = client.post(f"/v1/vms/{vm_id}/stop")
    assert stopped.status_code == 200
    assert stopped.json()["status"] == "STOPPED"

    deleted = client.delete(f"/v1/vms/{vm_id}")
    assert deleted.status_code == 200
    assert deleted.json()["status"] == "DELETED"


def test_transition_conflict(client):
    vm = _create_vm(client)
    vm_id = vm["id"]

    response = client.post(f"/v1/vms/{vm_id}/reboot")
    assert response.status_code == 409
    assert "RUNNING" in response.json()["detail"]


def test_not_found(client):
    response = client.get("/v1/vms/not-exists")
    assert response.status_code == 404


def test_metrics_endpoint(client):
    client.get("/v1/healthz")
    response = client.get("/v1/metrics")
    assert response.status_code == 200
    payload = response.json()
    assert payload["requests_total"] >= 1
    assert any("GET /v1/healthz 200" in key for key in payload["route_counts"])


def test_auth_rejects_missing_key(auth_client):
    response = auth_client.post(
        "/v1/vms",
        json={
            "name": "vm-auth",
            "image_id": "img-1",
            "flavor_id": "m1.small",
            "network_id": "net-001",
            "metadata": {},
        },
    )
    assert response.status_code == 401


def test_auth_accepts_valid_key(auth_client):
    vm = _create_vm(auth_client, headers={"X-API-Key": "secret"})
    assert vm["status"] == "STOPPED"


def test_persistence_survives_restart(monkeypatch, tmp_path):
    db_path = tmp_path / "persist.db"
    monkeypatch.setenv("APP_DB_PATH", str(db_path))
    monkeypatch.setenv("APP_AUTH_ENABLED", "false")
    monkeypatch.delenv("APP_API_KEY", raising=False)

    client1 = TestClient(create_app())
    vm = _create_vm(client1)
    vm_id = vm["id"]
    client1.close()

    client2 = TestClient(create_app())
    loaded = client2.get(f"/v1/vms/{vm_id}")
    assert loaded.status_code == 200
    assert loaded.json()["id"] == vm_id
    client2.close()
