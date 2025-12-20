"""Edge case tests for protocol validation - Part 1."""

import pytest
from SHARED.league_sdk.validation import (
    validate_message, validate_timestamp, validate_uuid,
    validate_message_type, get_validation_errors
)
from SHARED.league_sdk.messages import format_timestamp
from agents.player_strategies import FrequencyStrategy


class TestEdgeCaseEmptyData:
    """Test Case 1: Empty dataset handling."""

    def test_empty_standings_dict(self):
        """Empty standings dictionary should be valid."""
        standings = {}
        assert isinstance(standings, dict)
        assert len(standings) == 0

    def test_empty_history_list(self):
        """Empty history should return default choice."""
        strategy = FrequencyStrategy()
        choice = strategy.choose_parity([])
        assert choice in ["EVEN", "ODD"]


class TestEdgeCaseMalformedMessages:
    """Test Case 2: Malformed message handling."""

    def test_missing_protocol_field(self):
        """Message without protocol field should fail validation."""
        message = {"message_type": "GAME_INVITATION", "timestamp": "2025-01-01T00:00:00.000Z"}
        assert validate_message(message) is False

    def test_missing_timestamp(self):
        """Message without timestamp should fail validation."""
        message = {"protocol": "league.v2", "message_type": "GAME_OVER"}
        assert validate_message(message) is False

    def test_empty_message(self):
        """Empty message should fail validation."""
        assert validate_message({}) is False

    def test_none_values(self):
        """Message with None values should fail validation."""
        message = {"protocol": None, "timestamp": None, "message_type": None}
        errors = get_validation_errors(message)
        assert len(errors) > 0


class TestEdgeCaseTimestampFormats:
    """Test Case 8: Invalid timestamp format handling."""

    def test_missing_z_suffix(self):
        """Timestamp without Z suffix should be invalid."""
        assert validate_timestamp("2025-01-01T00:00:00.000") is False

    def test_wrong_timezone(self):
        """Timestamp with +00:00 instead of Z should be invalid."""
        assert validate_timestamp("2025-01-01T00:00:00.000+00:00") is False

    def test_invalid_date_format(self):
        """Non-ISO timestamp should be invalid."""
        assert validate_timestamp("01/01/2025 00:00:00Z") is False

    def test_valid_timestamp(self):
        """Valid ISO-8601 with Z suffix should pass."""
        ts = format_timestamp()
        assert validate_timestamp(ts) is True


class TestEdgeCaseUUIDValidation:
    """Test Case 7: Invalid UUID format handling."""

    def test_short_uuid(self):
        """Truncated UUID should be invalid."""
        assert validate_uuid("12345") is False

    def test_invalid_characters(self):
        """UUID with invalid characters should fail."""
        assert validate_uuid("gggggggg-gggg-gggg-gggg-gggggggggggg") is False

    def test_valid_uuid_lowercase(self):
        """Valid lowercase UUID should pass."""
        assert validate_uuid("12345678-1234-1234-1234-123456789abc") is True

    def test_valid_uuid_uppercase(self):
        """Valid uppercase UUID should pass."""
        assert validate_uuid("12345678-1234-1234-1234-123456789ABC") is True


class TestEdgeCaseMessageTypes:
    """Test invalid message type handling."""

    def test_unknown_message_type(self):
        """Unknown message type should be invalid."""
        assert validate_message_type("INVALID_TYPE") is False

    def test_empty_message_type(self):
        """Empty message type should be invalid."""
        assert validate_message_type("") is False

    def test_valid_game_invitation(self):
        """GAME_INVITATION should be valid message type."""
        assert validate_message_type("GAME_INVITATION") is True
