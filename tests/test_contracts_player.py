"""Player contract compliance tests.

Tests all Player message contracts as defined in
doc/protocol/v2/PLAYER.md
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, ParityChoice
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.player_contracts import build_game_join_ack, build_parity_choice


class TestGameJoinAckContract:
    """Test GAME_JOIN_ACK contract."""

    def test_game_join_ack_structure(self):
        """GAME_JOIN_ACK must have all required fields."""
        msg = build_game_join_ack(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            conversation_id="conv-123",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_JOIN_ACK
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "P01"
        assert msg[Field.CONVERSATION_ID] == "conv-123"

    def test_game_join_ack_preserves_conversation_id(self):
        """GAME_JOIN_ACK must use provided conversation_id."""
        original_conv_id = "880e8400-e29b-41d4-a716-446655440003"
        msg = build_game_join_ack(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            conversation_id=original_conv_id,
        )
        assert msg[Field.CONVERSATION_ID] == original_conv_id

    def test_game_join_ack_is_valid_base_message(self):
        """GAME_JOIN_ACK must pass base message validation."""
        msg = build_game_join_ack(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            conversation_id="conv-123",
        )
        assert validate_base_message(msg) is True

    def test_game_join_ack_timestamp_is_utc(self):
        """GAME_JOIN_ACK timestamp must end with Z (UTC)."""
        msg = build_game_join_ack(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            conversation_id="conv-123",
        )
        assert msg[Field.TIMESTAMP].endswith("Z")


class TestParityChoiceContract:
    """Test PARITY_CHOICE contract."""

    def test_parity_choice_structure(self):
        """PARITY_CHOICE must have all required fields."""
        msg = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id="conv-123",
        )

        assert msg[Field.PROTOCOL] == PROTOCOL_VERSION
        assert msg[Field.MESSAGE_TYPE] == MessageType.PARITY_CHOICE
        assert msg[Field.LEAGUE_ID] == "league_2025"
        assert msg[Field.ROUND_ID] == 1
        assert msg[Field.MATCH_ID] == "R1M1"
        assert msg[Field.SENDER] == "P01"
        assert msg[Field.CHOICE] == ParityChoice.EVEN
        assert msg[Field.CONVERSATION_ID] == "conv-123"

    def test_parity_choice_even(self):
        """PARITY_CHOICE accepts EVEN choice."""
        msg = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id="conv-123",
        )
        assert msg[Field.CHOICE] == ParityChoice.EVEN

    def test_parity_choice_odd(self):
        """PARITY_CHOICE accepts ODD choice."""
        msg = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.ODD,
            conversation_id="conv-123",
        )
        assert msg[Field.CHOICE] == ParityChoice.ODD

    def test_parity_choice_preserves_conversation_id(self):
        """PARITY_CHOICE must use provided conversation_id."""
        original_conv_id = "880e8400-e29b-41d4-a716-446655440003"
        msg = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id=original_conv_id,
        )
        assert msg[Field.CONVERSATION_ID] == original_conv_id

    def test_parity_choice_is_valid_base_message(self):
        """PARITY_CHOICE must pass base message validation."""
        msg = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id="conv-123",
        )
        assert validate_base_message(msg) is True

    def test_parity_choice_timestamp_is_utc(self):
        """PARITY_CHOICE timestamp must end with Z (UTC)."""
        msg = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id="conv-123",
        )
        assert msg[Field.TIMESTAMP].endswith("Z")


class TestValidChoiceValues:
    """Test valid choice values for players."""

    def test_valid_choices_are_lowercase(self):
        """Valid choices must be lowercase strings per spec."""
        assert ParityChoice.EVEN == "even"
        assert ParityChoice.ODD == "odd"

    def test_choice_validation_logic(self):
        """Simulate choice validation logic (case-insensitive)."""
        valid_choices = [ParityChoice.EVEN.lower(), ParityChoice.ODD.lower()]

        # Valid choices (lowercase as per spec)
        assert "even" in valid_choices
        assert "odd" in valid_choices

        # Invalid values
        assert "maybe" not in valid_choices  # Invalid value
        assert "" not in valid_choices  # Empty string


class TestConversationIdTracking:
    """Test conversation ID tracking for players."""

    def test_conversation_id_flows_through_game(self):
        """Conversation ID must flow from invitation to choice."""
        conv_id = "test-conv-id-12345"

        # Player receives invitation and responds with same conv_id
        join_ack = build_game_join_ack(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            conversation_id=conv_id,
        )
        assert join_ack[Field.CONVERSATION_ID] == conv_id

        # Player receives call and responds with same conv_id
        choice = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id=conv_id,
        )
        assert choice[Field.CONVERSATION_ID] == conv_id

    def test_multiple_matches_have_different_conversation_ids(self):
        """Different matches should have different conversation IDs."""
        match1_conv_id = "conv-match1"
        match2_conv_id = "conv-match2"

        choice1 = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id=match1_conv_id,
        )

        choice2 = build_parity_choice(
            league_id="league_2025",
            round_id=2,
            match_id="R2M1",
            player_id="P01",
            choice=ParityChoice.ODD,
            conversation_id=match2_conv_id,
        )

        assert choice1[Field.CONVERSATION_ID] != choice2[Field.CONVERSATION_ID]


class TestPlayerIdConsistency:
    """Test player ID consistency in messages."""

    def test_sender_is_player_id(self):
        """Sender field must be the player ID."""
        msg = build_game_join_ack(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            conversation_id="conv-123",
        )
        assert msg[Field.SENDER] == "P01"

    def test_different_players_have_different_senders(self):
        """Different players have different sender values."""
        msg_p01 = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P01",
            choice=ParityChoice.EVEN,
            conversation_id="conv-123",
        )

        msg_p02 = build_parity_choice(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            player_id="P02",
            choice=ParityChoice.ODD,
            conversation_id="conv-456",
        )

        assert msg_p01[Field.SENDER] == "P01"
        assert msg_p02[Field.SENDER] == "P02"


class TestMatchContext:
    """Test match context fields in player messages."""

    def test_game_join_ack_preserves_match_context(self):
        """GAME_JOIN_ACK preserves league, round, and match IDs."""
        msg = build_game_join_ack(
            league_id="league_2025_even_odd",
            round_id=2,
            match_id="R2M1",
            player_id="P03",
            conversation_id="conv-789",
        )

        assert msg[Field.LEAGUE_ID] == "league_2025_even_odd"
        assert msg[Field.ROUND_ID] == 2
        assert msg[Field.MATCH_ID] == "R2M1"

    def test_parity_choice_preserves_match_context(self):
        """PARITY_CHOICE preserves league, round, and match IDs."""
        msg = build_parity_choice(
            league_id="league_2025_even_odd",
            round_id=3,
            match_id="R3M2",
            player_id="P04",
            choice=ParityChoice.ODD,
            conversation_id="conv-abc",
        )

        assert msg[Field.LEAGUE_ID] == "league_2025_even_odd"
        assert msg[Field.ROUND_ID] == 3
        assert msg[Field.MATCH_ID] == "R3M2"
