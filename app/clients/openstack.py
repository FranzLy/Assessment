from __future__ import annotations

import logging
from typing import Protocol

from app.domain.models import VM

logger = logging.getLogger(__name__)


class OpenStackClient(Protocol):
    def create_server(self, vm: VM) -> None: ...

    def start_server(self, vm: VM) -> None: ...

    def stop_server(self, vm: VM) -> None: ...

    def reboot_server(self, vm: VM) -> None: ...

    def delete_server(self, vm: VM) -> None: ...


class MockOpenStackClient:
    """PoC adapter that mimics OpenStack operations with structured logs."""

    def create_server(self, vm: VM) -> None:
        logger.info("openstack.create_server vm_id=%s name=%s", vm.id, vm.name)

    def start_server(self, vm: VM) -> None:
        logger.info("openstack.start_server vm_id=%s", vm.id)

    def stop_server(self, vm: VM) -> None:
        logger.info("openstack.stop_server vm_id=%s", vm.id)

    def reboot_server(self, vm: VM) -> None:
        logger.info("openstack.reboot_server vm_id=%s", vm.id)

    def delete_server(self, vm: VM) -> None:
        logger.info("openstack.delete_server vm_id=%s", vm.id)
