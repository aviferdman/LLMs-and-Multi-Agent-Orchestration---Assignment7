"""Protocol compliance tests for game flow messages.

This module tests game flow message validation per league.v2 specification.
"""

import pytest

from SHARED.constants import MessageType
from SHARED.contracts.game_flow_contracts import (
    build_game_invitation,
    build_choose_parity_call,
)
from SHARED.contracts.game_result_contracts import (
    build_game_over,
    build_match_result_report,
)
from SHARED.contracts.player_contracts import (
    build_game_join_ack,
    build_choose_parity_response,
)


class TestGameFlowMessages:
    """Test game flow message types validate correctly."""

    def test_game_invitation_validates(self):
        """Test GAME_INVITATION message validation."""
        message = build_game_invitation(
            league_id="league_2025_even_odd",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            role_in_match="PLAYER_A",
        )

        params = message["params"]
        assert params["message_type"] == MessageType.GAME_INVITATION
        assert params["match_id"] == "R1M1"
        assert params["opponent_id"] == "P02"

    def test_game_join_ack_validates(self):
        """Test GAME_JOIN_ACK message validation."""
        message = build_game_join_ack(
            player_id="P01", match_id="R1M1", conversation_id="conv-123", accept=True
        )

        params = message["params"]
        assert params["message_type"] == MessageType.GAME_JOIN_ACK
        assert params["accept"] is True

    def test_choose_parity_call_validates(self):
        """Test CHOOSE_PARITY_CALL message validation."""
        message = build_choose_parity_call(
            league_id="league_2025_even_odd",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            player_standings={"wins": 0, "losses": 0},
        )

        params = message["params"]
        assert params["message_type"] == MessageType.CHOOSE_PARITY_CALL

    def test_parity_choice_validates(self):
        """Test CHOOSE_PARITY_RESPONSE message validation."""
        message = build_choose_parity_response(
            player_id="P01", match_id="R1M1", parity_choice="even", conversation_id="conv-123"
        )

        params = message["params"]
        assert params["message_type"] == MessageType.CHOOSE_PARITY_RESPONSE
        assert params["parity_choice"] in ["even", "odd"]

    def test_game_over_validates(self):
        """Test GAME_OVER message validation."""
        message = build_game_over(
            league_id="league_2025_even_odd",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="COMPLETED",
            winner_player_id="P01",
            drawn_number=8,
            number_parity="even",
            choices={"P01": "even", "P02": "odd"},
            reason="P01 correctly guessed even",
        )

        params = message["params"]
        assert params["message_type"] == MessageType.GAME_OVER
        assert params["game_result"]["winner_player_id"] == "P01"
        assert 1 <= params["game_result"]["drawn_number"] <= 10

    def test_match_result_report_validates(self):
        """Test MATCH_RESULT_REPORT message validation."""
        message = build_match_result_report(
            league_id="league_2025_even_odd",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            score={"P01": 2, "P02": 0},
            drawn_number=8,
            choices={"P01": "even", "P02": "odd"},
        )

        params = message["params"]
        assert params["message_type"] == MessageType.MATCH_RESULT_REPORT


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
