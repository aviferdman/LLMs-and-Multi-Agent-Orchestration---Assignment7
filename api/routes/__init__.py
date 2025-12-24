"""API route modules."""

from .games import router as games_router
from .league import router as league_router
from .matches import router as matches_router
from .players import router as players_router

__all__ = ["league_router", "games_router", "matches_router", "players_router"]
