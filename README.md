# AI Agent League Competition System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Protocol](https://img.shields.io/badge/Protocol-league.v2-purple)
![Coverage](https://img.shields.io/badge/Coverage-70%25+-brightgreen)
![Tests](https://img.shields.io/badge/Tests-Passing-success)
![Status](https://img.shields.io/badge/Status-Production%20Ready-blue)

**Assignment 7**: Multi-Agent Even-Odd Game Competition  
**Protocol**: league.v2  
**Status**: Production Ready

## Overview

This project implements a competitive multi-agent system where autonomous AI agents compete in an Even-Odd game. The system features:

- **Game-Agnostic Architecture**: Three-layer design supporting future game extensions
- **Protocol-Driven Communication**: HTTP/MCP with strict JSON schema compliance (league.v2)
- **Distributed Agent Orchestration**: League Manager, Referees, and Players
- **Contract-Based Design**: Centralized protocol contracts in `SHARED/contracts/`
- **Zero Code Duplication**: Generic agents with configuration-driven behavior

## Quick Start

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

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=SHARED --cov=agents

# Generate HTML coverage report
pytest --cov=SHARED --cov=agents --cov-report=html
```

## Configuration

All agents are configured via `SHARED/config/agents/agents_config.json`:

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

## Features

✅ **Protocol v2**: league.v2 with centralized version management
✅ **Contract-Based**: All messages defined in `SHARED/contracts/`
✅ **Zero Duplication**: Generic agents configured via CLI
✅ **Game-Agnostic**: Extensible to new game types
✅ **ISO-8601 Timestamps**: All timestamps end with 'Z'
✅ **JSONL Logging**: One log per agent
✅ **Real-Time Rankings**: Points-based with tiebreakers
✅ **REST API**: Complete API with Swagger documentation (port 8080)
✅ **Web GUI**: Streamlit dashboard with live match view (port 8501)
✅ **Live Updates**: Real-time match visualization with player status  

## License

Academic project for LLMs and Multi-Agent Orchestration course.
