"""WebSocket event definitions."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class EventType(str, Enum):
    """WebSocket event types."""

    PLAYER_THINKING = "player_thinking"
    PLAYER_MOVE = "player_move"
    ROUND_RESULT = "round_result"
    MATCH_START = "match_start"
    MATCH_END = "match_end"
    LEAGUE_STATUS = "league_status"
    ERROR = "error"


@dataclass
class BaseEvent:
    """Base class for all events."""

    event_type: EventType
    match_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "match_id": self.match_id,
            "timestamp": self.timestamp.isoformat() + "Z",
        }


@dataclass
class PlayerThinkingEvent(BaseEvent):
    """Event: Player is thinking (received PARITY_CALL)."""

    event_type: EventType = field(default=EventType.PLAYER_THINKING)
    player_id: str = ""
    round_number: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        data = super().to_dict()
        data["payload"] = {
            "player_id": self.player_id,
            "round_number": self.round_number,
            "status": "thinking",
        }
        return data


@dataclass
class PlayerMoveEvent(BaseEvent):
    """Event: Player submitted their move."""

    event_type: EventType = field(default=EventType.PLAYER_MOVE)
    player_id: str = ""
    move: str = ""  # The actual move (shown immediately)
    round_number: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        data = super().to_dict()
        data["payload"] = {
            "player_id": self.player_id,
            "move": self.move,
            "round_number": self.round_number,
            "status": "submitted",
        }
        return data


@dataclass
class RoundResultEvent(BaseEvent):
    """Event: Round completed with result."""

    event_type: EventType = field(default=EventType.ROUND_RESULT)
    round_number: int = 1
    player1_move: str = ""
    player2_move: str = ""
    winner: Optional[str] = None  # player_id or "draw"
    player1_score: int = 0
    player2_score: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        data = super().to_dict()
        data["payload"] = {
            "round_number": self.round_number,
            "player1_move": self.player1_move,
            "player2_move": self.player2_move,
            "winner": self.winner,
            "player1_score": self.player1_score,
            "player2_score": self.player2_score,
        }
        return data


@dataclass
class MatchStartEvent(BaseEvent):
    """Event: Match started."""

    event_type: EventType = field(default=EventType.MATCH_START)
    player1_id: str = ""
    player2_id: str = ""
    referee_id: str = ""
    total_rounds: int = 5

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        data = super().to_dict()
        data["payload"] = {
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "referee_id": self.referee_id,
            "total_rounds": self.total_rounds,
        }
        return data


@dataclass
class MatchEndEvent(BaseEvent):
    """Event: Match completed."""

    event_type: EventType = field(default=EventType.MATCH_END)
    winner_id: Optional[str] = None
    player1_final_score: int = 0
    player2_final_score: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        data = super().to_dict()
        data["payload"] = {
            "winner_id": self.winner_id,
            "player1_final_score": self.player1_final_score,
            "player2_final_score": self.player2_final_score,
            "status": "completed",
        }
        return data
