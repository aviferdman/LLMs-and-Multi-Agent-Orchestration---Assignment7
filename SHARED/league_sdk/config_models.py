"""Configuration data models for the league system."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from SHARED.protocol_constants import PROTOCOL_VERSION


@dataclass
class SystemConfig:
    """System-wide configuration settings."""

    schema_version: str
    protocol_version: str = PROTOCOL_VERSION
    timeouts: Dict[str, int] = field(default_factory=dict)
    retry_policy: Dict[str, int] = field(default_factory=dict)


@dataclass
class LeagueConfig:
    """League configuration settings."""

    league_id: str
    game_type: str
    scoring: Dict[str, int]
    total_rounds: int
    matches_per_round: int = 2


@dataclass
class PlayerConfig:
    """Player agent configuration."""

    player_id: str
    display_name: str
    endpoint: str
    port: int
    game_types: List[str]
    strategy: Optional[str] = None


@dataclass
class RefereeConfig:
    """Referee agent configuration."""

    referee_id: str
    display_name: str
    endpoint: str
    port: int
    game_types: List[str]


@dataclass
class GameConfig:
    """Game-specific configuration."""

    game_id: str
    game_name: str
    rules_version: str
    max_players: int
    metadata: Dict[str, any] = field(default_factory=dict)
