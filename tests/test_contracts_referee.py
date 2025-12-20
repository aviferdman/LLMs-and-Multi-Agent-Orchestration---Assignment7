"""Referee contract compliance tests.

Tests all Referee message contracts as defined in
doc/protocol/v2/REFEREE.md
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
        )

        # Base message fields
        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert Field.CONVERSATION_ID in msg
        assert msg[Field.SENDER] == "REF01"
        assert Field.TIMESTAMP in msg

        # Game invitation specific fields
        assert msg[Field.PLAYER_ID] == "P01"
        assert msg[Field.OPPONENT_ID] == "P02"

    def test_game_invitation_is_valid_base_message(self):
        """GAME_INVITATION must pass base message validation."""
        msg = build_game_invitation(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
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
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "REF01"
        assert msg[Field.PLAYER_ID] == "P01"

    def test_choose_parity_call_is_valid_base_message(self):
        """CHOOSE_PARITY_CALL must pass base message validation."""
        msg = build_choose_parity_call(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
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
            winner="P01",
            drawn_number=8,
            player_a_choice=ParityChoice.EVEN,
            player_b_choice=ParityChoice.ODD,
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "REF01"
        assert msg[Field.WINNER] == "P01"
        assert msg[Field.DRAWN_NUMBER] == 8
        assert msg[Field.PLAYER_A_CHOICE] == ParityChoice.EVEN
        assert msg[Field.PLAYER_B_CHOICE] == ParityChoice.ODD

    def test_game_over_with_draw_winner(self):
        """GAME_OVER winner can be 'draw'."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner=Winner.DRAW,
            drawn_number=5,
            player_a_choice=ParityChoice.ODD,
            player_b_choice=ParityChoice.ODD,
        )
        assert msg[Field.WINNER] == Winner.DRAW

    def test_game_over_drawn_number_range(self):
        """GAME_OVER drawn_number must be 1-10."""
        for num in range(1, 11):
            msg = build_game_over(
                league_id="league_2025",
                round_id=1,
                match_id="R1M1",
                referee_id="REF01",
                winner="P01",
                drawn_number=num,
                player_a_choice=ParityChoice.EVEN,
                player_b_choice=ParityChoice.ODD,
            )
            assert 1 <= msg[Field.DRAWN_NUMBER] <= 10

    def test_game_over_is_valid_base_message(self):
        """GAME_OVER must pass base message validation."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            drawn_number=8,
            player_a_choice=ParityChoice.EVEN,
            player_b_choice=ParityChoice.ODD,
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
            player_a="P01",
            player_b="P02",
            winner="P01",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "REF01"
        assert msg[Field.PLAYER_A] == "P01"
        assert msg[Field.PLAYER_B] == "P02"
        assert msg[Field.WINNER] == "P01"

    def test_match_result_report_with_draw(self):
        """MATCH_RESULT_REPORT winner can be 'draw'."""
        msg = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_a="P01",
            player_b="P02",
            winner=Winner.DRAW,
        )
        assert msg[Field.WINNER] == Winner.DRAW

    def test_match_result_report_is_valid_base_message(self):
        """MATCH_RESULT_REPORT must pass base message validation."""
        msg = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_a="P01",
            player_b="P02",
            winner="P01",
        )
        assert validate_base_message(msg) is True


class TestGameErrorContract:
    """Test GAME_ERROR contract."""

    def test_game_error_structure(self):
        """GAME_ERROR must have all required fields."""
        msg = build_game_error(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            error_code="E001",
            error_message="Response timeout",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_ERROR
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg["error_code"] == "E001"
        assert msg["error_message"] == "Response timeout"

    def test_game_error_with_details(self):
        """GAME_ERROR can include optional details."""
        msg = build_game_error(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            error_code="E001",
            error_message="Response timeout",
            details={"player_id": "P01", "timeout_seconds": 30},
        )

        assert msg["details"]["player_id"] == "P01"
        assert msg["details"]["timeout_seconds"] == 30

    def test_game_error_is_valid_base_message(self):
        """GAME_ERROR must pass base message validation."""
        msg = build_game_error(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            error_code="E001",
            error_message="Timeout",
        )
        assert validate_base_message(msg) is True


class TestWinnerValues:
    """Test valid winner values in referee messages."""

    def test_winner_constants_defined(self):
        """Winner constants must be defined."""
        assert Winner.PLAYER_A == "PLAYER_A"
        assert Winner.PLAYER_B == "PLAYER_B"
        assert Winner.DRAW == "DRAW"

    def test_game_over_accepts_player_id_as_winner(self):
        """GAME_OVER accepts specific player ID as winner."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",  # Specific player ID
            drawn_number=8,
            player_a_choice=ParityChoice.EVEN,
            player_b_choice=ParityChoice.ODD,
        )
        assert msg[Field.WINNER] == "P01"

    def test_game_over_accepts_generic_winner(self):
        """GAME_OVER accepts generic winner constants."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner=Winner.PLAYER_A,
            drawn_number=8,
            player_a_choice=ParityChoice.EVEN,
            player_b_choice=ParityChoice.ODD,
        )
        assert msg[Field.WINNER] == Winner.PLAYER_A


class TestParityChoiceValues:
    """Test valid parity choice values."""

    def test_parity_choice_constants_defined(self):
        """Parity choice constants must be defined."""
        assert ParityChoice.EVEN == "EVEN"
        assert ParityChoice.ODD == "ODD"

    def test_game_over_uses_correct_choices(self):
        """GAME_OVER choices must use constant values."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            drawn_number=8,
            player_a_choice=ParityChoice.EVEN,
            player_b_choice=ParityChoice.ODD,
        )
        assert msg[Field.PLAYER_A_CHOICE] == ParityChoice.EVEN
        assert msg[Field.PLAYER_B_CHOICE] == ParityChoice.ODD
