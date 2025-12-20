"""Edge case tests for game logic - Part 2."""

import pytest

from agents.referee_game_logic import EvenOddGameRules


class TestEdgeCaseInvalidParityChoice:
    """Test Case 3: Invalid parity choice handling."""

    def test_invalid_choice_blue(self):
        """Parity choice 'blue' should be invalid."""
        rules = EvenOddGameRules()
        assert rules.validate_parity_choice("blue") is False

    def test_invalid_choice_number(self):
        """Numeric parity choice should be invalid."""
        rules = EvenOddGameRules()
        assert rules.validate_parity_choice("123") is False

    def test_case_sensitive_choice(self):
        """Uppercase 'EVEN' should be valid."""
        rules = EvenOddGameRules()
        assert rules.validate_parity_choice("EVEN") is True

    def test_empty_choice(self):
        """Empty string choice should be invalid."""
        rules = EvenOddGameRules()
        assert rules.validate_parity_choice("") is False


class TestEdgeCaseGameLogic:
    """Edge cases for game logic."""

    def test_draw_number_range(self):
        """Drawn numbers should be in valid range 1-10."""
        rules = EvenOddGameRules()
        for _ in range(100):
            num = rules.draw_number()
            assert 1 <= num <= 10

    def test_parity_boundary_values(self):
        """Test parity at boundary values."""
        rules = EvenOddGameRules()
        assert rules.get_parity(1) == "ODD"
        assert rules.get_parity(10) == "EVEN"

    def test_determine_winner_draw(self):
        """Both same wrong choice = draw."""
        rules = EvenOddGameRules()
        winner = rules.determine_winner("even", "even", 3)
        assert winner == "DRAW"

    def test_determine_winner_player_a(self):
        """Player A wins when only A is correct."""
        rules = EvenOddGameRules()
        winner = rules.determine_winner("odd", "even", 3)
        assert winner == "PLAYER_A"

    def test_determine_winner_player_b(self):
        """Player B wins when only B is correct."""
        rules = EvenOddGameRules()
        winner = rules.determine_winner("even", "odd", 3)
        assert winner == "PLAYER_B"

    def test_parity_for_mid_range(self):
        """Test parity for values 2-9."""
        rules = EvenOddGameRules()
        assert rules.get_parity(2) == "EVEN"
        assert rules.get_parity(5) == "ODD"
        assert rules.get_parity(8) == "EVEN"
        assert rules.get_parity(9) == "ODD"
