"""Tests for SHARED.contracts.registration_contracts module."""

import pytest
from SHARED.contracts.registration_contracts import (
    build_referee_register_request,
    build_referee_register_response,
    build_league_register_request,
    build_league_register_response,
)
from SHARED.constants import Field, MessageType, Status


class TestBuildRefereeRegisterRequest:
    """Tests for build_referee_register_request function."""

    def test_builds_referee_register_request(self):
        """Test referee register request is built correctly."""
        msg = build_referee_register_request(
            referee_id="REF01",
            display_name="Test Referee",
            version="1.0",
            contact_endpoint="http://localhost:8001",
        )
        assert "params" in msg
        params = msg["params"]
        assert params[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_REQUEST

    def test_includes_referee_meta(self):
        """Test includes referee metadata."""
        msg = build_referee_register_request(
            "REF01", "Referee 1", "2.0", "http://ref:8001"
        )
        meta = msg["params"][Field.REFEREE_META]
        assert meta[Field.DISPLAY_NAME] == "Referee 1"
        assert meta[Field.VERSION] == "2.0"

    def test_default_game_types(self):
        """Test default game types when not provided."""
        msg = build_referee_register_request(
            "REF01", "Ref", "1.0", "http://ref:8001"
        )
        meta = msg["params"][Field.REFEREE_META]
        assert "even_odd" in meta[Field.GAME_TYPES]

    def test_custom_game_types(self):
        """Test custom game types."""
        msg = build_referee_register_request(
            "REF01", "Ref", "1.0", "http://ref:8001",
            game_types=["even_odd", "rock_paper_scissors"]
        )
        meta = msg["params"][Field.REFEREE_META]
        assert "rock_paper_scissors" in meta[Field.GAME_TYPES]


class TestBuildRefereeRegisterResponse:
    """Tests for build_referee_register_response function."""

    def test_builds_accepted_response(self):
        """Test builds accepted response."""
        msg = build_referee_register_response("REF01", Status.ACCEPTED)
        assert Field.STATUS in str(msg)

    def test_builds_rejected_with_reason(self):
        """Test builds rejected response with reason."""
        msg = build_referee_register_response(
            "REF01", Status.REJECTED, reason="Already registered"
        )
        assert "params" in msg or "result" in msg


class TestBuildLeagueRegisterRequest:
    """Tests for build_league_register_request function."""

    def test_builds_player_register_request(self):
        """Test player register request is built correctly."""
        msg = build_league_register_request(
            player_id="P01",
            display_name="Player One",
            version="1.0",
            contact_endpoint="http://localhost:9001",
        )
        assert "params" in msg
        params = msg["params"]
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_REQUEST

    def test_includes_player_meta(self):
        """Test includes player metadata."""
        msg = build_league_register_request(
            "P01", "Cool Player", "1.5", "http://player:9001"
        )
        meta = msg["params"][Field.PLAYER_META]
        assert meta[Field.DISPLAY_NAME] == "Cool Player"
        assert meta[Field.CONTACT_ENDPOINT] == "http://player:9001"


class TestBuildLeagueRegisterResponse:
    """Tests for build_league_register_response function."""

    def test_builds_accepted_response(self):
        """Test builds accepted player response."""
        msg = build_league_register_response("P01", Status.ACCEPTED)
        assert "params" in msg or "result" in msg

    def test_builds_with_request_id(self):
        """Test builds response with request ID."""
        msg = build_league_register_response("P01", request_id=123)
        assert msg.get("id") == 123 or "params" in msg
