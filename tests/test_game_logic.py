"""Unit tests for agents.referee_game_logic module.

Tests Even-Odd game rules implementation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.referee_game_logic import EvenOddGameRules


def test_draw_number_range():
    """Test drawn numbers are in valid range (1-10)."""
    rules = EvenOddGameRules()

    for _ in range(100):
        number = rules.draw_number()
        assert 1 <= number <= 10, f"Number {number} out of range"


def test_get_parity_even():
    """Test parity detection for even numbers."""
    rules = EvenOddGameRules()

    assert rules.get_parity(2) == "even"
    assert rules.get_parity(4) == "even"
    assert rules.get_parity(6) == "even"
    assert rules.get_parity(8) == "even"
    assert rules.get_parity(10) == "even"


def test_get_parity_odd():
    """Test parity detection for odd numbers."""
    rules = EvenOddGameRules()

    assert rules.get_parity(1) == "odd"
    assert rules.get_parity(3) == "odd"
    assert rules.get_parity(5) == "odd"
    assert rules.get_parity(7) == "odd"
    assert rules.get_parity(9) == "odd"


def test_determine_winner_player_a_wins():
    """Test winner determination when player A wins."""
    rules = EvenOddGameRules()

    # Player A chooses even and number is even
    winner = rules.determine_winner("even", "odd", 2)
    assert winner == "PLAYER_A"

    # Player A chooses odd and number is odd
    winner = rules.determine_winner("odd", "even", 3)
    assert winner == "PLAYER_A"


def test_determine_winner_player_b_wins():
    """Test winner determination when player B wins."""
    rules = EvenOddGameRules()

    # Player B chooses even and number is even
    winner = rules.determine_winner("odd", "even", 2)
    assert winner == "PLAYER_B"

    # Player B chooses odd and number is odd
    winner = rules.determine_winner("even", "odd", 3)
    assert winner == "PLAYER_B"


def test_determine_winner_draw():
    """Test winner determination when both choose same."""
    rules = EvenOddGameRules()

    # Both choose even
    winner = rules.determine_winner("even", "even", 2)
    assert winner == "DRAW"

    # Both choose odd
    winner = rules.determine_winner("odd", "odd", 3)
    assert winner == "DRAW"


def test_validate_parity_choice_valid():
    """Test validating valid parity choices (per spec: lowercase)."""
    rules = EvenOddGameRules()

    # Lowercase is canonical per spec
    assert rules.validate_parity_choice("even") == True
    assert rules.validate_parity_choice("odd") == True
    # Also accepts uppercase (case-insensitive)
    assert rules.validate_parity_choice("EVEN") == True
    assert rules.validate_parity_choice("ODD") == True


def test_validate_parity_choice_invalid():
    """Test validating invalid parity choices."""
    rules = EvenOddGameRules()

    # Lower case are actually valid due to .upper() in validation
    assert rules.validate_parity_choice("BLUE") == False
    assert rules.validate_parity_choice("") == False
    try:
        rules.validate_parity_choice(None)
    except AttributeError:
        # Expected - None doesn't have .upper()
        pass


if __name__ == "__main__":
    print("=" * 60)
    print("GAME LOGIC TESTS")
    print("=" * 60)

    tests = [
        ("draw_number_range", test_draw_number_range),
        ("get_parity_even", test_get_parity_even),
        ("get_parity_odd", test_get_parity_odd),
        ("determine_winner_player_a_wins", test_determine_winner_player_a_wins),
        ("determine_winner_player_b_wins", test_determine_winner_player_b_wins),
        ("determine_winner_draw", test_determine_winner_draw),
        ("validate_parity_choice_valid", test_validate_parity_choice_valid),
        ("validate_parity_choice_invalid", test_validate_parity_choice_invalid),
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
        print("\n✅ ALL GAME LOGIC TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
