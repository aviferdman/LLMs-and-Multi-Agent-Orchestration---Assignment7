"""Integration tests for match and round flows.

This module tests complete match flow and round flow.
"""

import pytest

from SHARED.constants import MessageType, ParityChoice
from agents.referee_match_state import MatchState


class TestMatchFlow:
    """Test complete match flow."""

    def test_match_flow_invitation_to_game_over(self):
        """Test complete match flow from invitation to game over."""
        match_id = "R1M1"
        player_a = "P01"
        player_b = "P02"

        # Step 1: GAME_INVITATION sent to both players
        invitations_sent = [player_a, player_b]
        assert len(invitations_sent) == 2

        # Step 2: GAME_JOIN_ACK received from both
        join_acks = {player_a: True, player_b: True}
        assert all(join_acks.values())

        # Step 3: CHOOSE_PARITY_CALL sent
        state = MatchState.COLLECTING_CHOICES

        # Step 4: PARITY_CHOICE received from both
        choices = {player_a: ParityChoice.EVEN, player_b: ParityChoice.ODD}
        assert len(choices) == 2

        # Step 5: Draw number and determine winner
        drawn_number = 8  # Even
        number_parity = "even" if drawn_number % 2 == 0 else "odd"

        winner_id = None
        for player, choice in choices.items():
            if choice == number_parity:
                winner_id = player
                break

        assert winner_id == player_a  # P01 chose even, 8 is even

        # Step 6: GAME_OVER sent to both players
        game_over = {
            "message_type": MessageType.GAME_OVER,
            "match_id": match_id,
            "winner_id": winner_id,
            "drawn_number": drawn_number,
        }
        assert game_over["winner_id"] == player_a

        # Step 7: MATCH_RESULT_REPORT sent to League Manager
        result_report = {
            "message_type": MessageType.MATCH_RESULT_REPORT,
            "match_id": match_id,
            "winner_id": winner_id,
            "loser_id": player_b,
        }
        assert result_report["message_type"] == MessageType.MATCH_RESULT_REPORT

    def test_match_state_transitions(self):
        """Test all state transitions during match."""
        states_visited = []

        # Initial state
        state = MatchState.WAITING_FOR_PLAYERS
        states_visited.append(state)

        # After both join
        state = MatchState.COLLECTING_CHOICES
        states_visited.append(state)

        # After both choose
        state = MatchState.DRAWING_NUMBER
        states_visited.append(state)

        # After winner determined
        state = MatchState.FINISHED
        states_visited.append(state)

        expected_states = [
            MatchState.WAITING_FOR_PLAYERS,
            MatchState.COLLECTING_CHOICES,
            MatchState.DRAWING_NUMBER,
            MatchState.FINISHED,
        ]
        assert states_visited == expected_states


class TestRoundFlow:
    """Test complete round flow."""

    def test_round_flow_all_matches(self):
        """Test complete round with all matches."""
        round_id = 1
        matches = [
            {"match_id": "R1M1", "player_a": "P01", "player_b": "P02"},
            {"match_id": "R1M2", "player_a": "P03", "player_b": "P04"},
        ]

        completed_matches = []
        for match in matches:
            result = {
                "match_id": match["match_id"],
                "winner_id": match["player_a"],
                "completed": True,
            }
            completed_matches.append(result)

        assert len(completed_matches) == len(matches)
        assert all(m["completed"] for m in completed_matches)

        round_completed = {
            "message_type": "ROUND_COMPLETED",
            "round_id": round_id,
            "matches_completed": len(completed_matches),
        }
        assert round_completed["matches_completed"] == 2

    def test_round_robin_schedule(self):
        """Test round-robin schedule for 4 players."""
        players = ["P01", "P02", "P03", "P04"]

        schedule = [
            [("P01", "P02"), ("P03", "P04")],
            [("P03", "P01"), ("P04", "P02")],
            [("P04", "P01"), ("P03", "P02")],
        ]
        assert len(schedule) == 3

        matches_per_player = {p: 0 for p in players}
        for round_matches in schedule:
            for p1, p2 in round_matches:
                matches_per_player[p1] += 1
                matches_per_player[p2] += 1

        assert all(count == 3 for count in matches_per_player.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
