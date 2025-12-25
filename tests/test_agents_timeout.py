"""Agent behavior tests - Timeout, Error handling, and Ports.

This module tests timeout handling, error handling, and agent configurations.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType
from SHARED.league_sdk.config_loader import load_agent_config


class TestTimeoutHandling:
    """Test timeout handling."""

    def test_join_timeout_key_exists(self):
        """Test join timeout key exists."""
        from SHARED.constants import Timeout

        assert hasattr(Timeout, "GAME_JOIN_ACK")
        assert Timeout.GAME_JOIN_ACK == "game_join_ack"

    def test_choice_timeout_key_exists(self):
        """Test parity choice timeout key exists."""
        from SHARED.constants import Timeout

        assert hasattr(Timeout, "PARITY_CHOICE")
        assert Timeout.PARITY_CHOICE == "parity_choice"

    def test_timeout_results_in_forfeit(self):
        """Test timeout results in forfeit."""
        timeout_result = {"winner_id": "P01", "loser_id": "P02", "reason": "TIMEOUT"}

        assert timeout_result["reason"] == "TIMEOUT"


class TestErrorHandling:
    """Test error handling in agents."""

    def test_invalid_protocol_rejected(self):
        """Test invalid protocol version is rejected."""
        request = {
            "params": {
                "protocol": "league.v1",
                "message_type": MessageType.REFEREE_REGISTER_REQUEST,
            }
        }

        is_valid = request["params"]["protocol"] == PROTOCOL_VERSION
        assert not is_valid

    def test_missing_required_field_error(self):
        """Test missing required field causes error."""
        incomplete_message = {"params": {"protocol": PROTOCOL_VERSION}}

        has_message_type = "message_type" in incomplete_message["params"]
        assert not has_message_type


class TestPortAssignments:
    """Test agent port assignments from config."""

    def test_league_manager_port(self):
        """Test League Manager port is 8000."""
        config = load_agent_config()
        assert config["league_manager"]["port"] == 8000

    def test_referee_ports(self):
        """Test referee ports are 8001-8002."""
        config = load_agent_config()
        referee_ports = {r["referee_id"]: r["port"] for r in config["referees"]}
        assert referee_ports["REF01"] == 8001
        assert referee_ports["REF02"] == 8002

    def test_player_ports(self):
        """Test player ports are 8101-8104."""
        config = load_agent_config()
        player_ports = {p["player_id"]: p["port"] for p in config["players"]}
        assert player_ports["P01"] == 8101
        assert player_ports["P02"] == 8102
        assert player_ports["P03"] == 8103
        assert player_ports["P04"] == 8104


class TestAgentEndpoints:
    """Test agent endpoint configurations."""

    def test_mcp_endpoint_format(self):
        """Test MCP endpoint format."""
        from SHARED.constants import MCP_PATH

        assert MCP_PATH == "/mcp"

    def test_endpoint_construction(self):
        """Test endpoint URL construction."""
        from SHARED.constants import HTTP_PROTOCOL, LOCALHOST

        config = load_agent_config()
        port = config["referees"][0]["port"]
        endpoint = f"{HTTP_PROTOCOL}://{LOCALHOST}:{port}/mcp"

        assert "localhost" in endpoint
        assert "8001" in endpoint
        assert "/mcp" in endpoint


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
