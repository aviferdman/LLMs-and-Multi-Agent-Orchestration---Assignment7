"""Games API routes."""

from fastapi import APIRouter, HTTPException

from api.schemas.games import GameListResponse, GameResponse
from api.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["Games"])
game_service = GameService()


@router.get("", response_model=GameListResponse, summary="List available games")
async def list_games():
    """
    Get a list of all available games.

    Returns the games that can be selected when launching a new league.
    Currently supported: Even-Odd Parity Game.
    """
    games = game_service.list_games()
    return GameListResponse(games=games, total=len(games))


@router.get("/{game_id}", response_model=GameResponse, summary="Get game details")
async def get_game(game_id: str):
    """
    Get detailed information about a specific game.

    Includes rules, player count limits, and game description.
    """
    game = game_service.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
    return game
