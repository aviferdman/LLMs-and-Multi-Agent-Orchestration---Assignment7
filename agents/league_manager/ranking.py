"""League Manager - Ranking and standings service."""

from typing import Any, Dict, List

from SHARED.constants import Winner
from SHARED.league_sdk.config_models import LeagueConfig
from SHARED.league_sdk.repositories import StandingsRepository


def calculate_rankings(standings_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calculate rankings based on points and wins.

    Primary: Points (descending)
    Tiebreaker: Wins (descending)
    """
    sorted_standings = sorted(standings_data, key=lambda p: (p["points"], p["wins"]), reverse=True)

    for rank, player in enumerate(sorted_standings, start=1):
        player["rank"] = rank

    return sorted_standings


def update_standings(
    player_a: str, player_b: str, winner: str, league_config: LeagueConfig
) -> None:
    """Update standings based on match result."""
    standings_repo = StandingsRepository(league_config.league_id)
    standings = standings_repo.load()

    scoring = league_config.scoring

    # Normalize winner value - could be Winner.PLAYER_A, Winner.PLAYER_B, Winner.DRAW, 
    # or an actual player ID (like "P01", "P02")
    if winner == player_a or winner == Winner.PLAYER_A:
        winner_normalized = Winner.PLAYER_A
    elif winner == player_b or winner == Winner.PLAYER_B:
        winner_normalized = Winner.PLAYER_B
    elif winner == Winner.DRAW or winner is None:
        winner_normalized = Winner.DRAW
    else:
        # Unknown winner value, treat as draw
        winner_normalized = Winner.DRAW

    # Update player statistics
    for player in standings["standings"]:
        if player["player_id"] == player_a:
            if winner_normalized == Winner.PLAYER_A:
                player["wins"] += 1
                player["points"] += scoring["win_points"]
            elif winner_normalized == Winner.DRAW:
                player["draws"] += 1
                player["points"] += scoring["draw_points"]
            else:
                player["losses"] += 1
            player["games_played"] += 1

        elif player["player_id"] == player_b:
            if winner_normalized == Winner.PLAYER_B:
                player["wins"] += 1
                player["points"] += scoring["win_points"]
            elif winner_normalized == Winner.DRAW:
                player["draws"] += 1
                player["points"] += scoring["draw_points"]
            else:
                player["losses"] += 1
            player["games_played"] += 1

    # Recalculate rankings
    standings["standings"] = calculate_rankings(standings["standings"])

    # Save updated standings
    standings_repo.save(standings)


def get_current_standings(league_id: str) -> List[Dict[str, Any]]:
    """Get current standings for league."""
    standings_repo = StandingsRepository(league_id)
    standings = standings_repo.load()
    return standings.get("standings", [])
