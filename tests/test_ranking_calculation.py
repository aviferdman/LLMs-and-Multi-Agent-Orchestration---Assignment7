"""Unit tests for ranking calculation.

Tests ranking calculation and tiebreaker functionality.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.league_manager.ranking import calculate_rankings


def test_calculate_rankings_basic():
    """Test basic ranking calculation."""
    players = [
        {"player_id": "P01", "points": 9, "wins": 3},
        {"player_id": "P02", "points": 3, "wins": 1},
        {"player_id": "P03", "points": 6, "wins": 2},
    ]

    ranked = calculate_rankings(players)

    assert ranked[0]["player_id"] == "P01"
    assert ranked[0]["rank"] == 1
    assert ranked[1]["player_id"] == "P03"
    assert ranked[1]["rank"] == 2
    assert ranked[2]["player_id"] == "P02"
    assert ranked[2]["rank"] == 3


def test_calculate_rankings_tiebreaker():
    """Test ranking with tie on points (wins tiebreaker)."""
    players = [
        {"player_id": "P01", "points": 3, "wins": 1},
        {"player_id": "P02", "points": 3, "wins": 0},
        {"player_id": "P03", "points": 6, "wins": 2},
    ]

    ranked = calculate_rankings(players)

    # P03 should be first (6 points)
    assert ranked[0]["player_id"] == "P03"
    assert ranked[0]["rank"] == 1

    # P01 should be second (3 points, 1 win)
    assert ranked[1]["player_id"] == "P01"
    assert ranked[1]["rank"] == 2

    # P02 should be third (3 points, 0 wins)
    assert ranked[2]["player_id"] == "P02"
    assert ranked[2]["rank"] == 3


def test_calculate_rankings_empty():
    """Test ranking with empty list."""
    ranked = calculate_rankings([])
    assert ranked == []


if __name__ == "__main__":
    print("=" * 60)
    print("RANKING CALCULATION TESTS")
    print("=" * 60)

    tests = [
        ("calculate_rankings_basic", test_calculate_rankings_basic),
        ("calculate_rankings_tiebreaker", test_calculate_rankings_tiebreaker),
        ("calculate_rankings_empty", test_calculate_rankings_empty),
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
        print("\n✅ ALL RANKING CALCULATION TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
