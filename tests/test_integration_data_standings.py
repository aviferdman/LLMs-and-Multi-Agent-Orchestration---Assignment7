"""Integration tests verifying tournament standings data.

Tests that the system produces valid standings output when run end-to-end.

Note: These tests require tournament data files to exist from a previous run.
They are skipped automatically if no data is available.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from SHARED.league_sdk.repositories import StandingsRepository


# Skip integration tests by default unless explicitly enabled
INTEGRATION_ENABLED = os.environ.get("RUN_INTEGRATION_TESTS", "").lower() == "true"

skip_integration = pytest.mark.skipif(
    not INTEGRATION_ENABLED,
    reason="Integration tests skipped. Set RUN_INTEGRATION_TESTS=true to run."
)


@skip_integration
def test_tournament_completed():
    """Verify a complete tournament was run."""
    standings_repo = StandingsRepository("league_2025_even_odd")
    data = standings_repo.load()
    assert data is not None
    assert "standings" in data
    assert len(data["standings"]) == 4


@skip_integration
def test_standings_have_ranks():
    """Verify all players have ranks assigned."""
    standings_repo = StandingsRepository("league_2025_even_odd")
    data = standings_repo.load()
    ranks = [p["rank"] for p in data["standings"]]
    assert sorted(ranks) == [1, 2, 3, 4]


@skip_integration
def test_standings_points_valid():
    """Verify points are calculated correctly."""
    standings_repo = StandingsRepository("league_2025_even_odd")
    data = standings_repo.load()
    for player in data["standings"]:
        expected = player["wins"] * 3 + player["draws"]
        assert player["points"] == expected


@skip_integration
def test_all_players_played_3_games():
    """Verify each player played exactly 3 games."""
    standings_repo = StandingsRepository("league_2025_even_odd")
    data = standings_repo.load()
    for player in data["standings"]:
        assert player["games_played"] == 3


@skip_integration
def test_standings_sorted_by_points():
    """Verify standings are sorted by points descending."""
    standings_repo = StandingsRepository("league_2025_even_odd")
    data = standings_repo.load()
    points = [p["points"] for p in data["standings"]]
    assert points == sorted(points, reverse=True)


if __name__ == "__main__":
    print("=" * 60)
    print("INTEGRATION DATA STANDINGS TESTS")
    print("=" * 60)
    tests = [
        ("tournament_completed", test_tournament_completed),
        ("standings_ranks", test_standings_have_ranks),
        ("points_valid", test_standings_points_valid),
        ("games_played", test_all_players_played_3_games),
        ("standings_sorted", test_standings_sorted_by_points),
    ]
    passed = failed = 0
    for name, test_func in tests:
        try:
            print(f"Testing {name}...", end=" ")
            test_func()
            print("✓")
            passed += 1
        except Exception as e:
            print(f"✗ {e}")
            failed += 1
    print(f"\n{'='*60}\nSUMMARY: {passed}/{len(tests)} tests passed\n{'='*60}")
    print(
        f"\n{'✅ ALL STANDINGS TESTS PASSED!' if failed == 0 else f'❌ {failed} test(s) failed'}"
    )
