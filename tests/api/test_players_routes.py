"""Tests for players API routes."""

import json
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

@pytest.fixture
def setup_player_data(tmp_path, monkeypatch):
    """Setup test player data."""
    test_data_dir = tmp_path / "data"
    test_data_dir.mkdir()
    (test_data_dir / "players").mkdir()

    monkeypatch.setenv("SHARED_DATA_DIR", str(test_data_dir))

    player_file = test_data_dir / "players" / "P01_history.json"
    player_data = {
        "player_id": "P01",
        "matches": [
            {
                "match_id": "match_001",
                "opponent_id": "P02",
                "result": "win",
                "score": 2,
                "opponent_score": 1,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            {
                "match_id": "match_003",
                "opponent_id": "P03",
                "result": "loss",
                "score": 1,
                "opponent_score": 2,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        ],
    }
    player_file.write_text(json.dumps(player_data))

    player_file2 = test_data_dir / "players" / "P02_history.json"
    player_data2 = {
        "player_id": "P02",
        "matches": [
            {
                "match_id": "match_001",
                "opponent_id": "P01",
                "result": "loss",
                "score": 1,
                "opponent_score": 2,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ],
    }
    player_file2.write_text(json.dumps(player_data2))

    yield test_data_dir

def test_list_players_success(setup_player_data):
    """Test GET /api/v1/players returns player list."""
    response = client.get("/api/v1/players")

    assert response.status_code == 200
    data = response.json()
    assert "players" in data
    assert isinstance(data["players"], list)

def test_get_player_by_id_success(setup_player_data):
    """Test GET /api/v1/players/{player_id} returns player details."""
    response = client.get("/api/v1/players/P01")

    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == "P01"
    assert "stats" in data

def test_get_player_not_found():
    """Test GET /api/v1/players/{player_id} with invalid ID."""
    response = client.get("/api/v1/players/invalid_player")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_get_player_history_success(setup_player_data):
    """Test GET /api/v1/players/{player_id}/history returns match history."""
    response = client.get("/api/v1/players/P01/history")

    assert response.status_code == 200
    data = response.json()
    assert "player_id" in data
    assert "matches" in data
    assert isinstance(data["matches"], list)

def test_get_player_history_not_found():
    """Test GET /api/v1/players/{player_id}/history with invalid ID."""
    response = client.get("/api/v1/players/invalid_player/history")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
