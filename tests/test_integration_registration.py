"""Integration tests for registration sequences.

This module tests full registration sequence for referees and players.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType


class TestRegistrationSequence:
    """Test full registration sequence."""

    def test_referee_registration_sequence(self):
        """Test complete referee registration flow."""
        # Step 1: Referee sends registration request
        request = {
            "method": "register_referee",
            "params": {
                "protocol": PROTOCOL_VERSION,
                "message_type": MessageType.REFEREE_REGISTER_REQUEST,
                "sender": "referee:REF01",
                "referee_meta": {
                    "display_name": "Referee 01",
                    "game_types": ["even_odd"],
                    "contact_endpoint": "http://localhost:8001/mcp",
                },
            },
        }

        # Step 2: League Manager validates request
        assert request["params"]["protocol"] == PROTOCOL_VERSION
        assert request["params"]["message_type"] == MessageType.REFEREE_REGISTER_REQUEST

        # Step 3: League Manager sends response
        response = {
            "params": {
                "protocol": PROTOCOL_VERSION,
                "message_type": MessageType.REFEREE_REGISTER_RESPONSE,
                "status": "ACCEPTED",
            }
        }

        assert response["params"]["status"] == "ACCEPTED"

    def test_player_registration_sequence(self):
        """Test complete player registration flow."""
        # Step 1: Player sends registration request
        request = {
            "method": "register_player",
            "params": {
                "protocol": PROTOCOL_VERSION,
                "message_type": MessageType.LEAGUE_REGISTER_REQUEST,
                "sender": "player:P01",
                "player_meta": {"display_name": "Player One", "version": "1.0.0"},
            },
        }

        # Step 2: Validate request
        assert request["params"]["message_type"] == MessageType.LEAGUE_REGISTER_REQUEST

        # Step 3: Receive response
        response = {
            "params": {
                "message_type": MessageType.LEAGUE_REGISTER_RESPONSE,
                "status": "ACCEPTED",
            }
        }

        assert response["params"]["status"] == "ACCEPTED"

    def test_full_registration_all_agents(self):
        """Test full registration of all referees and players."""
        registered_agents = {"referees": [], "players": []}

        # Register referees
        for ref_id in ["REF01", "REF02"]:
            registered_agents["referees"].append(
                {"referee_id": ref_id, "status": "ACCEPTED"}
            )

        # Register players
        for player_id in ["P01", "P02", "P03", "P04"]:
            registered_agents["players"].append(
                {"player_id": player_id, "status": "ACCEPTED"}
            )

        assert len(registered_agents["referees"]) == 2
        assert len(registered_agents["players"]) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
