# AI Agent League Competition System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Protocol](https://img.shields.io/badge/Protocol-league.v2-purple)
![Coverage](https://img.shields.io/badge/Coverage-70%25+-brightgreen)
![Tests](https://img.shields.io/badge/Tests-228%20Passing-success)
![Status](https://img.shields.io/badge/Status-Production%20Ready-blue)
![ISO 25010](https://img.shields.io/badge/ISO%2025010-Compliant-brightgreen)
![Documentation](https://img.shields.io/badge/Documentation-Complete-brightgreen)

**Assignment 7**: Multi-Agent Even-Odd Game Competition  
**Protocol**: league.v2  
**Status**: Production Ready ✅

---

## 📚 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Quick Navigation](#-quick-navigation)
4. [Quick Start](#-quick-start)
5. [Project Structure](#-project-structure)
6. [Architecture](#-architecture)
7. [Documentation Guide](#-documentation-guide)
8. [Running the System](#-running-the-system)
9. [Testing](#-testing)
10. [Troubleshooting](#-troubleshooting)
11. [Contributing](#-contributing)

---

## 🎯 Project Overview

This project implements a competitive multi-agent system where autonomous AI agents compete in an Even-Odd game tournament. The system uses a three-layer architecture with protocol-driven communication.

### MCP-Based Architecture

**Every agent in the system is an MCP (Model Context Protocol) server.** This includes:
- **League Manager** - MCP server for tournament orchestration
- **Referees** - MCP servers for match execution and rule enforcement
- **Players** - MCP servers for game participation with pluggable strategies

All agents communicate via HTTP POST requests to `/mcp` endpoints, enabling standardized, protocol-driven inter-agent communication.

### Research Question
**Can we design a scalable multi-agent competition system with protocol-driven communication and strategy-based gameplay?**

### What We've Built

| Component | Description | Status |
|-----------|-------------|--------|
| League Manager | Tournament orchestration | ✅ Complete |
| Referees (x2) | Match execution & rules | ✅ Complete |
| Players (x4) | Strategy-based agents | ✅ Complete |
| REST API | FastAPI with WebSocket | ✅ Complete |
| Streamlit GUI | Interactive dashboard | ✅ Complete |
| Protocol | league.v2 specification | ✅ Complete |
| Test Suite | 228 tests, 70%+ coverage | ✅ Complete |

---

## 🌟 Key Features

### 🏗️ Architecture Excellence
- ✅ Three-layer design (Orchestration, Execution, Participation)
- ✅ Protocol-driven communication (league.v2)
- ✅ Contract-based design (centralized in `SHARED/contracts/`)
- ✅ Zero code duplication (generic agents)
- ✅ Fault tolerance (circuit breaker pattern)

### 🎮 Game Features
- ✅ Even-Odd game implementation
- ✅ Best-of-5 match format
- ✅ Round-robin scheduling
- ✅ Multiple player strategies (Random, Frequency, Pattern)
- ✅ Real-time match visualization

### 📊 Observability
- ✅ JSONL structured logging
- ✅ Real-time WebSocket updates
- ✅ Comprehensive audit trail
- ✅ Performance metrics

### 🧪 Quality Assurance
- ✅ 228 automated tests
- ✅ 70%+ code coverage
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ ISO 25010 compliance audit
- ✅ Type hints throughout

---

## 🧭 Quick Navigation

### 📖 For Different User Types

**First-Time Visitors:**
1. ➜ Start here: **[START_HERE.md](START_HERE.md)** (5 min)
2. Then read: **[README.md](README.md)** - This file (15 min)
3. Try the GUI: `python run_gui.py`

**Researchers & Analysts:**
1. ➜ Read: **[doc/PRD.md](doc/PRD.md)** - Requirements (20 min)
2. Study: **[doc/AGENT_STRATEGY.md](doc/AGENT_STRATEGY.md)** - Strategies (15 min)
3. Review: **[doc/STATISTICAL_ANALYSIS.md](doc/STATISTICAL_ANALYSIS.md)** (15 min)

**Developers & Engineers:**
1. ➜ Read: **[doc/ARCHITECTURE.md](doc/ARCHITECTURE.md)** - System design (15 min)
2. Check: **[doc/protocol_spec.md](doc/protocol_spec.md)** - Protocol (20 min)
3. Review: **[doc/API.md](doc/API.md)** - API documentation (15 min)

**QA Engineers:**
1. ➜ Read: **[doc/TESTING.md](doc/TESTING.md)** - Test strategy (10 min)
2. Check: **[doc/EDGE_CASES.md](doc/EDGE_CASES.md)** - Edge cases (15 min)
3. Run: `pytest tests/ -v --cov`

### 📂 Document Map

| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| **[START_HERE.md](START_HERE.md)** | Quick navigation | Everyone | 5 min |
| **[README.md](README.md)** | This file | Everyone | 15 min |
| **[doc/ARCHITECTURE.md](doc/ARCHITECTURE.md)** | System design | Developers | 15 min |
| **[doc/PRD.md](doc/PRD.md)** | Requirements | Stakeholders | 20 min |
| **[doc/protocol_spec.md](doc/protocol_spec.md)** | Protocol details | Developers | 20 min |
| **[doc/API.md](doc/API.md)** | API documentation | Developers | 15 min |
| **[doc/AGENT_STRATEGY.md](doc/AGENT_STRATEGY.md)** | Player strategies | Researchers | 15 min |
| **[doc/TESTING.md](doc/TESTING.md)** | Test strategy | QA | 10 min |
| **[doc/EDGE_CASES.md](doc/EDGE_CASES.md)** | Edge case handling | Developers | 15 min |
| **[doc/SECURITY.md](doc/SECURITY.md)** | Security docs | Security | 15 min |
| **[doc/ISO_25010_COMPLIANCE.md](doc/ISO_25010_COMPLIANCE.md)** | Quality audit | QA | 20 min |
| **[doc/ADRs/](doc/ADRs/)** | Design decisions | Architects | 30 min |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Contribution guide | Contributors | 10 min |
| **[PROJECT_COMPLETION_SUMMARY.md](PROJECT_COMPLETION_SUMMARY.md)** | Completion report | Everyone | 10 min |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install league_sdk package
pip install -e .
```

### Running the System

**Option 1: With GUI (Recommended)**

```bash
# Terminal 1: Start the API server
python run_api.py

# Terminal 2: Start the GUI
python run_gui.py
```

The GUI will open at `http://localhost:8501` with:
- 🚀 League Launcher (start new leagues with game selection)
- 📊 Dashboard (league overview and statistics)
- 📺 Live Match View (real-time match updates)
- 🏅 Standings (rankings and charts)
- 📋 Matches (match history and filtering)
- 👥 Players (player profiles and stats)

**Option 2: Command Line Only**

```bash
# Start League Manager
python agents/league_manager/main.py

# Start Referees
python agents/generic_referee.py --referee-id REF01 --port 8001
python agents/generic_referee.py --referee-id REF02 --port 8002

# Start Players
python agents/generic_player.py --player-id P01 --strategy random --port 8101
python agents/generic_player.py --player-id P02 --strategy frequency --port 8102
python agents/generic_player.py --player-id P03 --strategy pattern --port 8103
python agents/generic_player.py --player-id P04 --strategy random --port 8104
```

**Option 2: Using Orchestrator**

```bash
python run_league.py
```

## Project Structure

```
.
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Test configuration
├── setup.py                     # Package setup
├── run_api.py                   # Entry: API server
├── run_gui.py                   # Entry: GUI dashboard
├── run_league.py                # Entry: League system
├── run_tournament.py            # Entry: Tournament runner
├── SHARED/
│   ├── contracts/               # Protocol contracts
│   │   ├── base_contract.py     # Base message structure (league.v2)
│   │   ├── game_flow_contracts.py
│   │   ├── game_result_contracts.py
│   │   ├── match_control_contracts.py
│   │   ├── player_contracts.py
│   │   ├── referee_contracts.py
│   │   ├── registration_contracts.py
│   │   ├── round_contracts.py
│   │   └── standings_contracts.py
│   ├── config/                  # Configuration files
│   │   ├── system.json          # Protocol v2, timeouts
│   │   ├── agents/              # Agent configurations
│   │   ├── leagues/             # League definitions
│   │   └── games/               # Game registry
│   ├── data/                    # Runtime data (gitignored)
│   ├── logs/                    # JSONL logs (gitignored)
│   └── league_sdk/              # Python SDK
│       ├── circuit_breaker.py   # Fault tolerance
│       ├── config_loader.py     # Configuration
│       ├── http_client.py       # Transport
│       ├── logger.py            # JSONL logging
│       ├── messages.py          # Message builders
│       ├── repositories.py      # Data persistence
│       └── validation.py        # Protocol validation
├── agents/
│   ├── generic_player.py        # Generic player (all strategies)
│   ├── generic_referee.py       # Generic referee (all game types)
│   ├── player_strategies.py     # Strategy implementations
│   ├── referee_game_logic.py    # Game logic
│   ├── referee_match_state.py   # Match state machine
│   └── league_manager/          # League orchestration
│       ├── main.py              # League manager entry
│       ├── ranking.py           # Standings calculation
│       └── scheduler.py         # Round-robin scheduling
├── api/                         # REST API (FastAPI)
│   ├── main.py                  # API entry point
│   ├── routes/                  # API endpoints
│   ├── schemas/                 # Pydantic models
│   ├── services/                # Business logic
│   └── websocket/               # WebSocket support
├── gui/                         # Streamlit GUI
│   ├── app.py                   # GUI entry point
│   ├── pages/                   # Dashboard pages
│   └── components/              # Reusable components
├── doc/                         # Documentation
│   ├── specs/                   # Assignment requirements
│   ├── protocol/                # Protocol documentation
│   ├── messageexamples/         # JSON message examples
│   ├── diagrams/                # Architecture diagrams
│   └── PROJECT_REPORT.md        # Consolidated report
└── tests/                       # Test suite (228 tests)
```

## Key Improvements (v2)

### 1. Protocol Version: league.v2
- Updated from league.v1 to league.v2
- Centralized version management in `SHARED/contracts/base_contract.py`
- All messages use `PROTOCOL_VERSION = "league.v2"`

### 2. Contracts Folder
All protocol contracts are now centralized in `SHARED/contracts/`:
- `base_contract.py` - Core message structure and validation
- `league_manager_contracts.py` - LM ↔ Referee/Player registration
- `referee_contracts.py` - Referee ↔ Player game messages  
- `player_contracts.py` - Player → Referee responses

**Benefits:**
- Single source of truth for all message formats
- Easy to modify contracts system-wide
- Clear separation of concerns
- Future-proof for protocol changes

### 3. Zero Code Duplication

**Generic Player Agent:**
```bash
python agents/generic_player.py --player-id P01 --strategy random --port 8101
```
- One codebase for all players
- Strategy selected via command-line argument
- Supports: random, frequency, pattern

**Generic Referee Agent:**
```bash
python agents/generic_referee.py --referee-id REF01 --port 8001
```
- One codebase for all referees
- Game type loaded dynamically
- Referee ID passed as argument

## Architecture

### Protocol Messages (league.v2)

**Registration:**
1. `REFEREE_REGISTER_REQUEST/RESPONSE`
2. `LEAGUE_REGISTER_REQUEST/RESPONSE`

**Game Flow:**
3. `GAME_INVITATION` (Referee → Player)
4. `GAME_JOIN_ACK` (Player → Referee)
5. `CHOOSE_PARITY_CALL` (Referee → Player)
6. `PARITY_CHOICE` (Player → Referee)
7. `GAME_OVER` (Referee → Players)
8. `MATCH_RESULT_REPORT` (Referee → League Manager)

### Strategies

- **Random**: Baseline 50/50 choice
- **Frequency**: Counters opponent's most frequent choice
- **Pattern**: Detects 3-choice sequences for prediction

## Documentation

- [Design Document](doc/DESIGN_DOCUMENT.md) - Complete system architecture
- [Implementation Plan](doc/IMPLEMENTATION_PLAN.md) - Step-by-step build guide  
- [PRD](doc/PRD.md) - Product requirements

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=SHARED --cov=agents --cov=api

# Generate HTML coverage report
pytest tests/ --cov=SHARED --cov=agents --cov=api --cov-report=html
```

### Test Summary

| Category | Count | Status |
|----------|-------|--------|
| Unit Tests | 150+ | ✅ Passing |
| Integration Tests | 50+ | ✅ Passing |
| Edge Case Tests | 28 | ✅ Passing |
| **Total** | **228** | ✅ **100%** |

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Import Errors

```bash
# Reinstall in development mode
pip install -e .
```

### Tests Failing

```bash
# Run with verbose output
pytest tests/ -v --tb=short

# Run specific test
pytest tests/test_agents.py -v
```

### GUI Not Loading

```bash
# Kill existing Streamlit process
Get-NetTCPConnection -LocalPort 8501 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Restart GUI
python run_gui.py
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes with tests
4. Run tests: `pytest tests/ -v`
5. Submit pull request

---

## 📊 Configuration

All agents configured via `SHARED/config/agents/agents_config.json`:

```json
{
  "league_manager": { "agent_id": "LM01", "port": 8000 },
  "referees": [
    { "referee_id": "REF01", "port": 8001 },
    { "referee_id": "REF02", "port": 8002 }
  ],
  "players": [
    { "player_id": "P01", "strategy": "random", "port": 8101 },
    { "player_id": "P02", "strategy": "frequency", "port": 8102 },
    { "player_id": "P03", "strategy": "pattern", "port": 8103 },
    { "player_id": "P04", "strategy": "random", "port": 8104 }
  ]
}
```

---

## ✨ Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| Protocol v2 | ✅ | league.v2 with centralized version |
| Contract-Based | ✅ | All messages in `SHARED/contracts/` |
| Zero Duplication | ✅ | Generic agents via CLI |
| Game-Agnostic | ✅ | Extensible to new games |
| ISO-8601 Timestamps | ✅ | All timestamps end with 'Z' |
| JSONL Logging | ✅ | One log per agent |
| Real-Time Rankings | ✅ | Points with tiebreakers |
| REST API | ✅ | FastAPI with OpenAPI docs |
| Web GUI | ✅ | Streamlit dashboard |
| Live Updates | ✅ | WebSocket real-time |
| CI/CD | ✅ | GitHub Actions pipeline |
| Test Coverage | ✅ | 70%+ coverage |

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

<div align="center">

## 🎯 Project Status: PRODUCTION READY

**228 Tests Passing** | **70%+ Coverage** | **ISO 25010 Compliant**

**Built with ❤️ for Multi-Agent Orchestration**

[START_HERE.md](START_HERE.md) | [Documentation](doc/) | [Contributing](CONTRIBUTING.md)

</div>
