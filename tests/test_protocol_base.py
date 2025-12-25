"""Protocol contract compliance tests - Base and Protocol Version.

Tests base message structure and protocol version compliance.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field
from SHARED.contracts.base_contract import create_game_message, validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.league_manager_contracts import (
    build_league_register_request,
    build_referee_register_request,
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
        msg = build_referee_register_request(
            referee_id="REF01", display_name="Test Referee",
            version="1.0.0", contact_endpoint="http://localhost:8001/mcp",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        assert get_params(msg)[Field.PROTOCOL] == PROTOCOL_VERSION

        msg = build_league_register_request(
            player_id="P01", display_name="Test Player",
            version="1.0.0", contact_endpoint="http://localhost:8101/mcp",
        )
        assert get_params(msg)[Field.PROTOCOL] == PROTOCOL_VERSION


class TestBaseMessageContract:
    """Test base message structure compliance."""

    def test_create_game_message_has_all_required_fields(self):
        """Game message must include all required fields."""
        msg = create_game_message(
            message_type="TEST_MESSAGE", sender_type="referee",
            sender_id="REF01", league_id="league_2025", round_id=1, match_id="R1M1",
        )
        required_fields = [
            Field.PROTOCOL, Field.MESSAGE_TYPE, Field.MATCH_ID,
            Field.CONVERSATION_ID, Field.SENDER, Field.TIMESTAMP,
        ]
        for field in required_fields:
            assert field in msg, f"Missing required field: {field}"

    def test_base_message_timestamp_ends_with_z(self):
        """Timestamp must be UTC (end with Z)."""
        msg = create_game_message(
            message_type="TEST", sender_type="referee",
            sender_id="REF01", league_id="league_2025", round_id=1, match_id="R1M1",
        )
        assert msg[Field.TIMESTAMP].endswith("Z")

    def test_validate_base_message_accepts_valid(self):
        """Validator accepts valid messages."""
        msg = create_game_message(
            message_type="TEST", sender_type="referee",
            sender_id="REF01", league_id="league_2025", round_id=1, match_id="R1M1",
        )
        assert validate_base_message(msg) is True

    def test_validate_base_message_rejects_wrong_protocol(self):
        """Validator rejects wrong protocol version."""
        msg = create_game_message(
            message_type="TEST", sender_type="referee",
            sender_id="REF01", league_id="league_2025", round_id=1, match_id="R1M1",
        )
        msg[Field.PROTOCOL] = "league.v1"
        assert validate_base_message(msg) is False

    def test_validate_base_message_rejects_non_utc_timestamp(self):
        """Validator rejects non-UTC timestamps."""
        msg = create_game_message(
            message_type="TEST", sender_type="referee",
            sender_id="REF01", league_id="league_2025", round_id=1, match_id="R1M1",
        )
        msg[Field.TIMESTAMP] = "2025-12-20T10:00:00+02:00"
        assert validate_base_message(msg) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
