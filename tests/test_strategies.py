"""Unit tests for agents.player_strategies module.

Tests different player strategy implementations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.player_strategies import FrequencyStrategy, PatternStrategy, RandomStrategy


def test_random_strategy_choices():
    """Test RandomStrategy produces valid choices (lowercase per spec)."""
    strategy = RandomStrategy()
    for _ in range(20):
        choice = strategy.choose_parity([])
        assert choice in ["even", "odd"], f"Invalid choice: {choice}"


def test_random_strategy_distribution():
    """Test RandomStrategy has reasonable distribution."""
    strategy = RandomStrategy()
    choices = [strategy.choose_parity([]) for _ in range(100)]
    even_count = choices.count("even")
    odd_count = choices.count("odd")
    assert 30 <= even_count <= 70, f"Unbalanced: {even_count} even"
    assert 30 <= odd_count <= 70, f"Unbalanced: {odd_count} odd"


def test_frequency_strategy_initialization():
    """Test FrequencyStrategy can be instantiated."""
    strategy = FrequencyStrategy()
    assert strategy is not None


def test_frequency_strategy_first_choice():
    """Test FrequencyStrategy handles empty history."""
    strategy = FrequencyStrategy()
    choice = strategy.choose_parity([])
    assert choice in ["even", "odd"]


def test_frequency_strategy_adapts():
    """Test FrequencyStrategy counters frequent choice."""
    strategy = FrequencyStrategy()
    opponent_history = ["even"] * 10
    choice = strategy.choose_parity(opponent_history)
    assert choice == "odd", "Should counter even with odd"


def test_pattern_strategy_initialization():
    """Test PatternStrategy can be instantiated."""
    strategy = PatternStrategy()
    assert strategy is not None


def test_pattern_strategy_short_history():
    """Test PatternStrategy with short history."""
    strategy = PatternStrategy()
    choice = strategy.choose_parity(["even"])
    assert choice in ["even", "odd"]


def test_pattern_strategy_detects_pattern():
    """Test PatternStrategy detects repeating patterns."""
    strategy = PatternStrategy()
    # Pattern: even, odd, even, repeating
    history = ["even", "odd", "even", "even", "odd", "even"]
    choice = strategy.choose_parity(history)
    assert choice in ["even", "odd"]


def test_all_strategies_valid_output():
    """Test all strategies produce valid output."""
    strategies = [RandomStrategy(), FrequencyStrategy(), PatternStrategy()]
    for strategy in strategies:
        choice = strategy.choose_parity(["even", "odd"])
        assert choice in ["even", "odd"]


if __name__ == "__main__":
    print("=" * 60)
    print("PLAYER STRATEGY TESTS")
    print("=" * 60)

    tests = [
        ("random_strategy_choices", test_random_strategy_choices),
        ("random_strategy_distribution", test_random_strategy_distribution),
        ("frequency_strategy_init", test_frequency_strategy_initialization),
        ("frequency_strategy_first", test_frequency_strategy_first_choice),
        ("frequency_strategy_adapts", test_frequency_strategy_adapts),
        ("pattern_strategy_init", test_pattern_strategy_initialization),
        ("pattern_strategy_short_history", test_pattern_strategy_short_history),
        ("pattern_strategy_detects", test_pattern_strategy_detects_pattern),
        ("all_strategies_valid", test_all_strategies_valid_output),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            print(f"Testing {name}...", end=" ")
            test_func()
            print("✓")
            passed += 1
        except Exception as e:
            print(f"✗ {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"SUMMARY: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ ALL STRATEGY TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
