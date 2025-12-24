# Command: /check-coverage

## Check Test Coverage Report

---

## 📋 Overview

The `/check-coverage` command generates and displays code coverage reports for the project's test suite.

---

## 🎯 Usage

### Basic Usage

```bash
# Generate coverage report
/check-coverage

# Equivalent to:
pytest tests/ --cov=SHARED --cov=agents --cov=api --cov-report=term-missing
```

### With Options

```bash
# Coverage for specific module
/check-coverage SHARED

# HTML report
/check-coverage --html

# Missing lines only
/check-coverage --missing
```

---

## 🔧 Options

| Option | Description | Example |
|--------|-------------|---------|
| `<module>` | Specific module | `/check-coverage agents` |
| `--html` | Generate HTML report | `/check-coverage --html` |
| `--missing` | Show missing lines | `/check-coverage --missing` |
| `--threshold <n>` | Minimum coverage | `/check-coverage --threshold 70` |

---

## 📊 Example Output

```
----------- coverage: platform win32, python 3.11.0 -----------
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
SHARED/contracts/base_contract.py            45      5    89%   23-25, 67-68
SHARED/contracts/player_contracts.py         62      8    87%   45-52
SHARED/contracts/referee_contracts.py        58      6    90%   78-83
SHARED/league_sdk/circuit_breaker.py         89     12    87%   102-113
SHARED/league_sdk/config_loader.py           56      8    86%   34-41
SHARED/league_sdk/http_client.py             78     15    81%   45-59
SHARED/league_sdk/logger.py                  45      5    89%   67-71
SHARED/league_sdk/messages.py                92     10    89%   123-132
SHARED/league_sdk/validation.py              67      8    88%   89-96
agents/generic_player.py                    125     25    80%   45-69
agents/generic_referee.py                   142     28    80%   78-105
agents/player_strategies.py                  89     12    87%   56-67
agents/referee_game_logic.py                 78     10    87%   89-98
-----------------------------------------------------------------------
TOTAL                                      1126    152    86%

Required coverage: 70%
Actual coverage: 86% ✅
```

---

## 📈 Coverage Targets

| Module | Target | Current |
|--------|--------|---------|
| SHARED/contracts/ | 85% | 89% ✅ |
| SHARED/league_sdk/ | 80% | 86% ✅ |
| agents/ | 75% | 82% ✅ |
| api/ | 70% | 75% ✅ |
| **Overall** | **70%** | **86%** ✅ |

---

## 🔗 Implementation

```bash
# Generate terminal report
pytest tests/ --cov=SHARED --cov=agents --cov=api --cov-report=term-missing

# Generate HTML report
pytest tests/ --cov=SHARED --cov=agents --cov=api --cov-report=html

# View HTML report
start htmlcov/index.html
```

---

**Status**: Ready for use  
**Last Updated**: December 24, 2025
