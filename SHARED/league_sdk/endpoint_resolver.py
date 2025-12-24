"""Endpoint resolver for looking up agent endpoints from configuration.

This module provides a modular way to resolve agent endpoints (players, referees)
from the agents_config.json configuration file.
"""

from pathlib import Path
from typing import Optional

from SHARED.league_sdk.endpoint_cache import EndpointCache

# Default path to agents config
DEFAULT_AGENTS_CONFIG_PATH = Path("SHARED/config/agents/agents_config.json")


class EndpointResolver:
    """Resolves agent endpoints from configuration."""

    def __init__(self, config_path: Path = None):
        """Initialize the resolver with optional custom config path."""
        self._config_path = config_path or DEFAULT_AGENTS_CONFIG_PATH
        self._cache = EndpointCache()

    def _ensure_loaded(self) -> None:
        """Ensure configuration is loaded."""
        if not self._cache.loaded:
            self._cache.load_from_file(self._config_path)

    def get_player_endpoint(self, player_id: str) -> Optional[str]:
        """Get the endpoint URL for a player by ID."""
        self._ensure_loaded()
        return self._cache.get_player(player_id)

    def get_referee_endpoint(self, referee_id: str) -> Optional[str]:
        """Get the endpoint URL for a referee by ID."""
        self._ensure_loaded()
        return self._cache.get_referee(referee_id)

    def get_league_manager_endpoint(self) -> Optional[str]:
        """Get the League Manager's endpoint URL."""
        self._ensure_loaded()
        return self._cache.get_league_manager()

    def get_all_player_ids(self) -> list:
        """Get list of all configured player IDs."""
        self._ensure_loaded()
        return list(self._cache.player_endpoints.keys())

    def get_all_referee_ids(self) -> list:
        """Get list of all configured referee IDs."""
        self._ensure_loaded()
        return list(self._cache.referee_endpoints.keys())

    def reload(self) -> None:
        """Force reload of configuration from disk."""
        self._cache.clear()
        self._cache.load_from_file(self._config_path)


# Module-level singleton
_default_resolver: Optional[EndpointResolver] = None


def get_resolver(config_path: Path = None) -> EndpointResolver:
    """Get the endpoint resolver instance."""
    global _default_resolver
    if config_path is not None:
        return EndpointResolver(config_path)
    if _default_resolver is None:
        _default_resolver = EndpointResolver()
    return _default_resolver


def get_player_endpoint(player_id: str) -> Optional[str]:
    """Convenience function to get player endpoint."""
    return get_resolver().get_player_endpoint(player_id)


def get_referee_endpoint(referee_id: str) -> Optional[str]:
    """Convenience function to get referee endpoint."""
    return get_resolver().get_referee_endpoint(referee_id)


def get_league_manager_endpoint() -> Optional[str]:
    """Convenience function to get LM endpoint."""
    return get_resolver().get_league_manager_endpoint()
