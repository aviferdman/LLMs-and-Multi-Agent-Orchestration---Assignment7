"""Referee contract compliance tests - GAME_OVER and MATCH_RESULT_REPORT.

Tests contracts as defined in doc/protocol/v2/CONTRACTS.md.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.referee_contracts import build_game_over, build_match_result_report
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request."""
    return extract_jsonrpc_params(msg)


class TestGameOverContract:
    """Test GAME_OVER contract."""

    def test_game_over_structure(self):
        """GAME_OVER must have all required fields."""
        msg = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="WIN", winner_player_id="P01", drawn_number=8, number_parity="even",
            choices={"P01": "even", "P02": "odd"}, reason="P01 correctly predicted",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        assert params[Field.MATCH_ID] == "R1M1"
        assert Field.GAME_RESULT in params
        assert params[Field.GAME_RESULT]["status"] == "WIN"

    def test_game_over_with_draw(self):
        """GAME_OVER can indicate a draw."""
        msg = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="DRAW", winner_player_id=None, drawn_number=5, number_parity="odd",
            choices={"P01": "odd", "P02": "odd"}, reason="Both players chose odd",
        )
        params = get_params(msg)
        assert params[Field.GAME_RESULT]["status"] == "DRAW"
        assert params[Field.GAME_RESULT]["winner_player_id"] is None

    def test_game_over_drawn_number_range(self):
        """GAME_OVER drawn_number must be 1-10."""
        for num in [1, 5, 10]:
            msg = build_game_over(
                league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
                status="WIN", winner_player_id="P01", drawn_number=num,
                number_parity="even" if num % 2 == 0 else "odd",
                choices={"P01": "even", "P02": "odd"}, reason="test",
            )
            params = get_params(msg)
            assert 1 <= params[Field.GAME_RESULT]["drawn_number"] <= 10

    def test_game_over_is_valid_base_message(self):
        """GAME_OVER params must pass base message validation."""
        msg = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="WIN", winner_player_id="P01", drawn_number=8, number_parity="even",
            choices={"P01": "even", "P02": "odd"}, reason="normal win",
        )
        params = get_params(msg)
        assert validate_base_message(params) is True


class TestMatchResultReportContract:
    """Test MATCH_RESULT_REPORT contract."""

    def test_match_result_report_structure(self):
        """MATCH_RESULT_REPORT must have all required fields."""
        msg = build_match_result_report(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            winner="P01", score={"P01": 1, "P02": 0}, drawn_number=8,
            choices={"P01": "even", "P02": "odd"},
        )
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert Field.RESULT in params
        assert params[Field.RESULT]["winner"] == "P01"

    def test_match_result_report_with_draw(self):
        """MATCH_RESULT_REPORT winner can be 'draw'."""
        msg = build_match_result_report(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            winner="draw", score={"P01": 0, "P02": 0}, drawn_number=5,
            choices={"P01": "odd", "P02": "odd"},
        )
        params = get_params(msg)
        assert params[Field.RESULT]["winner"] == "draw"

    def test_match_result_report_is_valid_base_message(self):
        """MATCH_RESULT_REPORT params must pass base message validation."""
        msg = build_match_result_report(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            winner="P01", score={"P01": 1, "P02": 0}, drawn_number=8,
            choices={"P01": "even", "P02": "odd"},
        )
        params = get_params(msg)
        assert validate_base_message(params) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
