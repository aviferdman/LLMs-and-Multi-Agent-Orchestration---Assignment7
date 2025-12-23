"""Endpoint caching and lookup utilities.

This module provides the core data structures for caching agent endpoints.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class EndpointCache:
    """Caches and provides lookup for agent endpoints."""

    def __init__(self):
        """Initialize empty endpoint cache."""
        self.config: Dict[str, Any] = {}
        self.player_endpoints: Dict[str, str] = {}
        self.referee_endpoints: Dict[str, str] = {}
        self.loaded = False

    def load_from_file(self, config_path: Path) -> None:
        """Load endpoints from configuration file.

        Args:
            config_path: Path to agents_config.json
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Agents config not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self._build_player_lookup()
        self._build_referee_lookup()
        self.loaded = True

    def _build_player_lookup(self) -> None:
        """Build player endpoint lookup from config."""
        for player in self.config.get("players", []):
            player_id = player.get("player_id")
            endpoint = player.get("endpoint")
            if player_id and endpoint:
                self.player_endpoints[player_id] = endpoint

    def _build_referee_lookup(self) -> None:
        """Build referee endpoint lookup from config."""
        for referee in self.config.get("referees", []):
            referee_id = referee.get("referee_id")
            endpoint = referee.get("endpoint")
            if referee_id and endpoint:
                self.referee_endpoints[referee_id] = endpoint

    def get_player(self, player_id: str) -> Optional[str]:
        """Get player endpoint by ID."""
        return self.player_endpoints.get(player_id)

    def get_referee(self, referee_id: str) -> Optional[str]:
        """Get referee endpoint by ID."""
        return self.referee_endpoints.get(referee_id)

    def get_league_manager(self) -> Optional[str]:
        """Get League Manager endpoint."""
        return self.config.get("league_manager", {}).get("endpoint")

    def clear(self) -> None:
        """Clear all cached data."""
        self.loaded = False
        self.player_endpoints.clear()
        self.referee_endpoints.clear()
