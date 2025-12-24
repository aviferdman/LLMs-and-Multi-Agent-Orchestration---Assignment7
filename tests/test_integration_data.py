"""Integration tests verifying actual tournament data.

Tests that the system produces valid output when run end-to-end.

Note: These tests require tournament data files to exist from a previous run.
They are skipped automatically if no data is available.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import json

import pytest

from SHARED.league_sdk.repositories import MatchRepository, StandingsRepository


def data_valid():
    """Check if tournament data is valid and complete."""
    try:
        standings_repo = StandingsRepository("league_2025_even_odd")
        data = standings_repo.load()
        if data is None or "standings" not in data:
            return False
        # Check that standings have valid data (not stale)
        if len(data["standings"]) != 4:
            return False
        # Check ranks exist and are valid
        for player in data["standings"]:
            if player.get("rank", 0) == 0:
                return False
            if player.get("games_played", 0) == 0:
                return False
        return True
    except Exception:
        return False


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
def test_all_matches_saved():
    """Verify all 6 matches were saved."""
    match_repo = MatchRepository("league_2025_even_odd")
    matches = match_repo.list_matches()
    assert len(matches) == 6
    expected = ["R1M1", "R1M2", "R2M1", "R2M2", "R3M1", "R3M2"]
    assert sorted(matches) == sorted(expected)


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
def test_match_data_structure():
    """Verify match data has required fields."""
    match_repo = MatchRepository("league_2025_even_odd")
    match = match_repo.load_match("R1M1")
    assert match is not None
    required = ["match_id", "player_a", "player_b", "winner"]
    assert all(field in match for field in required)


@skip_integration
def test_winner_consistency():
    """Verify match results consistent with standings."""
    standings_repo = StandingsRepository("league_2025_even_odd")
    match_repo = MatchRepository("league_2025_even_odd")
    data = standings_repo.load()

    player_wins = {p["player_id"]: 0 for p in data["standings"]}
    for match_id in match_repo.list_matches():
        match = match_repo.load_match(match_id)
        winner = match.get("winner")
        if winner == "PLAYER_A":
            player_wins[match["player_a"]] += 1
        elif winner == "PLAYER_B":
            player_wins[match["player_b"]] += 1

    for player in data["standings"]:
        assert player_wins[player["player_id"]] == player["wins"]


@skip_integration
def test_standings_sorted_by_points():
    """Verify standings are sorted by points descending."""
    standings_repo = StandingsRepository("league_2025_even_odd")
    data = standings_repo.load()
    points = [p["points"] for p in data["standings"]]
    assert points == sorted(points, reverse=True)


if __name__ == "__main__":
    print("=" * 60)
    print("INTEGRATION DATA TESTS")
    print("=" * 60)
    tests = [
        ("tournament_completed", test_tournament_completed),
        ("all_matches_saved", test_all_matches_saved),
        ("standings_ranks", test_standings_have_ranks),
        ("points_valid", test_standings_points_valid),
        ("games_played", test_all_players_played_3_games),
        ("match_structure", test_match_data_structure),
        ("winner_consistency", test_winner_consistency),
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
        f"\n{'✅ ALL INTEGRATION TESTS PASSED!' if failed == 0 else f'❌ {failed} test(s) failed'}"
    )
