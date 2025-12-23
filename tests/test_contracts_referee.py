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
from SHARED.contracts.referee_contracts import (
    build_choose_parity_call,
    build_game_error,
    build_game_invitation,
    build_game_over,
    build_match_result_report,
)


class TestGameInvitationContract:
    """Test GAME_INVITATION contract."""

    def test_game_invitation_structure(self):
        """GAME_INVITATION must have all required fields."""
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

        # Base message fields
        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "referee:REF01"
        assert Field.TIMESTAMP in msg
        assert Field.CONVERSATION_ID in msg

        # Game invitation specific fields
        assert msg[Field.OPPONENT_ID] == "P02"
        assert msg[Field.ROLE_IN_MATCH] == "player_a"
        assert msg[Field.GAME_TYPE] == "even_odd"

    def test_game_invitation_is_valid_base_message(self):
        """GAME_INVITATION must pass base message validation."""
        msg = build_game_invitation(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            role_in_match="player_a",
        )
        assert validate_base_message(msg) is True

    def test_game_invitation_timestamp_is_utc(self):
        """GAME_INVITATION timestamp must end with Z (UTC)."""
        msg = build_game_invitation(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            role_in_match="player_b",
        )
        assert msg[Field.TIMESTAMP].endswith("Z")


class TestChooseParityCallContract:
    """Test CHOOSE_PARITY_CALL contract."""

    def test_choose_parity_call_structure(self):
        """CHOOSE_PARITY_CALL must have all required fields."""
        msg = build_choose_parity_call(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            player_standings={"wins": 0, "losses": 0, "draws": 0},
            timeout_seconds=30,
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL
        # Note: league_id and round_id are in context, not top-level
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "referee:REF01"
        assert msg[Field.PLAYER_ID] == "P01"
        assert Field.DEADLINE in msg
        assert Field.CONTEXT in msg
        assert msg[Field.CONTEXT]["opponent_id"] == "P02"
        assert msg[Field.CONTEXT]["round_id"] == 1

    def test_choose_parity_call_is_valid_base_message(self):
        """CHOOSE_PARITY_CALL must pass base message validation."""
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
        assert validate_base_message(msg) is True


class TestGameOverContract:
    """Test GAME_OVER contract."""

    def test_game_over_structure(self):
        """GAME_OVER must have all required fields."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="WIN",
            winner_player_id="P01",
            drawn_number=8,
            number_parity="even",
            choices={"P01": "even", "P02": "odd"},
            reason="P01 correctly predicted even parity",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        # Note: league_id and round_id are not top-level in GAME_OVER
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "referee:REF01"
        assert Field.GAME_RESULT in msg
        assert msg[Field.GAME_RESULT]["status"] == "WIN"
        assert msg[Field.GAME_RESULT]["winner_player_id"] == "P01"
        assert msg[Field.GAME_RESULT]["drawn_number"] == 8

    def test_game_over_with_draw(self):
        """GAME_OVER can indicate a draw."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="DRAW",
            winner_player_id=None,
            drawn_number=5,
            number_parity="odd",
            choices={"P01": "odd", "P02": "odd"},
            reason="Both players chose odd",
        )
        assert msg[Field.GAME_RESULT]["status"] == "DRAW"
        assert msg[Field.GAME_RESULT]["winner_player_id"] is None

    def test_game_over_drawn_number_range(self):
        """GAME_OVER drawn_number must be 1-10."""
        for num in range(1, 11):
            msg = build_game_over(
                league_id="league_2025",
                round_id=1,
                match_id="R1M1",
                referee_id="REF01",
                status="WIN",
                winner_player_id="P01",
                drawn_number=num,
                number_parity="even" if num % 2 == 0 else "odd",
                choices={"P01": "even", "P02": "odd"},
                reason="test",
            )
            assert 1 <= msg[Field.GAME_RESULT]["drawn_number"] <= 10

    def test_game_over_is_valid_base_message(self):
        """GAME_OVER must pass base message validation."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="WIN",
            winner_player_id="P01",
            drawn_number=8,
            number_parity="even",
            choices={"P01": "even", "P02": "odd"},
            reason="normal win",
        )
        assert validate_base_message(msg) is True


class TestMatchResultReportContract:
    """Test MATCH_RESULT_REPORT contract."""

    def test_match_result_report_structure(self):
        """MATCH_RESULT_REPORT must have all required fields."""
        msg = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            score={"P01": 1, "P02": 0},
            drawn_number=8,
            choices={"P01": "even", "P02": "odd"},
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "referee:REF01"
        assert Field.RESULT in msg
        assert msg[Field.RESULT]["winner"] == "P01"

    def test_match_result_report_with_draw(self):
        """MATCH_RESULT_REPORT winner can be 'draw'."""
        msg = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="draw",
            score={"P01": 0, "P02": 0},
            drawn_number=5,
            choices={"P01": "odd", "P02": "odd"},
        )
        assert msg[Field.RESULT]["winner"] == "draw"

    def test_match_result_report_is_valid_base_message(self):
        """MATCH_RESULT_REPORT must pass base message validation."""
        msg = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            score={"P01": 1, "P02": 0},
            drawn_number=8,
            choices={"P01": "even", "P02": "odd"},
        )
        assert validate_base_message(msg) is True


class TestGameErrorContract:
    """Test GAME_ERROR contract."""

    def test_game_error_structure(self):
        """GAME_ERROR must have all required fields."""
        msg = build_game_error(
            match_id="R1M1",
            referee_id="REF01",
            error_code="E001",
            error_description="Response timeout",
            affected_player="P01",
            action_required="CHOOSE_PARITY_RESPONSE",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_ERROR
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.ERROR_CODE] == "E001"
        assert msg[Field.ERROR_DESCRIPTION] == "Response timeout"
        assert msg[Field.AFFECTED_PLAYER] == "P01"

    def test_game_error_with_details(self):
        """GAME_ERROR can include optional retry info."""
        msg = build_game_error(
            match_id="R1M1",
            referee_id="REF01",
            error_code="E001",
            error_description="Response timeout",
            affected_player="P01",
            action_required="CHOOSE_PARITY_RESPONSE",
            retry_info={"can_retry": False, "reason": "timeout exceeded"},
        )

        assert msg[Field.RETRY_INFO]["can_retry"] is False
        assert msg[Field.RETRY_INFO]["reason"] == "timeout exceeded"

    def test_game_error_is_valid_base_message(self):
        """GAME_ERROR must pass base message validation."""
        msg = build_game_error(
            match_id="R1M1",
            referee_id="REF01",
            error_code="E001",
            error_description="Timeout",
            affected_player="P01",
            action_required="CHOOSE_PARITY_RESPONSE",
        )
        assert validate_base_message(msg) is True


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
