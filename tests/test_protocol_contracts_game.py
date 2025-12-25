"""Protocol contract compliance tests - Game Messages.

Tests GAME_INVITATION, GAME_JOIN_ACK, and CHOOSE_PARITY messages.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import Field, MessageType
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.player_contracts import build_game_join_ack, build_choose_parity_response
from SHARED.contracts.referee_contracts import (
    build_choose_parity_call,
    build_game_invitation,
)


def get_params(msg):
    """Extract params from JSON-RPC message."""
    return extract_jsonrpc_params(msg)


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


if __name__ == "__main__":
    print("=" * 60)
    print("PROTOCOL CONTRACT COMPLIANCE TESTS - GAME MESSAGES")
    print("=" * 60)

    test_classes = [
        ("TestGameInvitationContract", TestGameInvitationContract),
        ("TestGameJoinAckContract", TestGameJoinAckContract),
        ("TestChooseParityContract", TestChooseParityContract),
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
