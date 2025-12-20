"""Game-related API schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class GameResponse(BaseModel):
    """Response model for a single game."""

    game_id: str = Field(..., description="Unique game identifier")
    name: str = Field(..., description="Display name of the game")
    description: str = Field(..., description="Game description")
    min_players: int = Field(..., ge=2, description="Minimum players required")
    max_players: int = Field(..., ge=2, description="Maximum players allowed")
    rules: Optional[str] = Field(None, description="Game rules in markdown")
    rules_version: str = Field(default="1.0", description="Rules version")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "game_id": "even_odd",
                "name": "Even-Odd Parity Game",
                "description": "Players choose even or odd numbers",
                "min_players": 2,
                "max_players": 8,
                "rules": "Each player picks a number...",
                "rules_version": "1.0",
            }
        }


class GameListResponse(BaseModel):
    """Response model for list of games."""

    games: List[GameResponse]
    total: int = Field(..., description="Total number of games available")
