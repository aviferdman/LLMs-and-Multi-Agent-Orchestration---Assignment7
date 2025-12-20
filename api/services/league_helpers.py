"""Helper functions for league service operations."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from api.schemas.league import LeagueStatus, PlayerStanding


def load_standings(data_dir: Path, league_id: str) -> Dict[str, Any]:
    """Load standings from file."""
    standings_path = data_dir / "leagues" / league_id / "standings.json"
    if not standings_path.exists():
        return {}
    with open(standings_path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_matches(data_dir: Path, league_id: str) -> List[Dict[str, Any]]:
    """List all match files."""
    matches_dir = data_dir / "matches" / league_id
    if not matches_dir.exists():
        return []
    matches = []
    for match_file in matches_dir.glob("*.json"):
        with open(match_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Map actual field names to expected field names
            match = {
                "match_id": data.get("match_id", ""),
                "player1_id": data.get("player_a", data.get("player1_id", "")),
                "player2_id": data.get("player_b", data.get("player2_id", "")),
                "round_number": data.get("round_id", data.get("round_number", 0)),
                "status": data.get("status", "completed"),
                "winner_id": _map_winner(data),
                "player1_score": data.get("player1_score", 0),
                "player2_score": data.get("player2_score", 0),
                "timestamp": data.get("timestamp"),
            }
            matches.append(match)
    return matches


def _map_winner(data: Dict[str, Any]) -> str:
    """Map winner field from data format to player ID."""
    winner = data.get("winner", data.get("winner_id"))
    if not winner:
        return None
    if winner == "PLAYER_A":
        return data.get("player_a", data.get("player1_id", ""))
    if winner == "PLAYER_B":
        return data.get("player_b", data.get("player2_id", ""))
    if winner == "DRAW":
        return None
    return winner


def determine_status(standings: Dict, completed: int, total: int) -> LeagueStatus:
    """Determine league status."""
    if not standings:
        return LeagueStatus.NOT_STARTED
    if completed >= total:
        return LeagueStatus.COMPLETED
    if completed > 0:
        return LeagueStatus.IN_PROGRESS
    return LeagueStatus.REGISTERING


def get_current_round(standings: Dict, matches: List[Dict] = None) -> int:
    """Get current round number from matches."""
    if matches:
        if not matches:
            return 0
        return max(m.get("round_number", 0) for m in matches)
    # Fallback to standings if no matches provided
    if not standings.get("standings"):
        return 0
    max_games = max((p.get("games_played", 0) for p in standings["standings"]), default=0)
    return max_games


def parse_standings_to_response(standings: Dict, league_id: str) -> List[PlayerStanding]:
    """Parse standings dict to PlayerStanding objects."""
    player_standings = []
    for idx, player in enumerate(standings.get("standings", []), 1):
        player_standings.append(
            PlayerStanding(
                player_id=player.get("player_id", ""),
                rank=idx,
                wins=player.get("wins", 0),
                losses=player.get("losses", 0),
                draws=player.get("draws", 0),
                games_played=player.get("games_played", 0),
                points=player.get("wins", 0) * 3 + player.get("draws", 0),
            )
        )

    # Sort by points descending
    player_standings.sort(key=lambda x: x.points, reverse=True)
    for idx, ps in enumerate(player_standings, 1):
        ps.rank = idx

    return player_standings


def load_league_config(config_dir: Path, league_id: str) -> Dict[str, Any]:
    """Load league configuration from file."""
    config_path = config_dir / "leagues" / f"{league_id}.json"
    if not config_path.exists():
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_agents_config(config_dir: Path) -> Dict[str, Any]:
    """Load agents configuration from file."""
    agents_path = config_dir / "agents" / "agents_config.json"
    if not agents_path.exists():
        return {}
    with open(agents_path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_available_leagues(data_dir: Path) -> List[str]:
    """List all available league IDs from matches directory."""
    matches_dir = data_dir / "matches"
    if not matches_dir.exists():
        return []
    return [d.name for d in matches_dir.iterdir() if d.is_dir()]
