"""League Manager control contract compliance tests.

Tests league status, run match, and match result ack contracts.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.contracts.league_manager_contracts import (
    build_league_status,
    build_match_result_ack,
    build_run_match,
)
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request or result from response."""
    if "params" in msg:
        return msg["params"]
    if "result" in msg:
        return msg["result"]
    return msg


class TestLeagueControlContract:
    """Test LEAGUE_STATUS contract."""

    def test_league_status_structure(self):
        """LEAGUE_STATUS must have required fields."""
        msg = build_league_status(
            league_id="league_2025", status="running",
            current_round=1, total_rounds=3, matches_completed=2,
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_STATUS
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert params[Field.STATUS] == "running"


class TestRunMatchContract:
    """Test RUN_MATCH contract."""

    def test_run_match_structure(self):
        """RUN_MATCH must have all required fields."""
        msg = build_run_match(
            league_id="league_2025", round_id=1, match_id="R1M1",
            player_a_id="P01", player_a_endpoint="http://localhost:8101/mcp",
            player_b_id="P02", player_b_endpoint="http://localhost:8102/mcp",
            game_type="even_odd",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.RUN_MATCH
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert params[Field.ROUND_ID] == 1
        assert params[Field.MATCH_ID] == "R1M1"


class TestMatchResultAckContract:
    """Test MATCH_RESULT_ACK contract."""

    def test_match_result_ack_structure(self):
        """MATCH_RESULT_ACK must have required fields."""
        msg = build_match_result_ack("R1M1")
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_ACK
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.STATUS] == Status.RECORDED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
