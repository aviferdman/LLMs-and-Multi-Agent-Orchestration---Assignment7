# Command: /run-tests

## Execute Test Suite

---

## 📋 Overview

The `/run-tests` command executes the project's test suite with various options for filtering, coverage, and output format.

---

## 🎯 Usage

### Basic Usage

```bash
# Run all tests
/run-tests

# Equivalent to:
pytest tests/ -v
```

### With Options

```bash
# Run specific test file
/run-tests test_agents.py

# Run tests matching pattern
/run-tests -k "player"

# Run with coverage
/run-tests --cov

# Run with verbose output
/run-tests -vv
```

---

## 🔧 Options

| Option | Description | Example |
|--------|-------------|---------|
| `<file>` | Specific test file | `/run-tests test_agents.py` |
| `-k <pattern>` | Filter by name | `/run-tests -k "player"` |
| `--cov` | Include coverage | `/run-tests --cov` |
| `-v` | Verbose output | `/run-tests -v` |
| `--fast` | Skip slow tests | `/run-tests --fast` |
| `--edge` | Edge cases only | `/run-tests --edge` |

---

## 📊 Example Output

```
========================= test session starts =========================
platform win32 -- Python 3.11.0, pytest-7.4.0
collected 228 items

tests/test_agents.py ............................            [ 12%]
tests/test_circuit_breaker.py ................             [ 19%]
tests/test_config_loader.py ............                   [ 25%]
tests/test_contracts_league_manager.py ..........          [ 29%]
tests/test_contracts_player.py ............                [ 34%]
tests/test_contracts_referee.py ..............             [ 40%]
tests/test_edge_cases_game.py ..........                   [ 45%]
tests/test_edge_cases_timeout.py ........                  [ 48%]
tests/test_edge_cases_validation.py ..........             [ 53%]
tests/test_game_logic.py ................                  [ 60%]
tests/test_integration.py ..............                   [ 66%]
tests/test_messages.py ................                    [ 73%]
tests/test_protocol_compliance_e2e.py ..........           [ 78%]
...

========================= 228 passed in 12.34s =========================
```

---

## 🔗 Implementation

```bash
# Actual command executed
pytest tests/ -v --tb=short

# With coverage
pytest tests/ -v --cov=SHARED --cov=agents --cov=api --cov-report=term-missing
```

---

## ✅ Test Categories

| Category | Count | Command |
|----------|-------|---------|
| All | 228 | `/run-tests` |
| Unit | 150+ | `/run-tests tests/test_*.py` |
| Integration | 50+ | `/run-tests tests/test_integration*.py` |
| Edge Cases | 28 | `/run-tests -k "edge"` |
| Protocol | 20+ | `/run-tests -k "protocol"` |

---

**Status**: Ready for use  
**Last Updated**: December 24, 2025
