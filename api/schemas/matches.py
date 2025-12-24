"""Match-related API schemas."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MatchStatus(str, Enum):
    """Match status enumeration."""

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MatchResponse(BaseModel):
    """Response model for a single match."""

    match_id: str
    round_number: int
    player1_id: str
    player2_id: str
    referee_id: Optional[str] = None
    status: MatchStatus
    winner_id: Optional[str] = None
    player1_score: int = 0
    player2_score: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    rounds_played: List[Dict[str, Any]] = Field(default_factory=list)


class MatchListResponse(BaseModel):
    """Response model for list of matches."""

    matches: List[MatchResponse]
    total: int
    page: int = 1
    page_size: int = 20
