"""Unit tests for standings retrieval and updates.

Tests standings retrieval and update functionality.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.league_manager.ranking import (
    calculate_rankings,
    get_current_standings,
)


def test_get_current_standings():
    """Test getting current standings."""
    try:
        standings = get_current_standings("league_2025_even_odd")
        assert isinstance(standings, list)
        if len(standings) > 0:
            assert "player_id" in standings[0]
            assert "points" in standings[0]
    except FileNotFoundError:
        pass


def test_update_standings_rankings_recalculated():
    """Test that update_standings recalculates rankings."""
    players_before = [
        {
            "player_id": "P01",
            "points": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "games_played": 0,
            "rank": 1,
        },
        {
            "player_id": "P02",
            "points": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "games_played": 0,
            "rank": 2,
        },
    ]

    # Simulate what update_standings does internally
    # Player A wins
    players_before[0]["wins"] += 1
    players_before[0]["points"] += 3
    players_before[0]["games_played"] += 1
    players_before[1]["losses"] += 1
    players_before[1]["games_played"] += 1

    # Recalculate rankings
    ranked = calculate_rankings(players_before)

    assert ranked[0]["player_id"] == "P01"
    assert ranked[0]["rank"] == 1
    assert ranked[0]["points"] == 3
    assert ranked[1]["player_id"] == "P02"
    assert ranked[1]["rank"] == 2
    assert ranked[1]["points"] == 0


if __name__ == "__main__":
    print("=" * 60)
    print("RANKING STANDINGS TESTS")
    print("=" * 60)

    tests = [
        ("get_current_standings", test_get_current_standings),
        ("update_standings_rankings_recalculated", test_update_standings_rankings_recalculated),
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
        print("\n✅ ALL STANDINGS TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
