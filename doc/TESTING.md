# Testing Guide

**Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete

---

## Overview

This guide covers the comprehensive test suite for the AI Agent League Competition System, including how to run tests, interpret results, and generate coverage reports.

---

## Test Suite Overview

The project includes **139 passing tests** across **19 test files**, organized into several categories:

| Category | Tests | Files | Purpose |
|----------|-------|-------|---------|
| **Line Count Compliance** | 6 | 1 | Verify 150-line limit |
| **SDK Unit Tests** | 28 | 6 | Test SDK modules |
| **League Manager Tests** | 14 | 2 | Test scheduling & ranking |
| **Referee Tests** | 21 | 2 | Test game logic & state machine |
| **Player Tests** | 9 | 1 | Test player strategies |
| **Integration Tests** | 8 | 1 | Test end-to-end flows |
| **Edge Case Tests** | 24 | 2 | Test boundary conditions |
| **Protocol Tests** | 23 | 2 | Test message compliance |
| **Validation Tests** | 7 | 2 | Test input validation |

**Total**: 139 tests, all passing ✅

---

## Running Tests

### Run All Tests

Execute the entire test suite:

```bash
pytest tests/
```

Expected output:
```
===================== test session starts ======================
collected 139 items

tests/test_config_loader.py ......                       [  4%]
tests/test_edge_cases_game.py ..........                 [ 11%]
tests/test_edge_cases_validation.py ............        [ 20%]
...
===================== 139 passed in 1.60s =====================
```

### Run Specific Test File

```bash
pytest tests/test_game_logic.py
```

### Run Specific Test Function

```bash
pytest tests/test_game_logic.py::test_draw_number
```

### Run Tests by Pattern

```bash
# Run all validation tests
pytest tests/ -k validation

# Run all edge case tests
pytest tests/ -k edge_cases

# Run all protocol tests
pytest tests/ -k protocol
```

### Verbose Output

See detailed test output:

```bash
pytest tests/ -v
```

### Show Print Statements

See print() output during tests:

```bash
pytest tests/ -s
```

### Stop on First Failure

```bash
pytest tests/ -x
```

### Run in Parallel (faster)

```bash
pytest tests/ -n auto
```

Requires: `pip install pytest-xdist`

---

## Test Coverage

### Generate Coverage Report

Run tests with coverage analysis:

```bash
pytest tests/ --cov=SHARED/league_sdk --cov=agents
```

Output shows coverage percentages:
```
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
SHARED/league_sdk/__init__.py                7      0   100%
SHARED/league_sdk/config_loader.py          36      0   100%
SHARED/league_sdk/config_models.py          39      0   100%
...
------------------------------------------------------------
TOTAL                                     1021    472    54%
```

### Generate HTML Coverage Report

Create detailed HTML report:

```bash
pytest tests/ --cov=SHARED/league_sdk --cov=agents --cov-report=html
```

Open report in browser:

```bash
# On Windows:
start htmlcov/index.html

# On macOS:
open htmlcov/index.html

# On Linux:
xdg-open htmlcov/index.html
```

The HTML report shows:
- Line-by-line coverage
- Highlighted uncovered lines
- Coverage per module
- Interactive navigation

### Coverage Thresholds

Verify minimum coverage requirements:

```bash
pytest tests/ --cov=SHARED/league_sdk --cov=agents --cov-fail-under=50
```

This fails if coverage drops below 50%.

### Missing Lines Report

See which lines aren't covered:

```bash
pytest tests/ --cov=SHARED/league_sdk --cov=agents --cov-report=term-missing
```

---

## Test Categories

### 1. Line Count Compliance Tests

**File**: `tests/test_line_count_compliance.py`  
**Tests**: 6  
**Purpose**: Ensure all Python files are ≤150 lines

Run:
```bash
pytest tests/test_line_count_compliance.py -v
```

Tests:
- `test_line_count_compliance` - Scans all .py files
- `test_constants_split` - Verifies constants modules
- `test_player_refactoring` - Verifies player split
- `test_referee_refactoring` - Verifies referee split
- `test_messages_refactoring` - Verifies messages split
- `test_no_violations` - Confirms 0 violations

### 2. SDK Unit Tests

**Files**: 
- `tests/test_config_loader.py` (6 tests)
- `tests/test_standings_repo.py` (2 tests)
- `tests/test_match_repo.py` (2 tests)
- `tests/test_player_history_repo.py` (2 tests)
- `tests/test_messages.py` (10 tests)
- `tests/test_validation_basic.py` (3 tests)
- `tests/test_validation_advanced.py` (4 tests)

Run SDK tests:
```bash
pytest tests/test_config_loader.py tests/test_*_repo.py tests/test_messages.py tests/test_validation*.py
```

Key tests:
- Configuration loading and parsing
- Data persistence (standings, matches, history)
- Message building and validation
- Timestamp and UUID format validation

### 3. League Manager Tests

**Files**:
- `tests/test_scheduler.py` (9 tests)
- `tests/test_ranking.py` (5 tests)

Run:
```bash
pytest tests/test_scheduler.py tests/test_ranking.py
```

Key tests:
- Round-robin schedule generation
- Player pairing coverage
- Referee assignment
- Ranking calculation
- Tiebreaker logic (points, then wins)

### 4. Referee Tests

**Files**:
- `tests/test_game_logic.py` (8 tests)
- `tests/test_state_machine.py` (13 tests)

Run:
```bash
pytest tests/test_game_logic.py tests/test_state_machine.py
```

Key tests:
- Number drawing (1-10 range)
- Parity determination (even/odd)
- Winner calculation
- State transitions
- Match context management

### 5. Player Tests

**File**: `tests/test_strategies.py` (9 tests)

Run:
```bash
pytest tests/test_strategies.py
```

Key tests:
- RandomStrategy behavior
- FrequencyStrategy adaptation
- PatternStrategy detection
- Valid parity output

### 6. Integration Tests

**File**: `tests/test_integration_data.py` (8 tests)

Run:
```bash
pytest tests/test_integration_data.py
```

Key tests:
- Complete tournament flow
- All matches saved correctly
- Standings calculated correctly
- Player statistics accurate
- Data consistency checks

### 7. Edge Case Tests

**Files**:
- `tests/test_edge_cases_validation.py` (14 tests)
- `tests/test_edge_cases_game.py` (10 tests)

Run:
```bash
pytest tests/test_edge_cases_*.py
```

Key tests:
- Empty datasets
- Malformed messages
- Invalid inputs
- Boundary values
- Missing fields
- Format violations

### 8. Protocol Tests

**Files**:
- `tests/test_protocol_structure.py` (13 tests)
- `tests/test_protocol_types.py` (10 tests)

Run:
```bash
pytest tests/test_protocol_*.py
```

Key tests:
- Required fields present
- Protocol version correct
- Timestamp format (ISO-8601 with Z)
- UUID format (v4)
- Message type enumeration
- Full message compliance

---

## Test Data

### Test Fixtures

Tests use fixtures in `tests/` for:
- Sample configurations
- Mock match data
- Test standings
- Player histories

### Temporary Data

Tests create temporary directories:
```
/tmp/test_data_*/
```

Cleaned up automatically after tests.

### Test Configurations

Special test configs in `tests/`:
- `test_config_*.json` - Test configuration files
- Used instead of production configs during testing

---

## Continuous Integration

### Running Tests in CI/CD

Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .
      - name: Run tests
        run: pytest tests/ --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### Pre-commit Hooks

Run tests before every commit:

```bash
# .git/hooks/pre-commit
#!/bin/sh
pytest tests/ -x
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Writing New Tests

### Test Template

```python
"""
Test module for [component].
"""
import pytest
from [module] import [function]


def test_[feature]():
    """Test [specific behavior]."""
    # Arrange
    input_data = "test"
    
    # Act
    result = function(input_data)
    
    # Assert
    assert result == expected_value


def test_[error_case]():
    """Test error handling for [scenario]."""
    with pytest.raises(ValueError):
        function(invalid_input)
```

### Best Practices

1. **One assertion per test** (when possible)
2. **Descriptive test names** - `test_scheduler_creates_six_matches`
3. **AAA pattern** - Arrange, Act, Assert
4. **Use fixtures** for repeated setup
5. **Test edge cases** - empty, None, invalid
6. **Mock external dependencies** (network, files)
7. **Keep tests independent** - no shared state

### Running Your New Test

```bash
pytest tests/test_your_module.py::test_your_function -v
```

---

## Debugging Tests

### Run with Python Debugger

```bash
pytest tests/test_game_logic.py --pdb
```

Drops into debugger on failure.

### Print Debugging

```bash
pytest tests/test_game_logic.py -s
```

Shows all print() statements.

### Capture Warnings

```bash
pytest tests/ -W all
```

### Show Local Variables on Failure

```bash
pytest tests/ -l
```

### Detailed Failure Output

```bash
pytest tests/ --tb=long
```

---

## Performance Testing

### Measure Test Duration

```bash
pytest tests/ --durations=10
```

Shows 10 slowest tests.

### Profile Tests

```bash
pytest tests/ --profile
```

Requires: `pip install pytest-profiling`

---

## Test Maintenance

### Update Test Data

When protocol changes:
1. Update message examples in `tests/`
2. Regenerate test fixtures
3. Update assertions

### Fixing Broken Tests

1. **Read the error message carefully**
2. **Run just the failing test** with `-v`
3. **Check recent code changes**
4. **Verify test data is still valid**
5. **Update test if requirements changed**

### Removing Obsolete Tests

When removing features:
1. Remove corresponding tests
2. Update coverage expectations
3. Document in commit message

---

## Coverage Goals

### Current Coverage: 54%

| Component | Coverage | Status |
|-----------|----------|--------|
| SDK Core | 83% | ✅ Excellent |
| Game Logic | 79% | ✅ Good |
| Scheduler | 100% | ✅ Perfect |
| State Machine | 100% | ✅ Perfect |
| HTTP Layer | 30-38% | ✅ Appropriate (integration tested) |

### Target Coverage

- **Minimum**: 50% overall ✅ **ACHIEVED**
- **SDK modules**: ≥70% ✅ **ACHIEVED (83%)**
- **Critical modules**: ≥90% ✅ **ACHIEVED (9 modules)**

### Improving Coverage

To increase coverage:

1. **Identify uncovered lines**:
   ```bash
   pytest --cov --cov-report=term-missing
   ```

2. **Write tests for uncovered code**
3. **Focus on business logic** first
4. **Accept low coverage for**:
   - Framework integration code
   - Error handling for rare cases
   - Logging statements

---

## Test Reports

### JUnit XML Report

For CI/CD systems:

```bash
pytest tests/ --junitxml=report.xml
```

### JSON Report

```bash
pytest tests/ --json-report --json-report-file=report.json
```

Requires: `pip install pytest-json-report`

### HTML Report

Pretty HTML output:

```bash
pytest tests/ --html=report.html
```

Requires: `pip install pytest-html`

---

## Troubleshooting

### Tests Pass Locally, Fail in CI

**Possible causes**:
- Different Python version
- Different dependency versions
- Missing environment variables
- File path differences (Windows vs Linux)

**Solution**:
- Pin dependency versions in `requirements.txt`
- Use `pytest tests/ -v` for detailed output
- Check CI logs carefully

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
pip install -e .
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Slow Tests

**If tests take >5 seconds**:

1. Run with profiling: `pytest --durations=10`
2. Identify slow tests
3. Use mocks for I/O operations
4. Run in parallel: `pytest -n auto`

---

## Next Steps

- **Read RUNNING.md** to learn how to run the system
- **Review COVERAGE_REPORT.md** for detailed coverage analysis
- **Check test files** in `tests/` for examples
- **Write new tests** for any new features

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete ✅
