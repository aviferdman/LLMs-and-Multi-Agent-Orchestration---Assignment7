"""Tests for league API routes."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


@pytest.fixture
def setup_test_data(tmp_path, monkeypatch):
    """Setup test data directories."""
    test_data_dir = tmp_path / "data"
    test_data_dir.mkdir()
    (test_data_dir / "leagues").mkdir()

    monkeypatch.setenv("SHARED_DATA_DIR", str(test_data_dir))

    standings_file = test_data_dir / "leagues" / "standings.json"
    standings_data = {
        "league_id": "league_2025",
        "players": [
            {
                "player_id": "P01",
                "wins": 2,
                "losses": 1,
                "draws": 0,
                "points": 6,
                "rank": 1,
            },
            {
                "player_id": "P02",
                "wins": 1,
                "losses": 1,
                "draws": 1,
                "points": 4,
                "rank": 2,
            },
        ],
    }
    standings_file.write_text(json.dumps(standings_data))

    yield test_data_dir


def test_get_league_status_success(setup_test_data):
    """Test GET /api/v1/league/status returns league status."""
    response = client.get("/api/v1/league/status")

    assert response.status_code == 200
    data = response.json()
    assert "league_id" in data
    assert "status" in data
    assert "total_rounds" in data


def test_get_league_standings_success(setup_test_data):
    """Test GET /api/v1/league/standings returns standings."""
    response = client.get("/api/v1/league/standings")

    assert response.status_code == 200
    data = response.json()
    assert "standings" in data
    assert isinstance(data["standings"], list)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "league-api"


def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
