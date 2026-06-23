"""Tests for logistics-agent."""

import pytest
from fastapi.testclient import TestClient

from smart_port_common.auth import create_token


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


@pytest.fixture
def auth_headers():
    token = create_token("test-user", roles=["operator"])
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_tools(client, auth_headers):
    response = client.get("/tools", headers=auth_headers)
    assert response.status_code == 200
    assert "tools" in response.json()
