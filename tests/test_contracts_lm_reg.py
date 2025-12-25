"""League Manager registration contract compliance tests.

Tests referee and player registration message contracts.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.contracts.league_manager_contracts import (
    build_league_register_request,
    build_league_register_response,
    build_referee_register_request,
    build_referee_register_response,
)
from SHARED.protocol_constants import JSONRPC_VERSION


def get_params(msg):
    """Extract params from JSON-RPC request or result from response."""
    if "params" in msg:
        return msg["params"]
    if "result" in msg:
        return msg["result"]
    return msg


class TestRefereeRegistrationContract:
    """Test REFEREE_REGISTER_REQUEST/RESPONSE contracts."""

    def test_referee_register_request_structure(self):
        """REFEREE_REGISTER_REQUEST must have required fields."""
        msg = build_referee_register_request(
            referee_id="REF01", display_name="Test Referee",
            version="1.0.0", contact_endpoint="http://localhost:8001/mcp",
        )
        assert msg["jsonrpc"] == JSONRPC_VERSION
        assert "method" in msg and "id" in msg
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_REQUEST
        assert params[Field.SENDER] == "referee:REF01"
        assert Field.REFEREE_META in params

    def test_referee_register_response_structure(self):
        """REFEREE_REGISTER_RESPONSE must have required fields."""
        msg = build_referee_register_response(referee_id="REF01", status=Status.ACCEPTED)
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_RESPONSE

    def test_referee_register_response_rejected(self):
        """REFEREE_REGISTER_RESPONSE can indicate rejection."""
        msg = build_referee_register_response(
            referee_id="REF01", status=Status.REJECTED, reason="Duplicate",
        )
        params = get_params(msg)
        assert params[Field.STATUS] == Status.REJECTED


class TestPlayerRegistrationContract:
    """Test LEAGUE_REGISTER_REQUEST/RESPONSE contracts."""

    def test_league_register_request_structure(self):
        """LEAGUE_REGISTER_REQUEST must have required fields."""
        msg = build_league_register_request(
            player_id="P01", display_name="Test Player",
            version="1.0.0", contact_endpoint="http://localhost:8101/mcp",
        )
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_REQUEST
        assert Field.PLAYER_META in params

    def test_league_register_response_structure(self):
        """LEAGUE_REGISTER_RESPONSE must have required fields."""
        msg = build_league_register_response(player_id="P01", status=Status.ACCEPTED)
        params = get_params(msg)
        assert params[Field.PROTOCOL] == PROTOCOL_VERSION
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_RESPONSE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
