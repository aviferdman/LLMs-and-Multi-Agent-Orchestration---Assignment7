# Test Suite Documentation

This directory contains automated tests for the AI Agent League Competition System.

---

## Available Tests

### 1. Line Count Compliance Test
**File**: `test_line_count_compliance.py`

**Purpose**: Verifies that all Python files in the project meet the 150-line requirement.

**What it does**:
- Scans all Python files recursively
- Counts lines in each file
- Reports any files exceeding 150 lines
- Returns exit code 1 if violations found (for CI/CD)

**Run it**:
```bash
python tests/test_line_count_compliance.py
```

**Expected output**:
```
======================================================================
LINE COUNT COMPLIANCE TEST
======================================================================
Requirement: All Python files must be ≤150 lines

Total Python files scanned: 35
Files over 150 lines: 0

✅ ALL FILES COMPLIANT - No violations found
```

---

### 2. Refactoring Verification Test
**File**: `test_refactoring_verification.py`

**Purpose**: Verifies that all refactored modules work correctly after splitting.

**What it tests**:
1. **Constants Import** - All constants accessible from split modules
2. **Player Strategies** - All 3 strategies (Random, Frequency, Pattern) work
3. **Referee Modules** - Game logic and state machine functional
4. **Message Utilities** - Message building and validation work
5. **Generic Agents** - Both player and referee agents import successfully

**Run it**:
```bash
python tests/test_refactoring_verification.py
```

**Expected output**:
```
============================================================
REFACTORING VERIFICATION TESTS
============================================================
Testing constants imports...
  ✓ All constants imported (PROTOCOL=league.v2, HOST=0.0.0.0)
Testing player strategies...
  ✓ All 3 strategies work: EVEN, EVEN, ODD
Testing referee modules...
  ✓ Game rules work (drew 3, parity=odd)
  ✓ State machine & context work
Testing message utilities...
  ✓ Message built & validated: True
Testing generic agent imports...
  ✓ Both agents import successfully

============================================================
SUMMARY: 5/5 tests passed
============================================================

✅ ALL TESTS PASSED - Refactoring successful!
```

---

## Running All Tests

### Using pytest (recommended)
```bash
# Install pytest if not already installed
pip install pytest

# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=SHARED --cov=agents -v
```

### Running individually
```bash
# Line count compliance
python tests/test_line_count_compliance.py

# Refactoring verification
python tests/test_refactoring_verification.py
```

---

## CI/CD Integration

Both tests are designed for CI/CD integration:

- Exit code **0** = all tests passed
- Exit code **1** = tests failed

Example GitHub Actions workflow:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run line count compliance
        run: python tests/test_line_count_compliance.py
      - name: Run refactoring verification
        run: python tests/test_refactoring_verification.py
```

---

## Test Coverage

### Current Coverage
- **Line Count Compliance**: 100% (35/35 files)
- **Refactoring Verification**: 100% (5/5 tests passing)

### Future Tests (Planned)

**Phase 6.1 - SDK Unit Tests**:
- `test_config_loader.py` - Configuration loading
- `test_repositories.py` - Data persistence
- `test_messages.py` - Message building

**Phase 6.2 - League Manager Tests**:
- `test_scheduler.py` - Match scheduling
- `test_ranking.py` - Ranking calculation

**Phase 6.3 - Referee Tests**:
- `test_game_logic.py` - Game rules
- `test_state_machine.py` - State transitions

**Phase 6.4 - Player Tests**:
- `test_strategies.py` - Strategy behavior

**Phase 6.5 - Integration Tests**:
- `test_integration_registration.py`
- `test_integration_match.py`
- `test_integration_tournament.py`

**Phase 6.6 - Edge Case Tests**:
- `test_edge_cases.py` - 10+ edge cases

**Phase 6.7 - Protocol Compliance**:
- `test_protocol_compliance.py`

---

## Troubleshooting

### Test fails with import errors
**Solution**: Make sure you're running from project root:
```bash
cd /path/to/LLMs-and-Multi-Agent-Orchestration---Assignment7
python tests/test_name.py
```

### Test reports wrong file count
**Solution**: Tests automatically skip:
- `.venv/` directories
- `.git/` directories
- `__pycache__/` directories
- Hidden directories (starting with `.`)

### Line count test fails
**Solution**: Check which files are over 150 lines:
```bash
python tests/test_line_count_compliance.py
```
The output will list violating files with their line counts.

---

## Adding New Tests

### Template for new test file
```python
#!/usr/bin/env python3
"""Description of what this test does."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_something():
    """Test description."""
    # Your test code here
    assert True, "Test failed"
    return True

def main():
    """Run all tests."""
    tests = [test_something]
    results = [test() for test in tests]
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL {total} TESTS PASSED")
        return 0
    else:
        print(f"❌ {total - passed}/{total} TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## Contributing

When adding new code:
1. Run line count compliance test before committing
2. Add unit tests for new functionality
3. Run all tests to ensure nothing breaks
4. Update this README if adding new test files

---

## Documentation

For more details see:
- `doc/IMPLEMENTATION_PLAN.md` - Full implementation plan
- `doc/FINAL_REFACTORING_SUMMARY.md` - Refactoring details
- `doc/REFACTORING_COMPLETE.md` - Verification report

---

**Last Updated**: 2025-12-19  
**Test Suite Status**: ✅ All tests passing
