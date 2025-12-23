"""Tests for games API routes."""

import sys
from pathlib import Path

# Add project root to path before importing api modules
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_list_games_success():
    """Test GET /api/v1/games returns game list."""
    response = client.get("/api/v1/games")

    assert response.status_code == 200
    data = response.json()
    assert "games" in data
    assert isinstance(data["games"], list)
    assert len(data["games"]) > 0

def test_list_games_has_even_odd():
    """Test that even_odd game is in the list."""
    response = client.get("/api/v1/games")

    assert response.status_code == 200
    data = response.json()
    games = data["games"]
    game_ids = [g["game_id"] for g in games]
    assert "even_odd" in game_ids

def test_get_game_by_id_success():
    """Test GET /api/v1/games/{game_id} returns game details."""
    response = client.get("/api/v1/games/even_odd")

    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == "even_odd"
    assert "name" in data
    assert "description" in data
    assert "min_players" in data
    assert "max_players" in data
    assert "rules" in data

def test_get_game_not_found():
    """Test GET /api/v1/games/{game_id} with invalid ID."""
    response = client.get("/api/v1/games/invalid_game")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_game_has_valid_player_range():
    """Test that game has valid min/max player range."""
    response = client.get("/api/v1/games/even_odd")

    assert response.status_code == 200
    data = response.json()
    assert data["min_players"] >= 2
    assert data["max_players"] >= data["min_players"]

def test_game_has_rules():
    """Test that game has rules defined."""
    response = client.get("/api/v1/games/even_odd")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["rules"], list)
    assert len(data["rules"]) > 0
