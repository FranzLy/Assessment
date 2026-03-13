from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class VMStatus(str, Enum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    REBOOTING = "REBOOTING"
    DELETED = "DELETED"


class VMCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    image_id: str = Field(min_length=1)
    flavor_id: str = Field(min_length=1)
    network_id: str = Field(min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)


class VM(BaseModel):
    id: str
    name: str
    image_id: str
    flavor_id: str
    network_id: str
    metadata: dict[str, str] = Field(default_factory=dict)
    status: VMStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def new(cls, vm_id: str, req: VMCreateRequest) -> "VM":
        now = datetime.now(timezone.utc)
        return cls(
            id=vm_id,
            name=req.name,
            image_id=req.image_id,
            flavor_id=req.flavor_id,
            network_id=req.network_id,
            metadata=req.metadata,
            status=VMStatus.STOPPED,
            created_at=now,
            updated_at=now,
        )
