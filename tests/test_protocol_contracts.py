"""Protocol contract compliance tests.

Tests that all agents in the system comply with the protocol contracts
as defined in doc/protocol/v2/.

Tests are organized by agent type:
- League Manager contracts
- Referee contracts
- Player contracts
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.contracts.base_contract import create_base_message, validate_base_message
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
from SHARED.contracts.player_contracts import build_game_join_ack, build_parity_choice
from SHARED.contracts.referee_contracts import (
    build_choose_parity_call,
    build_game_error,
    build_game_invitation,
    build_game_over,
    build_match_result_report,
)
from SHARED.contracts.round_lifecycle_contracts import (
    build_league_completed,
    build_league_error,
    build_league_standings_update,
    build_round_announcement,
    build_round_completed,
)


class TestProtocolVersion:
    """Test protocol version compliance."""

    def test_protocol_version_is_v2(self):
        """Protocol version must be league.v2."""
        assert PROTOCOL_VERSION == "league.v2"

    def test_all_messages_use_correct_protocol(self):
        """All message builders must use correct protocol version."""
        # Registration messages
        msg = build_referee_register_request("REF01", "http://localhost:8001/mcp")
        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION

        msg = build_league_register_request("P01", "http://localhost:8101/mcp")
        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION


class TestBaseMessageContract:
    """Test base message structure compliance."""

    def test_create_base_message_has_all_required_fields(self):
        """Base message must include all required fields."""
        msg = create_base_message(
            message_type="TEST_MESSAGE",
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            sender="test_sender",
        )

        required_fields = [
            Field.PROTOCOL,
            Field.MESSAGE_TYPE,
            Field.LEAGUE_ID,
            Field.ROUND_ID,
            Field.MATCH_ID,
            Field.CONVERSATION_ID,
            Field.SENDER,
            Field.TIMESTAMP,
        ]

        for field in required_fields:
            assert field in msg, f"Missing required field: {field}"

    def test_base_message_timestamp_ends_with_z(self):
        """Timestamp must be UTC (end with Z)."""
        msg = create_base_message(
            message_type="TEST",
            league_id="league",
            round_id=1,
            match_id="R1M1",
            sender="sender",
        )
        assert msg[Field.TIMESTAMP].endswith("Z")

    def test_validate_base_message_accepts_valid(self):
        """Validator accepts valid messages."""
        msg = create_base_message(
            message_type="TEST",
            league_id="league",
            round_id=1,
            match_id="R1M1",
            sender="sender",
        )
        assert validate_base_message(msg) is True

    def test_validate_base_message_rejects_wrong_protocol(self):
        """Validator rejects wrong protocol version."""
        msg = create_base_message(
            message_type="TEST",
            league_id="league",
            round_id=1,
            match_id="R1M1",
            sender="sender",
        )
        msg[Field.PROTOCOL] = "league.v1"  # Wrong version
        assert validate_base_message(msg) is False

    def test_validate_base_message_rejects_non_utc_timestamp(self):
        """Validator rejects non-UTC timestamps."""
        msg = create_base_message(
            message_type="TEST",
            league_id="league",
            round_id=1,
            match_id="R1M1",
            sender="sender",
        )
        msg[Field.TIMESTAMP] = "2025-12-20T10:00:00+02:00"  # Not UTC
        assert validate_base_message(msg) is False
