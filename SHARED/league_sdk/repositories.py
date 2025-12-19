"""Data persistence repositories."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class StandingsRepository:
    """Repository for league standings data."""

    def __init__(self, league_id: str, data_dir: Path = None):
        """Initialize standings repository."""
        if data_dir is None:
            data_dir = Path("SHARED/data/leagues")
        self.standings_file = data_dir / league_id / "standings.json"
        self.standings_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """Load standings from file."""
        if not self.standings_file.exists():
            return self._create_empty_standings()
        
        with open(self.standings_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save(self, standings: Dict[str, Any]) -> None:
        """Save standings to file."""
        with open(self.standings_file, 'w', encoding='utf-8') as f:
            json.dump(standings, f, indent=2)

    def update_player(self, player_id: str, wins: int = 0, 
                     losses: int = 0, draws: int = 0) -> None:
        """Update player statistics."""
        standings = self.load()
        
        for player in standings.get("standings", []):
            if player["player_id"] == player_id:
                player["wins"] += wins
                player["losses"] += losses
                player["draws"] += draws
                player["games_played"] = (
                    player["wins"] + player["losses"] + player["draws"]
                )
                break
        
        self.save(standings)

    def _create_empty_standings(self) -> Dict[str, Any]:
        """Create empty standings structure."""
        return {
            "version": 1,
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "standings": []
        }

class MatchRepository:
    """Repository for match data."""

    def __init__(self, league_id: str, data_dir: Path = None):
        """Initialize match repository."""
        if data_dir is None:
            data_dir = Path("SHARED/data/matches")
        self.matches_dir = data_dir / league_id
        self.matches_dir.mkdir(parents=True, exist_ok=True)

    def save_match(self, match_id: str, match_data: Dict[str, Any]) -> None:
        """Save match data to file."""
        match_file = self.matches_dir / f"{match_id}.json"
        with open(match_file, 'w', encoding='utf-8') as f:
            json.dump(match_data, f, indent=2)

    def load_match(self, match_id: str) -> Optional[Dict[str, Any]]:
        """Load match data from file."""
        match_file = self.matches_dir / f"{match_id}.json"
        if not match_file.exists():
            return None
        
        with open(match_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_matches(self) -> List[str]:
        """List all match IDs."""
        return [f.stem for f in self.matches_dir.glob("*.json")]

class PlayerHistoryRepository:
    """Repository for player history."""

    def __init__(self, player_id: str, data_dir: Path = None):
        """Initialize player history repository."""
        if data_dir is None:
            data_dir = Path("SHARED/data/players")
        self.history_file = data_dir / player_id / "history.json"
        self.history_file.parent.mkdir(parents=True, exist_ok=True)

    def save_history(self, history: Dict[str, Any]) -> None:
        """Save player history to file."""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)

    def load_history(self) -> Dict[str, Any]:
        """Load player history from file."""
        if not self.history_file.exists():
            return {"matches": []}
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def append_match(self, match_data: Dict[str, Any]) -> None:
        """Append match to player history."""
        history = self.load_history()
        history["matches"].append(match_data)
        self.save_history(history)
