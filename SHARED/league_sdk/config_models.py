"""Configuration data models for the league system."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from SHARED.protocol_constants import PROTOCOL_VERSION


@dataclass
class SystemConfig:
    """System-wide configuration settings."""

    schema_version: str
    protocol_version: str = PROTOCOL_VERSION
    system_id: str = ""
    active_league_id: str = ""
    timeouts: Dict[str, int] = field(default_factory=dict)
    retry_policy: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ParticipantsConfig:
    """Participants limits configuration."""

    min_players: int = 2
    max_players: int = 10000


@dataclass
class LeagueConfig:
    """League configuration settings."""

    league_id: str
    game_type: str
    scoring: Dict[str, int]
    status: str = "ACTIVE"
    participants: Optional[ParticipantsConfig] = None


@dataclass
class PlayerConfig:
    """Player agent configuration."""

    player_id: str
    display_name: str
    version: str = "1.0.0"
    preferred_leagues: List[str] = field(default_factory=list)
    game_types: List[str] = field(default_factory=list)
    default_endpoint: str = ""
    active: bool = True


@dataclass
class RefereeConfig:
    """Referee agent configuration."""

    referee_id: str
    display_name: str
    endpoint: str
    version: str = "1.0.0"
    game_types: List[str] = field(default_factory=list)
    max_concurrent_matches: int = 1
    active: bool = True


@dataclass
class GameConfig:
    """Game-specific configuration."""

    game_id: str
    game_name: str
    rules_version: str
    max_players: int
    metadata: Dict[str, Any] = field(default_factory=dict)
