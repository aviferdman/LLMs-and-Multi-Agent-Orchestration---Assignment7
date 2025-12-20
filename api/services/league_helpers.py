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
            matches.append(json.load(f))
    return matches


def determine_status(standings: Dict, completed: int, total: int) -> LeagueStatus:
    """Determine league status."""
    if not standings:
        return LeagueStatus.NOT_STARTED
    if completed >= total:
        return LeagueStatus.COMPLETED
    if completed > 0:
        return LeagueStatus.IN_PROGRESS
    return LeagueStatus.REGISTERING


def get_current_round(standings: Dict) -> int:
    """Get current round number."""
    if not standings.get("standings"):
        return 0
    total_games = sum(p.get("games_played", 0) for p in standings["standings"])
    return (total_games // 2) + 1


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
