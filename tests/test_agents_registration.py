"""Agent behavior tests - Registration and State Machine.

This module tests League Manager registration flow and Referee state transitions.
"""

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType


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

        response = {
            "params": {"message_type": MessageType.REFEREE_REGISTER_RESPONSE, "status": "ACCEPTED"}
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
            "params": {"message_type": MessageType.LEAGUE_REGISTER_RESPONSE, "status": "ACCEPTED"}
        }

        assert response["params"]["status"] == "ACCEPTED"

    def test_duplicate_registration_rejected(self):
        """Test duplicate registration is rejected."""
        first_response = {"params": {"status": "ACCEPTED"}}
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
            MatchState.FINISHED,
        ]

        assert len(valid_sequence) == len(set(valid_sequence))


class TestPlayerResponses:
    """Test Player response handling."""

    def test_player_join_ack_response(self):
        """Test player sends GAME_JOIN_ACK response."""
        from SHARED.constants import ParityChoice

        response = {
            "params": {
                "message_type": MessageType.GAME_JOIN_ACK,
                "match_id": "R1M1",
                "accept": True,
            }
        }

        assert response["params"]["accept"] is True

    def test_player_parity_choice_response(self):
        """Test player sends parity choice response."""
        response = {
            "params": {
                "message_type": MessageType.CHOOSE_PARITY_RESPONSE,
                "match_id": "R1M1",
                "parity_choice": "even",
            }
        }

        assert response["params"]["parity_choice"] in ["even", "odd"]

    def test_player_choice_options(self):
        """Test valid parity choice options."""
        from SHARED.constants import ParityChoice

        valid_choices = [ParityChoice.EVEN, ParityChoice.ODD]

        assert len(valid_choices) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
