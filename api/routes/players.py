"""Players API routes."""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from api.schemas.players import (
    MatchHistoryEntry,
    PlayerHistoryResponse,
    PlayerListResponse,
    PlayerResponse,
)

router = APIRouter(prefix="/players", tags=["Players"])

DEFAULT_LEAGUE_ID = "league_2025_even_odd"


@router.get("", response_model=PlayerListResponse, summary="List all players")
async def list_players(league_id: str = DEFAULT_LEAGUE_ID):
    """Get a list of all registered players with their stats."""
    data_dir = Path("SHARED/data/leagues") / league_id
    standings_file = data_dir / "standings.json"

    if not standings_file.exists():
        return PlayerListResponse(players=[], total=0)

    with open(standings_file, "r", encoding="utf-8") as f:
        standings = json.load(f)

    players = []
    for player in standings.get("standings", []):
        games = player.get("games_played", 0)
        wins = player.get("wins", 0)
        # Win rate as decimal (0-1), not percentage
        win_rate = (wins / games) if games > 0 else 0.0

        players.append(
            PlayerResponse(
                player_id=player.get("player_id", ""),
                name=player.get("player_id", ""),
                is_registered=True,
                is_active=True,
                wins=wins,
                losses=player.get("losses", 0),
                draws=player.get("draws", 0),
                games_played=games,
                win_rate=round(win_rate, 4),
            )
        )

    return PlayerListResponse(players=players, total=len(players))


@router.get("/{player_id}", response_model=PlayerResponse, summary="Get player details")
async def get_player(player_id: str, league_id: str = DEFAULT_LEAGUE_ID):
    """Get detailed information about a specific player."""
    result = await list_players(league_id)

    for player in result.players:
        if player.player_id == player_id:
            return player

    raise HTTPException(status_code=404, detail=f"Player '{player_id}' not found")


@router.get(
    "/{player_id}/history",
    response_model=PlayerHistoryResponse,
    summary="Get player history",
)
async def get_player_history(player_id: str):
    """Get match history for a specific player."""
    history_file = Path("SHARED/data/players") / player_id / "history.json"

    if not history_file.exists():
        return PlayerHistoryResponse(player_id=player_id, total_matches=0, matches=[])

    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    matches = []
    for match in history.get("matches", []):
        matches.append(
            MatchHistoryEntry(
                match_id=match.get("match_id", ""),
                opponent_id=match.get("opponent_id", ""),
                result=match.get("result", ""),
                player_score=match.get("player_score", 0),
                opponent_score=match.get("opponent_score", 0),
            )
        )

    return PlayerHistoryResponse(player_id=player_id, total_matches=len(matches), matches=matches)
