from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = "OpenStack VM Lifecycle API"
    app_env: str = "dev"
    log_level: str = "INFO"
    db_path: str = "data/vms.db"
    auth_enabled: bool = False
    api_key: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_env=os.getenv("APP_ENV", cls.app_env),
            log_level=os.getenv("APP_LOG_LEVEL", cls.log_level).upper(),
            db_path=os.getenv("APP_DB_PATH", cls.db_path),
            auth_enabled=_env_bool("APP_AUTH_ENABLED", cls.auth_enabled),
            api_key=os.getenv("APP_API_KEY", cls.api_key),
        )
