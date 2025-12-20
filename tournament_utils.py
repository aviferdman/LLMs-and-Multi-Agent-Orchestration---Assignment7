"""Utility functions for tournament runner."""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import psutil

PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "SHARED" / "logs" / "agents"


def clean_logs() -> None:
    """Clean up log files before tournament."""
    for log_file in LOGS_DIR.glob("*.jsonl"):
        log_file.unlink(missing_ok=True)


def clean_data(data_dir: Path) -> None:
    """Clean up data files before tournament."""
    matches_dir = data_dir / "matches" / "league_2025_even_odd"
    if matches_dir.exists():
        for f in matches_dir.glob("*.json"):
            f.unlink(missing_ok=True)


def parse_tournament_logs(result: Dict[str, Any]) -> Dict[str, Any]:
    """Parse logs to extract tournament results."""
    lm_log = LOGS_DIR / "LM01.log.jsonl"
    if not lm_log.exists():
        result["error"] = "League manager log not found"
        return result

    with open(lm_log, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                event = entry.get("event_type", "")
                if event == "MATCH_RESULT":
                    result["matches_completed"] += 1
                elif event == "ROUND_COMPLETED_SENT":
                    result["rounds_completed"] += 1
                elif event == "LEAGUE_COMPLETED_SENT":
                    result["success"] = True
                    result["standings"] = entry.get("data", {}).get("standings", [])
            except json.JSONDecodeError:
                continue

    return result


def run_subprocess_with_metrics(cmd: List[str], timeout: int, cwd: str) -> Dict[str, Any]:
    """Run subprocess and collect metrics."""
    metrics = {"exit_code": None, "memory_mb": 0.0, "error": None}

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
        )

        start_mem = psutil.Process().memory_info().rss / (1024 * 1024)
        proc.wait(timeout=timeout)
        end_mem = psutil.Process().memory_info().rss / (1024 * 1024)

        metrics["memory_mb"] = max(end_mem - start_mem, 0)
        metrics["exit_code"] = proc.returncode

    except subprocess.TimeoutExpired:
        proc.kill()
        metrics["error"] = "Tournament timed out"
    except Exception as e:
        metrics["error"] = str(e)

    return metrics


def check_consistency(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check consistency across successful runs."""
    consistency = {"all_6_matches": True, "all_3_rounds": True, "issues": []}

    for r in results:
        if r["matches_completed"] != 6:
            consistency["all_6_matches"] = False
            consistency["issues"].append(f"Run {r['run_id']}: {r['matches_completed']} matches")
        if r["rounds_completed"] != 3:
            consistency["all_3_rounds"] = False
            consistency["issues"].append(f"Run {r['run_id']}: {r['rounds_completed']} rounds")

    return consistency


def calculate_performance_metrics(successful_runs: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate performance metrics from successful runs."""
    if not successful_runs:
        return {"avg_duration": 0, "min_duration": 0, "max_duration": 0, "avg_memory_mb": 0}

    durations = [r["duration_seconds"] for r in successful_runs]

    return {
        "avg_duration": sum(durations) / len(durations),
        "min_duration": min(durations),
        "max_duration": max(durations),
        "avg_memory_mb": sum(r["memory_mb"] for r in successful_runs) / len(successful_runs),
    }


def print_formatted_report(report: Dict[str, Any]) -> None:
    """Print formatted report to console."""
    print("\n" + "=" * 60)
    print("TOURNAMENT REPORT")
    print("=" * 60)

    s = report["summary"]
    print(f"\nSummary:")
    print(f"  Total: {s['total_runs']} | Success: {s['successful']} | Failed: {s['failed']}")
    print(f"  Success Rate: {s['success_rate']:.1f}%")

    p = report["performance"]
    print(f"\nPerformance:")
    print(
        f"  Duration: {p['avg_duration']:.2f}s (min: {p['min_duration']:.2f}s, max: {p['max_duration']:.2f}s)"
    )
    print(f"  Memory: {p['avg_memory_mb']:.2f} MB")

    c = report["consistency"]
    print(f"\nConsistency:")
    print(
        f"  6 Matches: {'✅' if c['all_6_matches'] else '❌'} | 3 Rounds: {'✅' if c['all_3_rounds'] else '❌'}"
    )
    if c["issues"]:
        print(f"  Issues: {', '.join(c['issues'])}")

    if report["failures"]:
        print(f"\nFailures:")
        for f in report["failures"]:
            print(f"  Run {f['run_id']}: {f['error']}")

    print("\n" + "=" * 60)
