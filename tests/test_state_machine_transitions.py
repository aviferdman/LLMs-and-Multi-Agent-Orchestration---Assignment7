"""Unit tests for match state machine transitions.

Tests match state machine initialization and transitions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.referee_match_state import MatchState, MatchStateMachine


def test_match_state_machine_initialization():
    """Test state machine initializes to WAITING_FOR_PLAYERS."""
    assert MatchStateMachine().current_state == MatchState.WAITING_FOR_PLAYERS


def test_valid_state_transitions():
    """Test valid state transitions work."""
    sm = MatchStateMachine()
    assert (
        sm.transition(MatchState.COLLECTING_CHOICES)
        and sm.current_state == MatchState.COLLECTING_CHOICES
    )
    assert (
        sm.transition(MatchState.DRAWING_NUMBER) and sm.current_state == MatchState.DRAWING_NUMBER
    )
    assert sm.transition(MatchState.FINISHED) and sm.current_state == MatchState.FINISHED


def test_invalid_state_transitions():
    """Test invalid state transitions are rejected."""
    sm = MatchStateMachine()
    assert (
        not sm.transition(MatchState.FINISHED)
        and sm.current_state == MatchState.WAITING_FOR_PLAYERS
    )


def test_finished_state_no_transitions():
    """Test finished state allows no transitions."""
    sm = MatchStateMachine()
    sm.transition(MatchState.COLLECTING_CHOICES)
    sm.transition(MatchState.DRAWING_NUMBER)
    sm.transition(MatchState.FINISHED)
    assert not sm.transition(MatchState.WAITING_FOR_PLAYERS)


def test_is_finished():
    """Test is_finished method."""
    sm = MatchStateMachine()
    assert not sm.is_finished()
    sm.transition(MatchState.COLLECTING_CHOICES)
    sm.transition(MatchState.DRAWING_NUMBER)
    sm.transition(MatchState.FINISHED)
    assert sm.is_finished()


if __name__ == "__main__":
    print("=" * 60)
    print("STATE MACHINE TRANSITION TESTS")
    print("=" * 60)
    tests = [
        ("sm_init", test_match_state_machine_initialization),
        ("valid_trans", test_valid_state_transitions),
        ("invalid_trans", test_invalid_state_transitions),
        ("finished_no_trans", test_finished_state_no_transitions),
        ("is_finished", test_is_finished),
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
        f"\n{'✅ ALL TRANSITION TESTS PASSED!' if failed == 0 else f'❌ {failed} test(s) failed'}"
    )
