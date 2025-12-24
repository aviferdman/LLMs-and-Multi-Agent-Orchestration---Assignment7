"""League API routes."""

import subprocess
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

from api.schemas.league import (
    AgentsStatusResponse,
    LeagueConfigResponse,
    LeagueStatus,
    LeagueStatusResponse,
    StandingsResponse,
    StartLeagueRequest,
    StartLeagueResponse,
)
from api.services.game_service import GameService
from api.services.league_service import LeagueService

router = APIRouter(prefix="/league", tags=["League"])
league_service = LeagueService()
game_service = GameService()

# Default league ID
DEFAULT_LEAGUE_ID = "league_2025_even_odd"


@router.get("/list", summary="List available leagues")
async def list_leagues():
    """Get list of all available league IDs."""
    leagues = league_service.list_leagues()
    return {"leagues": leagues, "default": leagues[-1] if leagues else DEFAULT_LEAGUE_ID}


@router.get("/status", response_model=LeagueStatusResponse, summary="Get league status")
async def get_league_status(league_id: str = DEFAULT_LEAGUE_ID):
    """Get current status of the league including progress and participants."""
    status = league_service.get_league_status(league_id)
    if not status:
        # Return default not-started status
        return LeagueStatusResponse(
            league_id=league_id,
            status=LeagueStatus.NOT_STARTED,
            game_type="even_odd",
            current_round=0,
            total_rounds=3,
            matches_completed=0,
            matches_total=6,
            players_registered=0,
            referees_registered=0,
        )
    return status


@router.get("/standings", response_model=StandingsResponse, summary="Get league standings")
async def get_league_standings(league_id: str = DEFAULT_LEAGUE_ID):
    """Get current standings sorted by points."""
    standings = league_service.get_standings(league_id)
    if not standings:
        raise HTTPException(status_code=404, detail="Standings not found")
    return standings


@router.get("/config", response_model=LeagueConfigResponse, summary="Get league configuration")
async def get_league_config(league_id: str = DEFAULT_LEAGUE_ID):
    """Get league configuration including scoring and rounds."""
    config = league_service.get_league_config(league_id)
    if not config:
        raise HTTPException(status_code=404, detail="League config not found")
    return config


@router.get("/agents", response_model=AgentsStatusResponse, summary="Get agents status")
async def get_agents_status():
    """Check if all required agents are registered and ready."""
    return league_service.get_agents_status()


@router.post("/start", response_model=StartLeagueResponse, summary="Start a league")
async def start_league(request: StartLeagueRequest):
    """
    Start a new league with the specified configuration.

    This will launch the league manager and all agents, then begin the tournament.
    """
    # Validate game exists
    game = game_service.get_game(request.game_id)
    if not game:
        raise HTTPException(status_code=400, detail=f"Game '{request.game_id}' not found")

    # Validate player count
    if not game_service.validate_player_count(request.game_id, request.num_players):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid player count. {game.name} requires "
            f"{game.min_players}-{game.max_players} players",
        )

    # Generate league ID and validate uniqueness
    league_id = request.league_name.lower().replace(" ", "_")
    existing_leagues = league_service.list_leagues()
    if league_id in existing_leagues:
        raise HTTPException(
            status_code=400,
            detail=f"League name '{request.league_name}' already exists. Please choose a unique name.",
        )

    try:
        # Launch the league using run_league.py
        project_root = Path(__file__).parent.parent.parent
        run_league_path = project_root / "run_league.py"

        # Start the league in background
        subprocess.Popen(
            [sys.executable, str(run_league_path)],
            cwd=str(project_root),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return StartLeagueResponse(
            success=True,
            league_id=league_id,
            message=f"League '{league_id}' started with {request.num_players} players",
            status=LeagueStatus.IN_PROGRESS,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start league: {e}")
