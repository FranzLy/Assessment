from __future__ import annotations

from fastapi import APIRouter, Request, status

from app.domain.models import VM, VMCreateRequest
from app.services.vm_service import VMService

router = APIRouter(prefix="/v1", tags=["vms"])


def _svc(request: Request) -> VMService:
    return request.app.state.vm_service


@router.get("/healthz", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/vms", response_model=VM, status_code=status.HTTP_201_CREATED)
def create_vm(payload: VMCreateRequest, request: Request) -> VM:
    return _svc(request).create_vm(payload)


@router.get("/vms", response_model=list[VM])
def list_vms(request: Request) -> list[VM]:
    return _svc(request).list_vms()


@router.get("/vms/{vm_id}", response_model=VM)
def get_vm(vm_id: str, request: Request) -> VM:
    return _svc(request).get_vm(vm_id)


@router.post("/vms/{vm_id}/start", response_model=VM)
def start_vm(vm_id: str, request: Request) -> VM:
    return _svc(request).start_vm(vm_id)


@router.post("/vms/{vm_id}/stop", response_model=VM)
def stop_vm(vm_id: str, request: Request) -> VM:
    return _svc(request).stop_vm(vm_id)


@router.post("/vms/{vm_id}/reboot", response_model=VM)
def reboot_vm(vm_id: str, request: Request) -> VM:
    return _svc(request).reboot_vm(vm_id)


@router.delete("/vms/{vm_id}", response_model=VM)
def delete_vm(vm_id: str, request: Request) -> VM:
    return _svc(request).delete_vm(vm_id)
