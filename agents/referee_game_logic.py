"""Game logic for Even-Odd game."""

import random
from SHARED.constants import EVEN_ODD_MIN_NUMBER, EVEN_ODD_MAX_NUMBER, ParityChoice, Winner

class EvenOddGameRules:
    """Game rules for Even-Odd game."""
    
    def __init__(self):
        """Initialize game rules."""
        self.draw_range = (EVEN_ODD_MIN_NUMBER, EVEN_ODD_MAX_NUMBER)
        self.valid_choices = [ParityChoice.EVEN.lower(), ParityChoice.ODD.lower()]
    
    def draw_number(self) -> int:
        """Draw random number between 1 and 10 inclusive."""
        return random.randint(self.draw_range[0], self.draw_range[1])
    
    def get_parity(self, number: int) -> str:
        """Get parity of number (even or odd)."""
        return ParityChoice.EVEN.lower() if number % 2 == 0 else ParityChoice.ODD.lower()
    
    def validate_parity_choice(self, choice: str) -> bool:
        """Validate if parity choice is valid."""
        return choice.lower() in self.valid_choices
    
    def determine_winner(self, choice_a: str, choice_b: str, drawn_number: int) -> str:
        """Determine winner based on choices and drawn number."""
        parity = self.get_parity(drawn_number)
        a_correct = (choice_a.lower() == parity)
        b_correct = (choice_b.lower() == parity)
        
        if a_correct and not b_correct:
            return Winner.PLAYER_A
        elif b_correct and not a_correct:
            return Winner.PLAYER_B
        else:
            return Winner.DRAW
