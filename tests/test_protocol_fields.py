"""Protocol compliance tests for required fields and data types.

This module tests required fields and data type validation per league.v2 specification.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType, Field
from SHARED.contracts.registration_contracts import build_referee_register_request
from SHARED.contracts.game_flow_contracts import build_game_invitation
from SHARED.contracts.game_result_contracts import build_game_over
from SHARED.contracts.player_contracts import build_choose_parity_response


class TestRequiredFields:
    """Test required fields are present in all messages."""

    def test_all_messages_have_protocol(self):
        """All messages must have protocol field."""
        messages = [
            build_referee_register_request("REF01", "Referee", "1.0", "http://localhost:8001/mcp"),
            build_game_invitation("league", 1, "R1M1", "REF01", "P01", "P02", "PLAYER_A"),
            build_choose_parity_response("P01", "R1M1", "even", "conv-123"),
        ]

        for msg in messages:
            assert "params" in msg
            assert "protocol" in msg["params"]
            assert msg["params"]["protocol"] == PROTOCOL_VERSION

    def test_all_messages_have_timestamp(self):
        """All messages must have timestamp field."""
        messages = [
            build_referee_register_request("REF01", "Referee", "1.0", "http://localhost:8001/mcp"),
            build_game_invitation("league", 1, "R1M1", "REF01", "P01", "P02", "PLAYER_A"),
            build_choose_parity_response("P01", "R1M1", "even", "conv-123"),
        ]

        for msg in messages:
            assert "timestamp" in msg["params"]

    def test_all_messages_have_sender(self):
        """All messages must have sender field."""
        messages = [
            build_referee_register_request("REF01", "Referee", "1.0", "http://localhost:8001/mcp"),
            build_game_invitation("league", 1, "R1M1", "REF01", "P01", "P02", "PLAYER_A"),
            build_choose_parity_response("P01", "R1M1", "even", "conv-123"),
        ]

        for msg in messages:
            assert "sender" in msg["params"]


class TestDataTypes:
    """Test correct data types for all fields."""

    def test_drawn_number_is_integer(self):
        """Drawn number must be an integer."""
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
            reason="P01 guessed correctly",
        )
        assert isinstance(message["params"]["game_result"]["drawn_number"], int)

    def test_drawn_number_in_range(self):
        """Drawn number must be 1-10."""
        for num in [1, 5, 10]:
            message = build_game_over(
                league_id="league_2025_even_odd",
                round_id=1,
                match_id="R1M1",
                referee_id="REF01",
                status="COMPLETED",
                winner_player_id="P01",
                drawn_number=num,
                number_parity="even" if num % 2 == 0 else "odd",
                choices={"P01": "even", "P02": "odd"},
                reason="P01 guessed correctly",
            )
            assert 1 <= message["params"]["game_result"]["drawn_number"] <= 10

    def test_round_id_is_integer(self):
        """Round ID must be an integer."""
        message = build_game_invitation(
            league_id="league_2025_even_odd",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            role_in_match="PLAYER_A",
        )
        assert isinstance(message["params"]["round_id"], int)

    def test_parity_choice_is_valid_string(self):
        """Parity choice must be 'even' or 'odd'."""
        for choice in ["even", "odd"]:
            message = build_choose_parity_response("P01", "R1M1", choice, "conv-123")
            assert message["params"]["parity_choice"] in ["even", "odd"]


class TestMessageTypeConstants:
    """Test message type constants are correctly defined."""

    def test_registration_message_types(self):
        """Test registration message types exist."""
        assert hasattr(MessageType, "REFEREE_REGISTER_REQUEST")
        assert hasattr(MessageType, "REFEREE_REGISTER_RESPONSE")
        assert hasattr(MessageType, "LEAGUE_REGISTER_REQUEST")
        assert hasattr(MessageType, "LEAGUE_REGISTER_RESPONSE")

    def test_game_flow_message_types(self):
        """Test game flow message types exist."""
        assert hasattr(MessageType, "GAME_INVITATION")
        assert hasattr(MessageType, "GAME_JOIN_ACK")
        assert hasattr(MessageType, "CHOOSE_PARITY_CALL")
        assert hasattr(MessageType, "CHOOSE_PARITY_RESPONSE")
        assert hasattr(MessageType, "GAME_OVER")
        assert hasattr(MessageType, "MATCH_RESULT_REPORT")


class TestFieldConstants:
    """Test field constants are correctly defined."""

    def test_required_fields_exist(self):
        """Test required field constants exist."""
        assert hasattr(Field, "PROTOCOL")
        assert hasattr(Field, "MESSAGE_TYPE")
        assert hasattr(Field, "SENDER")
        assert hasattr(Field, "TIMESTAMP")
        assert hasattr(Field, "CONVERSATION_ID")

    def test_game_fields_exist(self):
        """Test game-related field constants exist."""
        assert hasattr(Field, "MATCH_ID")
        assert hasattr(Field, "PLAYER_ID")
        assert hasattr(Field, "PARITY_CHOICE")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
