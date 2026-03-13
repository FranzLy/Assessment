from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "OpenStack VM Lifecycle API"
    app_env: str = "dev"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_env=os.getenv("APP_ENV", cls.app_env),
            log_level=os.getenv("APP_LOG_LEVEL", cls.log_level).upper(),
        )
