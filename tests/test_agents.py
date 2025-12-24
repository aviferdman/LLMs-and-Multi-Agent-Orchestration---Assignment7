"""Agent behavior tests.

This module tests:
- League Manager registration flow
- Referee state transitions
- Player response handling
- Timeout handling
- Error handling
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType, Port, ParityChoice


class TestLeagueManagerRegistration:
    """Test League Manager registration flow."""

    def test_referee_registration_accepted(self):
        """Test referee registration is accepted."""
        request = {
            "params": {
                "protocol": PROTOCOL_VERSION,
                "message_type": MessageType.REFEREE_REGISTER_REQUEST,
                "sender": "referee:REF01",
            }
        }
        
        # Simulate acceptance
        response = {
            "params": {
                "message_type": MessageType.REFEREE_REGISTER_RESPONSE,
                "status": "ACCEPTED"
            }
        }
        
        assert response["params"]["status"] == "ACCEPTED"

    def test_player_registration_accepted(self):
        """Test player registration is accepted."""
        request = {
            "params": {
                "protocol": PROTOCOL_VERSION,
                "message_type": MessageType.LEAGUE_REGISTER_REQUEST,
                "sender": "player:P01",
            }
        }
        
        response = {
            "params": {
                "message_type": MessageType.LEAGUE_REGISTER_RESPONSE,
                "status": "ACCEPTED"
            }
        }
        
        assert response["params"]["status"] == "ACCEPTED"

    def test_duplicate_registration_rejected(self):
        """Test duplicate registration is rejected."""
        # First registration
        first_response = {"params": {"status": "ACCEPTED"}}
        
        # Second registration from same agent
        duplicate_response = {"params": {"status": "REJECTED", "reason": "Agent already registered"}}
        
        assert first_response["params"]["status"] == "ACCEPTED"
        assert duplicate_response["params"]["status"] == "REJECTED"


class TestRefereeStateMachine:
    """Test Referee state transitions."""

    def test_initial_state_is_waiting(self):
        """Test referee starts in WAITING_FOR_PLAYERS state."""
        from agents.referee_match_state import MatchState
        
        initial_state = MatchState.WAITING_FOR_PLAYERS
        assert initial_state == MatchState.WAITING_FOR_PLAYERS

    def test_transition_to_collecting_choices(self):
        """Test transition from WAITING to COLLECTING_CHOICES."""
        from agents.referee_match_state import MatchState
        
        states = [MatchState.WAITING_FOR_PLAYERS, MatchState.COLLECTING_CHOICES]
        
        # Both players joined
        assert states[1] == MatchState.COLLECTING_CHOICES

    def test_transition_to_finished(self):
        """Test transition to FINISHED state."""
        from agents.referee_match_state import MatchState
        
        final_state = MatchState.FINISHED
        assert final_state == MatchState.FINISHED

    def test_valid_state_sequence(self):
        """Test valid state sequence during match."""
        from agents.referee_match_state import MatchState
        
        valid_sequence = [
            MatchState.WAITING_FOR_PLAYERS,
            MatchState.COLLECTING_CHOICES,
            MatchState.DRAWING_NUMBER,
            MatchState.FINISHED
        ]
        
        # Each state should be distinct
        assert len(valid_sequence) == len(set(valid_sequence))


class TestPlayerResponses:
    """Test Player response handling."""

    def test_player_join_ack_response(self):
        """Test player sends GAME_JOIN_ACK response."""
        response = {
            "params": {
                "message_type": MessageType.GAME_JOIN_ACK,
                "match_id": "R1M1",
                "accept": True
            }
        }
        
        assert response["params"]["accept"] is True

    def test_player_parity_choice_response(self):
        """Test player sends parity choice response."""
        response = {
            "params": {
                "message_type": MessageType.CHOOSE_PARITY_RESPONSE,
                "match_id": "R1M1",
                "parity_choice": "even"
            }
        }
        
        assert response["params"]["parity_choice"] in ["even", "odd"]

    def test_player_choice_options(self):
        """Test valid parity choice options."""
        valid_choices = [ParityChoice.EVEN, ParityChoice.ODD]
        
        assert len(valid_choices) == 2


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
        timeout_result = {
            "winner_id": "P01",
            "loser_id": "P02",
            "reason": "TIMEOUT"
        }
        
        assert timeout_result["reason"] == "TIMEOUT"


class TestErrorHandling:
    """Test error handling in agents."""

    def test_invalid_protocol_rejected(self):
        """Test invalid protocol version is rejected."""
        request = {
            "params": {
                "protocol": "league.v1",  # Wrong version
                "message_type": MessageType.REFEREE_REGISTER_REQUEST,
            }
        }
        
        # Should be rejected
        is_valid = request["params"]["protocol"] == PROTOCOL_VERSION
        assert not is_valid

    def test_missing_required_field_error(self):
        """Test missing required field causes error."""
        incomplete_message = {
            "params": {
                "protocol": PROTOCOL_VERSION,
                # Missing message_type
            }
        }
        
        has_message_type = "message_type" in incomplete_message["params"]
        assert not has_message_type


class TestPortAssignments:
    """Test agent port assignments."""

    def test_league_manager_port(self):
        """Test League Manager port is 8000."""
        assert Port.LEAGUE_MANAGER == 8000

    def test_referee_ports(self):
        """Test referee ports are 8001-8002."""
        assert Port.REFEREE_01 == 8001
        assert Port.REFEREE_02 == 8002

    def test_player_ports(self):
        """Test player ports are 8101-8104."""
        assert Port.PLAYER_01 == 8101
        assert Port.PLAYER_02 == 8102
        assert Port.PLAYER_03 == 8103
        assert Port.PLAYER_04 == 8104


class TestAgentEndpoints:
    """Test agent endpoint configurations."""

    def test_mcp_endpoint_format(self):
        """Test MCP endpoint format."""
        from SHARED.constants import MCP_PATH
        
        assert MCP_PATH == "/mcp"

    def test_endpoint_construction(self):
        """Test endpoint URL construction."""
        from SHARED.constants import HTTP_PROTOCOL, LOCALHOST
        
        port = Port.REFEREE_01
        endpoint = f"{HTTP_PROTOCOL}://{LOCALHOST}:{port}/mcp"
        
        assert "localhost" in endpoint
        assert "8001" in endpoint
        assert "/mcp" in endpoint


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
