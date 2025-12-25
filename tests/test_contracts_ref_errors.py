"""Referee contract compliance tests - GAME_ERROR and Value Constants.

Tests contracts as defined in doc/protocol/v2/CONTRACTS.md.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, ParityChoice, Winner
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.referee_contracts import build_game_error
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request."""
    return extract_jsonrpc_params(msg)


class TestGameErrorContract:
    """Test GAME_ERROR contract."""

    def test_game_error_structure(self):
        """GAME_ERROR must have all required fields."""
        msg = build_game_error(
            match_id="R1M1", referee_id="REF01", error_code="E001",
            error_description="Response timeout", affected_player="P01",
            action_required="CHOOSE_PARITY_RESPONSE",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_ERROR
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.ERROR_CODE] == "E001"
        assert params[Field.ERROR_DESCRIPTION] == "Response timeout"
        assert params[Field.AFFECTED_PLAYER] == "P01"

    def test_game_error_with_details(self):
        """GAME_ERROR can include optional retry info."""
        msg = build_game_error(
            match_id="R1M1", referee_id="REF01", error_code="E001",
            error_description="Response timeout", affected_player="P01",
            action_required="CHOOSE_PARITY_RESPONSE",
            retry_info={"can_retry": False, "reason": "timeout exceeded"},
        )
        params = get_params(msg)
        assert params[Field.RETRY_INFO]["can_retry"] is False
        assert params[Field.RETRY_INFO]["reason"] == "timeout exceeded"

    def test_game_error_is_valid_base_message(self):
        """GAME_ERROR params must pass base message validation."""
        msg = build_game_error(
            match_id="R1M1", referee_id="REF01", error_code="E001",
            error_description="Timeout", affected_player="P01",
            action_required="CHOOSE_PARITY_RESPONSE",
        )
        params = get_params(msg)
        assert validate_base_message(params) is True


class TestWinnerValues:
    """Test valid winner values in referee messages."""

    def test_winner_constants_defined(self):
        """Winner constants must be defined."""
        assert Winner.PLAYER_A == "PLAYER_A"
        assert Winner.PLAYER_B == "PLAYER_B"
        assert Winner.DRAW == "DRAW"


class TestParityChoiceValues:
    """Test valid parity choice values."""

    def test_parity_choice_constants_defined(self):
        """Parity choice constants must be defined per spec (lowercase)."""
        assert ParityChoice.EVEN == "even"
        assert ParityChoice.ODD == "odd"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
