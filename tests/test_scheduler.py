"""Unit tests for agents.league_manager.scheduler module.

Tests round-robin match scheduling logic.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.league_manager.scheduler import (
    RoundState,
    check_round_complete,
    generate_round_robin_schedule,
    get_match_schedule,
    start_round,
)


def test_generate_round_robin_schedule_structure():
    """Test that schedule has correct structure."""
    schedule = generate_round_robin_schedule(["P01", "P02", "P03", "P04"], ["REF01", "REF02"])
    assert len(schedule) == 3 and all(len(r) == 2 for r in schedule)


def test_generate_round_robin_all_pairings():
    """Test that all player pairings are included."""
    schedule = generate_round_robin_schedule(["P01", "P02", "P03", "P04"], ["REF01", "REF02"])
    pairings = set()
    for round_matches in schedule:
        for match in round_matches:
            pairings.add(tuple(sorted([match["player_a"], match["player_b"]])))
    assert len(pairings) == 6


def test_generate_round_robin_referee_assignment():
    """Test that referees are assigned correctly."""
    schedule = generate_round_robin_schedule(["P01", "P02", "P03", "P04"], ["REF01", "REF02"])
    for round_matches in schedule:
        assert all(m["referee_id"] in ["REF01", "REF02"] for m in round_matches)


def test_generate_round_robin_match_ids():
    """Test that match IDs are correctly formatted."""
    schedule = generate_round_robin_schedule(["P01", "P02", "P03", "P04"], ["REF01", "REF02"])
    for r_idx, round_matches in enumerate(schedule):
        for m_idx, match in enumerate(round_matches):
            assert match["match_id"] == f"R{r_idx + 1}M{m_idx + 1}"


def test_get_match_schedule_structure():
    """Test predefined schedule structure."""
    schedule = get_match_schedule()
    assert len(schedule) == 3 and all(len(r) == 2 for r in schedule)


def test_get_match_schedule_total_matches():
    """Test total number of matches."""
    assert sum(len(r) for r in get_match_schedule()) == 6


def test_get_match_schedule_player_coverage():
    """Test that all players participate."""
    players = set()
    for r in get_match_schedule():
        for m in r:
            players.update([m["player_a"], m["player_b"]])
    assert players == {"P01", "P02", "P03", "P04"}


def test_get_match_schedule_no_duplicate_pairings():
    """Test that no pairing plays twice."""
    pairings = [
        tuple(sorted([m["player_a"], m["player_b"]])) for r in get_match_schedule() for m in r
    ]
    assert len(pairings) == len(set(pairings))


def test_get_match_schedule_round_ids():
    """Test that round IDs are sequential."""
    for r_idx, round_matches in enumerate(get_match_schedule()):
        assert all(m["round_id"] == r_idx + 1 for m in round_matches)


def test_round_state_init():
    """Test RoundState initialization."""
    state = RoundState(total_rounds=3, matches_per_round=2)
    assert state.total_rounds == 3
    assert state.matches_per_round == 2
    assert state.current_round == 0


def test_start_round_success():
    """Test starting a valid round."""
    state = RoundState(total_rounds=3)
    assert start_round(state, 1) is True
    assert state.current_round == 1
    assert 1 in state.round_results


def test_start_round_invalid_round():
    """Test starting an invalid round number."""
    state = RoundState(total_rounds=3)
    assert start_round(state, 0) is False
    assert start_round(state, 4) is False


def test_start_round_duplicate():
    """Test starting same round twice fails."""
    state = RoundState(total_rounds=3)
    assert start_round(state, 1) is True
    assert start_round(state, 1) is False


def test_check_round_complete_empty():
    """Test round complete check with no results."""
    state = RoundState(total_rounds=3, matches_per_round=2)
    start_round(state, 1)
    assert check_round_complete(state, 1) is False


def test_check_round_complete_partial():
    """Test round complete check with partial results."""
    state = RoundState(total_rounds=3, matches_per_round=2)
    start_round(state, 1)
    state.add_match_result(1, {"match_id": "R1M1", "winner": "P01"})
    assert check_round_complete(state, 1) is False


def test_check_round_complete_full():
    """Test round complete check with all results."""
    state = RoundState(total_rounds=3, matches_per_round=2)
    start_round(state, 1)
    state.add_match_result(1, {"match_id": "R1M1", "winner": "P01"})
    state.add_match_result(1, {"match_id": "R1M2", "winner": "P03"})
    assert check_round_complete(state, 1) is True


def test_check_round_complete_not_started():
    """Test round complete check for non-started round."""
    state = RoundState(total_rounds=3)
    assert check_round_complete(state, 1) is False
