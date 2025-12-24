# Installation Guide

**Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete

---

## Overview

This guide provides step-by-step instructions for installing and configuring the AI Agent League Competition System on your local machine.

---

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **Python**: Version 3.9 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB free space
- **Network**: Internet connection for dependency installation

### Required Software
1. **Python 3.9+**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version` or `python3 --version`

2. **pip** (Python package manager)
   - Usually included with Python
   - Verify installation: `pip --version` or `pip3 --version`

3. **Git** (optional, for cloning repository)
   - Download from: https://git-scm.com/downloads
   - Verify installation: `git --version`

---

## Installation Steps

### Step 1: Obtain the Source Code

#### Option A: Clone from Repository (Recommended)
```bash
git clone https://github.com/your-org/assignment7.git
cd assignment7
```

#### Option B: Download ZIP Archive
1. Download the ZIP file from the repository
2. Extract to your desired location
3. Navigate to the extracted directory:
   ```bash
   cd assignment7
   ```

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment isolates the project dependencies from your system Python installation.

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal prompt indicating the virtual environment is active.

### Step 3: Install Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

This will install:
- **fastapi** (0.104.0+) - Web framework for agents
- **uvicorn** (0.24.0+) - ASGI server
- **httpx** (0.25.0+) - HTTP client for inter-agent communication
- **pydantic** (2.0.0+) - Data validation
- **pytest** (7.4.0+) - Testing framework
- **pytest-cov** (4.1.0+) - Code coverage reporting
- **pytest-asyncio** (0.21.0+) - Async test support

### Step 4: Verify Installation

Check that all dependencies are installed correctly:

```bash
pip list
```

You should see all the packages listed above in the output.

### Step 5: Install the League SDK Package

Install the project's shared SDK package in development mode:

```bash
pip install -e .
```

This installs the `league_sdk` package, making it importable from anywhere in the project.

### Step 6: Verify Project Structure

Ensure all required directories and files exist:

```bash
# Check main directories
ls -la SHARED/
ls -la agents/
ls -la tests/
ls -la doc/

# Check configuration files
ls -la SHARED/config/
ls -la SHARED/config/agents/
ls -la SHARED/config/leagues/
ls -la SHARED/config/games/
```

Expected directory structure:
```
assignment7/
├── SHARED/
│   ├── config/
│   ├── data/
│   ├── logs/
│   ├── league_sdk/
│   └── contracts/
├── agents/
│   ├── league_manager/
│   ├── launch_player_*.py
│   └── launch_referee_*.py
├── tests/
├── doc/
├── requirements.txt
├── setup.py
└── run_league.py
```

### Step 7: Verify Configuration Files

Check that all configuration files are present:

```bash
cat SHARED/config/system.json
cat SHARED/config/agents/agents_config.json
cat SHARED/config/leagues/league_2025_even_odd.json
cat SHARED/config/games/games_registry.json
```

All files should contain valid JSON.

### Step 8: Run Tests to Verify Installation

Execute the test suite to confirm everything is working:

```bash
pytest tests/ -v
```

Expected output:
```
===================== test session starts ======================
collected 139 items

tests/test_config_loader.py::test_load_system_config PASSED
tests/test_config_loader.py::test_load_league_config PASSED
...
===================== 139 passed in 1.60s ======================
```

All 139 tests should pass.

### Step 9: Check Line Count Compliance

Verify that all Python files comply with the 150-line limit:

```bash
pytest tests/test_line_count_compliance.py -v
```

Expected output:
```
tests/test_line_count_compliance.py::test_line_count_compliance PASSED
```

---

## Configuration

### System Configuration

Edit `SHARED/config/system.json` if needed:

```json
{
  "schema_version": "1.0",
  "protocol_version": "league.v2",
  "active_league_id": "league_2025_even_odd",
  "timeouts": {
    "match_timeout": 30,
    "response_timeout": 5,
    "registration_timeout": 10
  },
  "retry_policy": {
    "max_retries": 3,
    "retry_delay": 1
  }
}
```

### Agent Configuration

Agent endpoints and ports are defined in `SHARED/config/agents/agents_config.json`:

- **League Manager**: LM01 on port 8000
- **Referees**: REF01 (8001), REF02 (8002)
- **Players**: P01-P04 on ports 8101-8104

**Note**: Change ports if they conflict with other services on your machine.

### League Configuration

Tournament settings in `SHARED/config/leagues/league_2025_even_odd.json`:

```json
{
  "league_id": "league_2025_even_odd",
  "game_type": "even_odd",
  "scoring": {
    "win_points": 3,
    "draw_points": 1,
    "loss_points": 0
  },
  "total_rounds": 3,
  "matches_per_round": 2
}
```

---

## Troubleshooting

### Issue: Python Version Too Old

**Error**: `Python 3.9 or higher is required`

**Solution**:
```bash
# Check your Python version
python --version

# If too old, install Python 3.9+ from python.org
# Then use the new version explicitly:
python3.9 -m venv venv
```

### Issue: pip Command Not Found

**Error**: `'pip' is not recognized as an internal or external command`

**Solution**:
```bash
# Use python -m pip instead:
python -m pip install -r requirements.txt
```

### Issue: Permission Denied

**Error**: `Permission denied` when installing packages

**Solution**:
```bash
# On Windows, run Command Prompt as Administrator
# On macOS/Linux, use --user flag:
pip install --user -r requirements.txt
```

### Issue: Port Already in Use

**Error**: `[Errno 48] Address already in use`

**Solution**:
1. Find and kill the process using the port:
   ```bash
   # On Windows:
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # On macOS/Linux:
   lsof -ti:8000 | xargs kill -9
   ```

2. Or change the port in `agents_config.json`

### Issue: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'league_sdk'`

**Solution**:
```bash
# Make sure you installed the package:
pip install -e .

# If still not working, check PYTHONPATH:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Tests Failing

**Error**: Multiple test failures

**Solution**:
1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Check that configuration files are valid JSON

3. Clear any stale data:
   ```bash
   rm -rf SHARED/data/leagues/*/
   rm -rf SHARED/data/matches/*/
   ```

4. Re-run tests with verbose output:
   ```bash
   pytest tests/ -v -s
   ```

---

## Uninstallation

To remove the installation:

### Step 1: Deactivate Virtual Environment
```bash
deactivate
```

### Step 2: Remove Virtual Environment
```bash
# On Windows:
rmdir /s venv

# On macOS/Linux:
rm -rf venv
```

### Step 3: Remove Project Directory
```bash
cd ..
rm -rf assignment7
```

---

## Next Steps

After successful installation:

1. **Read the RUNNING.md guide** to learn how to start the system
2. **Read the TESTING.md guide** to understand the test suite
3. **Read the ARCHITECTURE.md** to understand system design
4. **Run a tournament** using `python run_league.py`

---

## Support

For issues not covered in this guide:

1. Check the `doc/` directory for additional documentation
2. Review test files in `tests/` for usage examples
3. Check configuration files in `SHARED/config/` for defaults
4. Run tests with `-v` flag for detailed output

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-20 | Initial installation guide |

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete ✅
