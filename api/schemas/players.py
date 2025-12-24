"""Player-related API schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PlayerResponse(BaseModel):
    """Response model for a single player."""

    player_id: str
    name: str
    is_registered: bool
    is_active: bool
    endpoint: Optional[str] = None
    wins: int = 0
    losses: int = 0
    draws: int = 0
    games_played: int = 0
    win_rate: float = 0.0


class PlayerListResponse(BaseModel):
    """Response model for list of players."""

    players: List[PlayerResponse]
    total: int


class MatchHistoryEntry(BaseModel):
    """Single match in player history."""

    match_id: str
    opponent_id: str
    result: str  # "win", "loss", "draw"
    player_score: int
    opponent_score: int
    played_at: Optional[datetime] = None


class PlayerHistoryResponse(BaseModel):
    """Response model for player match history."""

    player_id: str
    total_matches: int
    matches: List[MatchHistoryEntry]
