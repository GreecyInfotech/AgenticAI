"""Platform smoke tests."""

import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


def _load_app(service_dir: str):
    path = ROOT / service_dir / "main.py"
    spec = importlib.util.spec_from_file_location(f"{service_dir.replace('-', '_')}_main", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.app


api = TestClient(_load_app("api-gateway"))


def test_api_gateway_health():
    response = api.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_services_registry():
    response = api.get("/services")
    assert response.status_code == 200
    assert "api-gateway" in response.json()
