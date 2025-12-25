"""Player contract compliance tests - GAME_JOIN_ACK.

Tests GAME_JOIN_ACK message contract.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.player_contracts import build_game_join_ack
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request."""
    return extract_jsonrpc_params(msg)


class TestGameJoinAckContract:
    """Test GAME_JOIN_ACK contract."""

    def test_game_join_ack_structure(self):
        """GAME_JOIN_ACK must have all required fields."""
        msg = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id="conv-123", accept=True,
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_JOIN_ACK
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.ACCEPT] is True

    def test_game_join_ack_preserves_conversation_id(self):
        """GAME_JOIN_ACK must use provided conversation_id."""
        original_conv_id = "880e8400-e29b-41d4-a716-446655440003"
        msg = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id=original_conv_id, accept=True,
        )
        params = get_params(msg)
        assert params[Field.CONVERSATION_ID] == original_conv_id

    def test_game_join_ack_is_valid_base_message(self):
        """GAME_JOIN_ACK params must pass base message validation."""
        msg = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id="conv-123", accept=True,
        )
        params = get_params(msg)
        assert validate_base_message(params) is True

    def test_game_join_ack_timestamp_is_utc(self):
        """GAME_JOIN_ACK timestamp must end with Z (UTC)."""
        msg = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id="conv-123", accept=True,
        )
        params = get_params(msg)
        assert params[Field.TIMESTAMP].endswith("Z")

    def test_game_join_ack_decline(self):
        """GAME_JOIN_ACK can indicate decline."""
        msg = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id="conv-123", accept=False,
        )
        params = get_params(msg)
        assert params[Field.ACCEPT] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
