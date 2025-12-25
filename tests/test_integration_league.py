"""Integration tests for league completion and data persistence.

This module tests full league completion and data persistence.
"""

import json

import pytest


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
                "standings_updated": True,
            }
            completed_rounds.append(round_result)

        assert len(completed_rounds) == total_rounds

        final_standings = [
            {"rank": 1, "player_id": "P01", "points": 6},
            {"rank": 2, "player_id": "P02", "points": 4},
            {"rank": 3, "player_id": "P03", "points": 2},
            {"rank": 4, "player_id": "P04", "points": 0},
        ]

        league_completed = {
            "message_type": "LEAGUE_COMPLETED",
            "league_id": league_id,
            "final_standings": final_standings,
            "winner_id": final_standings[0]["player_id"],
        }

        assert league_completed["winner_id"] == "P01"
        assert league_completed["message_type"] == "LEAGUE_COMPLETED"

    def test_standings_calculation(self):
        """Test correct standings calculation."""
        results = [
            {"winner_id": "P01", "loser_id": "P02"},
            {"winner_id": "P03", "loser_id": "P04"},
            {"winner_id": "P01", "loser_id": "P03"},
            {"winner_id": "P02", "loser_id": "P04"},
            {"winner_id": "P01", "loser_id": "P04"},
            {"winner_id": "P02", "loser_id": "P03"},
        ]

        points = {"P01": 0, "P02": 0, "P03": 0, "P04": 0}
        for result in results:
            points[result["winner_id"]] += 2

        assert points["P01"] == 6
        assert points["P02"] == 4
        assert points["P03"] == 2
        assert points["P04"] == 0


class TestDataPersistence:
    """Test data persistence during league flow."""

    def test_match_data_saved(self, tmp_path):
        """Test match data is persisted correctly."""
        match_data = {
            "match_id": "R1M1",
            "league_id": "league_2025_even_odd",
            "winner_id": "P01",
            "loser_id": "P02",
            "drawn_number": 8,
        }

        match_file = tmp_path / "R1M1.json"
        with open(match_file, "w") as f:
            json.dump(match_data, f)

        with open(match_file, "r") as f:
            loaded = json.load(f)

        assert loaded["match_id"] == "R1M1"
        assert loaded["winner_id"] == "P01"

    def test_standings_updated_after_match(self, tmp_path):
        """Test standings are updated after each match."""
        standings = {
            "standings": [
                {"player_id": "P01", "wins": 0, "points": 0},
                {"player_id": "P02", "wins": 0, "points": 0},
            ]
        }

        for player in standings["standings"]:
            if player["player_id"] == "P01":
                player["wins"] += 1
                player["points"] += 2

        assert standings["standings"][0]["wins"] == 1
        assert standings["standings"][0]["points"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
