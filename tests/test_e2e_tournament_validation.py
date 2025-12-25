#!/usr/bin/env python3
"""End-to-End Testing Script for League System - Validation.

This script validates tournament results including standings and matches.

Usage:
    python tests/test_e2e_tournament_validation.py

Note: These tests require spawning the full league system and may timeout
in CI environments. They are marked as skip unless explicitly run.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Skip E2E tests unless explicitly requested
E2E_ENABLED = os.environ.get("RUN_E2E_TESTS", "").lower() == "true"
skip_e2e = pytest.mark.skipif(
    not E2E_ENABLED,
    reason="E2E tests skipped. Set RUN_E2E_TESTS=true to run."
)


def run_tournament(timeout: int = 120) -> dict:
    """Run a single tournament and return results."""
    result = {"success": False, "logs": [], "error": None}

    try:
        # Clean up logs before running
        logs_dir = PROJECT_ROOT / "SHARED" / "logs" / "agents"
        for log_file in logs_dir.glob("*.jsonl"):
            log_file.unlink(missing_ok=True)

        # Run the league
        proc = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "run_league.py")],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT),
        )

        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr

        # Check for LEAGUE_COMPLETED in logs
        lm_log = logs_dir / "LM01.log.jsonl"
        if lm_log.exists():
            with open(lm_log, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        result["logs"].append(entry)
                        if entry.get("event_type") == "LEAGUE_COMPLETED_SENT":
                            result["success"] = True
                    except json.JSONDecodeError:
                        pass

    except subprocess.TimeoutExpired:
        result["error"] = "Tournament timed out"
    except Exception as e:
        result["error"] = str(e)

    return result


def test_tournament_produces_standings():
    """Verify tournament produces valid standings."""
    if not E2E_ENABLED:
        pytest.skip("E2E tests skipped. Set RUN_E2E_TESTS=true to run.")
    print("Testing tournament standings output...")
    result = run_tournament()
    standings_found = any(
        "standings" in str(log) or log.get("event_type") == "STANDINGS_UPDATE_SENT"
        for log in result["logs"]
    )
    assert standings_found, "No standings updates found in logs"
    print("✅ Standings validation passed")


def test_all_matches_completed():
    """Verify all 6 matches completed."""
    if not E2E_ENABLED:
        pytest.skip("E2E tests skipped. Set RUN_E2E_TESTS=true to run.")
    print("Testing all matches completed...")
    result = run_tournament()
    match_results = [log for log in result["logs"] if log.get("event_type") == "MATCH_RESULT"]
    assert len(match_results) >= 6, f"Expected 6 matches, got {len(match_results)}"
    print("✅ All matches completed")


if __name__ == "__main__":
    print("=" * 60)
    print("END-TO-END TOURNAMENT VALIDATION TESTING")
    print("=" * 60)

    tests = [
        ("standings_output", test_tournament_produces_standings),
        ("all_matches", test_all_matches_completed),
    ]

    passed = failed = 0
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {name}: Unexpected error - {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{len(tests)} passed")
    print("=" * 60)
    sys.exit(0 if failed == 0 else 1)
