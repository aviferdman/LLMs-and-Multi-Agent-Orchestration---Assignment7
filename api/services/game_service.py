"""Game service for managing available games."""

from typing import List, Optional

from api.schemas.games import GameResponse


class GameService:
    """Service for game-related operations."""

    # Registry of supported games
    GAMES_REGISTRY = {
        "even_odd": {
            "game_id": "even_odd",
            "name": "Even-Odd Parity Game",
            "description": "Two players each choose a number (1-10). "
            "The sum determines the winner based on parity rules.",
            "min_players": 2,
            "max_players": 8,
            "rules_version": "1.0",
            "rules": """## Even-Odd Parity Game Rules

**Objective**: Win rounds by correctly predicting the parity of the sum.

**Gameplay**:
1. Each player secretly chooses a number from 1-10
2. Numbers are revealed simultaneously
3. The sum is calculated
4. Winner determined by parity (even/odd)

**Scoring**:
- Win: 3 points
- Draw: 1 point
- Loss: 0 points

**Tournament**: Round-robin format where each player faces every other player.
""",
        }
    }

    def list_games(self) -> List[GameResponse]:
        """List all available games."""
        return [GameResponse(**game) for game in self.GAMES_REGISTRY.values()]

    def get_game(self, game_id: str) -> Optional[GameResponse]:
        """Get a specific game by ID."""
        game_data = self.GAMES_REGISTRY.get(game_id)
        if game_data:
            return GameResponse(**game_data)
        return None

    def validate_player_count(self, game_id: str, num_players: int) -> bool:
        """Validate if player count is valid for the game."""
        game = self.GAMES_REGISTRY.get(game_id)
        if not game:
            return False
        return game["min_players"] <= num_players <= game["max_players"]
