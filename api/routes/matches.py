"""Matches API routes."""

from fastapi import APIRouter, HTTPException

from api.schemas.live import LiveMatchState, PlayerStatus
from api.schemas.matches import MatchListResponse, MatchResponse
from api.services.league_service import LeagueService

router = APIRouter(prefix="/matches", tags=["Matches"])
league_service = LeagueService()

DEFAULT_LEAGUE_ID = "league_2025_even_odd"

# In-memory store for live match states (in production, use Redis)
live_matches: dict[str, LiveMatchState] = {}


@router.get("", response_model=MatchListResponse, summary="List all matches")
async def list_matches(
    league_id: str = DEFAULT_LEAGUE_ID,
    round_number: int = None,
    status: str = None,
):
    """
    Get a list of all matches in the league.

    Optionally filter by round number or status.
    """
    result = league_service.get_matches(league_id)

    # Apply filters
    matches = result.matches
    if round_number is not None:
        matches = [m for m in matches if m.round_number == round_number]
    if status is not None:
        matches = [m for m in matches if m.status.value == status]

    return MatchListResponse(matches=matches, total=len(matches))


@router.get("/{match_id}", response_model=MatchResponse, summary="Get match details")
async def get_match(match_id: str, league_id: str = DEFAULT_LEAGUE_ID):
    """Get detailed information about a specific match."""
    result = league_service.get_matches(league_id)

    for match in result.matches:
        if match.match_id == match_id:
            return match

    raise HTTPException(status_code=404, detail=f"Match '{match_id}' not found")


@router.get("/{match_id}/live", response_model=LiveMatchState, summary="Get live match state")
async def get_live_match_state(match_id: str):
    """
    Get the current live state of an in-progress match.

    Shows player thinking status and moves as they are submitted.
    """
    if match_id in live_matches:
        return live_matches[match_id]

    # Return default state if match not found in live store
    return LiveMatchState(
        match_id=match_id,
        player1_id="unknown",
        player2_id="unknown",
        player1_status=PlayerStatus.WAITING,
        player2_status=PlayerStatus.WAITING,
    )


def update_live_match(match_id: str, state: LiveMatchState):
    """Update live match state (called by WebSocket handler)."""
    live_matches[match_id] = state


def remove_live_match(match_id: str):
    """Remove match from live store when completed."""
    live_matches.pop(match_id, None)
