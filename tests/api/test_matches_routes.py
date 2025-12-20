"""Tests for matches API routes."""

import json
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

@pytest.fixture
def setup_match_data(tmp_path, monkeypatch):
    """Setup test match data."""
    test_data_dir = tmp_path / "data"
    test_data_dir.mkdir()
    (test_data_dir / "matches").mkdir()

    monkeypatch.setenv("SHARED_DATA_DIR", str(test_data_dir))

    match_file = test_data_dir / "matches" / "match_001.json"
    match_data = {
        "match_id": "match_001",
        "player_a_id": "P01",
        "player_b_id": "P02",
        "referee_id": "REF01",
        "status": "completed",
        "winner": "P01",
        "score": {"P01": 2, "P02": 1},
        "rounds": 3,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    match_file.write_text(json.dumps(match_data))

    match_file2 = test_data_dir / "matches" / "match_002.json"
    match_data2 = {
        "match_id": "match_002",
        "player_a_id": "P03",
        "player_b_id": "P04",
        "referee_id": "REF02",
        "status": "in_progress",
        "score": {"P03": 1, "P04": 1},
        "rounds": 2,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    match_file2.write_text(json.dumps(match_data2))

    yield test_data_dir

def test_list_matches_success(setup_match_data):
    """Test GET /api/v1/matches returns match list."""
    response = client.get("/api/v1/matches")

    assert response.status_code == 200
    data = response.json()
    assert "matches" in data
    assert isinstance(data["matches"], list)
    assert len(data["matches"]) >= 0

def test_list_matches_pagination():
    """Test GET /api/v1/matches with pagination."""
    response = client.get("/api/v1/matches?skip=0&limit=10")

    assert response.status_code == 200
    data = response.json()
    assert "matches" in data

def test_get_match_by_id_success(setup_match_data):
    """Test GET /api/v1/matches/{match_id} returns match details."""
    response = client.get("/api/v1/matches/match_001")

    assert response.status_code == 200
    data = response.json()
    assert data["match_id"] == "match_001"
    assert "player_a_id" in data
    assert "player_b_id" in data
    assert "status" in data

def test_get_match_not_found():
    """Test GET /api/v1/matches/{match_id} with invalid ID."""
    response = client.get("/api/v1/matches/invalid_match")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_list_matches_filter_by_status(setup_match_data):
    """Test filtering matches by status."""
    response = client.get("/api/v1/matches?status=completed")

    assert response.status_code == 200
    data = response.json()
    assert "matches" in data
