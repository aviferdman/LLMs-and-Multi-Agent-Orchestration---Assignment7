"""Game logic for Even-Odd game and game rules factory."""

import random

from SHARED.constants import EVEN_ODD_MAX_NUMBER, EVEN_ODD_MIN_NUMBER, GameID, ParityChoice, Winner


class BaseGameRules:
    """Base class for all game rules - defines the interface."""

    def draw_number(self) -> int:
        """Draw a random number for the game."""
        raise NotImplementedError

    def validate_parity_choice(self, choice: str) -> bool:
        """Validate a player's choice."""
        raise NotImplementedError

    def determine_winner(self, choice_a: str, choice_b: str, drawn_number: int) -> str:
        """Determine the winner based on choices and drawn number."""
        raise NotImplementedError


class EvenOddGameRules(BaseGameRules):
    """Game rules for Even-Odd game."""

    def __init__(self):
        """Initialize game rules."""
        self.draw_range = (EVEN_ODD_MIN_NUMBER, EVEN_ODD_MAX_NUMBER)
        self.valid_choices = [ParityChoice.EVEN, ParityChoice.ODD]

    def draw_number(self) -> int:
        """Draw random number between 1 and 10 inclusive."""
        return random.randint(self.draw_range[0], self.draw_range[1])

    def get_parity(self, number: int) -> str:
        """Get parity of number (even or odd)."""
        return ParityChoice.EVEN if number % 2 == 0 else ParityChoice.ODD

    def validate_parity_choice(self, choice: str) -> bool:
        """Validate if parity choice is valid (case-insensitive per spec)."""
        return choice.lower() in self.valid_choices

    def determine_winner(self, choice_a: str, choice_b: str, drawn_number: int) -> str:
        """Determine winner based on choices and drawn number."""
        parity = self.get_parity(drawn_number)
        a_correct = choice_a.lower() == parity
        b_correct = choice_b.lower() == parity

        if a_correct and not b_correct:
            return Winner.PLAYER_A
        elif b_correct and not a_correct:
            return Winner.PLAYER_B
        else:
            return Winner.DRAW


# Game rules registry - maps game type to rules class (game-agnostic factory)
_GAME_RULES_REGISTRY = {
    GameID.EVEN_ODD: EvenOddGameRules,
}


def get_game_rules(game_type: str) -> BaseGameRules:
    """Factory function to get game rules by game type (game-agnostic)."""
    rules_class = _GAME_RULES_REGISTRY.get(game_type)
    if rules_class is None:
        raise ValueError(f"Unknown game type: {game_type}")
    return rules_class()
