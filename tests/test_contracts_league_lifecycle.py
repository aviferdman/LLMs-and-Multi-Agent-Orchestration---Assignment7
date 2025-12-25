"""League Manager lifecycle contract compliance tests.

Tests round and league lifecycle message contracts as defined in
doc/protocol/v2/CONTRACTS.md
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.contracts.round_lifecycle_contracts import (
    build_league_completed,
    build_league_error,
    build_league_standings_update,
    build_round_announcement,
    build_round_completed,
)
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request or result from response."""
    if "params" in msg:
        return msg["params"]
    if "result" in msg:
        return msg["result"]
    return msg


class TestRoundAnnouncementContract:
    """Test ROUND_ANNOUNCEMENT contract."""

    def test_round_announcement_structure(self):
        """ROUND_ANNOUNCEMENT must have required fields."""
        matches = [
            {"match_id": "R1M1", "player_A_id": "P01", "player_B_id": "P02", "game_type": "even_odd"},
        ]
        msg = build_round_announcement(league_id="league_2025", round_id=1, matches=matches)
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.ROUND_ANNOUNCEMENT
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert params[Field.ROUND_ID] == 1


class TestRoundCompletedContract:
    """Test ROUND_COMPLETED contract."""

    def test_round_completed_structure(self):
        """ROUND_COMPLETED must have required fields."""
        summary = {"total_matches": 2, "wins": 1, "draws": 1, "technical_losses": 0}
        msg = build_round_completed(
            league_id="league_2025", round_id=1, matches_completed=2,
            summary=summary, next_round_id=2,
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.ROUND_COMPLETED
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert params[Field.ROUND_ID] == 1


class TestLeagueStandingsUpdateContract:
    """Test LEAGUE_STANDINGS_UPDATE contract."""

    def test_league_standings_update_structure(self):
        """LEAGUE_STANDINGS_UPDATE must have required fields."""
        standings = [{"player_id": "P01", "wins": 1, "losses": 0, "draws": 0, "points": 3}]
        msg = build_league_standings_update(league_id="league_2025", round_id=1, standings=standings)
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_STANDINGS_UPDATE
        assert params[Field.LEAGUE_ID] == "league_2025"


class TestLeagueCompletedContract:
    """Test LEAGUE_COMPLETED contract."""

    def test_league_completed_structure(self):
        """LEAGUE_COMPLETED must have required fields."""
        standings = [{"player_id": "P01", "wins": 3, "points": 9}]
        champion = {"player_id": "P01", "total_wins": 3, "total_points": 9}
        msg = build_league_completed(
            league_id="league_2025", total_rounds=3, total_matches=6,
            final_standings=standings, champion=champion,
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_COMPLETED
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert Field.CHAMPION in params


class TestLeagueErrorContract:
    """Test LEAGUE_ERROR contract."""

    def test_league_error_structure(self):
        """LEAGUE_ERROR must have required fields."""
        msg = build_league_error(error_code="E005", error_description="Player not registered")
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_ERROR
        assert params[Field.ERROR_CODE] == "E005"
        assert params[Field.ERROR_DESCRIPTION] == "Player not registered"

    def test_league_error_with_details(self):
        """LEAGUE_ERROR can include optional details."""
        msg = build_league_error(
            error_code="E005", error_description="Player not registered",
            context={"player_id": "P99"},
        )
        params = get_params(msg)
        assert params[Field.CONTEXT]["player_id"] == "P99"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
