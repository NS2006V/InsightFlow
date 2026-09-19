"""
Phase 0 tests: confirm the app factory builds correctly and the two
skeleton routes respond as expected.

Run with:
    pytest
"""

import pytest
from app import create_app


@pytest.fixture
def client():
    """A test client built with TestingConfig, not the dev/prod config."""
    app = create_app("testing")
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"InsightFlow" in response.data


def test_health_endpoint_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["app"] == "InsightFlow"
