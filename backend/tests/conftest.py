import sys
from pathlib import Path

# Add backend/ to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Provides a TestClient instance for API testing.
    """
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """
    Logs in as admin and returns Authorization headers.
    """
    response = client.post(
        "/auth/token",
        data={
            "username": "admin@test.com",
            "password": "admin123",
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
