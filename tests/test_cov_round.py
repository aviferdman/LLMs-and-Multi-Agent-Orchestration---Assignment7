"""Tests for SHARED.contracts.round_contracts module."""

import pytest
from SHARED.contracts.round_contracts import (
    build_round_announcement,
    build_round_completed,
)
from SHARED.constants import Field, MessageType


class TestBuildRoundAnnouncement:
    """Tests for build_round_announcement function."""

    def test_builds_round_announcement(self):
        """Test round announcement is built correctly."""
        matches = [{"match_id": "M1", "player_a": "P01", "player_b": "P02"}]
        msg = build_round_announcement(
            league_id="league-1", round_id=1, matches=matches
        )
        assert "params" in msg
        params = msg["params"]
        assert params[Field.MESSAGE_TYPE] == MessageType.ROUND_ANNOUNCEMENT

    def test_includes_league_and_round_id(self):
        """Test includes league and round IDs."""
        msg = build_round_announcement("test-league", 3, [])
        params = msg["params"]
        assert params[Field.LEAGUE_ID] == "test-league"
        assert params[Field.ROUND_ID] == 3

    def test_includes_matches_list(self):
        """Test includes matches list."""
        matches = [
            {"match_id": "M1", "player_a": "P01", "player_b": "P02"},
            {"match_id": "M2", "player_a": "P03", "player_b": "P04"},
        ]
        msg = build_round_announcement("league-1", 1, matches)
        assert len(msg["params"][Field.MATCHES]) == 2

    def test_with_conversation_id(self):
        """Test with custom conversation ID."""
        msg = build_round_announcement(
            "league-1", 1, [], conversation_id="round-conv-123"
        )
        assert msg["params"][Field.CONVERSATION_ID] == "round-conv-123"


class TestBuildRoundCompleted:
    """Tests for build_round_completed function."""

    def test_builds_round_completed(self):
        """Test round completed is built correctly."""
        summary = {"P01": 3, "P02": 1, "P03": 2, "P04": 2}
        msg = build_round_completed(
            league_id="league-1",
            round_id=1,
            matches_completed=2,
            summary=summary,
        )
        assert "params" in msg
        params = msg["params"]
        assert params[Field.MESSAGE_TYPE] == MessageType.ROUND_COMPLETED

    def test_includes_matches_completed_count(self):
        """Test includes matches completed count."""
        msg = build_round_completed("league-1", 1, 5, {})
        assert msg["params"][Field.MATCHES_COMPLETED] == 5

    def test_includes_summary(self):
        """Test includes summary dictionary."""
        summary = {"P01": 10, "P02": 8}
        msg = build_round_completed("league-1", 2, 1, summary)
        assert msg["params"][Field.SUMMARY] == summary

    def test_includes_next_round_id(self):
        """Test includes next round ID when provided."""
        msg = build_round_completed(
            "league-1", 1, 2, {}, next_round_id=2
        )
        assert msg["params"][Field.NEXT_ROUND_ID] == 2

    def test_no_next_round_for_final(self):
        """Test no next round ID for final round."""
        msg = build_round_completed("league-1", 5, 1, {})
        assert Field.NEXT_ROUND_ID not in msg["params"]
