from __future__ import annotations


def _create_vm(client):
    payload = {
        "name": "vm-1",
        "image_id": "img-ubuntu-22",
        "flavor_id": "m1.small",
        "network_id": "net-001",
        "metadata": {"owner": "assessment"},
    }
    response = client.post("/v1/vms", json=payload)
    assert response.status_code == 201
    return response.json()


def test_healthcheck(client):
    response = client.get("/v1/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


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
