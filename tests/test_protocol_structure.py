"""Protocol compliance tests - Message structure and version."""

import uuid
from datetime import datetime

import pytest

from SHARED.league_sdk.messages import (
    build_choose_parity_call,
    build_game_invitation,
    build_game_join_ack,
    build_game_over,
    build_match_result_report,
    build_parity_choice,
    create_base_message,
    format_timestamp,
)
from SHARED.league_sdk.validation import (
    validate_protocol_version,
    validate_timestamp,
    validate_uuid,
)
from SHARED.protocol_constants import PROTOCOL_VERSION, Field


class TestProtocolRequiredFields:
    """Test all messages have required fields."""

    @pytest.fixture
    def base_msg(self):
        """Create a base message for testing."""
        return create_base_message("GAME_INVITATION", "L001", 1, "M001", "REF01")

    def test_base_message_has_protocol(self, base_msg):
        """All messages must have protocol field."""
        assert Field.PROTOCOL in base_msg

    def test_base_message_has_message_type(self, base_msg):
        """All messages must have message_type field."""
        assert Field.MESSAGE_TYPE in base_msg

    def test_base_message_has_timestamp(self, base_msg):
        """All messages must have timestamp field."""
        assert Field.TIMESTAMP in base_msg

    def test_base_message_has_conversation_id(self, base_msg):
        """All messages must have conversation_id field."""
        assert Field.CONVERSATION_ID in base_msg

    def test_base_message_has_sender(self, base_msg):
        """All messages must have sender field."""
        assert Field.SENDER in base_msg

    def test_game_invitation_has_player_fields(self):
        """Game invitation must have player_id and opponent_id."""
        msg = build_game_invitation("L001", 1, "M001", "REF01", "P01", "P02")
        assert "player_id" in msg
        assert "opponent_id" in msg


class TestProtocolVersionCompliance:
    """Test protocol version is correct in all messages."""

    def test_protocol_version_constant(self):
        """Protocol version should be 'league.v2'."""
        assert PROTOCOL_VERSION == "league.v2"

    def test_base_message_uses_correct_version(self):
        """Messages should use correct protocol version."""
        msg = create_base_message("GAME_OVER", "L001", 1, "M001", "REF01")
        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION

    def test_all_builders_use_correct_version(self):
        """All message builders should set correct protocol."""
        messages = [
            build_game_invitation("L001", 1, "M001", "REF01", "P01", "P02"),
            build_game_join_ack("L001", 1, "M001", "P01", str(uuid.uuid4())),
            build_choose_parity_call("L001", 1, "M001", "REF01", "P01"),
            build_parity_choice("L001", 1, "M001", "P01", "even", str(uuid.uuid4())),
            build_game_over("L001", 1, "M001", "REF01", "P01", 5, "even", "odd"),
            build_match_result_report("L001", 1, "M001", "REF01", "P01", "P02", "P01"),
        ]
        for msg in messages:
            assert validate_protocol_version(msg[Field.PROTOCOL])


class TestTimestampCompliance:
    """Test timestamps use correct format with Z suffix."""

    def test_timestamps_end_with_z(self):
        """All timestamps must end with Z suffix."""
        ts = format_timestamp()
        assert ts.endswith("Z")

    def test_timestamps_are_iso8601(self):
        """Timestamps must be valid ISO-8601 format."""
        ts = format_timestamp()
        iso_part = ts.rstrip("Z")
        try:
            datetime.fromisoformat(iso_part)
            assert True
        except ValueError:
            pytest.fail("Timestamp is not ISO-8601 format")

    def test_message_timestamps_valid(self):
        """Messages should have valid timestamps."""
        msg = create_base_message("TEST", "L001", 1, "M001", "SENDER")
        assert validate_timestamp(msg[Field.TIMESTAMP])


class TestUUIDCompliance:
    """Test UUIDs are valid format."""

    def test_conversation_id_is_valid_uuid(self):
        """Conversation IDs must be valid UUIDs."""
        msg = create_base_message("TEST", "L001", 1, "M001", "SENDER")
        assert validate_uuid(msg[Field.CONVERSATION_ID])

    def test_generated_uuid_format(self):
        """Generated UUIDs should follow standard format."""
        test_uuid = str(uuid.uuid4())
        assert validate_uuid(test_uuid)
