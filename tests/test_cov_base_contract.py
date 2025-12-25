"""Tests for SHARED.contracts.base_contract module."""

import pytest
from SHARED.contracts.base_contract import (
    create_base_message,
    create_game_message,
)
from SHARED.constants import Field, PROTOCOL_VERSION


class TestCreateBaseMessage:
    """Tests for create_base_message function."""

    def test_creates_base_message_with_required_fields(self):
        """Test base message has all required protocol fields."""
        msg = create_base_message("TEST_MSG", "player", "P01")
        assert Field.PROTOCOL in msg
        assert Field.MESSAGE_TYPE in msg
        assert Field.SENDER in msg
        assert Field.TIMESTAMP in msg
        assert Field.CONVERSATION_ID in msg

    def test_message_type_set_correctly(self):
        """Test message type is set correctly."""
        msg = create_base_message("TEST_TYPE", "player", "P01")
        assert msg[Field.MESSAGE_TYPE] == "TEST_TYPE"

    def test_sender_formatted_correctly(self):
        """Test sender is formatted correctly."""
        msg = create_base_message("TEST", "referee", "REF01")
        assert "referee" in msg[Field.SENDER].lower()

    def test_protocol_version_included(self):
        """Test protocol version is included."""
        msg = create_base_message("TEST", "player", "P01")
        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION

    def test_custom_conversation_id_used(self):
        """Test custom conversation ID is used when provided."""
        msg = create_base_message("TEST", "player", "P01", conversation_id="conv-123")
        assert msg[Field.CONVERSATION_ID] == "conv-123"

    def test_auto_generates_conversation_id(self):
        """Test conversation ID is auto-generated when not provided."""
        msg = create_base_message("TEST", "player", "P01")
        assert msg[Field.CONVERSATION_ID] is not None
        assert len(msg[Field.CONVERSATION_ID]) > 0

    def test_extra_fields_included(self):
        """Test extra fields are included in message."""
        msg = create_base_message("TEST", "player", "P01", custom_field="value")
        assert msg.get("custom_field") == "value"


class TestCreateGameMessage:
    """Tests for create_game_message function."""

    def test_creates_game_message_with_game_fields(self):
        """Test game message includes league/round/match IDs."""
        msg = create_game_message(
            "GAME_MSG", "referee", "REF01", "league-1", 1, "match-1"
        )
        assert Field.LEAGUE_ID in msg
        assert Field.ROUND_ID in msg
        assert Field.MATCH_ID in msg

    def test_league_id_set_correctly(self):
        """Test league ID is set correctly."""
        msg = create_game_message(
            "GAME_MSG", "referee", "REF01", "test-league", 1, "match-1"
        )
        assert msg[Field.LEAGUE_ID] == "test-league"

    def test_round_id_set_correctly(self):
        """Test round ID is set correctly."""
        msg = create_game_message(
            "GAME_MSG", "referee", "REF01", "league-1", 5, "match-1"
        )
        assert msg[Field.ROUND_ID] == 5

    def test_match_id_set_correctly(self):
        """Test match ID is set correctly."""
        msg = create_game_message(
            "GAME_MSG", "referee", "REF01", "league-1", 1, "test-match"
        )
        assert msg[Field.MATCH_ID] == "test-match"

    def test_game_message_has_base_fields(self):
        """Test game message also includes base message fields."""
        msg = create_game_message(
            "GAME_MSG", "referee", "REF01", "league-1", 1, "match-1"
        )
        assert Field.PROTOCOL in msg
        assert Field.MESSAGE_TYPE in msg
        assert Field.SENDER in msg

    def test_game_message_with_conversation_id(self):
        """Test game message with custom conversation ID."""
        msg = create_game_message(
            "GAME_MSG", "referee", "REF01", "league-1", 1, "match-1",
            conversation_id="game-conv-123"
        )
        assert msg[Field.CONVERSATION_ID] == "game-conv-123"

    def test_game_message_extra_fields(self):
        """Test game message with extra fields."""
        msg = create_game_message(
            "GAME_MSG", "referee", "REF01", "league-1", 1, "match-1",
            extra_data="test"
        )
        assert msg.get("extra_data") == "test"
