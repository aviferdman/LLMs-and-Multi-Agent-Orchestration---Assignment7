#!/usr/bin/env python3
"""Test that all Python files comply with 150-line limit.

Note: This is a code quality policy test. Some files may exceed the limit
during development. The test is marked as xfail (expected to fail) until
files are refactored.
"""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def get_all_python_files():
    """Get all Python files in the project."""
    files = []
    for root, dirs, filenames in os.walk(project_root):
        # Skip venv, hidden dirs, pycache, htmlcov, and tests
        if any(
            skip in root for skip in [".venv", ".git", "__pycache__", ".pytest", "htmlcov", "tests"]
        ):
            continue
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.join(root, filename))
    return files


def check_line_counts():
    """Check all files for line count compliance."""
    files = get_all_python_files()
    violations = []

    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                line_count = sum(1 for _ in f)
            if line_count > 150:
                violations.append((filepath, line_count))
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    return files, violations


def main():
    """Run line count compliance check."""
    print("=" * 70)
    print("LINE COUNT COMPLIANCE TEST")
    print("=" * 70)
    print("Requirement: All Python files must be ≤150 lines\n")

    files, violations = check_line_counts()

    print(f"Total Python files scanned: {len(files)}")
    print(f"Files over 150 lines: {len(violations)}\n")

    if violations:
        print("VIOLATIONS FOUND:")
        for filepath, lines in sorted(violations, key=lambda x: -x[1]):
            rel_path = os.path.relpath(filepath, project_root)
            print(f"  {lines:4} lines - {rel_path}")
        print(f"\n❌ TEST FAILED - {len(violations)} file(s) exceed 150 lines")
        return 1
    else:
        print("✅ ALL FILES COMPLIANT - No violations found")
        return 0


@pytest.mark.line_count
def test_line_count_compliance():
    """Pytest test for line count compliance."""
    files, violations = check_line_counts()
    assert len(violations) == 0, f"Files over 150 lines: {violations}"


if __name__ == "__main__":
    sys.exit(main())
