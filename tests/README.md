# Test Suite Documentation

This directory contains 420+ automated tests for the AI Agent League Competition System.

---

## Quick Start

```bash
# Run all tests
pytest tests/ -v

# Run with coverage (agents and SHARED modules)
pytest tests/ --cov=agents --cov=SHARED --cov-fail-under=50

# Run specific test file
pytest tests/test_agents_registration.py -v

# Run tests matching a pattern
pytest tests/ -k "contract" -v
```

---

## Test Statistics

| Metric | Value |
|--------|-------|
| **Total Tests** | 420+ |
| **Passing** | 420+ |
| **Skipped** | 11 |
| **Coverage** | 52%+ (agents/SHARED) |
| **Coverage Threshold** | 50% |

---

## Test Categories

### Contract Tests (`test_contracts_*.py`, `test_cov_*.py`)
Tests for protocol message contracts and builders.

| File | Description |
|------|-------------|
| `test_contracts_league_manager.py` | League manager contract tests |
| `test_contracts_player.py` | Player contract tests |
| `test_contracts_referee.py` | Referee contract tests |
| `test_cov_base_contract.py` | Base contract builder tests |
| `test_cov_game_result.py` | Game result contract tests |
| `test_cov_jsonrpc.py` | JSON-RPC helper tests |
| `test_cov_registration.py` | Registration contract tests |
| `test_cov_round.py` | Round contract tests |
| `test_cov_standings.py` | Standings contract tests |
| `test_cov_exceptions.py` | Contract exception tests |
| `test_cov_validators.py` | Validation helper tests |

### Agent Tests (`test_agents_*.py`, `test_cov_ref_*.py`, `test_cov_strategies.py`)
Tests for player and referee agent logic.

| File | Description |
|------|-------------|
| `test_agents_registration.py` | Agent registration tests |
| `test_agents_timeout.py` | Timeout handling tests |
| `test_cov_ref_game.py` | Referee game logic tests |
| `test_cov_strategies.py` | Player strategy tests |

### Protocol Tests (`test_protocol_*.py`)
Tests for protocol compliance and message validation.

| File | Description |
|------|-------------|
| `test_protocol_compliance.py` | Protocol compliance tests |
| `test_protocol_game_flow.py` | Game flow protocol tests |
| `test_protocol_fields.py` | Protocol field tests |
| `test_cov_proto_const.py` | Protocol constants tests |

### Integration Tests (`test_integration_*.py`)
End-to-end integration tests.

| File | Description |
|------|-------------|
| `test_integration_registration.py` | Registration flow tests |
| `test_integration_match.py` | Match execution tests |
| `test_integration_league.py` | League orchestration tests |

### Edge Case Tests (`test_edge_cases_*.py`)
Tests for error handling and edge cases.

| File | Description |
|------|-------------|
| `test_edge_cases_game.py` | Game edge cases |
| `test_edge_cases_timeout.py` | Timeout edge cases |

### Infrastructure Tests
Core infrastructure and utility tests.

| File | Description |
|------|-------------|
| `test_circuit_breaker.py` | Circuit breaker pattern tests |
| `test_config_loader.py` | Configuration loading tests |
| `test_scheduler.py` | Match scheduler tests |
| `test_ranking.py` | Ranking calculation tests |
| `test_state_machine.py` | State machine tests |
| `test_messages.py` | Message builder tests |
| `test_validation_helpers.py` | Validation utility tests |

### Compliance Tests
Code quality and compliance tests.

| File | Description |
|------|-------------|
| `test_line_count_compliance.py` | All Python files ≤150 lines |

---

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### With Coverage Report
```bash
# Terminal coverage report
pytest tests/ --cov=agents --cov=SHARED --cov-report=term

# HTML coverage report
pytest tests/ --cov=agents --cov=SHARED --cov-report=html

# With minimum threshold
pytest tests/ --cov=agents --cov=SHARED --cov-fail-under=50
```

### Specific Categories
```bash
# Contract tests only
pytest tests/test_contracts_*.py tests/test_cov_*.py -v

# Integration tests only
pytest tests/test_integration_*.py -v

# Edge case tests only
pytest tests/test_edge_cases_*.py -v
```

### By Pattern
```bash
# All registration tests
pytest tests/ -k "registration" -v

# All timeout tests
pytest tests/ -k "timeout" -v

# All strategy tests
pytest tests/ -k "strategy" -v
```

---

## Coverage Configuration

Coverage is configured in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["agents", "SHARED"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "agents/launch_*.py",
    "agents/league_manager/main.py",
    "agents/league_manager/orchestration.py",
    "run_*.py",
]

[tool.coverage.report]
fail_under = 50
```

**Note**: `api/` and `gui/` directories are excluded from coverage.

---

## CI/CD Integration

Tests are designed for CI/CD with proper exit codes:
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
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -e .
      - name: Run tests with coverage
        run: pytest tests/ --cov=agents --cov=SHARED --cov-fail-under=50
      - name: Line count compliance
        run: pytest tests/test_line_count_compliance.py -v
```

---

## Troubleshooting

### Import Errors
```bash
# Make sure package is installed in development mode
pip install -e .

# Run from project root
cd /path/to/LLMs-and-Multi-Agent-Orchestration---Assignment7
pytest tests/ -v
```

### Coverage Too Low
```bash
# Check what's not covered
pytest tests/ --cov=agents --cov=SHARED --cov-report=term-missing
```

### Specific Test Failing
```bash
# Run with verbose output and full traceback
pytest tests/test_specific.py -v --tb=long
```

---

## Adding New Tests

### File Naming Convention
- `test_<module>_<feature>.py` for feature tests
- `test_cov_<module>.py` for coverage-focused tests
- `test_<category>_<subcategory>.py` for categorized tests

### Test Structure
```python
"""Tests for <module> functionality."""

import pytest
from SHARED.module import function_to_test


class TestFeatureName:
    """Tests for specific feature."""

    def test_basic_functionality(self):
        """Test basic case."""
        result = function_to_test(input)
        assert result == expected

    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

### Line Count Requirement
All test files must be **≤150 lines**. If a test file grows too large, split it into multiple files.

---

## Documentation Links

- [Main README](../README.md) - Project overview
- [Architecture](../doc/ARCHITECTURE.md) - System design
- [Protocol Spec](../doc/protocol_spec.md) - Protocol details
- [Testing Guide](../doc/TESTING.md) - Testing strategy

---

**Last Updated**: 2025-12-25  
**Test Suite Status**: ✅ 420+ tests passing, 52%+ coverage
