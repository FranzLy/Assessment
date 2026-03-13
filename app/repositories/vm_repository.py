from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from threading import Lock
from typing import Protocol

from app.domain.models import VM, VMStatus


class VMRepository(Protocol):
    def save(self, vm: VM) -> VM: ...

    def get(self, vm_id: str) -> VM | None: ...

    def list(self) -> list[VM]: ...


class SQLiteVMRepository:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._lock = Lock()
        self._init_db()

    def save(self, vm: VM) -> VM:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO vms (
                    id, name, image_id, flavor_id, network_id,
                    metadata, status, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    image_id=excluded.image_id,
                    flavor_id=excluded.flavor_id,
                    network_id=excluded.network_id,
                    metadata=excluded.metadata,
                    status=excluded.status,
                    updated_at=excluded.updated_at
                """,
                (
                    vm.id,
                    vm.name,
                    vm.image_id,
                    vm.flavor_id,
                    vm.network_id,
                    json.dumps(vm.metadata, sort_keys=True),
                    vm.status.value,
                    vm.created_at.isoformat(),
                    vm.updated_at.isoformat(),
                ),
            )
            conn.commit()
        return vm

    def get(self, vm_id: str) -> VM | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id, name, image_id, flavor_id, network_id,
                       metadata, status, created_at, updated_at
                FROM vms
                WHERE id = ?
                """,
                (vm_id,),
            ).fetchone()
        return self._row_to_vm(row) if row else None

    def list(self) -> list[VM]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, name, image_id, flavor_id, network_id,
                       metadata, status, created_at, updated_at
                FROM vms
                ORDER BY created_at ASC
                """
            ).fetchall()
        return [self._row_to_vm(row) for row in rows]

    def _init_db(self) -> None:
        if self._db_path != ":memory:":
            db_dir = os.path.dirname(self._db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS vms (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    image_id TEXT NOT NULL,
                    flavor_id TEXT NOT NULL,
                    network_id TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, check_same_thread=False)

    @staticmethod
    def _row_to_vm(row: tuple) -> VM:
        return VM(
            id=row[0],
            name=row[1],
            image_id=row[2],
            flavor_id=row[3],
            network_id=row[4],
            metadata=json.loads(row[5]),
            status=VMStatus(row[6]),
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8]),
        )
