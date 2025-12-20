"""League-related API schemas."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class LeagueStatus(str, Enum):
    """League status enumeration."""

    NOT_STARTED = "not_started"
    REGISTERING = "registering"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"


class PlayerStanding(BaseModel):
    """Individual player standing."""

    player_id: str
    rank: int
    wins: int = 0
    losses: int = 0
    draws: int = 0
    games_played: int = 0
    points: int = 0


class LeagueStatusResponse(BaseModel):
    """Response model for league status."""

    league_id: str
    status: LeagueStatus
    game_type: str
    current_round: int
    total_rounds: int
    matches_completed: int
    matches_total: int
    players_registered: int
    referees_registered: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class StandingsResponse(BaseModel):
    """Response model for league standings."""

    league_id: str
    last_updated: datetime
    standings: List[PlayerStanding]


class LeagueConfigResponse(BaseModel):
    """Response model for league configuration."""

    league_id: str
    game_type: str
    total_rounds: int
    matches_per_round: int
    scoring: Dict[str, int]
    timeout_seconds: int = 30


class StartLeagueRequest(BaseModel):
    """Request model for starting a league."""

    game_id: str = Field(..., description="ID of the game to play")
    num_players: int = Field(..., ge=2, le=8, description="Number of players")
    league_name: Optional[str] = Field(None, description="Custom league name")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "game_id": "even_odd",
                "num_players": 4,
                "league_name": "My Tournament",
            }
        }


class StartLeagueResponse(BaseModel):
    """Response model for league start."""

    success: bool
    league_id: str
    message: str
    status: LeagueStatus


class AgentStatus(BaseModel):
    """Status of a single agent."""

    agent_id: str
    agent_type: str  # "player" or "referee"
    is_registered: bool
    is_ready: bool
    endpoint: Optional[str] = None


class AgentsStatusResponse(BaseModel):
    """Response model for agents status."""

    players: List[AgentStatus]
    referees: List[AgentStatus]
    all_ready: bool
    message: str
