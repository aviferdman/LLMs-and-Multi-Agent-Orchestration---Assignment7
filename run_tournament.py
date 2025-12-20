#!/usr/bin/env python3
"""Tournament Runner - Automated E2E testing with performance metrics."""
import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from tournament_utils import (
    calculate_performance_metrics,
    check_consistency,
    clean_data,
    clean_logs,
    parse_tournament_logs,
    print_formatted_report,
    run_subprocess_with_metrics,
)

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "SHARED" / "data"


class TournamentRunner:
    """Manages tournament execution and metrics collection."""

    def __init__(self, timeout: int = 120):
        """Initialize runner with timeout."""
        self.timeout = timeout
        self.results: List[Dict[str, Any]] = []

    def run_single_tournament(self, run_id: int) -> Dict[str, Any]:
        """Run a single tournament and return results."""
        result = {
            "run_id": run_id,
            "success": False,
            "start_time": datetime.utcnow().isoformat() + "Z",
            "end_time": None,
            "duration_seconds": 0.0,
            "matches_completed": 0,
            "rounds_completed": 0,
            "standings": [],
            "memory_mb": 0.0,
            "error": None,
        }

        clean_logs()
        start_time = time.time()

        # Run subprocess and collect metrics
        cmd = [sys.executable, str(PROJECT_ROOT / "run_league.py")]
        metrics = run_subprocess_with_metrics(cmd, self.timeout, str(PROJECT_ROOT))

        result["exit_code"] = metrics["exit_code"]
        result["memory_mb"] = metrics["memory_mb"]
        result["error"] = metrics["error"]

        # Parse logs if no error
        if not result["error"]:
            result = parse_tournament_logs(result)

        end_time = time.time()
        result["end_time"] = datetime.utcnow().isoformat() + "Z"
        result["duration_seconds"] = round(end_time - start_time, 2)

        return result

    def run_multiple(self, num_runs: int) -> List[Dict[str, Any]]:
        """Run multiple tournaments and collect results."""
        self.results = []
        for i in range(1, num_runs + 1):
            print(f"\n{'='*60}")
            print(f"Tournament Run {i}/{num_runs}")
            print("=" * 60)

            result = self.run_single_tournament(i)
            self.results.append(result)

            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
            print(f"Status: {status}")
            print(f"Duration: {result['duration_seconds']:.2f}s")
            print(f"Matches: {result['matches_completed']}/6")
            print(f"Rounds: {result['rounds_completed']}/3")
            if result["error"]:
                print(f"Error: {result['error']}")

            time.sleep(2)

        return self.results

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive report from results."""
        if not self.results:
            return {"error": "No results to report"}

        successful = [r for r in self.results if r["success"]]
        failed = [r for r in self.results if not r["success"]]

        report = {
            "summary": {
                "total_runs": len(self.results),
                "successful": len(successful),
                "failed": len(failed),
                "success_rate": len(successful) / len(self.results) * 100,
            },
            "performance": calculate_performance_metrics(successful),
            "consistency": check_consistency(successful),
            "failures": [{"run_id": r["run_id"], "error": r["error"]} for r in failed],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        return report

    def save_report(self, report: Dict[str, Any], filepath: Path) -> None:
        """Save report to JSON file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {filepath}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tournament tests")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")
    parser.add_argument("--report", action="store_true", help="Save report to file")
    args = parser.parse_args()

    print("Tournament Runner - E2E Testing")
    print(f"Runs: {args.runs}, Timeout: {args.timeout}s")

    runner = TournamentRunner(timeout=args.timeout)
    runner.run_multiple(args.runs)

    report = runner.generate_report()
    print_formatted_report(report)

    if args.report:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_path = PROJECT_ROOT / "test_logs" / f"tournament_report_{ts}.json"
        runner.save_report(report, report_path)

    sys.exit(0 if report["summary"]["success_rate"] == 100 else 1)


if __name__ == "__main__":
    main()
