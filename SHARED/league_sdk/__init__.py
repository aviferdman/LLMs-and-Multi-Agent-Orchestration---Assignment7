"""League SDK - Core components for AI Agent League Competition System."""

from .config_models import (
    SystemConfig,
    LeagueConfig,
    PlayerConfig,
    RefereeConfig,
    GameConfig,
)
from .config_loader import (
    load_system_config,
    load_league_config,
    load_agent_config,
    load_game_config,
)

__version__ = "1.0.0"
__all__ = [
    "SystemConfig",
    "LeagueConfig",
    "PlayerConfig",
    "RefereeConfig",
    "GameConfig",
    "load_system_config",
    "load_league_config",
    "load_agent_config",
    "load_game_config",
]
