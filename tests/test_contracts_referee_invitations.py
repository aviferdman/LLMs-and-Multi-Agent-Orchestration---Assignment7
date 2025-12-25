"""Referee contract compliance tests - Part 1: Invitations and Parity.

Tests GAME_INVITATION and CHOOSE_PARITY_CALL contracts as defined in
doc/protocol/v2/CONTRACTS.md
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.referee_contracts import (
    build_choose_parity_call,
    build_game_invitation,
)
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request."""
    return extract_jsonrpc_params(msg)


class TestGameInvitationContract:
    """Test GAME_INVITATION contract."""

    def test_game_invitation_structure(self):
        """GAME_INVITATION must have all required fields."""
        msg = build_game_invitation(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            role_in_match="player_a", game_type="even_odd",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
        assert params[Field.LEAGUE_ID] == "league_2025"
        assert params[Field.ROUND_ID] == 1
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.SENDER] == "referee:REF01"
        assert Field.TIMESTAMP in params
        assert Field.CONVERSATION_ID in params
        assert params[Field.OPPONENT_ID] == "P02"
        assert params[Field.ROLE_IN_MATCH] == "player_a"
        assert params[Field.GAME_TYPE] == "even_odd"

    def test_game_invitation_is_valid_base_message(self):
        """GAME_INVITATION params must pass base message validation."""
        msg = build_game_invitation(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02", role_in_match="player_a",
        )
        params = get_params(msg)
        assert validate_base_message(params) is True

    def test_game_invitation_timestamp_is_utc(self):
        """GAME_INVITATION timestamp must end with Z (UTC)."""
        msg = build_game_invitation(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02", role_in_match="player_b",
        )
        params = get_params(msg)
        assert params[Field.TIMESTAMP].endswith("Z")


class TestChooseParityCallContract:
    """Test CHOOSE_PARITY_CALL contract."""

    def test_choose_parity_call_structure(self):
        """CHOOSE_PARITY_CALL must have all required fields."""
        msg = build_choose_parity_call(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            player_standings={"wins": 0, "losses": 0, "draws": 0}, timeout_seconds=30,
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL
        assert params[Field.MATCH_ID] == "R1M1"
        assert params[Field.SENDER] == "referee:REF01"
        assert params[Field.PLAYER_ID] == "P01"
        assert Field.DEADLINE in params
        assert Field.CONTEXT in params
        assert params[Field.CONTEXT]["opponent_id"] == "P02"
        assert params[Field.CONTEXT]["round_id"] == 1

    def test_choose_parity_call_is_valid_base_message(self):
        """CHOOSE_PARITY_CALL params must pass base message validation."""
        msg = build_choose_parity_call(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            player_standings={}, timeout_seconds=30,
        )
        params = get_params(msg)
        assert validate_base_message(params) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
