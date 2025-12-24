"""API schema modules."""

from .common import ErrorResponse, PaginationParams, SuccessResponse
from .games import GameListResponse, GameResponse
from .league import (
    AgentsStatusResponse,
    LeagueConfigResponse,
    LeagueStatusResponse,
    StandingsResponse,
    StartLeagueRequest,
    StartLeagueResponse,
)
from .live import LiveMatchState, RoundResult, WebSocketMessage
from .matches import MatchListResponse, MatchResponse
from .players import PlayerHistoryResponse, PlayerListResponse, PlayerResponse

__all__ = [
    "ErrorResponse",
    "SuccessResponse",
    "PaginationParams",
    "GameResponse",
    "GameListResponse",
    "LeagueStatusResponse",
    "LeagueConfigResponse",
    "StandingsResponse",
    "StartLeagueRequest",
    "StartLeagueResponse",
    "AgentsStatusResponse",
    "MatchResponse",
    "MatchListResponse",
    "PlayerResponse",
    "PlayerListResponse",
    "PlayerHistoryResponse",
    "LiveMatchState",
    "RoundResult",
    "WebSocketMessage",
]
