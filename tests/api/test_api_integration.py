"""Integration tests for API with real SDK components."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

@pytest.fixture
def integration_data(tmp_path, monkeypatch):
    """Setup complete integration test data."""
    test_data_dir = tmp_path / "data"
    test_data_dir.mkdir()
    (test_data_dir / "leagues").mkdir()
    (test_data_dir / "matches").mkdir()
    (test_data_dir / "players").mkdir()

    monkeypatch.setenv("SHARED_DATA_DIR", str(test_data_dir))

    standings = {
        "league_id": "league_2025",
        "players": [
            {"player_id": "P01", "wins": 3, "losses": 0, "points": 9, "rank": 1},
            {"player_id": "P02", "wins": 2, "losses": 1, "points": 6, "rank": 2},
            {"player_id": "P03", "wins": 1, "losses": 2, "points": 3, "rank": 3},
            {"player_id": "P04", "wins": 0, "losses": 3, "points": 0, "rank": 4},
        ],
    }
    (test_data_dir / "leagues" / "standings.json").write_text(json.dumps(standings))

    for i, match_id in enumerate(["match_001", "match_002", "match_003"], start=1):
        match_data = {
            "match_id": match_id,
            "player_a_id": f"P0{i}",
            "player_b_id": f"P0{i+1}",
            "status": "completed",
            "winner": f"P0{i}",
        }
        (test_data_dir / "matches" / f"{match_id}.json").write_text(
            json.dumps(match_data)
        )

    for player_id in ["P01", "P02", "P03", "P04"]:
        history = {"player_id": player_id, "matches": []}
        (test_data_dir / "players" / f"{player_id}_history.json").write_text(
            json.dumps(history)
        )

    yield test_data_dir

def test_full_api_workflow(integration_data):
    """Test complete API workflow."""
    status_response = client.get("/api/v1/league/status")
    assert status_response.status_code == 200

    standings_response = client.get("/api/v1/league/standings")
    assert standings_response.status_code == 200
    standings = standings_response.json()["standings"]
    assert len(standings) == 4

    matches_response = client.get("/api/v1/matches")
    assert matches_response.status_code == 200

    players_response = client.get("/api/v1/players")
    assert players_response.status_code == 200

def test_api_response_format_compliance(integration_data):
    """Test that all API responses follow expected format."""
    endpoints = [
        "/api/v1/league/status",
        "/api/v1/league/standings",
        "/api/v1/matches",
        "/api/v1/players",
        "/api/v1/games",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

def test_standings_rankings_consistent(integration_data):
    """Test that standings are properly ranked."""
    response = client.get("/api/v1/league/standings")
    standings = response.json()["standings"]

    ranks = [p["rank"] for p in standings]
    assert ranks == sorted(ranks)

    points = [p["points"] for p in standings]
    assert points == sorted(points, reverse=True)
