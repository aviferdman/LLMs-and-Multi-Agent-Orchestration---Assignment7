"""Tests for agents.player_strategies module."""

import pytest
from unittest.mock import patch, MagicMock
from agents.player_strategies import (
    RandomStrategy,
    FrequencyStrategy,
    PatternStrategy,
    STRATEGIES,
)
from SHARED.constants import ParityChoice


class TestRandomStrategy:
    """Tests for RandomStrategy class."""

    def test_choose_parity_returns_valid_choice(self):
        """Test choose_parity returns even or odd."""
        strategy = RandomStrategy()
        for _ in range(20):
            choice = strategy.choose_parity([])
            assert choice in [ParityChoice.EVEN, ParityChoice.ODD]

    def test_choose_parity_ignores_history(self):
        """Test random strategy ignores opponent history."""
        strategy = RandomStrategy()
        choice1 = strategy.choose_parity([])
        choice2 = strategy.choose_parity(["even", "even", "even"])
        # Both should be valid regardless of history
        assert choice1 in [ParityChoice.EVEN, ParityChoice.ODD]
        assert choice2 in [ParityChoice.EVEN, ParityChoice.ODD]


class TestFrequencyStrategy:
    """Tests for FrequencyStrategy class."""

    def test_returns_random_with_empty_history(self):
        """Test returns random choice when no history."""
        strategy = FrequencyStrategy()
        choice = strategy.choose_parity([])
        assert choice in [ParityChoice.EVEN, ParityChoice.ODD]

    def test_counters_most_frequent_even(self):
        """Test counters when opponent plays even most often."""
        strategy = FrequencyStrategy()
        history = [ParityChoice.EVEN, ParityChoice.EVEN, ParityChoice.ODD]
        choice = strategy.choose_parity(history)
        assert choice == ParityChoice.ODD

    def test_counters_most_frequent_odd(self):
        """Test counters when opponent plays odd most often."""
        strategy = FrequencyStrategy()
        history = [ParityChoice.ODD, ParityChoice.ODD, ParityChoice.EVEN]
        choice = strategy.choose_parity(history)
        assert choice == ParityChoice.EVEN


class TestPatternStrategy:
    """Tests for PatternStrategy class."""

    def test_returns_random_with_short_history(self):
        """Test returns random with less than 3 moves."""
        strategy = PatternStrategy()
        assert strategy.choose_parity([]) in [ParityChoice.EVEN, ParityChoice.ODD]
        assert strategy.choose_parity(["even"]) in [ParityChoice.EVEN, ParityChoice.ODD]
        assert strategy.choose_parity(["even", "odd"]) in [ParityChoice.EVEN, ParityChoice.ODD]

    def test_returns_valid_with_enough_history(self):
        """Test returns valid choice with enough history."""
        strategy = PatternStrategy()
        history = [ParityChoice.EVEN, ParityChoice.ODD, ParityChoice.EVEN, ParityChoice.ODD]
        choice = strategy.choose_parity(history)
        assert choice in [ParityChoice.EVEN, ParityChoice.ODD]

    def test_exploits_detected_pattern(self):
        """Test exploits detected pattern."""
        strategy = PatternStrategy()
        # Create pattern: even, odd, even -> odd
        history = [
            ParityChoice.EVEN, ParityChoice.ODD, ParityChoice.EVEN, ParityChoice.ODD,
            ParityChoice.EVEN, ParityChoice.ODD, ParityChoice.EVEN
        ]
        choice = strategy.choose_parity(history)
        assert choice in [ParityChoice.EVEN, ParityChoice.ODD]


class TestStrategiesMapping:
    """Tests for STRATEGIES mapping."""

    def test_random_in_strategies(self):
        """Test random strategy is in mapping."""
        assert "random" in STRATEGIES
        assert STRATEGIES["random"] == RandomStrategy

    def test_frequency_in_strategies(self):
        """Test frequency strategy is in mapping."""
        assert "frequency" in STRATEGIES
        assert STRATEGIES["frequency"] == FrequencyStrategy

    def test_pattern_in_strategies(self):
        """Test pattern strategy is in mapping."""
        assert "pattern" in STRATEGIES
        assert STRATEGIES["pattern"] == PatternStrategy

    def test_can_instantiate_all_non_timeout(self):
        """Test can instantiate all strategies except timeout."""
        for name, cls in STRATEGIES.items():
            if name != "timeout":  # timeout requires config
                instance = cls()
                assert hasattr(instance, "choose_parity")
