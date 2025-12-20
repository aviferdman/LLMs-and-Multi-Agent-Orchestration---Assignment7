"""Tests for WebSocket live updates."""

import json

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.websocket.events import (
    MatchEndEvent,
    MatchStartEvent,
    PlayerMoveEvent,
    PlayerThinkingEvent,
    RoundResultEvent,
)

client = TestClient(app)

def test_websocket_connection():
    """Test WebSocket connection establishment."""
    with client.websocket_connect("/api/v1/ws/live") as websocket:
        assert websocket is not None

def test_websocket_ping_pong():
    """Test WebSocket ping/pong functionality."""
    with client.websocket_connect("/api/v1/ws/live") as websocket:
        websocket.send_json({"action": "ping"})
        data = websocket.receive_json()

        assert data["event_type"] == "pong"

def test_websocket_subscribe_to_match():
    """Test subscribing to a specific match."""
    with client.websocket_connect("/api/v1/ws/live") as websocket:
        websocket.send_json({"action": "subscribe", "match_id": "match_001"})
        data = websocket.receive_json()

        assert data["event_type"] == "subscribed"
        assert data["match_id"] == "match_001"

def test_websocket_unsubscribe_from_match():
    """Test unsubscribing from a match."""
    with client.websocket_connect("/api/v1/ws/live") as websocket:
        websocket.send_json({"action": "subscribe", "match_id": "match_001"})
        websocket.receive_json()

        websocket.send_json({"action": "unsubscribe", "match_id": "match_001"})

def test_websocket_invalid_json():
    """Test WebSocket handles invalid JSON gracefully."""
    with client.websocket_connect("/api/v1/ws/live") as websocket:
        websocket.send_text("invalid json{")
        data = websocket.receive_json()

        assert data["event_type"] == "error"
        assert "Invalid JSON" in data["message"]

def test_match_start_event_structure():
    """Test MatchStartEvent has correct structure."""
    event = MatchStartEvent(
        match_id="match_001", player_a_id="P01", player_b_id="P02"
    )

    event_dict = event.to_dict()
    assert event_dict["event_type"] == "match_start"
    assert event_dict["match_id"] == "match_001"
    assert event_dict["player_a_id"] == "P01"
    assert event_dict["player_b_id"] == "P02"
    assert "timestamp" in event_dict

def test_player_thinking_event_structure():
    """Test PlayerThinkingEvent has correct structure."""
    event = PlayerThinkingEvent(match_id="match_001", player_id="P01", round_num=1)

    event_dict = event.to_dict()
    assert event_dict["event_type"] == "player_thinking"
    assert event_dict["match_id"] == "match_001"
    assert event_dict["player_id"] == "P01"
    assert event_dict["round"] == 1

def test_player_move_event_structure():
    """Test PlayerMoveEvent has correct structure."""
    event = PlayerMoveEvent(
        match_id="match_001", player_id="P01", round_num=1, move="even"
    )

    event_dict = event.to_dict()
    assert event_dict["event_type"] == "player_move"
    assert event_dict["match_id"] == "match_001"
    assert event_dict["player_id"] == "P01"
    assert event_dict["move"] == "even"

def test_round_result_event_structure():
    """Test RoundResultEvent has correct structure."""
    event = RoundResultEvent(
        match_id="match_001",
        round_num=1,
        drawn_number=5,
        player_a_choice="odd",
        player_b_choice="even",
        winner="P01",
    )

    event_dict = event.to_dict()
    assert event_dict["event_type"] == "round_result"
    assert event_dict["round"] == 1
    assert event_dict["drawn_number"] == 5
    assert event_dict["winner"] == "P01"

def test_match_end_event_structure():
    """Test MatchEndEvent has correct structure."""
    event = MatchEndEvent(
        match_id="match_001", winner="P01", final_score={"P01": 2, "P02": 1}
    )

    event_dict = event.to_dict()
    assert event_dict["event_type"] == "match_end"
    assert event_dict["match_id"] == "match_001"
    assert event_dict["winner"] == "P01"
    assert event_dict["final_score"] == {"P01": 2, "P02": 1}
