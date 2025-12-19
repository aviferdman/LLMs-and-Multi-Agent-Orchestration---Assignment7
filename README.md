# AI Agent League Competition System

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

### Running a Tournament

**Option 1: Using Generic Agents (Recommended)**

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
assignment7/
├── SHARED/
│   ├── contracts/               # Protocol contracts (NEW!)
│   │   ├── base_contract.py    # Base message structure (league.v2)
│   │   ├── league_manager_contracts.py
│   │   ├── referee_contracts.py
│   │   └── player_contracts.py
│   ├── config/                  # Configuration files
│   │   ├── system.json         # Protocol v2, timeouts
│   │   ├── agents/             # Agent configurations
│   │   ├── leagues/            # League definitions
│   │   └── games/              # Game registry
│   ├── data/                    # Runtime data
│   ├── logs/                    # JSONL logs
│   └── league_sdk/             # Python SDK (7 modules)
├── agents/
│   ├── generic_player.py       # Generic player (all strategies)
│   ├── generic_referee.py      # Generic referee (all game types)
│   ├── league_manager/         # League orchestration (4 modules)
│   ├── referee_REF01/          # Shared referee logic
│   └── player_P01/             # Shared strategy implementations
├── tests/                       # Test suite
├── doc/                         # Documentation
├── run_league.py               # Orchestrator
└── README.md
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

## License

Academic project for LLMs and Multi-Agent Orchestration course.
