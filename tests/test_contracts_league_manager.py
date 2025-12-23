"""League Manager contract compliance tests.

Tests all League Manager message contracts as defined in
doc/protocol/v2/CONTRACTS.md
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.contracts.league_manager_contracts import (
    build_league_register_request,
    build_league_register_response,
    build_league_status,
    build_match_result_ack,
    build_referee_register_request,
    build_referee_register_response,
    build_run_match,
)
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


class TestRefereeRegistrationContract:
    """Test REFEREE_REGISTER_REQUEST/RESPONSE contracts."""

    def test_referee_register_request_structure(self):
        """REFEREE_REGISTER_REQUEST must have required fields."""
        msg = build_referee_register_request(
            referee_id="REF01",
            display_name="Test Referee",
            version="1.0.0",
            contact_endpoint="http://localhost:8001/mcp",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        assert "method" in msg and "id" in msg
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_REQUEST
        assert params[Field.SENDER] == "referee:REF01"
        assert Field.REFEREE_META in params

    def test_referee_register_response_structure(self):
        """REFEREE_REGISTER_RESPONSE must have required fields."""
        msg = build_referee_register_response(referee_id="REF01", status=Status.ACCEPTED)
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_RESPONSE
        assert params[Field.REFEREE_ID] == "REF01"
        assert params[Field.STATUS] == Status.ACCEPTED

    def test_referee_register_response_rejected(self):
        """REFEREE_REGISTER_RESPONSE can indicate rejection."""
        msg = build_referee_register_response(
            referee_id="REF01", status=Status.REJECTED, reason="Duplicate referee ID",
        )
        params = get_params(msg)
        assert params[Field.STATUS] == Status.REJECTED


class TestPlayerRegistrationContract:
    """Test LEAGUE_REGISTER_REQUEST/RESPONSE contracts."""

    def test_league_register_request_structure(self):
        """LEAGUE_REGISTER_REQUEST must have required fields."""
        msg = build_league_register_request(
            player_id="P01", display_name="Test Player",
            version="1.0.0", contact_endpoint="http://localhost:8101/mcp",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_REQUEST
        assert params[Field.SENDER] == "player:P01"
        assert Field.PLAYER_META in params

    def test_league_register_response_structure(self):
        """LEAGUE_REGISTER_RESPONSE must have required fields."""
        msg = build_league_register_response(player_id="P01", status=Status.ACCEPTED)
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_RESPONSE
        assert params[Field.PLAYER_ID] == "P01"
        assert params[Field.STATUS] == Status.ACCEPTED


class TestLeagueControlContract:
    """Test LEAGUE_STATUS contract."""

    def test_league_status_structure(self):
        """LEAGUE_STATUS must have required fields."""
        msg = build_league_status(
            league_id="league_2025",
            status="running",
            current_round=1,
            total_rounds=3,
            matches_completed=2,
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
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_a_id="P01",
            player_a_endpoint="http://localhost:8101/mcp",
            player_b_id="P02",
            player_b_endpoint="http://localhost:8102/mcp",
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
