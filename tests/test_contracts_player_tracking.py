"""Player contract compliance tests - Tracking contracts.

Tests conversation ID tracking and sender format compliance
as defined in doc/protocol/v2/CONTRACTS.md
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import Field, ParityChoice
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.player_contracts import (
    build_game_join_ack,
    build_choose_parity_response,
)


def get_params(msg):
    """Extract params from JSON-RPC request or result from response."""
    return extract_jsonrpc_params(msg)


class TestConversationIdTracking:
    """Test conversation ID tracking for players."""

    def test_conversation_id_flows_through_game(self):
        """Conversation ID must flow from invitation to choice."""
        conv_id = "test-conv-id-12345"
        join_ack = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id=conv_id, accept=True,
        )
        assert get_params(join_ack)[Field.CONVERSATION_ID] == conv_id
        choice = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.EVEN, conversation_id=conv_id,
        )
        assert get_params(choice)[Field.CONVERSATION_ID] == conv_id

    def test_multiple_matches_have_different_conversation_ids(self):
        """Different matches should have different conversation IDs."""
        match1_conv_id = "conv-match1"
        match2_conv_id = "conv-match2"
        choice1 = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.EVEN, conversation_id=match1_conv_id,
        )
        choice2 = build_choose_parity_response(
            match_id="R2M1", player_id="P01",
            parity_choice=ParityChoice.ODD, conversation_id=match2_conv_id,
        )
        assert get_params(choice1)[Field.CONVERSATION_ID] != get_params(choice2)[Field.CONVERSATION_ID]


class TestSenderFormat:
    """Test sender format compliance."""

    def test_sender_is_prefixed_player_id(self):
        """Sender field must be prefixed player ID."""
        msg = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id="conv-123", accept=True,
        )
        params = get_params(msg)
        assert params[Field.SENDER] == "player:P01"

    def test_different_players_have_different_senders(self):
        """Different players have different sender values."""
        msg_p01 = build_choose_parity_response(
            match_id="R1M1", player_id="P01",
            parity_choice=ParityChoice.EVEN, conversation_id="conv-123",
        )
        msg_p02 = build_choose_parity_response(
            match_id="R1M1", player_id="P02",
            parity_choice=ParityChoice.ODD, conversation_id="conv-456",
        )
        assert get_params(msg_p01)[Field.SENDER] == "player:P01"
        assert get_params(msg_p02)[Field.SENDER] == "player:P02"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
