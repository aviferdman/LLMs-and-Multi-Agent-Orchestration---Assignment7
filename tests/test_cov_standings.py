"""Tests for SHARED.contracts.standings_contracts module."""

import pytest
from SHARED.contracts.standings_contracts import (
    build_league_completed,
    build_league_standings_update,
    build_league_error,
)
from SHARED.constants import Field, MessageType


class TestBuildLeagueCompleted:
    """Tests for build_league_completed function."""

    def test_builds_league_completed(self):
        """Test league completed message is built correctly."""
        champion = {"player_id": "P01", "wins": 10, "losses": 2}
        standings = [
            {"player_id": "P01", "points": 30, "rank": 1},
            {"player_id": "P02", "points": 25, "rank": 2},
        ]
        msg = build_league_completed(
            league_id="league-1",
            total_rounds=5,
            total_matches=10,
            champion=champion,
            final_standings=standings,
        )
        assert "params" in msg
        params = msg["params"]
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_COMPLETED

    def test_includes_champion_info(self):
        """Test includes champion information."""
        champion = {"player_id": "P02", "wins": 15}
        msg = build_league_completed("league-1", 5, 10, champion, [])
        assert msg["params"][Field.CHAMPION] == champion

    def test_includes_total_counts(self):
        """Test includes total rounds and matches."""
        msg = build_league_completed("league-1", 8, 20, {}, [])
        assert msg["params"][Field.TOTAL_ROUNDS] == 8
        assert msg["params"][Field.TOTAL_MATCHES] == 20


class TestBuildLeagueStandingsUpdate:
    """Tests for build_league_standings_update function."""

    def test_builds_standings_update(self):
        """Test standings update is built correctly."""
        standings = [
            {"player_id": "P01", "points": 6, "rank": 1},
            {"player_id": "P02", "points": 3, "rank": 2},
        ]
        msg = build_league_standings_update("league-1", 2, standings)
        assert "params" in msg
        params = msg["params"]
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_STANDINGS_UPDATE

    def test_includes_round_id(self):
        """Test includes round ID."""
        msg = build_league_standings_update("league-1", 4, [])
        assert msg["params"][Field.ROUND_ID] == 4

    def test_includes_standings_list(self):
        """Test includes standings list."""
        standings = [{"player_id": "P01", "points": 9}]
        msg = build_league_standings_update("league-1", 1, standings)
        assert msg["params"][Field.STANDINGS] == standings


class TestBuildLeagueError:
    """Tests for build_league_error function."""

    def test_builds_league_error(self):
        """Test league error is built correctly."""
        msg = build_league_error(
            error_code="INVALID_PLAYER",
            error_description="Player not registered",
        )
        assert "params" in msg
        params = msg["params"]
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_ERROR

    def test_includes_error_details(self):
        """Test includes error code and description."""
        msg = build_league_error("TIMEOUT", "Match timed out")
        params = msg["params"]
        assert params[Field.ERROR_CODE] == "TIMEOUT"
        assert params[Field.ERROR_DESCRIPTION] == "Match timed out"

    def test_includes_original_message_type(self):
        """Test includes original message type when provided."""
        msg = build_league_error(
            "ERROR", "Desc",
            original_message_type="PLAYER_REGISTER_REQUEST"
        )
        assert Field.ORIGINAL_MESSAGE_TYPE in msg["params"]

    def test_includes_context(self):
        """Test includes context when provided."""
        context = {"player_id": "P01", "attempt": 3}
        msg = build_league_error("ERROR", "Desc", context=context)
        assert msg["params"][Field.CONTEXT] == context
