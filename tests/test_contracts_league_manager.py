"""League Manager contract compliance tests.

Tests all League Manager message contracts as defined in
doc/protocol/v2/LEAGUE_MANAGER.md
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
    build_run_match_ack,
    build_start_league,
)
from SHARED.contracts.round_lifecycle_contracts import (
    build_league_completed,
    build_league_error,
    build_league_standings_update,
    build_round_announcement,
    build_round_completed,
)


class TestRefereeRegistrationContract:
    """Test REFEREE_REGISTER_REQUEST/RESPONSE contracts."""

    def test_referee_register_request_structure(self):
        """REFEREE_REGISTER_REQUEST must have required fields."""
        msg = build_referee_register_request("REF01", "http://localhost:8001/mcp")

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_REQUEST
        assert msg[Field.REFEREE_ID] == "REF01"
        assert msg[Field.ENDPOINT] == "http://localhost:8001/mcp"

    def test_referee_register_response_structure(self):
        """REFEREE_REGISTER_RESPONSE must have required fields."""
        msg = build_referee_register_response("REF01", "auth_token_123")

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_RESPONSE
        assert msg[Field.REFEREE_ID] == "REF01"
        assert msg[Field.AUTH_TOKEN] == "auth_token_123"
        assert msg[Field.STATUS] == Status.REGISTERED

    def test_referee_register_response_custom_status(self):
        """REFEREE_REGISTER_RESPONSE allows custom status."""
        msg = build_referee_register_response("REF01", "token", status=Status.ERROR)
        assert msg[Field.STATUS] == Status.ERROR


class TestPlayerRegistrationContract:
    """Test LEAGUE_REGISTER_REQUEST/RESPONSE contracts."""

    def test_league_register_request_structure(self):
        """LEAGUE_REGISTER_REQUEST must have required fields."""
        msg = build_league_register_request("P01", "http://localhost:8101/mcp")

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_REQUEST
        assert msg[Field.PLAYER_ID] == "P01"
        assert msg[Field.ENDPOINT] == "http://localhost:8101/mcp"

    def test_league_register_response_structure(self):
        """LEAGUE_REGISTER_RESPONSE must have required fields."""
        msg = build_league_register_response("P01", "league_2025", "auth_token_456")

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_RESPONSE
        assert msg[Field.PLAYER_ID] == "P01"
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.AUTH_TOKEN] == "auth_token_456"
        assert msg[Field.STATUS] == Status.REGISTERED


class TestLeagueControlContract:
    """Test START_LEAGUE and LEAGUE_STATUS contracts."""

    def test_start_league_structure(self):
        """START_LEAGUE must have required fields."""
        msg = build_start_league("league_2025", "launcher")

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.START_LEAGUE
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.SENDER] == "launcher"

    def test_league_status_structure(self):
        """LEAGUE_STATUS must have required fields."""
        msg = build_league_status(
            league_id="league_2025",
            status="running",
            current_round=1,
            total_rounds=3,
            matches_completed=2,
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.LEAGUE_STATUS
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.STATUS] == "running"
        assert msg["current_round"] == 1
        assert msg["total_rounds"] == 3
        assert msg["matches_completed"] == 2


class TestRunMatchContract:
    """Test RUN_MATCH and RUN_MATCH_ACK contracts."""

    def test_run_match_structure(self):
        """RUN_MATCH must have all required fields."""
        msg = build_run_match(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_a="P01",
            player_a_endpoint="http://localhost:8101/mcp",
            player_b="P02",
            player_b_endpoint="http://localhost:8102/mcp",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.RUN_MATCH
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.REFEREE_ID] == "REF01"
        assert msg[Field.PLAYER_A] == "P01"
        assert msg["player_a_endpoint"] == "http://localhost:8101/mcp"
        assert msg[Field.PLAYER_B] == "P02"
        assert msg["player_b_endpoint"] == "http://localhost:8102/mcp"

    def test_run_match_ack_structure(self):
        """RUN_MATCH_ACK must have required fields."""
        msg = build_run_match_ack("R1M1")

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.RUN_MATCH_ACK
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.STATUS] == Status.ACKNOWLEDGED


class TestMatchResultAckContract:
    """Test MATCH_RESULT_ACK contract."""

    def test_match_result_ack_structure(self):
        """MATCH_RESULT_ACK must have required fields."""
        msg = build_match_result_ack("R1M1")

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_ACK
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.STATUS] == Status.RECORDED


class TestRoundAnnouncementContract:
    """Test ROUND_ANNOUNCEMENT contract."""

    def test_round_announcement_structure(self):
        """ROUND_ANNOUNCEMENT must have required fields."""
        matches = [
            {"match_id": "R1M1", "player_a": "P01", "player_b": "P02", "referee_id": "REF01"},
            {"match_id": "R1M2", "player_a": "P03", "player_b": "P04", "referee_id": "REF02"},
        ]
        msg = build_round_announcement("league_2025", round_id=1, total_rounds=3, matches=matches)

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.ROUND_ANNOUNCEMENT
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg["total_rounds"] == 3
        assert len(msg["matches"]) == 2


class TestRoundCompletedContract:
    """Test ROUND_COMPLETED contract."""

    def test_round_completed_structure(self):
        """ROUND_COMPLETED must have required fields."""
        results = [
            {"match_id": "R1M1", "winner": "P01"},
            {"match_id": "R1M2", "winner": "P03"},
        ]
        msg = build_round_completed("league_2025", round_id=1, results=results)

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.ROUND_COMPLETED
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert len(msg["results"]) == 2


class TestLeagueStandingsUpdateContract:
    """Test LEAGUE_STANDINGS_UPDATE contract."""

    def test_league_standings_update_structure(self):
        """LEAGUE_STANDINGS_UPDATE must have required fields."""
        standings = [
            {"rank": 1, "player_id": "P01", "points": 3, "wins": 1, "losses": 0, "draws": 0},
            {"rank": 2, "player_id": "P02", "points": 0, "wins": 0, "losses": 1, "draws": 0},
        ]
        msg = build_league_standings_update("league_2025", round_id=1, standings=standings)

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.LEAGUE_STANDINGS_UPDATE
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert len(msg["standings"]) == 2


class TestLeagueCompletedContract:
    """Test LEAGUE_COMPLETED contract."""

    def test_league_completed_structure(self):
        """LEAGUE_COMPLETED must have required fields."""
        standings = [{"rank": 1, "player_id": "P01", "points": 9}]
        msg = build_league_completed("league_2025", final_standings=standings, total_matches=6)

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.LEAGUE_COMPLETED
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg["total_matches"] == 6
        assert len(msg["final_standings"]) == 1


class TestLeagueErrorContract:
    """Test LEAGUE_ERROR contract."""

    def test_league_error_structure(self):
        """LEAGUE_ERROR must have required fields."""
        msg = build_league_error(
            league_id="league_2025",
            error_code="E005",
            error_message="Player not registered",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.LEAGUE_ERROR
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg["error_code"] == "E005"
        assert msg["error_message"] == "Player not registered"

    def test_league_error_with_details(self):
        """LEAGUE_ERROR can include optional details."""
        msg = build_league_error(
            league_id="league_2025",
            error_code="E005",
            error_message="Player not registered",
            details={"player_id": "P99"},
        )

        assert msg["details"]["player_id"] == "P99"
