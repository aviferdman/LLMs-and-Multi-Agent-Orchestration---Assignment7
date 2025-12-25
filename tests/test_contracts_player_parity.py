"""Player contract compliance tests - CHOOSE_PARITY_RESPONSE.

Tests CHOOSE_PARITY_RESPONSE message contract.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, ParityChoice
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.player_contracts import build_choose_parity_response
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request."""
    return extract_jsonrpc_params(msg)


class TestParityChoiceContract:
    """Test CHOOSE_PARITY_RESPONSE contract."""

    def test_parity_choice_structure(self):
        """CHOOSE_PARITY_RESPONSE must have all required fields."""
        msg = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.EVEN, conversation_id="conv-123",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_RESPONSE
        assert params[Field.PARITY_CHOICE] == ParityChoice.EVEN

    def test_parity_choice_even(self):
        """CHOOSE_PARITY_RESPONSE accepts EVEN choice."""
        msg = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.EVEN, conversation_id="conv-123",
        )
        params = get_params(msg)
        assert params[Field.PARITY_CHOICE] == ParityChoice.EVEN

    def test_parity_choice_odd(self):
        """CHOOSE_PARITY_RESPONSE accepts ODD choice."""
        msg = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.ODD, conversation_id="conv-123",
        )
        params = get_params(msg)
        assert params[Field.PARITY_CHOICE] == ParityChoice.ODD

    def test_parity_choice_is_valid_base_message(self):
        """CHOOSE_PARITY_RESPONSE params must pass base message validation."""
        msg = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.EVEN, conversation_id="conv-123",
        )
        params = get_params(msg)
        assert validate_base_message(params) is True

    def test_parity_choice_timestamp_is_utc(self):
        """CHOOSE_PARITY_RESPONSE timestamp must end with Z (UTC)."""
        msg = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.EVEN, conversation_id="conv-123",
        )
        params = get_params(msg)
        assert params[Field.TIMESTAMP].endswith("Z")


class TestValidChoiceValues:
    """Test valid choice values for players."""

    def test_valid_choices_are_lowercase(self):
        """Valid choices must be lowercase strings per spec."""
        assert ParityChoice.EVEN == "even"
        assert ParityChoice.ODD == "odd"

    def test_choice_validation_logic(self):
        """Simulate choice validation logic."""
        valid_choices = [ParityChoice.EVEN.lower(), ParityChoice.ODD.lower()]
        assert "even" in valid_choices
        assert "odd" in valid_choices
        assert "maybe" not in valid_choices


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
