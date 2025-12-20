"""Protocol compliance tests - Message types and full validation."""

import uuid

import pytest

from SHARED.league_sdk.messages import build_game_invitation, build_game_over, build_parity_choice
from SHARED.league_sdk.validation import get_validation_errors, validate_message_type
from SHARED.protocol_constants import MessageType


class TestMessageTypeCompliance:
    """Test message types are valid enum values."""

    def test_game_invitation_type_valid(self):
        """GAME_INVITATION is a valid message type."""
        assert validate_message_type(MessageType.GAME_INVITATION)

    def test_game_join_ack_type_valid(self):
        """GAME_JOIN_ACK is a valid message type."""
        assert validate_message_type(MessageType.GAME_JOIN_ACK)

    def test_choose_parity_call_type_valid(self):
        """CHOOSE_PARITY_CALL is a valid message type."""
        assert validate_message_type(MessageType.CHOOSE_PARITY_CALL)

    def test_parity_choice_type_valid(self):
        """PARITY_CHOICE is a valid message type."""
        assert validate_message_type(MessageType.PARITY_CHOICE)

    def test_game_over_type_valid(self):
        """GAME_OVER is a valid message type."""
        assert validate_message_type(MessageType.GAME_OVER)

    def test_match_result_report_type_valid(self):
        """MATCH_RESULT_REPORT is a valid message type."""
        assert validate_message_type(MessageType.MATCH_RESULT_REPORT)

    def test_registration_types_valid(self):
        """Registration message types should be valid."""
        assert validate_message_type(MessageType.LEAGUE_REGISTER_REQUEST)
        assert validate_message_type(MessageType.LEAGUE_REGISTER_RESPONSE)
        assert validate_message_type(MessageType.REFEREE_REGISTER_REQUEST)
        assert validate_message_type(MessageType.REFEREE_REGISTER_RESPONSE)


class TestFullMessageCompliance:
    """Test complete messages pass all validation."""

    def test_game_invitation_fully_valid(self):
        """Complete GAME_INVITATION should have no errors."""
        msg = build_game_invitation("L001", 1, "M001", "REF01", "P01", "P02")
        errors = get_validation_errors(msg)
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_parity_choice_fully_valid(self):
        """Complete PARITY_CHOICE should have no errors."""
        msg = build_parity_choice("L001", 1, "M001", "P01", "even", str(uuid.uuid4()))
        errors = get_validation_errors(msg)
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_game_over_fully_valid(self):
        """Complete GAME_OVER should have no errors."""
        msg = build_game_over("L001", 1, "M001", "REF01", "P01", 5, "even", "odd")
        errors = get_validation_errors(msg)
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_multiple_games_unique_ids(self):
        """Multiple game invitations should have unique conversation IDs."""
        msg1 = build_game_invitation("L001", 1, "M001", "REF01", "P01", "P02")
        msg2 = build_game_invitation("L001", 1, "M002", "REF01", "P03", "P04")
        assert msg1["conversation_id"] != msg2["conversation_id"]
