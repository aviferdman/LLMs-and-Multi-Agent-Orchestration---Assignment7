"""End-to-end protocol compliance tests - Part 3: Edge Cases.

Tests edge cases including draw results, timeouts, and rejected registrations.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from SHARED.constants import Field, Status
from SHARED.contracts import build_game_over
from SHARED.contracts.league_manager_contracts import build_league_register_response
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params


def get_params(msg):
    """Extract params from JSON-RPC message."""
    return extract_jsonrpc_params(msg)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_draw_game_result(self):
        """Test GAME_OVER with draw result."""
        game_over = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="DRAW", winner_player_id=None, drawn_number=4, number_parity="even",
            choices={"P01": "EVEN", "P02": "EVEN"}, reason="Both players chose the same parity",
        )
        params = get_params(game_over)
        assert params[Field.GAME_RESULT]["status"] == "DRAW"
        assert params[Field.GAME_RESULT]["winner_player_id"] is None
        assert validate_base_message(params)

    def test_timeout_game_result(self):
        """Test GAME_OVER with timeout result."""
        game_over = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="TECHNICAL_LOSS", winner_player_id="P02", drawn_number=0, number_parity="even",
            choices={"P01": "NO_RESPONSE", "P02": "ODD"}, reason="P01 timed out",
        )
        params = get_params(game_over)
        assert params[Field.GAME_RESULT]["status"] == "TECHNICAL_LOSS"
        assert params[Field.GAME_RESULT]["reason"] == "P01 timed out"
        assert validate_base_message(params)

    def test_rejected_registration(self):
        """Test rejected registration response."""
        response = build_league_register_response(
            player_id="P99", status=Status.REJECTED, reason="League is full")
        params = get_params(response)
        assert params[Field.STATUS] == Status.REJECTED
        assert params.get(Field.REASON) == "League is full"
        assert validate_base_message(params)


class TestDoubleTimeout:
    """Test double timeout scenarios."""

    def test_both_players_timeout(self):
        """Test GAME_OVER when both players time out."""
        game_over = build_game_over(
            league_id="league_2025", round_id=1, match_id="R1M1", referee_id="REF01",
            status="DRAW", winner_player_id=None, drawn_number=0, number_parity="even",
            choices={"P01": "NO_RESPONSE", "P02": "NO_RESPONSE"},
            reason="Both players timed out",
        )
        params = get_params(game_over)
        assert params[Field.GAME_RESULT]["status"] == "DRAW"
        assert params[Field.GAME_RESULT]["winner_player_id"] is None
        assert "NO_RESPONSE" in params[Field.GAME_RESULT]["choices"]["P01"]
        assert validate_base_message(params)


if __name__ == "__main__":
    from tests.test_protocol_e2e_part1 import TestCompleteGameLifecycle
    from tests.test_protocol_e2e_part2 import TestRoundLifecycleFlow, TestProtocolCompliance

    print("=" * 60)
    print("END-TO-END PROTOCOL COMPLIANCE TESTS")
    print("=" * 60)

    test_classes = [
        ("TestCompleteGameLifecycle", TestCompleteGameLifecycle),
        ("TestRoundLifecycleFlow", TestRoundLifecycleFlow),
        ("TestProtocolCompliance", TestProtocolCompliance),
        ("TestEdgeCases", TestEdgeCases),
        ("TestDoubleTimeout", TestDoubleTimeout),
    ]

    passed = 0
    failed = 0

    for class_name, test_class in test_classes:
        print(f"\n{class_name}:")
        print("-" * 40)
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    print(f"  {method_name}...", end=" ")
                    getattr(instance, method_name)()
                    print("✓")
                    passed += 1
                except Exception as e:
                    print(f"✗ {e}")
                    failed += 1

    print()
    print("=" * 60)
    print(f"SUMMARY: {passed}/{passed + failed} tests passed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ ALL E2E PROTOCOL COMPLIANCE TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
