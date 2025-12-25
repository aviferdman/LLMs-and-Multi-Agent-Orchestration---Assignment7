"""End-to-end protocol compliance tests - Registration and Invitation.

Validates registration and invitation message flows.
"""

import pytest

from SHARED.constants import Field, MessageType, Status
from SHARED.contracts import build_game_invitation, build_game_join_ack
from SHARED.contracts.league_manager_contracts import (
    build_league_register_request,
    build_league_register_response,
    build_referee_register_request,
    build_referee_register_response,
)
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params


def get_params(msg):
    """Extract params from JSON-RPC message."""
    return extract_jsonrpc_params(msg)


class TestRegistrationFlow:
    """Test registration message flow."""

    def test_player_registration(self):
        """Test player registration message flow."""
        player_reg = build_league_register_request(
            player_id="P01", display_name="Test Player 1",
            version="1.0.0", contact_endpoint="http://localhost:8101/mcp",
        )
        params = get_params(player_reg)
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_REQUEST
        assert Field.PLAYER_META in params
        assert validate_base_message(params)

    def test_player_registration_response(self):
        """Test player registration response."""
        player_resp = build_league_register_response(player_id="P01", status=Status.ACCEPTED)
        params = get_params(player_resp)
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_RESPONSE
        assert params[Field.STATUS] == Status.ACCEPTED

    def test_referee_registration(self):
        """Test referee registration message flow."""
        ref_reg = build_referee_register_request(
            referee_id="REF01", display_name="Test Referee 1",
            version="1.0.0", contact_endpoint="http://localhost:8001/mcp",
        )
        params = get_params(ref_reg)
        assert params[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_REQUEST
        assert Field.REFEREE_META in params

    def test_referee_registration_response(self):
        """Test referee registration response."""
        ref_resp = build_referee_register_response(referee_id="REF01", status=Status.ACCEPTED)
        params = get_params(ref_resp)
        assert params[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_RESPONSE


class TestInvitationFlow:
    """Test match invitation message flow."""

    def test_game_invitation(self):
        """Test game invitation message."""
        invitation = build_game_invitation(
            league_id="league_2025", round_id=1, match_id="R1M1",
            referee_id="REF01", player_id="P01", opponent_id="P02",
            role_in_match="player_a", game_type="even_odd",
        )
        params = get_params(invitation)
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
        assert params[Field.ROLE_IN_MATCH] == "player_a"
        assert validate_base_message(params)

    def test_game_join_ack(self):
        """Test game join acknowledgment."""
        join_ack = build_game_join_ack(
            match_id="R1M1", player_id="P01", conversation_id="conv-123", accept=True,
        )
        params = get_params(join_ack)
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_JOIN_ACK
        assert params[Field.ACCEPT] is True
        assert validate_base_message(params)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
