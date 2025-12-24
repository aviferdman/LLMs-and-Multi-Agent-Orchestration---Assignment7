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
from SHARED.contracts.base_contract import create_game_message, validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
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
from SHARED.contracts.player_contracts import build_game_join_ack, build_choose_parity_response
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
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC message."""
    return extract_jsonrpc_params(msg)


class TestProtocolVersion:
    """Test protocol version compliance."""

    def test_protocol_version_is_v2(self):
        """Protocol version must be league.v2."""
        assert PROTOCOL_VERSION == "league.v2"

    def test_all_messages_use_correct_protocol(self):
        """All message builders must use correct protocol version."""
        # Registration messages
        msg = build_referee_register_request(
            referee_id="REF01",
            display_name="Test Referee",
            version="1.0.0",
            contact_endpoint="http://localhost:8001/mcp",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        assert get_params(msg)[Field.PROTOCOL] == PROTOCOL_VERSION

        msg = build_league_register_request(
            player_id="P01",
            display_name="Test Player",
            version="1.0.0",
            contact_endpoint="http://localhost:8101/mcp",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        assert get_params(msg)[Field.PROTOCOL] == PROTOCOL_VERSION


class TestBaseMessageContract:
    """Test base message structure compliance."""

    def test_create_game_message_has_all_required_fields(self):
        """Game message must include all required fields."""
        msg = create_game_message(
            message_type="TEST_MESSAGE",
            sender_type="referee",
            sender_id="REF01",
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
        )

        required_fields = [
            Field.PROTOCOL,
            Field.MESSAGE_TYPE,
            Field.MATCH_ID,
            Field.CONVERSATION_ID,
            Field.SENDER,
            Field.TIMESTAMP,
        ]

        for field in required_fields:
            assert field in msg, f"Missing required field: {field}"

    def test_base_message_timestamp_ends_with_z(self):
        """Timestamp must be UTC (end with Z)."""
        msg = create_game_message(
            message_type="TEST",
            sender_type="referee",
            sender_id="REF01",
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
        )
        assert msg[Field.TIMESTAMP].endswith("Z")

    def test_validate_base_message_accepts_valid(self):
        """Validator accepts valid messages."""
        msg = create_game_message(
            message_type="TEST",
            sender_type="referee",
            sender_id="REF01",
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
        )
        assert validate_base_message(msg) is True

    def test_validate_base_message_rejects_wrong_protocol(self):
        """Validator rejects wrong protocol version."""
        msg = create_game_message(
            message_type="TEST",
            sender_type="referee",
            sender_id="REF01",
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
        )
        msg[Field.PROTOCOL] = "league.v1"  # Wrong version
        assert validate_base_message(msg) is False

    def test_validate_base_message_rejects_non_utc_timestamp(self):
        """Validator rejects non-UTC timestamps."""
        msg = create_game_message(
            message_type="TEST",
            sender_type="referee",
            sender_id="REF01",
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
        )
        msg[Field.TIMESTAMP] = "2025-12-20T10:00:00+02:00"  # Not UTC
        assert validate_base_message(msg) is False


class TestGameInvitationContract:
    """Test GAME_INVITATION message compliance."""

    def test_game_invitation_has_required_fields(self):
        """GAME_INVITATION must have all protocol-required fields."""
        msg = build_game_invitation(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            role_in_match="player_a",
            game_type="even_odd",
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
        assert params[Field.OPPONENT_ID] == "P02"
        assert params[Field.ROLE_IN_MATCH] == "player_a"
        assert params[Field.GAME_TYPE] == "even_odd"


class TestGameJoinAckContract:
    """Test GAME_JOIN_ACK message compliance."""

    def test_game_join_ack_has_required_fields(self):
        """GAME_JOIN_ACK must have all protocol-required fields."""
        msg = build_game_join_ack(
            match_id="R1M1",
            player_id="P01",
            conversation_id="conv-123",
            accept=True,
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_JOIN_ACK
        assert params[Field.ACCEPT] is True
        assert Field.ARRIVAL_TIMESTAMP in params


class TestChooseParityContract:
    """Test CHOOSE_PARITY_CALL and CHOOSE_PARITY_RESPONSE message compliance."""

    def test_choose_parity_call_has_required_fields(self):
        """CHOOSE_PARITY_CALL must have all protocol-required fields."""
        msg = build_choose_parity_call(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            player_standings={},
            timeout_seconds=30,
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL
        assert params[Field.PLAYER_ID] == "P01"
        assert Field.DEADLINE in params
        assert Field.CONTEXT in params
        assert params[Field.CONTEXT]["opponent_id"] == "P02"

    def test_choose_parity_response_has_required_fields(self):
        """CHOOSE_PARITY_RESPONSE must have all protocol-required fields."""
        msg = build_choose_parity_response(
            match_id="R1M1",
            player_id="P01",
            parity_choice="EVEN",
            conversation_id="conv-123",
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_RESPONSE
        assert params[Field.PARITY_CHOICE] == "EVEN"


class TestGameOverContract:
    """Test GAME_OVER message compliance."""

    def test_game_over_has_game_result_structure(self):
        """GAME_OVER must have game_result object per protocol."""
        from SHARED.contracts.referee_contracts import build_game_over
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="WIN",
            winner_player_id="P01",
            drawn_number=4,
            number_parity="even",
            choices={"P01": "EVEN", "P02": "ODD"},
            reason="P01 chose correctly",
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        assert Field.GAME_RESULT in params
        assert params[Field.GAME_RESULT]["winner_player_id"] == "P01"


class TestMatchResultReportContract:
    """Test MATCH_RESULT_REPORT message compliance."""

    def test_match_result_report_has_result_structure(self):
        """MATCH_RESULT_REPORT must have result object per protocol."""
        from SHARED.contracts.referee_contracts import build_match_result_report
        msg = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            score={"P01": 1, "P02": 0},
            drawn_number=4,
            choices={"P01": "EVEN", "P02": "ODD"},
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert Field.RESULT in params
        assert params[Field.RESULT]["winner"] == "P01"


if __name__ == "__main__":
    print("=" * 60)
    print("PROTOCOL CONTRACT COMPLIANCE TESTS")
    print("=" * 60)

    test_classes = [
        ("TestProtocolVersion", TestProtocolVersion),
        ("TestBaseMessageContract", TestBaseMessageContract),
        ("TestGameInvitationContract", TestGameInvitationContract),
        ("TestGameJoinAckContract", TestGameJoinAckContract),
        ("TestChooseParityContract", TestChooseParityContract),
        ("TestGameOverContract", TestGameOverContract),
        ("TestMatchResultReportContract", TestMatchResultReportContract),
    ]

    passed = 0
    failed = 0

    for class_name, test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    print(f"Testing {class_name}.{method_name}...", end=" ")
                    getattr(instance, method_name)()
                    print("✓")
                    passed += 1
                except Exception as e:
                    print(f"✗ {e}")
                    failed += 1

    print()
    print("=" * 60)
    print(f"SUMMARY: {passed}/{passed + failed} tests passed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ ALL PROTOCOL CONTRACT TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")