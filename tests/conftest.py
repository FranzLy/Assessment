from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(monkeypatch, tmp_path) -> TestClient:
    monkeypatch.setenv("APP_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("APP_AUTH_ENABLED", "false")
    monkeypatch.delenv("APP_API_KEY", raising=False)
    app = create_app()
    return TestClient(app)


@pytest.fixture
def auth_client(monkeypatch, tmp_path) -> TestClient:
    monkeypatch.setenv("APP_DB_PATH", str(tmp_path / "test-auth.db"))
    monkeypatch.setenv("APP_AUTH_ENABLED", "true")
    monkeypatch.setenv("APP_API_KEY", "secret")
    app = create_app()
    return TestClient(app)
