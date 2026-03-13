from __future__ import annotations

from threading import Lock
from time import time


class MetricsCollector:
    def __init__(self) -> None:
        self._lock = Lock()
        self._started_at = time()
        self._requests_total = 0
        self._errors_total = 0
        self._route_counts: dict[str, int] = {}

    def record(self, method: str, route: str, status_code: int, duration_ms: float) -> None:
        route_key = f"{method} {route} {status_code}"
        with self._lock:
            self._requests_total += 1
            if status_code >= 500:
                self._errors_total += 1
            self._route_counts[route_key] = self._route_counts.get(route_key, 0) + 1

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            return {
                "uptime_seconds": int(time() - self._started_at),
                "requests_total": self._requests_total,
                "errors_total": self._errors_total,
                "route_counts": dict(self._route_counts),
            }
