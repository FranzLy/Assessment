from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from app.clients.openstack import OpenStackClient
from app.domain.errors import InvalidStateTransitionError, VMNotFoundError
from app.domain.models import VM, VMCreateRequest, VMStatus
from app.repositories.vm_repository import VMRepository


class VMService:
    def __init__(self, openstack_client: OpenStackClient, repository: VMRepository):
        self._openstack = openstack_client
        self._repository = repository
        self._lock = Lock()

    def create_vm(self, req: VMCreateRequest) -> VM:
        vm = VM.new(str(uuid4()), req)
        self._openstack.create_server(vm)
        return self._repository.save(vm)

    def list_vms(self) -> list[VM]:
        return self._repository.list()

    def get_vm(self, vm_id: str) -> VM:
        vm = self._repository.get(vm_id)
        if vm is None:
            raise VMNotFoundError(f"vm_id={vm_id} not found")
        return vm

    def start_vm(self, vm_id: str) -> VM:
        vm = self.get_vm(vm_id)
        if vm.status == VMStatus.DELETED:
            raise InvalidStateTransitionError("Cannot start a deleted VM")
        if vm.status == VMStatus.RUNNING:
            return vm
        if vm.status != VMStatus.STOPPED:
            raise InvalidStateTransitionError(f"Cannot start VM in status={vm.status}")
        self._openstack.start_server(vm)
        return self._update_status(vm_id, VMStatus.RUNNING)

    def stop_vm(self, vm_id: str) -> VM:
        vm = self.get_vm(vm_id)
        if vm.status == VMStatus.DELETED:
            raise InvalidStateTransitionError("Cannot stop a deleted VM")
        if vm.status == VMStatus.STOPPED:
            return vm
        if vm.status != VMStatus.RUNNING:
            raise InvalidStateTransitionError(f"Cannot stop VM in status={vm.status}")
        self._openstack.stop_server(vm)
        return self._update_status(vm_id, VMStatus.STOPPED)

    def reboot_vm(self, vm_id: str) -> VM:
        vm = self.get_vm(vm_id)
        if vm.status != VMStatus.RUNNING:
            raise InvalidStateTransitionError("Reboot requires VM in RUNNING status")
        self._openstack.reboot_server(vm)
        vm = self._update_status(vm_id, VMStatus.REBOOTING)
        return self._update_status(vm.id, VMStatus.RUNNING)

    def delete_vm(self, vm_id: str) -> VM:
        vm = self.get_vm(vm_id)
        if vm.status == VMStatus.DELETED:
            return vm
        self._openstack.delete_server(vm)
        return self._update_status(vm_id, VMStatus.DELETED)

    def _update_status(self, vm_id: str, status: VMStatus) -> VM:
        with self._lock:
            vm = self._repository.get(vm_id)
            if vm is None:
                raise VMNotFoundError(f"vm_id={vm_id} not found")
            vm.status = status
            vm.updated_at = datetime.now(timezone.utc)
            return self._repository.save(vm)
