#!/usr/bin/env python3
"""Verification tests for refactored modules."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_constants_import():
    """Test constants import from split modules."""
    print("Testing constants imports...")
    from SHARED.constants import (
        PROTOCOL_VERSION,
        SERVER_HOST,
        AgentID,
        Field,
        GameStatus,
        LogEvent,
        MessageType,
        ParityChoice,
        Points,
        Status,
        StrategyType,
        Timeout,
        Winner,
    )

    print(f"  ✓ All constants imported (PROTOCOL={PROTOCOL_VERSION}, HOST={SERVER_HOST})")
    return True


def test_player_strategies():
    """Test player strategies."""
    print("Testing player strategies...")
    from agents.player_strategies import (
        STRATEGIES,
        FrequencyStrategy,
        PatternStrategy,
        RandomStrategy,
    )

    r, f, p = RandomStrategy(), FrequencyStrategy(), PatternStrategy()
    c1, c2, c3 = r.choose_parity([]), f.choose_parity([]), p.choose_parity([])
    print(f"  ✓ All 3 strategies work: {c1}, {c2}, {c3}")
    return True


def test_referee_modules():
    """Test referee modules."""
    print("Testing referee modules...")
    from agents.referee_game_logic import EvenOddGameRules
    from agents.referee_match_state import MatchContext, MatchStateMachine

    rules = EvenOddGameRules()
    num = rules.draw_number()
    print(f"  ✓ Game rules work (drew {num}, parity={rules.get_parity(num)})")

    sm = MatchStateMachine()
    ctx = MatchContext("m1", "P01", "P02")
    print(f"  ✓ State machine & context work")
    return True


def test_messages():
    """Test message utilities."""
    print("Testing message utilities...")
    from SHARED.league_sdk.messages import build_game_invitation, validate_message

    # build_game_invitation requires role_in_match parameter
    msg = build_game_invitation("l1", 1, "m1", "REF01", "P01", "P02", "player_a")
    print(f"  ✓ Message built & validated: {validate_message(msg)}")
    return True


def test_generic_imports():
    """Test generic agent imports."""
    print("Testing generic agent imports...")
    import agents.generic_player
    import agents.generic_referee

    print("  ✓ Both agents import successfully")
    return True


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("REFACTORING VERIFICATION TESTS")
    print("=" * 60)

    tests = [
        test_constants_import,
        test_player_strategies,
        test_referee_modules,
        test_messages,
        test_generic_imports,
    ]

    try:
        results = [test() for test in tests]
        passed = sum(results)
        total = len(results)

        print("\n" + "=" * 60)
        print(f"SUMMARY: {passed}/{total} tests passed")
        print("=" * 60)

        if passed == total:
            print("\n✅ ALL TESTS PASSED - Refactoring successful!")
            return 0
        else:
            print(f"\n❌ {total - passed} tests failed")
            return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
