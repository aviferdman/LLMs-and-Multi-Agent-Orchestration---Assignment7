"""Protocol compliance tests for message structure.

This module tests protocol compliance for message types per league.v2 specification.
"""

import re

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType
from SHARED.contracts.base_contract import create_base_message
from SHARED.contracts.registration_contracts import (
    build_referee_register_request,
    build_referee_register_response,
    build_league_register_request,
    build_league_register_response,
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
            conversation_id="conv-123",
        )

        assert message["protocol"] == PROTOCOL_VERSION
        assert message["message_type"] == "TEST_MESSAGE"
        assert message["sender"] == "test:agent1"
        assert message["conversation_id"] == "conv-123"
        assert "timestamp" in message

    def test_timestamp_format_iso8601_utc(self):
        """Test all timestamps are ISO-8601 with Z suffix."""
        message = create_base_message(
            message_type="TEST", sender_type="test", sender_id="agent1"
        )

        timestamp = message["timestamp"]
        assert timestamp.endswith("Z"), "Timestamp must end with Z (UTC)"

        iso_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        assert re.match(iso_pattern, timestamp), "Timestamp must be ISO-8601 format"


class TestRegistrationMessages:
    """Test registration message types validate correctly."""

    def test_referee_register_request_validates(self):
        """Test REFEREE_REGISTER_REQUEST message validation."""
        message = build_referee_register_request(
            referee_id="REF01",
            display_name="Referee 01",
            version="1.0.0",
            contact_endpoint="http://localhost:8001/mcp",
        )

        assert message["method"] == "register_referee"
        params = message["params"]
        assert params["message_type"] == MessageType.REFEREE_REGISTER_REQUEST
        assert "referee_meta" in params
        assert params["referee_meta"]["display_name"] == "Referee 01"

    def test_referee_register_response_validates(self):
        """Test REFEREE_REGISTER_RESPONSE message validation."""
        message = build_referee_register_response(
            referee_id="REF01", conversation_id="conv-123", status="ACCEPTED"
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
            contact_endpoint="http://localhost:8101/mcp",
        )

        params = message["params"]
        assert params["message_type"] == MessageType.LEAGUE_REGISTER_REQUEST
        assert "player_meta" in params

    def test_league_register_response_validates(self):
        """Test LEAGUE_REGISTER_RESPONSE message validation."""
        message = build_league_register_response(
            player_id="P01", conversation_id="conv-123", status="ACCEPTED"
        )

        params = message["params"]
        assert params["message_type"] == MessageType.LEAGUE_REGISTER_RESPONSE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
