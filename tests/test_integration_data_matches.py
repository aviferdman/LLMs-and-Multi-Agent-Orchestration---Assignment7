"""Integration tests verifying tournament match data.

Tests that the system produces valid match output when run end-to-end.

Note: These tests require tournament data files to exist from a previous run.
They are skipped automatically if no data is available.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from SHARED.league_sdk.repositories import MatchRepository, StandingsRepository


# Skip integration tests by default unless explicitly enabled
INTEGRATION_ENABLED = os.environ.get("RUN_INTEGRATION_TESTS", "").lower() == "true"

skip_integration = pytest.mark.skipif(
    not INTEGRATION_ENABLED,
    reason="Integration tests skipped. Set RUN_INTEGRATION_TESTS=true to run."
)


@skip_integration
def test_all_matches_saved():
    """Verify all 6 matches were saved."""
    match_repo = MatchRepository("league_2025_even_odd")
    matches = match_repo.list_matches()
    assert len(matches) == 6
    expected = ["R1M1", "R1M2", "R2M1", "R2M2", "R3M1", "R3M2"]
    assert sorted(matches) == sorted(expected)


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


if __name__ == "__main__":
    print("=" * 60)
    print("INTEGRATION DATA MATCHES TESTS")
    print("=" * 60)
    tests = [
        ("all_matches_saved", test_all_matches_saved),
        ("match_structure", test_match_data_structure),
        ("winner_consistency", test_winner_consistency),
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
        f"\n{'✅ ALL MATCH TESTS PASSED!' if failed == 0 else f'❌ {failed} test(s) failed'}"
    )
