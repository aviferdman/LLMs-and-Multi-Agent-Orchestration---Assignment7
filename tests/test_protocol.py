"""Protocol compliance tests for message validation.

This module tests all message types against JSON schema validation
and ensures protocol compliance per league.v2 specification.
"""

import json
import re
import uuid
from datetime import datetime

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType, Field, ParityChoice
from SHARED.contracts.base_contract import create_base_message, create_game_message
from SHARED.contracts.registration_contracts import (
    build_referee_register_request,
    build_referee_register_response,
    build_league_register_request,
    build_league_register_response,
)
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


class TestProtocolCompliance:
    """Test protocol compliance for all message types."""

    def test_protocol_version_is_league_v2(self):
        """Verify protocol version is league.v2."""
        assert PROTOCOL_VERSION == "league.v2"

    def test_base_message_structure(self):
        """Test base message parameters structure."""
        message = create_base_message(
            message_type="TEST_MESSAGE",
            sender_type="test",
            sender_id="agent1",
            conversation_id="conv-123"
        )
        
        assert message["protocol"] == PROTOCOL_VERSION
        assert message["message_type"] == "TEST_MESSAGE"
        assert message["sender"] == "test:agent1"
        assert message["conversation_id"] == "conv-123"
        assert "timestamp" in message

    def test_timestamp_format_iso8601_utc(self):
        """Test all timestamps are ISO-8601 with Z suffix."""
        message = create_base_message(
            message_type="TEST",
            sender_type="test",
            sender_id="agent1"
        )
        
        timestamp = message["timestamp"]
        assert timestamp.endswith("Z"), "Timestamp must end with Z (UTC)"
        
        # Verify ISO-8601 format
        iso_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        assert re.match(iso_pattern, timestamp), "Timestamp must be ISO-8601 format"


class TestMessageTypesValidation:
    """Test all required message types validate correctly."""

    # Registration Messages
    def test_referee_register_request_validates(self):
        """Test REFEREE_REGISTER_REQUEST message validation."""
        message = build_referee_register_request(
            referee_id="REF01",
            display_name="Referee 01",
            version="1.0.0",
            contact_endpoint="http://localhost:8001/mcp"
        )
        
        assert message["method"] == "register_referee"
        params = message["params"]
        assert params["message_type"] == MessageType.REFEREE_REGISTER_REQUEST
        assert "referee_meta" in params
        assert params["referee_meta"]["display_name"] == "Referee 01"

    def test_referee_register_response_validates(self):
        """Test REFEREE_REGISTER_RESPONSE message validation."""
        message = build_referee_register_response(
            referee_id="REF01",
            conversation_id="conv-123",
            status="ACCEPTED"
        )
        
        params = message["params"]
        assert params["message_type"] == MessageType.REFEREE_REGISTER_RESPONSE
        assert params["status"] == "ACCEPTED"

    def test_league_register_request_validates(self):
        """Test LEAGUE_REGISTER_REQUEST message validation."""
        message = build_league_register_request(
            player_id="P01",
            display_name="Player One",
            version="1.0.0",
            contact_endpoint="http://localhost:8101/mcp"
        )
        
        params = message["params"]
        assert params["message_type"] == MessageType.LEAGUE_REGISTER_REQUEST
        assert "player_meta" in params

    def test_league_register_response_validates(self):
        """Test LEAGUE_REGISTER_RESPONSE message validation."""
        message = build_league_register_response(
            player_id="P01",
            conversation_id="conv-123",
            status="ACCEPTED"
        )
        
        params = message["params"]
        assert params["message_type"] == MessageType.LEAGUE_REGISTER_RESPONSE

    # Game Flow Messages
    def test_game_invitation_validates(self):
        """Test GAME_INVITATION message validation."""
        message = build_game_invitation(
            league_id="league_2025_even_odd",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            role_in_match="PLAYER_A"
        )
        
        params = message["params"]
        assert params["message_type"] == MessageType.GAME_INVITATION
        assert params["match_id"] == "R1M1"
        assert params["opponent_id"] == "P02"

    def test_game_join_ack_validates(self):
        """Test GAME_JOIN_ACK message validation."""
        message = build_game_join_ack(
            player_id="P01",
            match_id="R1M1",
            conversation_id="conv-123",
            accept=True
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
            player_standings={"wins": 0, "losses": 0}
        )
        
        params = message["params"]
        assert params["message_type"] == MessageType.CHOOSE_PARITY_CALL

    def test_parity_choice_validates(self):
        """Test CHOOSE_PARITY_RESPONSE message validation."""
        message = build_choose_parity_response(
            player_id="P01",
            match_id="R1M1",
            parity_choice="even",
            conversation_id="conv-123"
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
            reason="P01 correctly guessed even"
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
            choices={"P01": "even", "P02": "odd"}
        )
        
        params = message["params"]
        assert params["message_type"] == MessageType.MATCH_RESULT_REPORT


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
            reason="P01 guessed correctly"
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
                reason="P01 guessed correctly"
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
            role_in_match="PLAYER_A"
        )
        
        assert isinstance(message["params"]["round_id"], int)

    def test_parity_choice_is_valid_string(self):
        """Parity choice must be 'even' or 'odd'."""
        for choice in ["even", "odd"]:
            message = build_choose_parity_response(
                player_id="P01",
                match_id="R1M1",
                parity_choice=choice,
                conversation_id="conv-123"
            )
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
