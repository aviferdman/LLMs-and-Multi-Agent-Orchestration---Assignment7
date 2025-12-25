"""Protocol contract compliance tests - Result Messages.

Tests GAME_OVER and MATCH_RESULT_REPORT messages.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import Field, MessageType
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params
from SHARED.contracts.referee_contracts import (
    build_game_over,
    build_match_result_report,
)


def get_params(msg):
    """Extract params from JSON-RPC message."""
    return extract_jsonrpc_params(msg)


class TestGameOverContract:
    """Test GAME_OVER message compliance."""

    def test_game_over_has_game_result_structure(self):
        """GAME_OVER must have game_result object per protocol."""
        msg = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="WIN",
            winner_player_id="P01",
            drawn_number=4,
            number_parity="even",
            choices={"P01": "EVEN", "P02": "ODD"},
            reason="P01 chose correctly",
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        assert Field.GAME_RESULT in params
        assert params[Field.GAME_RESULT]["winner_player_id"] == "P01"


class TestMatchResultReportContract:
    """Test MATCH_RESULT_REPORT message compliance."""

    def test_match_result_report_has_result_structure(self):
        """MATCH_RESULT_REPORT must have result object per protocol."""
        msg = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            score={"P01": 1, "P02": 0},
            drawn_number=4,
            choices={"P01": "EVEN", "P02": "ODD"},
        )
        params = get_params(msg)
        assert params[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert Field.RESULT in params
        assert params[Field.RESULT]["winner"] == "P01"


if __name__ == "__main__":
    print("=" * 60)
    print("PROTOCOL CONTRACT COMPLIANCE TESTS - RESULTS")
    print("=" * 60)

    test_classes = [
        ("TestGameOverContract", TestGameOverContract),
        ("TestMatchResultReportContract", TestMatchResultReportContract),
    ]

    passed = 0
    failed = 0

    for class_name, test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    print(f"Testing {class_name}.{method_name}...", end=" ")
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
