"""End-to-end protocol compliance tests - Game Flow.

Validates parity choice and game resolution message flows.
"""

import pytest

from SHARED.constants import Field, MessageType
from SHARED.contracts import (
    build_choose_parity_call,
    build_choose_parity_response,
    build_game_over,
    build_match_result_report,
)
from SHARED.contracts.league_manager_contracts import build_match_result_ack
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params


def get_params(msg):
    """Extract params from JSON-RPC message."""
    return extract_jsonrpc_params(msg)


class TestParityChoiceFlow:
    """Test parity choice collection message flow."""

    def test_parity_call(self):
        """Test parity choice call."""
        parity_call = build_choose_parity_call(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            player_standings={"wins": 0, "losses": 0, "draws": 0}, timeout_seconds=30,
        )
        params = get_params(parity_call)
        assert params[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL
        assert Field.DEADLINE in params
        assert validate_base_message(params)

    def test_parity_response(self):
        """Test parity choice response."""
        parity_response = build_choose_parity_response(
            match_id="R1M1", player_id="P01", parity_choice="EVEN", conversation_id="conv-123",
        )
        params = get_params(parity_response)
        assert params[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_RESPONSE
        assert params[Field.PARITY_CHOICE] == "EVEN"


class TestGameResolutionFlow:
    """Test game resolution message flow."""

    def test_game_over(self):
        """Test game over message."""
        game_over = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="WIN", winner_player_id="P01", drawn_number=4, number_parity="even",
            choices={"P01": "EVEN", "P02": "ODD"}, reason="P01 correctly predicted",
        )
        params = get_params(game_over)
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        assert Field.GAME_RESULT in params
        assert params[Field.GAME_RESULT]["status"] == "WIN"
        assert validate_base_message(params)

    def test_match_result_report(self):
        """Test match result report."""
        result_report = build_match_result_report(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            winner="P01", score={"P01": 1, "P02": 0}, drawn_number=4,
            choices={"P01": "EVEN", "P02": "ODD"},
        )
        params = get_params(result_report)
        assert params[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert Field.RESULT in params
        assert validate_base_message(params)

    def test_match_result_ack(self):
        """Test match result acknowledgment."""
        result_ack = build_match_result_ack(match_id="R1M1", conversation_id="conv-123")
        params = get_params(result_ack)
        assert params[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_ACK


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
