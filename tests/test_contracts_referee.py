"""Referee contract compliance tests.

Tests all Referee message contracts as defined in
doc/protocol/v2/CONTRACTS.md
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, ParityChoice, Winner
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.referee_contracts import (
    build_choose_parity_call,
    build_game_error,
    build_game_invitation,
    build_game_over,
    build_match_result_report,
)
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request."""
    return extract_jsonrpc_params(msg)


class TestGameInvitationContract:
    """Test GAME_INVITATION contract."""

    def test_game_invitation_structure(self):
        """GAME_INVITATION must have all required fields."""
        msg = build_game_invitation(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            role_in_match="player_a", game_type="even_odd",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert params[Field.ROUND_ID] == 1
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.SENDER] == "referee:REF01"
        assert Field.TIMESTAMP in params
        assert Field.CONVERSATION_ID in params
        assert params[Field.OPPONENT_ID] == "P02"
        assert params[Field.ROLE_IN_MATCH] == "player_a"
        assert params[Field.GAME_TYPE] == "even_odd"

    def test_game_invitation_is_valid_base_message(self):
        """GAME_INVITATION params must pass base message validation."""
        msg = build_game_invitation(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02", role_in_match="player_a",
        )
        params = get_params(msg)
        assert validate_base_message(params) is True

    def test_game_invitation_timestamp_is_utc(self):
        """GAME_INVITATION timestamp must end with Z (UTC)."""
        msg = build_game_invitation(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02", role_in_match="player_b",
        )
        params = get_params(msg)
        assert params[Field.TIMESTAMP].endswith("Z")


class TestChooseParityCallContract:
    """Test CHOOSE_PARITY_CALL contract."""

    def test_choose_parity_call_structure(self):
        """CHOOSE_PARITY_CALL must have all required fields."""
        msg = build_choose_parity_call(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            player_standings={"wins": 0, "losses": 0, "draws": 0}, timeout_seconds=30,
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.SENDER] == "referee:REF01"
        assert params[Field.PLAYER_ID] == "P01"
        assert Field.DEADLINE in params
        assert Field.CONTEXT in params
        assert params[Field.CONTEXT]["opponent_id"] == "P02"
        assert params[Field.CONTEXT]["round_id"] == 1

    def test_choose_parity_call_is_valid_base_message(self):
        """CHOOSE_PARITY_CALL params must pass base message validation."""
        msg = build_choose_parity_call(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            player_standings={}, timeout_seconds=30,
        )
        params = get_params(msg)
        assert validate_base_message(params) is True


class TestGameOverContract:
    """Test GAME_OVER contract."""

    def test_game_over_structure(self):
        """GAME_OVER must have all required fields."""
        msg = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="WIN", winner_player_id="P01", drawn_number=8, number_parity="even",
            choices={"P01": "even", "P02": "odd"}, reason="P01 correctly predicted even parity",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.SENDER] == "referee:REF01"
        assert Field.GAME_RESULT in params
        assert params[Field.GAME_RESULT]["status"] == "WIN"
        assert params[Field.GAME_RESULT]["winner_player_id"] == "P01"
        assert params[Field.GAME_RESULT]["drawn_number"] == 8

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
        for num in range(1, 11):
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
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert params[Field.ROUND_ID] == 1
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.SENDER] == "referee:REF01"
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
