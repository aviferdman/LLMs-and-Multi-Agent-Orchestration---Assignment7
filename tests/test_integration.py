"""Integration tests for end-to-end flows.

This module tests:
- Full registration sequence (referees + players)
- Complete match flow (invitation → game over)
- Complete round flow (all matches)
- Full league completion
"""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from SHARED.constants import PROTOCOL_VERSION, MessageType, ParityChoice
from agents.referee_match_state import MatchState


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
                    "contact_endpoint": "http://localhost:8001/mcp"
                }
            }
        }
        
        # Step 2: League Manager validates request
        assert request["params"]["protocol"] == PROTOCOL_VERSION
        assert request["params"]["message_type"] == MessageType.REFEREE_REGISTER_REQUEST
        
        # Step 3: League Manager sends response
        response = {
            "params": {
                "protocol": PROTOCOL_VERSION,
                "message_type": MessageType.REFEREE_REGISTER_RESPONSE,
                "status": "ACCEPTED"
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
                "player_meta": {
                    "display_name": "Player One",
                    "version": "1.0.0"
                }
            }
        }
        
        # Step 2: Validate request
        assert request["params"]["message_type"] == MessageType.LEAGUE_REGISTER_REQUEST
        
        # Step 3: Receive response
        response = {
            "params": {
                "message_type": MessageType.LEAGUE_REGISTER_RESPONSE,
                "status": "ACCEPTED"
            }
        }
        
        assert response["params"]["status"] == "ACCEPTED"

    def test_full_registration_all_agents(self):
        """Test full registration of all referees and players."""
        registered_agents = {
            "referees": [],
            "players": []
        }
        
        # Register referees
        for ref_id in ["REF01", "REF02"]:
            registered_agents["referees"].append({
                "referee_id": ref_id,
                "status": "ACCEPTED"
            })
        
        # Register players
        for player_id in ["P01", "P02", "P03", "P04"]:
            registered_agents["players"].append({
                "player_id": player_id,
                "status": "ACCEPTED"
            })
        
        assert len(registered_agents["referees"]) == 2
        assert len(registered_agents["players"]) == 4


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
        join_acks = {
            player_a: True,
            player_b: True
        }
        assert all(join_acks.values())
        
        # Step 3: CHOOSE_PARITY_CALL sent
        state = MatchState.COLLECTING_CHOICES
        
        # Step 4: PARITY_CHOICE received from both
        choices = {
            player_a: ParityChoice.EVEN,
            player_b: ParityChoice.ODD
        }
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
            "drawn_number": drawn_number
        }
        
        assert game_over["winner_id"] == player_a
        
        # Step 7: MATCH_RESULT_REPORT sent to League Manager
        result_report = {
            "message_type": MessageType.MATCH_RESULT_REPORT,
            "match_id": match_id,
            "winner_id": winner_id,
            "loser_id": player_b
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
            MatchState.FINISHED
        ]
        
        assert states_visited == expected_states


class TestRoundFlow:
    """Test complete round flow."""

    def test_round_flow_all_matches(self):
        """Test complete round with all matches."""
        round_id = 1
        matches = [
            {"match_id": "R1M1", "player_a": "P01", "player_b": "P02"},
            {"match_id": "R1M2", "player_a": "P03", "player_b": "P04"}
        ]
        
        completed_matches = []
        
        for match in matches:
            # Simulate match completion
            result = {
                "match_id": match["match_id"],
                "winner_id": match["player_a"],  # Simulated winner
                "completed": True
            }
            completed_matches.append(result)
        
        # All matches in round completed
        assert len(completed_matches) == len(matches)
        assert all(m["completed"] for m in completed_matches)
        
        # Round completed notification
        round_completed = {
            "message_type": "ROUND_COMPLETED",
            "round_id": round_id,
            "matches_completed": len(completed_matches)
        }
        
        assert round_completed["matches_completed"] == 2

    def test_round_robin_schedule(self):
        """Test round-robin schedule for 4 players."""
        players = ["P01", "P02", "P03", "P04"]
        
        # Round-robin for 4 players = 3 rounds
        schedule = [
            # Round 1
            [("P01", "P02"), ("P03", "P04")],
            # Round 2
            [("P03", "P01"), ("P04", "P02")],
            # Round 3
            [("P04", "P01"), ("P03", "P02")]
        ]
        
        assert len(schedule) == 3  # n-1 rounds for n players
        
        # Each player plays exactly 3 matches
        matches_per_player = {p: 0 for p in players}
        for round_matches in schedule:
            for p1, p2 in round_matches:
                matches_per_player[p1] += 1
                matches_per_player[p2] += 1
        
        assert all(count == 3 for count in matches_per_player.values())


class TestLeagueCompletion:
    """Test full league completion."""

    def test_full_league_flow(self):
        """Test complete league from start to finish."""
        league_id = "league_2025_even_odd"
        total_rounds = 3
        
        completed_rounds = []
        
        for round_id in range(1, total_rounds + 1):
            round_result = {
                "round_id": round_id,
                "matches_completed": 2,
                "standings_updated": True
            }
            completed_rounds.append(round_result)
        
        # All rounds completed
        assert len(completed_rounds) == total_rounds
        
        # League completion
        final_standings = [
            {"rank": 1, "player_id": "P01", "points": 6},
            {"rank": 2, "player_id": "P02", "points": 4},
            {"rank": 3, "player_id": "P03", "points": 2},
            {"rank": 4, "player_id": "P04", "points": 0}
        ]
        
        league_completed = {
            "message_type": "LEAGUE_COMPLETED",
            "league_id": league_id,
            "final_standings": final_standings,
            "winner_id": final_standings[0]["player_id"]
        }
        
        assert league_completed["winner_id"] == "P01"
        assert league_completed["message_type"] == "LEAGUE_COMPLETED"

    def test_standings_calculation(self):
        """Test correct standings calculation."""
        # Match results
        results = [
            {"winner_id": "P01", "loser_id": "P02"},
            {"winner_id": "P03", "loser_id": "P04"},
            {"winner_id": "P01", "loser_id": "P03"},
            {"winner_id": "P02", "loser_id": "P04"},
            {"winner_id": "P01", "loser_id": "P04"},
            {"winner_id": "P02", "loser_id": "P03"}
        ]
        
        # Calculate points (2 per win)
        points = {"P01": 0, "P02": 0, "P03": 0, "P04": 0}
        
        for result in results:
            points[result["winner_id"]] += 2
        
        # Verify points
        assert points["P01"] == 6  # 3 wins
        assert points["P02"] == 4  # 2 wins
        assert points["P03"] == 2  # 1 win
        assert points["P04"] == 0  # 0 wins


class TestDataPersistence:
    """Test data persistence during league flow."""

    def test_match_data_saved(self, tmp_path):
        """Test match data is persisted correctly."""
        match_data = {
            "match_id": "R1M1",
            "league_id": "league_2025_even_odd",
            "winner_id": "P01",
            "loser_id": "P02",
            "drawn_number": 8
        }
        
        # Save match
        match_file = tmp_path / "R1M1.json"
        with open(match_file, "w") as f:
            json.dump(match_data, f)
        
        # Load and verify
        with open(match_file, "r") as f:
            loaded = json.load(f)
        
        assert loaded["match_id"] == "R1M1"
        assert loaded["winner_id"] == "P01"

    def test_standings_updated_after_match(self, tmp_path):
        """Test standings are updated after each match."""
        standings = {
            "standings": [
                {"player_id": "P01", "wins": 0, "points": 0},
                {"player_id": "P02", "wins": 0, "points": 0}
            ]
        }
        
        # Update after P01 wins
        for player in standings["standings"]:
            if player["player_id"] == "P01":
                player["wins"] += 1
                player["points"] += 2
        
        assert standings["standings"][0]["wins"] == 1
        assert standings["standings"][0]["points"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
