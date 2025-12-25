"""Tests for agents.referee_game_logic module."""

import pytest
from agents.referee_game_logic import (
    EvenOddGameRules,
    get_game_rules,
    BaseGameRules,
)
from SHARED.constants import GameID, ParityChoice, Winner


class TestEvenOddGameRules:
    """Tests for EvenOddGameRules class."""

    def test_init_sets_draw_range(self):
        """Test initializer sets draw range."""
        rules = EvenOddGameRules()
        assert rules.draw_range[0] >= 1
        assert rules.draw_range[1] <= 10

    def test_draw_number_in_range(self):
        """Test draw number is within range."""
        rules = EvenOddGameRules()
        for _ in range(20):
            num = rules.draw_number()
            assert 1 <= num <= 10

    def test_get_parity_even(self):
        """Test get_parity returns even for even numbers."""
        rules = EvenOddGameRules()
        assert rules.get_parity(2) == ParityChoice.EVEN
        assert rules.get_parity(4) == ParityChoice.EVEN
        assert rules.get_parity(10) == ParityChoice.EVEN

    def test_get_parity_odd(self):
        """Test get_parity returns odd for odd numbers."""
        rules = EvenOddGameRules()
        assert rules.get_parity(1) == ParityChoice.ODD
        assert rules.get_parity(5) == ParityChoice.ODD
        assert rules.get_parity(9) == ParityChoice.ODD

    def test_validate_parity_choice_valid(self):
        """Test validate_parity_choice accepts valid choices."""
        rules = EvenOddGameRules()
        assert rules.validate_parity_choice("even")
        assert rules.validate_parity_choice("odd")
        assert rules.validate_parity_choice("EVEN")
        assert rules.validate_parity_choice("ODD")

    def test_validate_parity_choice_invalid(self):
        """Test validate_parity_choice rejects invalid choices."""
        rules = EvenOddGameRules()
        assert not rules.validate_parity_choice("invalid")
        assert not rules.validate_parity_choice("")
        assert not rules.validate_parity_choice("neither")

    def test_determine_winner_player_a_wins(self):
        """Test player A wins when only A correct."""
        rules = EvenOddGameRules()
        result = rules.determine_winner("odd", "even", 3)  # 3 is odd
        assert result == Winner.PLAYER_A

    def test_determine_winner_player_b_wins(self):
        """Test player B wins when only B correct."""
        rules = EvenOddGameRules()
        result = rules.determine_winner("even", "odd", 5)  # 5 is odd
        assert result == Winner.PLAYER_B

    def test_determine_winner_draw_both_correct(self):
        """Test draw when both players correct."""
        rules = EvenOddGameRules()
        result = rules.determine_winner("even", "even", 4)  # 4 is even
        assert result == Winner.DRAW

    def test_determine_winner_draw_both_wrong(self):
        """Test draw when both players wrong."""
        rules = EvenOddGameRules()
        result = rules.determine_winner("odd", "odd", 2)  # 2 is even
        assert result == Winner.DRAW


class TestGetGameRules:
    """Tests for get_game_rules factory function."""

    def test_get_even_odd_rules(self):
        """Test getting even_odd game rules."""
        rules = get_game_rules(GameID.EVEN_ODD)
        assert isinstance(rules, EvenOddGameRules)

    def test_unknown_game_type_raises(self):
        """Test unknown game type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown game type"):
            get_game_rules("unknown_game")


class TestBaseGameRules:
    """Tests for BaseGameRules abstract class."""

    def test_draw_number_not_implemented(self):
        """Test draw_number raises NotImplementedError."""
        rules = BaseGameRules()
        with pytest.raises(NotImplementedError):
            rules.draw_number()

    def test_validate_not_implemented(self):
        """Test validate_parity_choice raises NotImplementedError."""
        rules = BaseGameRules()
        with pytest.raises(NotImplementedError):
            rules.validate_parity_choice("even")

    def test_determine_winner_not_implemented(self):
        """Test determine_winner raises NotImplementedError."""
        rules = BaseGameRules()
        with pytest.raises(NotImplementedError):
            rules.determine_winner("even", "odd", 5)
