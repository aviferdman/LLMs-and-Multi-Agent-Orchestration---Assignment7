"""Live match state schemas for WebSocket."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PlayerStatus(str, Enum):
    """Player status in a live match."""

    WAITING = "waiting"
    THINKING = "thinking"
    SUBMITTED = "submitted"


class RoundResult(BaseModel):
    """Result of a single round in a match."""

    round_number: int
    player1_move: Optional[str] = None
    player2_move: Optional[str] = None
    winner: Optional[str] = None  # player_id or "draw"


class LiveMatchState(BaseModel):
    """Current state of a live match."""

    match_id: str
    player1_id: str
    player2_id: str
    player1_status: PlayerStatus = PlayerStatus.WAITING
    player2_status: PlayerStatus = PlayerStatus.WAITING
    player1_move: Optional[str] = None  # Shown immediately when submitted
    player2_move: Optional[str] = None  # Shown immediately when submitted
    current_round: int = 1
    total_rounds: int = 5
    rounds_played: List[RoundResult] = Field(default_factory=list)
    player1_score: int = 0
    player2_score: int = 0
    started_at: Optional[datetime] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class EventType(str, Enum):
    """WebSocket event types."""

    PLAYER_THINKING = "player_thinking"
    PLAYER_MOVE = "player_move"
    ROUND_RESULT = "round_result"
    MATCH_START = "match_start"
    MATCH_END = "match_end"
    LEAGUE_STATUS = "league_status"


class WebSocketMessage(BaseModel):
    """WebSocket message format."""

    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    match_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
