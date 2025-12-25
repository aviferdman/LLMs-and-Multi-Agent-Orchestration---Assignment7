"""Tests for SHARED.contracts.game_result_contracts module."""

import pytest
from SHARED.contracts.game_result_contracts import (
    build_game_over,
    build_match_result_report,
    build_game_error,
)
from SHARED.constants import Field, MessageType


class TestBuildGameOver:
    """Tests for build_game_over function."""

    def test_builds_game_over_message(self):
        """Test game over message is built correctly."""
        msg = build_game_over(
            league_id="league-1",
            round_id=1,
            match_id="match-1",
            referee_id="REF01",
            status="completed",
            winner_player_id="P01",
            drawn_number=5,
            number_parity="odd",
            choices={"P01": "odd", "P02": "even"},
            reason="Player 1 guessed correctly",
        )
        assert "params" in msg
        assert msg["params"][Field.MESSAGE_TYPE] == MessageType.GAME_OVER

    def test_game_over_includes_match_id(self):
        """Test game over includes match ID."""
        msg = build_game_over(
            "league-1", 1, "test-match", "REF01", "completed",
            "P01", 7, "odd", {"P01": "odd", "P02": "even"}, "P01 won"
        )
        assert msg["params"][Field.MATCH_ID] == "test-match"

    def test_game_over_includes_game_result(self):
        """Test game over includes game result details."""
        msg = build_game_over(
            "league-1", 1, "match-1", "REF01", "completed",
            "P02", 4, "even", {"P01": "odd", "P02": "even"}, "P02 won"
        )
        result = msg["params"][Field.GAME_RESULT]
        assert result["status"] == "completed"
        assert result["winner_player_id"] == "P02"
        assert result["drawn_number"] == 4

    def test_game_over_with_tie(self):
        """Test game over with tie result."""
        msg = build_game_over(
            "league-1", 1, "match-1", "REF01", "tie",
            None, 3, "odd", {"P01": "odd", "P02": "odd"}, "Both guessed same"
        )
        result = msg["params"][Field.GAME_RESULT]
        assert result["status"] == "tie"
        assert result["winner_player_id"] is None


class TestBuildMatchResultReport:
    """Tests for build_match_result_report function."""

    def test_builds_match_result_report(self):
        """Test match result report is built correctly."""
        msg = build_match_result_report(
            league_id="league-1",
            round_id=1,
            match_id="match-1",
            referee_id="REF01",
            winner="P01",
            score={"P01": 3, "P02": 1},
            drawn_number=6,
            choices={"P01": "even", "P02": "odd"},
        )
        assert "params" in msg
        assert Field.RESULT in msg["params"]

    def test_match_result_includes_score(self):
        """Test match result includes score."""
        msg = build_match_result_report(
            "league-1", 1, "match-1", "REF01", "P01",
            {"P01": 2, "P02": 0}, 8, {"P01": "even", "P02": "odd"}
        )
        assert msg["params"][Field.RESULT]["score"] == {"P01": 2, "P02": 0}


class TestBuildGameError:
    """Tests for build_game_error function."""

    def test_builds_game_error_message(self):
        """Test game error message is built correctly."""
        msg = build_game_error(
            match_id="match-1",
            referee_id="REF01",
            error_code="TIMEOUT",
            error_description="Player timed out",
            affected_player="P02",
            action_required="forfeit",
        )
        assert "params" in msg
        assert msg["params"][Field.ERROR_CODE] == "TIMEOUT"

    def test_game_error_includes_affected_player(self):
        """Test game error includes affected player."""
        msg = build_game_error(
            "match-1", "REF01", "INVALID_MOVE", "Bad move",
            "P01", "retry"
        )
        assert msg["params"][Field.AFFECTED_PLAYER] == "P01"

    def test_game_error_with_retry_info(self):
        """Test game error with retry information."""
        msg = build_game_error(
            "match-1", "REF01", "CONN_ERROR", "Connection lost",
            "P01", "retry", retry_info={"attempts": 3, "delay": 5}
        )
        assert "params" in msg
