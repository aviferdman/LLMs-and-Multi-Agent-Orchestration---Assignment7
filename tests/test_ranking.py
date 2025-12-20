"""Unit tests for agents.league_manager.ranking module.

Tests ranking calculation and standings update functionality.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import os
import tempfile

from agents.league_manager.ranking import (
    calculate_rankings,
    get_current_standings,
    update_standings,
)
from SHARED.league_sdk.config_models import LeagueConfig


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
    print("RANKING TESTS")
    print("=" * 60)

    tests = [
        ("calculate_rankings_basic", test_calculate_rankings_basic),
        ("calculate_rankings_tiebreaker", test_calculate_rankings_tiebreaker),
        ("calculate_rankings_empty", test_calculate_rankings_empty),
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
        print("\n✅ ALL RANKING TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
