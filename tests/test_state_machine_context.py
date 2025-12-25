"""Unit tests for match context management.

Tests match context initialization and player handling.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.referee_match_state import (
    MatchContext,
    handle_game_join_ack,
    handle_parity_choice,
)
from SHARED.league_sdk.logger import LeagueLogger


def test_match_context_initialization():
    """Test match context initialization."""
    ctx = MatchContext("M1", "P01", "P02")
    assert ctx.match_id == "M1" and ctx.player_a == "P01" and ctx.player_b == "P02"
    assert not ctx.player_a_joined and not ctx.player_b_joined


def test_record_join():
    """Test recording player joins."""
    ctx = MatchContext("M1", "P01", "P02")
    ctx.record_join("P01", "conv1")
    assert ctx.player_a_joined and ctx.conversation_ids["P01"] == "conv1"


def test_both_players_joined():
    """Test checking if both players joined."""
    ctx = MatchContext("M1", "P01", "P02")
    assert not ctx.both_players_joined()
    ctx.record_join("P01", "conv1")
    assert not ctx.both_players_joined()
    ctx.record_join("P02", "conv2")
    assert ctx.both_players_joined()


def test_record_choice():
    """Test recording player choices."""
    ctx = MatchContext("M1", "P01", "P02")
    ctx.record_choice("P01", "even")
    ctx.record_choice("P02", "odd")
    assert ctx.player_a_choice == "even" and ctx.player_b_choice == "odd"


def test_both_choices_received():
    """Test checking if both choices received."""
    ctx = MatchContext("M1", "P01", "P02")
    assert not ctx.both_choices_received()
    ctx.record_choice("P01", "even")
    assert not ctx.both_choices_received()
    ctx.record_choice("P02", "odd")
    assert ctx.both_choices_received()


def test_handle_game_join_ack():
    """Test handle_game_join_ack function."""
    ctx = MatchContext("M1", "P01", "P02")
    msg = {"sender": "P01", "conversation_id": "conv1"}
    assert handle_game_join_ack(msg, ctx, LeagueLogger("test", Path("test_logs")))
    assert ctx.player_a_joined


def test_handle_parity_choice_valid():
    """Test handle_parity_choice with valid choice."""
    ctx = MatchContext("M1", "P01", "P02")
    # Use correct field name "parity_choice" per protocol
    msg = {"sender": "P01", "parity_choice": "even"}
    assert handle_parity_choice(msg, ctx, LeagueLogger("test", Path("test_logs")))
    assert ctx.player_a_choice == "even"


def test_handle_parity_choice_invalid():
    """Test handle_parity_choice with invalid choice."""
    ctx = MatchContext("M1", "P01", "P02")
    # Use correct field name "parity_choice" per protocol
    msg = {"sender": "P01", "parity_choice": "BLUE"}
    assert not handle_parity_choice(msg, ctx, LeagueLogger("test", Path("test_logs")))


if __name__ == "__main__":
    print("=" * 60)
    print("STATE MACHINE CONTEXT TESTS")
    print("=" * 60)
    tests = [
        ("ctx_init", test_match_context_initialization),
        ("record_join", test_record_join),
        ("both_joined", test_both_players_joined),
        ("record_choice", test_record_choice),
        ("both_choices", test_both_choices_received),
        ("handle_join", test_handle_game_join_ack),
        ("handle_choice_valid", test_handle_parity_choice_valid),
        ("handle_choice_invalid", test_handle_parity_choice_invalid),
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
        f"\n{'✅ ALL CONTEXT TESTS PASSED!' if failed == 0 else f'❌ {failed} test(s) failed'}"
    )
