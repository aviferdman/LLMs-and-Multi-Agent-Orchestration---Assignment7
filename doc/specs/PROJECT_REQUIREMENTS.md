# Assignment 7 - Project Requirements

**Document Version**: 2.0  
**Created**: December 13, 2025  
**Updated**: December 19, 2025  
**Status**: Planning Phase  

---

## 📋 Overview

This document defines the requirements for Assignment 7: AI Agent League Competition. The project implements a multi-agent system where autonomous agents compete in an Even-Odd game following a standardized MCP-based protocol.

---

## 🎯 Core Requirements Summary

Based on the assignment specification and multi-agent competition requirements:

### 1. **Project Structure** (20% of grade)
### 2. **Protocol Compliance** (25% of grade)
### 3. **Agent Implementation** (25% of grade)
### 4. **Testing & QA** (15% of grade)
### 5. **Documentation** (15% of grade)

---

## 📁 MANDATORY PROJECT STRUCTURE

The project MUST have exactly **3 main folders** at the root level:

```
assignment7/
├── SHARED/           # Shared resources, config, data, logs, SDK
├── agents/           # All agent implementations
└── doc/              # Documentation and examples
```

### SHARED/ Directory (Configuration & Data Layer)

```
SHARED/
├── config/                           # Configuration layer
│   ├── system.json                   # Global system settings
│   ├── agents/
│   │   └── agents_config.json        # All agents registry
│   ├── leagues/
│   │   └── league_2025_even_odd.json # League configuration
│   ├── games/
│   │   └── games_registry.json       # Supported game types
│   └── defaults/
│       ├── referee.json              # Default referee settings
│       └── player.json               # Default player settings
│
├── data/                             # Runtime data layer
│   ├── leagues/
│   │   └── league_2025_even_odd/
│   │       ├── standings.json        # Current standings
│   │       └── rounds.json           # Round history
│   ├── matches/
│   │   └── league_2025_even_odd/
│   │       ├── R1M1.json             # Match data files
│   │       └── ...
│   └── players/
│       ├── P01/
│       │   └── history.json          # Player match history
│       └── ...
│
├── logs/                             # Logging layer
│   ├── league/
│   │   └── league_2025_even_odd/
│   │       └── league.log.jsonl
│   ├── agents/
│   │   ├── REF01.log.jsonl
│   │   ├── P01.log.jsonl
│   │   └── ...
│   └── system/
│       └── orchestrator.log.jsonl
│
└── league_sdk/                       # Python SDK
    ├── __init__.py
    ├── config_models.py              # Dataclass definitions
    ├── config_loader.py              # ConfigLoader class
    ├── repositories.py               # Data repositories
    └── logger.py                     # JsonLogger class
```

### agents/ Directory (Agent Implementations)

```
agents/
├── league_manager/
│   ├── main.py                       # Entry point (port 8000)
│   ├── handlers.py                   # Message handlers
│   ├── scheduler.py                  # Round-robin scheduling
│   └── requirements.txt
│
├── referee_REF01/
│   ├── main.py                       # Entry point (port 8001)
│   ├── game_logic.py                 # Even/Odd rules
│   ├── handlers.py                   # Message handlers
│   └── requirements.txt
│
├── referee_REF02/
│   ├── main.py                       # Entry point (port 8002)
│   ├── game_logic.py
│   ├── handlers.py
│   └── requirements.txt
│
├── player_P01/
│   ├── main.py                       # Entry point (port 8101)
│   ├── strategy.py                   # Playing strategy
│   ├── handlers.py                   # Message handlers
│   └── requirements.txt
│
├── player_P02/                       # Port 8102
│   └── ...
├── player_P03/                       # Port 8103
│   └── ...
└── player_P04/                       # Port 8104
    └── ...
```

### doc/ Directory (Documentation)

```
doc/
├── protocol_spec.md                  # Full protocol specification
├── message_examples/                 # JSON message examples
│   ├── registration/
│   │   ├── referee_register_request.json
│   │   └── player_register_request.json
│   ├── gameflow/
│   │   ├── game_invitation.json
│   │   ├── game_join_ack.json
│   │   ├── choose_parity_call.json
│   │   ├── parity_choice.json
│   │   └── game_over.json
│   └── errors/
│       ├── timeout_error.json
│       └── invalid_move.json
├── diagrams/
│   ├── architecture.png
│   ├── message_flow.png
│   └── state_machine.png
└── ARCHITECTURE.md
```

---

## ⚙️ CONFIGURATION LAYER SPECIFICATION

The Configuration Layer (`SHARED/config/`) contains the system's "genetic code" – static settings that are read when agents start.

### 1. Global System File – `config/system.json`

**Purpose**: Global parameters for the entire system.  
**Users**: All agents, top-level Orchestrator.  
**Location**: `SHARED/config/system.json`

This file defines default values for:
- **Network settings** – ports and addresses
- **Security settings** – tokens and TTLs
- **Timeouts** – corresponding to protocol settings
- **Retry policy** – matches protocol settings

**Example `system.json`**:
```json
{
  "schema_version": "1.0.0",
  "system_id": "league_system_prod",
  "protocol_version": "league.v2",
  "timeouts": {
    "move_timeout_sec": 30,
    "generic_response_timeout_sec": 10
  },
  "retry_policy": {
    "max_retries": 3,
    "backoff_strategy": "exponential"
  }
}
```

### 2. Agent Registration – `config/agents/agents_config.json`

**Purpose**: Centralized management of all agents.  
**Users**: League Manager, Deployment tools.  
**Location**: `SHARED/config/agents/agents_config.json`

This file contains the "citizenship registry" of system agents:
- `league_manager` – league manager details
- `referees[]` – list of all registered referees
- `players[]` – list of all registered players

**Example `agents_config.json`**:
```json
{
  "schema_version": "1.0.0",
  "league_manager": {
    "id": "LM01",
    "endpoint": "http://localhost:8000/mcp",
    "status": "ACTIVE"
  },
  "referees": [
    {
      "id": "REF01",
      "endpoint": "http://localhost:8001/mcp",
      "supported_games": ["even_odd"],
      "status": "ACTIVE"
    },
    {
      "id": "REF02",
      "endpoint": "http://localhost:8002/mcp",
      "supported_games": ["even_odd"],
      "status": "ACTIVE"
    }
  ],
  "players": [
    {
      "id": "P01",
      "display_name": "Player One",
      "endpoint": "http://localhost:8101/mcp",
      "status": "REGISTERED"
    },
    {
      "id": "P02",
      "display_name": "Player Two",
      "endpoint": "http://localhost:8102/mcp",
      "status": "REGISTERED"
    }
  ]
}
```

### 3. League Configuration – `config/leagues/<league_id>.json`

**Purpose**: League-specific settings.  
**Users**: League Manager, referees.  
**Location**: `SHARED/config/leagues/league_2025_even_odd.json`

Each league is an "independent state" with its own rules.

**Example `league_2025_even_odd.json`**:
```json
{
  "league_id": "league_2025_even_odd",
  "game_type": "even_odd",
  "status": "ACTIVE",
  "scoring": {
    "win_points": 2,
    "draw_points": 1,
    "loss_points": 0
  },
  "participants": {
    "min_players": 2,
    "max_players": 10000
  },
  "schedule": {
    "algorithm": "round_robin",
    "total_rounds": 3
  }
}
```

### 4. Game Types Registry – `config/games/games_registry.json`

**Purpose**: Registers all supported game types.  
**Users**: Referees (to load rules module), League Manager.  
**Location**: `SHARED/config/games/games_registry.json`

The system supports multiple game types. Each game defines:
- `game_type` – unique identifier
- `rules_module` – rules module to load
- `max_round_time_sec` – maximum time per round

**Example `games_registry.json`**:
```json
{
  "schema_version": "1.0.0",
  "games": [
    {
      "game_type": "even_odd",
      "display_name": "Even-Odd Parity Game",
      "rules_module": "game_logic.even_odd",
      "max_round_time_sec": 30,
      "min_players": 2,
      "max_players": 2,
      "description": "Players predict parity of a random number 1-10"
    }
  ]
}
```

### 5. Default Agent Settings – `config/defaults/`

**Purpose**: Default values for each agent type.  
**Files**: `referee.json`, `player.json`  
**Location**: `SHARED/config/defaults/`

These files allow a new agent to start with reasonable default settings without needing to specify every parameter individually.

**Example `referee.json`**:
```json
{
  "schema_version": "1.0.0",
  "default_settings": {
    "game_join_timeout_sec": 5,
    "parity_choice_timeout_sec": 30,
    "max_concurrent_games": 1,
    "retry_on_timeout": false
  },
  "logging": {
    "level": "INFO",
    "format": "jsonl"
  }
}
```

**Example `player.json`**:
```json
{
  "schema_version": "1.0.0",
  "default_settings": {
    "response_timeout_sec": 5,
    "strategy": "random",
    "auto_register": true
  },
  "logging": {
    "level": "INFO",
    "format": "jsonl"
  }
}
```

---

## 📊 RUNTIME DATA LAYER SPECIFICATION

If the Configuration Layer is the system's "genetic code," the Runtime Data Layer (`SHARED/data/`) is its "historical memory." Here all events occurring in the system are stored.

### 1. Standings Table – `data/leagues/<league_id>/standings.json`

**Purpose**: Stores the current standings of the league.  
**Updated by**: League Manager (after `MATCH_RESULT_REPORT`).  
**Location**: `SHARED/data/leagues/league_2025_even_odd/standings.json`

**Example `standings.json`**:
```json
{
  "schema_version": "1.0.0",
  "league_id": "league_2025_even_odd",
  "version": 12,
  "last_updated": "2025-12-19T14:30:00.000Z",
  "rounds_completed": 3,
  "standings": [
    {
      "rank": 1,
      "player_id": "P01",
      "display_name": "Agent Alpha",
      "wins": 3,
      "draws": 0,
      "losses": 0,
      "points": 6,
      "games_played": 3
    },
    {
      "rank": 2,
      "player_id": "P03",
      "display_name": "Agent Gamma",
      "wins": 2,
      "draws": 0,
      "losses": 1,
      "points": 4,
      "games_played": 3
    },
    {
      "rank": 3,
      "player_id": "P02",
      "display_name": "Agent Beta",
      "wins": 1,
      "draws": 0,
      "losses": 2,
      "points": 2,
      "games_played": 3
    },
    {
      "rank": 4,
      "player_id": "P04",
      "display_name": "Agent Delta",
      "wins": 0,
      "draws": 0,
      "losses": 3,
      "points": 0,
      "games_played": 3
    }
  ]
}
```

### 2. Rounds History – `data/leagues/<league_id>/rounds.json`

**Purpose**: Records all rounds that have taken place.  
**Updated by**: League Manager (after `ROUND_COMPLETED`).  
**Location**: `SHARED/data/leagues/league_2025_even_odd/rounds.json`

**Example `rounds.json`**:
```json
{
  "schema_version": "1.0.0",
  "league_id": "league_2025_even_odd",
  "total_rounds": 3,
  "rounds": [
    {
      "round_id": 1,
      "status": "COMPLETED",
      "started_at": "2025-12-19T10:00:00.000Z",
      "completed_at": "2025-12-19T10:15:00.000Z",
      "matches": [
        {"match_id": "R1M1", "player_a": "P01", "player_b": "P02", "winner": "P01"},
        {"match_id": "R1M2", "player_a": "P03", "player_b": "P04", "winner": "P03"}
      ]
    },
    {
      "round_id": 2,
      "status": "COMPLETED",
      "started_at": "2025-12-19T10:20:00.000Z",
      "completed_at": "2025-12-19T10:35:00.000Z",
      "matches": [
        {"match_id": "R2M1", "player_a": "P03", "player_b": "P01", "winner": "P01"},
        {"match_id": "R2M2", "player_a": "P04", "player_b": "P02", "winner": "P02"}
      ]
    }
  ]
}
```

### 3. Single Match Data – `data/matches/<league_id>/<match_id>.json`

**Purpose**: Full documentation of a single match ("identity card" of the match).  
**Updated by**: The referee of that match.  
**Location**: `SHARED/data/matches/league_2025_even_odd/R1M1.json`

This file contains:
- `lifecycle` – the game state and timestamps
- `transcript[]` – all messages exchanged (move history)
- `result` – the final result (matches `GAME_OVER`)

**Example `R1M1.json`**:
```json
{
  "schema_version": "1.0.0",
  "match_id": "R1M1",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "referee_id": "REF01",
  "lifecycle": {
    "state": "FINISHED",
    "created_at": "2025-12-19T10:00:00.000Z",
    "started_at": "2025-12-19T10:00:05.000Z",
    "finished_at": "2025-12-19T10:00:12.000Z"
  },
  "players": {
    "player_a": {
      "id": "P01",
      "display_name": "Agent Alpha",
      "joined_at": "2025-12-19T10:00:02.000Z"
    },
    "player_b": {
      "id": "P02",
      "display_name": "Agent Beta",
      "joined_at": "2025-12-19T10:00:03.000Z"
    }
  },
  "transcript": [
    {
      "sequence": 1,
      "message_type": "GAME_INVITATION",
      "timestamp": "2025-12-19T10:00:00.000Z",
      "to": ["P01", "P02"]
    },
    {
      "sequence": 2,
      "message_type": "GAME_JOIN_ACK",
      "timestamp": "2025-12-19T10:00:02.000Z",
      "from": "P01"
    },
    {
      "sequence": 3,
      "message_type": "GAME_JOIN_ACK",
      "timestamp": "2025-12-19T10:00:03.000Z",
      "from": "P02"
    },
    {
      "sequence": 4,
      "message_type": "CHOOSE_PARITY_CALL",
      "timestamp": "2025-12-19T10:00:05.000Z",
      "to": ["P01", "P02"]
    },
    {
      "sequence": 5,
      "message_type": "PARITY_CHOICE",
      "timestamp": "2025-12-19T10:00:07.000Z",
      "from": "P01",
      "choice": "even"
    },
    {
      "sequence": 6,
      "message_type": "PARITY_CHOICE",
      "timestamp": "2025-12-19T10:00:08.000Z",
      "from": "P02",
      "choice": "odd"
    }
  ],
  "result": {
    "drawn_number": 8,
    "number_parity": "even",
    "winner_id": "P01",
    "loser_id": "P02",
    "winner_choice": "even",
    "loser_choice": "odd",
    "points_awarded": 2
  }
}
```

### 4. Player History – `data/players/<player_id>/history.json`

**Purpose**: Player's personal "memory" for strategy building.  
**User**: The player themselves (for strategy improvement).  
**Location**: `SHARED/data/players/P01/history.json`

A smart player can use this file as a "memory" to improve their strategy based on past matches and opponent behavior.

**Example `history.json`**:
```json
{
  "schema_version": "1.0.0",
  "player_id": "P01",
  "display_name": "Agent Alpha",
  "last_updated": "2025-12-19T14:30:00.000Z",
  "stats": {
    "total_matches": 3,
    "wins": 3,
    "losses": 0,
    "draws": 0,
    "win_rate": 1.0,
    "total_points": 6
  },
  "matches": [
    {
      "match_id": "R1M1",
      "round_id": 1,
      "league_id": "league_2025_even_odd",
      "opponent_id": "P02",
      "opponent_name": "Agent Beta",
      "result": "WIN",
      "my_choice": "even",
      "opponent_choice": "odd",
      "drawn_number": 8,
      "points_earned": 2,
      "timestamp": "2025-12-19T10:00:12.000Z"
    },
    {
      "match_id": "R2M1",
      "round_id": 2,
      "league_id": "league_2025_even_odd",
      "opponent_id": "P03",
      "opponent_name": "Agent Gamma",
      "result": "WIN",
      "my_choice": "odd",
      "opponent_choice": "even",
      "drawn_number": 7,
      "points_earned": 2,
      "timestamp": "2025-12-19T10:25:00.000Z"
    }
  ],
  "opponent_history": {
    "P02": {
      "matches_played": 1,
      "wins": 1,
      "losses": 0,
      "their_choices": ["odd"]
    },
    "P03": {
      "matches_played": 1,
      "wins": 1,
      "losses": 0,
      "their_choices": ["even"]
    }
  }
}
```

---

## 📋 LOGS LAYER SPECIFICATION

The Logs Layer is the system's "nervous system" – it provides visibility into what is actually happening across the distributed multi-agent system.

**Directory Structure:**
```
SHARED/logs/
├── league/
│   └── <league_id>/
│       └── league.log.jsonl
└── agents/
    ├── LM01.log.jsonl
    ├── REF01.log.jsonl
    ├── REF02.log.jsonl
    ├── P01.log.jsonl
    ├── P02.log.jsonl
    ├── P03.log.jsonl
    └── P04.log.jsonl
```

### 1. Central League Log – `logs/league/<league_id>/league.log.jsonl`

**Format**: JSONLines (each line is a separate JSON object).  
**Users**: DevOps, technical support.  
**Location**: `SHARED/logs/league/league_2025_even_odd/league.log.jsonl`

This log captures all significant events at the league level, providing a centralized view of the competition's progress.

**Log Entry Schema:**
```json
{
  "timestamp": "<ISO-8601 timestamp>",
  "component": "<component_id>",
  "event_type": "<EVENT_TYPE>",
  "level": "DEBUG|INFO|WARNING|ERROR",
  "details": { "<event-specific data>" }
}
```

**Example League Log Entries:**

```jsonl
{"timestamp": "2025-01-15T10:00:00Z", "component": "league_manager", "event_type": "LEAGUE_STARTED", "level": "INFO", "details": {"league_id": "league_2025_even_odd", "total_players": 4, "total_rounds": 3}}
{"timestamp": "2025-01-15T10:00:05Z", "component": "league_manager", "event_type": "REFEREE_REGISTERED", "level": "INFO", "details": {"referee_id": "REF01", "endpoint": "http://localhost:8001/mcp"}}
{"timestamp": "2025-01-15T10:00:10Z", "component": "league_manager", "event_type": "REFEREE_REGISTERED", "level": "INFO", "details": {"referee_id": "REF02", "endpoint": "http://localhost:8002/mcp"}}
{"timestamp": "2025-01-15T10:01:00Z", "component": "league_manager", "event_type": "PLAYER_REGISTERED", "level": "INFO", "details": {"player_id": "P01", "display_name": "Agent Alpha"}}
{"timestamp": "2025-01-15T10:15:00Z", "component": "league_manager", "event_type": "ROUND_ANNOUNCEMENT_SENT", "level": "INFO", "details": {"round_id": 1, "matches_count": 2}}
{"timestamp": "2025-01-15T10:30:00Z", "component": "league_manager", "event_type": "ROUND_COMPLETED", "level": "INFO", "details": {"round_id": 1, "completed_matches": 2}}
{"timestamp": "2025-01-15T11:00:00Z", "component": "league_manager", "event_type": "LEAGUE_COMPLETED", "level": "INFO", "details": {"winner_id": "P01", "final_standings": ["P01", "P02", "P03", "P04"]}}
```

**Event Types for League Log:**
| Event Type | Level | Description |
|------------|-------|-------------|
| `LEAGUE_STARTED` | INFO | League competition initialized |
| `REFEREE_REGISTERED` | INFO | Referee successfully registered |
| `PLAYER_REGISTERED` | INFO | Player successfully registered |
| `ROUND_ANNOUNCEMENT_SENT` | INFO | Round announcement broadcast to referees |
| `MATCH_ASSIGNED` | INFO | Match assigned to a referee |
| `MATCH_RESULT_RECEIVED` | INFO | Match result received from referee |
| `ROUND_COMPLETED` | INFO | All matches in round finished |
| `STANDINGS_UPDATED` | INFO | League standings recalculated |
| `LEAGUE_COMPLETED` | INFO | Competition finished |
| `REGISTRATION_TIMEOUT` | WARNING | Agent failed to register in time |
| `REFEREE_ERROR` | ERROR | Referee reported an error |

### 2. Agent Log – `logs/agents/<agent_id>.log.jsonl`

**Purpose**: Per-agent tracking for debugging.  
**Users**: Agent developers.  
**Location**: `SHARED/logs/agents/P01.log.jsonl`

Each agent records the messages it sends and receives, enabling end-to-end trace of every interaction in the system.

**Agent Log Entry Schema:**
```json
{
  "timestamp": "<ISO-8601 timestamp>",
  "agent_id": "<agent_id>",
  "direction": "SENT|RECEIVED",
  "message_type": "<MESSAGE_TYPE>",
  "level": "DEBUG|INFO|WARNING|ERROR",
  "peer": "<other_agent_id>",
  "details": { "<message-specific data>" }
}
```

**Example Player Agent Log (`P01.log.jsonl`):**

```jsonl
{"timestamp": "2025-01-15T10:01:00Z", "agent_id": "P01", "direction": "SENT", "message_type": "LEAGUE_REGISTER_REQUEST", "level": "INFO", "peer": "LM01", "details": {"display_name": "Agent Alpha"}}
{"timestamp": "2025-01-15T10:01:01Z", "agent_id": "P01", "direction": "RECEIVED", "message_type": "LEAGUE_REGISTER_RESPONSE", "level": "INFO", "peer": "LM01", "details": {"status": "ACCEPTED"}}
{"timestamp": "2025-01-15T10:15:00Z", "agent_id": "P01", "direction": "RECEIVED", "message_type": "GAME_INVITATION", "level": "INFO", "peer": "REF01", "details": {"match_id": "R1M1", "opponent_id": "P02"}}
{"timestamp": "2025-01-15T10:15:01Z", "agent_id": "P01", "direction": "SENT", "message_type": "GAME_JOIN_ACK", "level": "INFO", "peer": "REF01", "details": {"match_id": "R1M1"}}
{"timestamp": "2025-01-15T10:15:05Z", "agent_id": "P01", "direction": "RECEIVED", "message_type": "CHOOSE_PARITY_CALL", "level": "INFO", "peer": "REF01", "details": {"match_id": "R1M1"}}
{"timestamp": "2025-01-15T10:15:06Z", "agent_id": "P01", "direction": "SENT", "message_type": "PARITY_CHOICE", "level": "INFO", "peer": "REF01", "details": {"match_id": "R1M1", "choice": "even"}}
{"timestamp": "2025-01-15T10:15:10Z", "agent_id": "P01", "direction": "RECEIVED", "message_type": "GAME_OVER", "level": "INFO", "peer": "REF01", "details": {"match_id": "R1M1", "result": "WIN", "points_earned": 2}}
```

**Example Referee Agent Log (`REF01.log.jsonl`):**

```jsonl
{"timestamp": "2025-01-15T10:00:05Z", "agent_id": "REF01", "direction": "SENT", "message_type": "REFEREE_REGISTER_REQUEST", "level": "INFO", "peer": "LM01", "details": {"capabilities": ["even_odd_game"]}}
{"timestamp": "2025-01-15T10:00:06Z", "agent_id": "REF01", "direction": "RECEIVED", "message_type": "REFEREE_REGISTER_RESPONSE", "level": "INFO", "peer": "LM01", "details": {"status": "ACCEPTED"}}
{"timestamp": "2025-01-15T10:15:00Z", "agent_id": "REF01", "direction": "RECEIVED", "message_type": "ROUND_ANNOUNCEMENT", "level": "INFO", "peer": "LM01", "details": {"round_id": 1, "assigned_matches": ["R1M1"]}}
{"timestamp": "2025-01-15T10:15:00Z", "agent_id": "REF01", "direction": "SENT", "message_type": "GAME_INVITATION", "level": "INFO", "peer": "P01", "details": {"match_id": "R1M1"}}
{"timestamp": "2025-01-15T10:15:00Z", "agent_id": "REF01", "direction": "SENT", "message_type": "GAME_INVITATION", "level": "INFO", "peer": "P02", "details": {"match_id": "R1M1"}}
{"timestamp": "2025-01-15T10:15:10Z", "agent_id": "REF01", "direction": "SENT", "message_type": "MATCH_RESULT_REPORT", "level": "INFO", "peer": "LM01", "details": {"match_id": "R1M1", "winner_id": "P01"}}
```

### Logging Requirements Checklist

- [ ] All agents write logs to SHARED/logs/ directory
- [ ] Log format is JSONLines (one JSON object per line)
- [ ] All log entries include required fields (timestamp, level, etc.)
- [ ] Timestamps are ISO-8601 format
- [ ] Both SENT and RECEIVED messages are logged
- [ ] Peer agent is identified in each log entry
- [ ] Log levels used appropriately (DEBUG, INFO, WARNING, ERROR)
- [ ] League Manager maintains central league log
- [ ] Each agent maintains its own agent log

---

## 🌐 HTTP SERVER REQUIREMENTS

### Port Assignments (MANDATORY)

| Agent | Port | Endpoint |
|-------|------|----------|
| League Manager | 8000 | http://localhost:8000/mcp |
| Referee REF01 | 8001 | http://localhost:8001/mcp |
| Referee REF02 | 8002 | http://localhost:8002/mcp |
| Player P01 | 8101 | http://localhost:8101/mcp |
| Player P02 | 8102 | http://localhost:8102/mcp |
| Player P03 | 8103 | http://localhost:8103/mcp |
| Player P04 | 8104 | http://localhost:8104/mcp |

### Server Implementation Requirements

Each agent MUST:
- [ ] Run as an HTTP server on its assigned port
- [ ] Expose `/mcp` POST endpoint for MCP messages
- [ ] Accept JSON request bodies
- [ ] Return JSON responses
- [ ] Handle concurrent requests
- [ ] Implement proper error handling

---

## 📚 CRITICAL REQUIREMENTS (Must Have)

### 1. Protocol Compliance (25%)

#### Message Validation
- [ ] All messages conform to `league.v1` protocol
- [ ] All required base fields present in every message
- [ ] Correct data types for all fields
- [ ] Valid UUIDs for `league_id` and `conversation_id`
- [ ] ISO-8601 timestamps
- [ ] Proper sender identification

#### Required Message Types Support

**Registration Messages:**
- [ ] `REFEREE_REGISTER_REQUEST`
- [ ] `REFEREE_REGISTER_RESPONSE`
- [ ] `LEAGUE_REGISTER_REQUEST`
- [ ] `LEAGUE_REGISTER_RESPONSE`

**Round Management Messages:**
- [ ] `ROUND_ANNOUNCEMENT`
- [ ] `LEAGUE_STANDINGS_UPDATE`
- [ ] `ROUND_COMPLETED`
- [ ] `LEAGUE_COMPLETED`

**Game Flow Messages:**
- [ ] `GAME_INVITATION`
- [ ] `GAME_JOIN_ACK`
- [ ] `CHOOSE_PARITY_CALL`
- [ ] `PARITY_CHOICE`
- [ ] `GAME_OVER`
- [ ] `MATCH_RESULT_REPORT`

**Error Messages:**
- [ ] `TIMEOUT_ERROR`
- [ ] `INVALID_MOVE_ERROR`

### 2. Startup Sequence Compliance

**Mandatory Order:**
1. [ ] League Manager starts first (port 8000)
2. [ ] Referees start and register with League Manager
3. [ ] Players start and register with League Manager
4. [ ] League starts only after all registrations complete

### 3. Game State Machine

**States:**
```
WAITING_FOR_PLAYERS → COLLECTING_CHOICES → DRAWING_NUMBER → FINISHED
```

**Required Transitions:**
- [ ] `WAITING_FOR_PLAYERS`: Wait for `GAME_JOIN_ACK` from both players (5s timeout)
- [ ] `COLLECTING_CHOICES`: Send `CHOOSE_PARITY_CALL`, collect `PARITY_CHOICE` (30s timeout)
- [ ] `DRAWING_NUMBER`: Draw number 1-10, determine winner
- [ ] `FINISHED`: Send `GAME_OVER` to players, `MATCH_RESULT_REPORT` to league

### 4. Round Robin Schedule

**For 4 Players:**
| Match ID | Player A | Player B |
|----------|----------|----------|
| R1M1 | P01 | P02 |
| R1M2 | P03 | P04 |
| R2M1 | P03 | P01 |
| R2M2 | P04 | P02 |
| R3M1 | P04 | P01 |
| R3M2 | P03 | P02 |

- [ ] Total Rounds: 3
- [ ] Matches per Round: 2
- [ ] Total Matches: 6

### 5. Scoring System

- [ ] Winner: **2 points**
- [ ] Loser: **0 points**
- [ ] Ranking by total points

---

## 📖 Documentation Requirements (15%)

### Required Documents in `doc/`

1. **protocol_spec.md**
   - Complete protocol specification
   - All message types with schemas
   - State transitions

2. **ARCHITECTURE.md**
   - System architecture diagram
   - 3-layer architecture explanation
   - Component responsibilities
   - Data flow diagrams

3. **message_examples/** directory
   - JSON example for each message type
   - Organized by category (registration, gameflow, errors)

4. **diagrams/**
   - Architecture diagram (PNG/SVG)
   - Message flow sequence diagram
   - State machine diagram

### Root Level Documents

5. **README.md**
   - Project overview
   - Setup instructions
   - How to run the league
   - Port assignments
   - Troubleshooting

6. **AGENT_STRATEGY.md** (for each player)
   - Strategy explanation (max 500 words)
   - Decision-making logic
   - Any opponent modeling used

---

## 🔧 AGENT IMPLEMENTATION REQUIREMENTS (25%)

### League Manager Requirements

- [ ] Start HTTP server on port 8000
- [ ] Accept and validate referee registrations
- [ ] Accept and validate player registrations
- [ ] Generate round-robin schedule after all registrations
- [ ] Send `ROUND_ANNOUNCEMENT` to all players
- [ ] Track match results via `MATCH_RESULT_REPORT`
- [ ] Calculate standings after each round
- [ ] Send `LEAGUE_STANDINGS_UPDATE` after each round
- [ ] Send `ROUND_COMPLETED` after all matches in a round
- [ ] Send `LEAGUE_COMPLETED` after all rounds

### Referee Requirements

- [ ] Start HTTP server on assigned port (8001, 8002)
- [ ] Register with League Manager on startup
- [ ] Implement game state machine (4 states)
- [ ] Send `GAME_INVITATION` to both players
- [ ] Collect `GAME_JOIN_ACK` (5s timeout)
- [ ] Send `CHOOSE_PARITY_CALL` to both players
- [ ] Collect `PARITY_CHOICE` (30s timeout)
- [ ] Draw random number 1-10
- [ ] Determine winner based on parity match
- [ ] Send `GAME_OVER` to both players
- [ ] Send `MATCH_RESULT_REPORT` to League Manager
- [ ] Handle timeout/invalid move errors

### Player Requirements

- [ ] Start HTTP server on assigned port (8101-8104)
- [ ] Register with League Manager on startup
- [ ] Handle `ROUND_ANNOUNCEMENT` messages
- [ ] Respond to `GAME_INVITATION` with `GAME_JOIN_ACK` (within 5s)
- [ ] Respond to `CHOOSE_PARITY_CALL` with `PARITY_CHOICE` (within 30s)
- [ ] Handle `GAME_OVER` messages
- [ ] Handle `LEAGUE_STANDINGS_UPDATE` messages
- [ ] Implement strategy for choosing "even" or "odd"
- [ ] Log all interactions

---

## 🧪 TESTING REQUIREMENTS (15%)

### Protocol Compliance Tests

- [ ] All message types validate against JSON schema
- [ ] Required fields present in all messages
- [ ] Correct data types for all fields
- [ ] UUID format validation
- [ ] Timestamp format validation

### Agent Behavior Tests

- [ ] League Manager registration flow
- [ ] Referee game state transitions
- [ ] Player response to all message types
- [ ] Timeout handling
- [ ] Error message handling

### Integration Tests

- [ ] Full registration sequence (referees + players)
- [ ] Complete match flow (invitation → game over)
- [ ] Complete round flow (all matches)
- [ ] Full league completion

### Edge Case Tests (Minimum 10)

1. [ ] Player timeout on `GAME_JOIN_ACK`
2. [ ] Player timeout on `PARITY_CHOICE`
3. [ ] Invalid parity choice value
4. [ ] Malformed JSON message
5. [ ] Missing required fields
6. [ ] Duplicate registration
7. [ ] Agent disconnection mid-game
8. [ ] Concurrent message handling
9. [ ] Out-of-order messages
10. [ ] Network latency simulation

### Test Coverage

- [ ] Overall coverage ≥70%
- [ ] Agent handlers coverage ≥85%
- [ ] Protocol validation coverage ≥90%

---

## 📊 VISUALIZATION & QUALITY REQUIREMENTS

### 7. **VISUALIZATION_QUALITY.md**
   - Publication standards (300 DPI, professional typography)
   - Colorblind-friendly palette documentation
   - Chart-specific features
   - Quality checklist
   - Accessibility standards

### 8. **API.md**
   - Every public function/class documented
   - Parameter types and descriptions
   - Return values
   - Exceptions raised
   - Usage examples
   - Consistent format (Google style docstrings)

### 9. **MATHEMATICAL_FOUNDATIONS.md**
   - All formulas in LaTeX notation
   - Probability calculations for Even-Odd game
   - Ranking calculations
   - Effect size calculations

### 10. **TEST_COVERAGE_REPORT.md**
    - Overall coverage percentage (≥70% target)
    - Module-by-module coverage
    - Critical modules at ≥85%
    - Test statistics (total, passed, failed)

### 11. **REFERENCES.md**
    - Primary research papers
    - Methodological references
    - Related work
    - Consistent citation format (APA/IEEE)

### 12. **ADRs/** (Architectural Decision Records)
    - ADR-001, ADR-002, etc.
- Must be installable: `pip install -e .`
- Proper `__init__.py` files
- Clear module separation
- No standalone scripts (convert to CLI commands)

### 3. Test Coverage

**Minimum Requirements**:
- **Overall coverage**: ≥70%
- **Critical modules**: ≥85%
- **Edge case tests**: All 10+ edge cases tested
- **Test files**:
  - `conftest.py` (shared fixtures)
  - `test_protocol.py` (message validation)
  - `test_agents.py` (agent behavior)
  - `test_integration.py` (end-to-end)

**Test Execution**:
```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

---

## ✅ QUALITY CHECKLIST

### Protocol Compliance
- [ ] All message types implemented
- [ ] All required fields present
- [ ] Valid UUID generation
- [ ] ISO-8601 timestamps
- [ ] Correct sender identification
- [ ] JSON schema validation

### Agent Implementation
- [ ] League Manager on port 8000
- [ ] Referees on ports 8001-8002
- [ ] Players on ports 8101-8104
- [ ] All agents expose `/mcp` endpoint
- [ ] Proper startup sequence
- [ ] Registration flow working

### Game Logic
- [ ] State machine implemented (4 states)
- [ ] Parity choices collected correctly
- [ ] Random number 1-10 drawing
- [ ] Winner determination logic
- [ ] Point allocation (2-0)

### Testing
- [ ] Protocol compliance tests
- [ ] Agent behavior tests
- [ ] Integration tests
- [ ] Edge case tests (10+)
- [ ] Coverage ≥70%

### Documentation
- [ ] README.md complete
- [ ] ARCHITECTURE.md complete
- [ ] protocol_spec.md complete
- [ ] Message examples provided
- [ ] Diagrams created

---

## 📝 FINAL NOTES

### Remember
1. **Protocol compliance is critical** - Zero tolerance for violations
2. **Test the startup sequence** - Order matters!
3. **Handle timeouts properly** - 5s for join, 30s for parity choice
4. **Log all interactions** - Debug with JSONL logs
5. **Implement state machine** - Follow the 4 states exactly

### Common Pitfalls to Avoid
- ❌ Wrong port assignments
- ❌ Missing base message fields
- ❌ Incorrect sender identification
- ❌ Timeout handling failures
- ❌ Invalid parity choice values
- ❌ Not handling concurrent requests
- ❌ Forgetting to report match results

---

## 📦 APPENDIX: league_sdk

This appendix presents `league_sdk`, a Python library that bridges between JSON configuration files and the objects used by agents. The library implements two main design patterns:

1. **Dataclasses** – typed models that reflect the structure of the JSON files
2. **Repository Pattern** – a layer that abstracts access to runtime data

### Library Structure

```
SHARED/league_sdk/
├── __init__.py          # Package entry point
├── config_models.py     # Data classes
├── config_loader.py     # Configuration loading
├── repositories.py      # Runtime data management
└── logger.py            # Logging utilities
```

| Module | Purpose |
|--------|---------|
| `__init__.py` | Package entry point, exports public API |
| `config_models.py` | Typed dataclass models matching JSON schemas |
| `config_loader.py` | Load and validate configuration files |
| `repositories.py` | Runtime data access (standings, matches, history) |
| `logger.py` | JSONLines logging utilities |

### Typed Models – `config_models.py`

#### Approach: Dataclasses

Python 3.7+ provides the `@dataclass` decorator, which allows defining data classes concisely. Each field in the JSON becomes a field in the class with a defined type.

**Example: Defining a Dataclass**

```python
from dataclasses import dataclass
from typing import List

@dataclass
class NetworkConfig:
    base_host: str
    default_league_manager_port: int
    default_referee_port_range: List[int]
    default_player_port_range: List[int]
```

**Example: Agent Configuration Model**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentConfig:
    agent_id: str
    agent_type: str  # "league_manager" | "referee" | "player"
    display_name: str
    port: int
    endpoint: str
    capabilities: Optional[List[str]] = None
```

**Example: Scoring Configuration Model**

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ScoringConfig:
    win_points: int
    draw_points: int
    loss_points: int
    technical_loss_points: int
    tiebreakers: List[str]
```

**Example: League Configuration Model**

```python
from dataclasses import dataclass
from typing import List

@dataclass
class LeagueConfig:
    schema_version: str
    league_id: str
    display_name: str
    game_type: str
    status: str
    scoring: ScoringConfig
    total_rounds: int
    matches_per_round: int
    players: List[str]
    referees: List[str]
    league_manager: str
    scoring: dict
    timeouts: dict
```

**Example: Referee Configuration Model**

```python
from dataclasses import dataclass
from typing import List

@dataclass
class RefereeConfig:
    referee_id: str
    display_name: str
    endpoint: str
    version: str
    game_types: List[str]
    max_concurrent_matches: int
    active: bool = True
```

**Example: Player Configuration Model**

```python
from dataclasses import dataclass
from typing import List

@dataclass
class PlayerConfig:
    player_id: str
    display_name: str
    version: str
    preferred_leagues: List[str]
    game_types: List[str]
    default_endpoint: str
    active: bool = True
```

> **Note**: This dataclass pattern allows automatic mapping from JSON to Python objects, making it easy to load configuration and validate agent settings programmatically. Each field corresponds to a configuration value, and `active` defaults to `True`. Lists are used for multiple game types or preferred leagues.

### Configuration Loader – `config_loader.py`

#### Principle: Lazy Loading with Cache

The `ConfigLoader` class implements the **Lazy Loading** pattern – configuration files are loaded only when needed and are cached for subsequent access. This optimizes performance and avoids redundant file I/O.

**Structure of ConfigLoader**

```python
import json
from pathlib import Path
from typing import TypeVar, Type, Dict, Optional

T = TypeVar('T')
CONFIG_ROOT = Path('SHARED/config')

class ConfigLoader:
    def __init__(self, root: Path = CONFIG_ROOT):
        self.root = root
        self._system: Optional[SystemConfig] = None       # lazy cache
        self._agents: Optional[AgentsConfig] = None       # lazy cache
        self._leagues: Dict[str, LeagueConfig] = {}       # league_id -> LeagueConfig
        self._games_registry: Optional[GamesRegistry] = None
    
    def load_system(self) -> 'SystemConfig':
        """Load global system configuration (cached)."""
        if self._system:
            return self._system
        path = self.root / "system.json"
        data = json.loads(path.read_text(encoding="utf8"))
        self._system = SystemConfig(**data)
        return self._system
    
    def load_agents(self) -> 'AgentsConfig':
        """Load all agents configuration (cached)."""
        if self._agents:
            return self._agents
        path = self.root / "agents_config.json"
        data = json.loads(path.read_text(encoding="utf8"))
        self._agents = AgentsConfig(**data)
        return self._agents
    
    def load_league(self, league_id: str) -> 'LeagueConfig':
        """Load configuration for a specific league (cached per league_id)."""
        if league_id in self._leagues:
            return self._leagues[league_id]
        path = self.root / "leagues" / f"{league_id}.json"
        data = json.loads(path.read_text(encoding="utf8"))
        self._leagues[league_id] = LeagueConfig(**data)
        return self._leagues[league_id]
    
    def load_games_registry(self) -> 'GamesRegistry':
        """Load registry of all supported game types (cached)."""
        if self._games_registry:
            return self._games_registry
        path = self.root / "games_registry.json"
        data = json.loads(path.read_text(encoding="utf8"))
        self._games_registry = GamesRegistry(**data)
        return self._games_registry
    
    # --- Helper Methods ---
    
    def get_referee_by_id(self, referee_id: str) -> 'RefereeConfig':
        """Get a referee configuration by ID."""
        agents = self.load_agents()
        for ref in agents.referees:
            if ref.referee_id == referee_id:
                return ref
        raise ValueError(f"Referee not found: {referee_id}")
    
    def get_player_by_id(self, player_id: str) -> 'PlayerConfig':
        """Get a player configuration by ID."""
        agents = self.load_agents()
        for player in agents.players:
            if player.player_id == player_id:
                return player
        raise ValueError(f"Player not found: {player_id}")
```

#### Loading Methods

`ConfigLoader` provides a unified API for loading all types of configuration:

| Method | Returns | Description |
|--------|---------|-------------|
| `load_system()` | `SystemConfig` | Global system configuration |
| `load_agents()` | `AgentsConfig` | List of all agents |
| `load_league(id)` | `LeagueConfig` | Configuration of a specific league |
| `load_games_registry()` | `GamesRegistry` | Registry of all supported game types |

#### Helper Methods

In addition to direct loading, the class provides convenient search methods:

| Method | Returns | Description |
|--------|---------|-------------|
| `get_referee_by_id(id)` | `RefereeConfig` | Find referee config by ID |
| `get_player_by_id(id)` | `PlayerConfig` | Find player config by ID |

> **Key Point**: Each load method loads the file only once and caches it for future calls, optimizing performance and avoiding redundant file I/O.

### Runtime Data Repositories – `repositories.py`

The Repository Pattern abstracts access to runtime data files, providing a clean API for agents to read and write data.

#### Available Data Repositories

| Repository | File | Role / Purpose |
|------------|------|----------------|
| `StandingsRepository` | `standings.json` | League standings table |
| `RoundsRepository` | `rounds.json` | History of rounds |
| `MatchRepository` | `<match_id>.json` | Single match data |
| `PlayerHistoryRepository` | `history.json` | Player personal history / memory |

Each repository abstracts file I/O and provides methods for loading, saving, and updating relevant runtime data, making it easier for agents and the League Manager to maintain consistent state.

**Example: Standings Repository**

```python
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Optional

DATA_ROOT = Path('SHARED/data')

class StandingsRepository:
    def __init__(self, league_id: str, data_root: Path = DATA_ROOT):
        self.league_id = league_id
        self.path = data_root / "leagues" / league_id / "standings.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict:
        """Load standings from JSON file."""
        if not self.path.exists():
            return {"schema_version": "1.0.0", "standings": []}
        return json.loads(self.path.read_text(encoding="utf8"))
    
    def save(self, standings: Dict) -> None:
        """Save standings to JSON file."""
        standings["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.path.write_text(json.dumps(standings, indent=2))
    
    def update_player(self, player_id: str, result: str, points: int) -> None:
        """Update a player's standings after a match."""
        standings = self.load()
        for player in standings["standings"]:
            if player["player_id"] == player_id:
                player["games_played"] += 1
                player["points"] += points
                if result == "WIN":
                    player["wins"] += 1
                elif result == "LOSS":
                    player["losses"] += 1
                elif result == "DRAW":
                    player["draws"] += 1
                break
        # Re-rank players by points
        standings["standings"].sort(key=lambda p: -p["points"])
        for i, player in enumerate(standings["standings"]):
            player["rank"] = i + 1
        self.save(standings)
```

**Example: Rounds Repository**

```python
class RoundsRepository:
    def __init__(self, league_id: str, data_root: Path = DATA_ROOT):
        self.league_id = league_id
        self.path = data_root / "leagues" / league_id / "rounds.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict:
        """Load rounds history from JSON file."""
        if not self.path.exists():
            return {"schema_version": "1.0.0", "league_id": self.league_id, "rounds": []}
        return json.loads(self.path.read_text(encoding="utf8"))
    
    def add_round(self, round_data: Dict) -> None:
        """Add a completed round to history."""
        rounds = self.load()
        rounds["rounds"].append(round_data)
        rounds["total_rounds"] = len(rounds["rounds"])
        self.path.write_text(json.dumps(rounds, indent=2))
```

**Example: Match Repository**

```python
class MatchRepository:
    def __init__(self, league_id: str, data_root: Path = DATA_ROOT):
        self.matches_dir = data_root / 'matches' / league_id
        self.matches_dir.mkdir(parents=True, exist_ok=True)
    
    def save_match(self, match_id: str, match_data: Dict) -> None:
        """Save match data to file."""
        filepath = self.matches_dir / f'{match_id}.json'
        filepath.write_text(json.dumps(match_data, indent=2))
    
    def get_match(self, match_id: str) -> Optional[Dict]:
        """Get match data by ID."""
        filepath = self.matches_dir / f'{match_id}.json'
        if not filepath.exists():
            return None
        return json.loads(filepath.read_text(encoding="utf8"))
    
    def list_matches(self) -> List[str]:
        """List all match IDs in this league."""
        return [f.stem for f in self.matches_dir.glob("*.json")]
```

**Example: Player History Repository**

```python
class PlayerHistoryRepository:
    def __init__(self, player_id: str, data_root: Path = DATA_ROOT):
        self.player_id = player_id
        self.filepath = data_root / 'players' / player_id / 'history.json'
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
    
    def get_history(self) -> Optional[Dict]:
        """Get player's match history."""
        if not self.filepath.exists():
            return None
        return json.loads(self.filepath.read_text(encoding="utf8"))
    
    def add_match_result(self, match_result: Dict) -> None:
        """Add a match result to player history."""
        history = self.get_history() or self._create_empty_history()
        history['matches'].append(match_result)
        self._update_stats(history)
        self._save_history(history)
    
    def _create_empty_history(self) -> Dict:
        """Create empty history structure."""
        return {
            "schema_version": "1.0.0",
            "player_id": self.player_id,
            "stats": {"total_matches": 0, "wins": 0, "losses": 0, "draws": 0},
            "matches": [],
            "opponent_history": {}
        }
    
    def _update_stats(self, history: Dict) -> None:
        """Recalculate stats from match history."""
        history["stats"]["total_matches"] = len(history["matches"])
        history["stats"]["wins"] = sum(1 for m in history["matches"] if m["result"] == "WIN")
        history["stats"]["losses"] = sum(1 for m in history["matches"] if m["result"] == "LOSS")
        history["stats"]["draws"] = sum(1 for m in history["matches"] if m["result"] == "DRAW")
        if history["stats"]["total_matches"] > 0:
            history["stats"]["win_rate"] = history["stats"]["wins"] / history["stats"]["total_matches"]
    
    def _save_history(self, history: Dict) -> None:
        """Save history to file."""
        history["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.filepath.write_text(json.dumps(history, indent=2))
```

### Logger Utilities – `logger.py`

#### JSONLines Format

The library uses **JSONLines (JSONL)** – each line in the log file is a separate JSON object. This format allows:

- **Efficient appending** of new records (append-only)
- **Reading and processing** with standard tools
- **Streaming logs** in real time

#### JsonLogger Class

```python
from pathlib import Path
import json
from datetime import datetime
from typing import Any, Dict, Optional

LOG_ROOT = Path('SHARED/logs')

class JsonLogger:
    def __init__(self, component: str, league_id: Optional[str] = None):
        self.component = component
        
        # Determine log directory
        if league_id:
            subdir = LOG_ROOT / "league" / league_id
        else:
            subdir = LOG_ROOT / "system"
        subdir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = subdir / f"{component}.log.jsonl"
    
    def log(self, event_type: str, level: str = "INFO", **details) -> None:
        """Log an event with optional details."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": self.component,
            "event_type": event_type,
            "level": level,
            **details,
        }
        with self.log_file.open("a", encoding="utf8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    # --- Convenience Methods ---
    
    def debug(self, event_type: str, **details) -> None:
        """Log a DEBUG level event."""
        self.log(event_type, level="DEBUG", **details)
    
    def info(self, event_type: str, **details) -> None:
        """Log an INFO level event."""
        self.log(event_type, level="INFO", **details)
    
    def warning(self, event_type: str, **details) -> None:
        """Log a WARNING level event."""
        self.log(event_type, level="WARNING", **details)
    
    def error(self, event_type: str, **details) -> None:
        """Log an ERROR level event."""
        self.log(event_type, level="ERROR", **details)
    
    def log_message_sent(self, message_type: str, recipient: str, **details) -> None:
        """Log a message sent to another agent."""
        self.debug("MESSAGE_SENT", message_type=message_type, recipient=recipient, **details)
    
    def log_message_received(self, message_type: str, sender: str, **details) -> None:
        """Log a message received from another agent."""
        self.debug("MESSAGE_RECEIVED", message_type=message_type, sender=sender, **details)
```

> **Note**: `JsonLogger` provides a structured way to log events per component or league. Convenience methods (`debug`, `info`, `warning`, `error`) simplify logging with standard levels. `log_message_sent` and `log_message_received` are helper methods for logging messages exchanged between agents.

#### Agent-Specific Logger

For per-agent logging with message direction tracking:

```python
class AgentLogger:
    def __init__(self, agent_id: str, logs_dir: Path = LOG_ROOT):
        self.agent_id = agent_id
        self.filepath = logs_dir / 'agents' / f'{agent_id}.log.jsonl'
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, direction: str, message_type: str, peer: str, 
            level: str = 'INFO', details: Dict[str, Any] = None) -> None:
        """Log a message interaction."""
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'agent_id': self.agent_id,
            'direction': direction,  # 'SENT' or 'RECEIVED'
            'message_type': message_type,
            'level': level,
            'peer': peer,
            'details': details or {}
        }
        with self.filepath.open('a', encoding='utf8') as f:
            f.write(json.dumps(entry) + '\n')
    
    def log_sent(self, message_type: str, peer: str, details: dict = None) -> None:
        """Log a sent message."""
        self.log('SENT', message_type, peer, details=details)
    
    def log_received(self, message_type: str, peer: str, details: dict = None) -> None:
        """Log a received message."""
        self.log('RECEIVED', message_type, peer, details=details)


class LeagueLogger:
    def __init__(self, league_id: str, logs_dir: Path = LOG_ROOT):
        self.league_id = league_id
        self.filepath = logs_dir / 'league' / league_id / 'league.log.jsonl'
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, component: str, event_type: str, 
            level: str = 'INFO', details: Dict[str, Any] = None) -> None:
        """Log a league event."""
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'component': component,
            'event_type': event_type,
            'level': level,
            'details': details or {}
        }
        with self.filepath.open('a', encoding='utf8') as f:
            f.write(json.dumps(entry) + '\n')
    
    def info(self, component: str, event_type: str, **details) -> None:
        """Log an INFO level league event."""
        self.log(component, event_type, level='INFO', details=details or None)
    
    def error(self, component: str, event_type: str, **details) -> None:
        """Log an ERROR level league event."""
        self.log(component, event_type, level='ERROR', details=details or None)
```

### SDK Usage Examples

#### Example: Using ConfigLoader in LeagueManager

```python
from league_sdk import ConfigLoader, JsonLogger

class LeagueManager:
    def __init__(self, league_id: str):
        loader = ConfigLoader()
        self.system_cfg = loader.load_system()
        self.agents_cfg = loader.load_agents()
        self.league_cfg = loader.load_league(league_id)
        
        # Build lookup maps for active referees
        self.referees_by_id = {
            r.referee_id: r.endpoint
            for r in self.agents_cfg.referees if r.active
        }
        
        self.logger = JsonLogger("league_manager", league_id)
    
    def get_timeout_for_move(self) -> int:
        return self.system_cfg.timeouts.move_timeout_sec
```

> **Explanation**: Loads system, agents, and league configuration lazily via `ConfigLoader`. Builds a map of active referees for quick access. Initializes a `JsonLogger` scoped to the league manager component. Provides utility methods, e.g., to get the move timeout from the system config.

#### Example: Using ConfigLoader in RefereeAgent

```python
from league_sdk import ConfigLoader, JsonLogger

class RefereeAgent:
    def __init__(self, referee_id: str, league_id: str):
        loader = ConfigLoader()
        self.system_cfg = loader.load_system()
        self.league_cfg = loader.load_league(league_id)
        self.self_cfg = loader.get_referee_by_id(referee_id)
        
        self.logger = JsonLogger(f"referee:{referee_id}", league_id)
    
    def register_to_league(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "register_referee",
            "params": {
                "protocol": self.system_cfg.protocol_version,
                "message_type": "REFEREE_REGISTER_REQUEST",
                "referee_meta": {
                    "display_name": self.self_cfg.display_name,
                    "version": self.self_cfg.version,
                    "game_types": self.self_cfg.game_types,
                }
            }
        }
        # ... send request to League Manager
```

> **Explanation**: Each referee agent loads the relevant configs lazily. Sets up a personal logger for tracing events. Prepares a registration payload to notify the League Manager.

#### Example: Logging a Timeout Error

```python
logger = JsonLogger("referee:REF01", "league_2025_even_odd")
logger.error(
    "GAME_ERROR",
    match_id="R1M1",
    error_code="TIMEOUT_MOVE",
    player_id="P02",
    timeout_sec=30,
)
```

**Output in `logs/league/league_2025_even_odd/referee:REF01.log.jsonl`:**

```json
{
  "timestamp": "2025-01-15T10:15:00Z",
  "component": "referee:REF01",
  "event_type": "GAME_ERROR",
  "level": "ERROR",
  "match_id": "R1M1",
  "error_code": "TIMEOUT_MOVE",
  "player_id": "P02",
  "timeout_sec": 30
}
```

> **Explanation**: Errors such as a move timeout are logged in JSONLines format. Each entry is timestamped and includes contextual information for debugging or auditing.

#### Example: Using Repositories and Loggers Together

```python
from pathlib import Path
from league_sdk import ConfigLoader, StandingsRepository, AgentLogger

# Initialize SDK components
config_loader = ConfigLoader()
standings_repo = StandingsRepository('league_2025_even_odd')
logger = AgentLogger('P01')

# Load configuration
system_config = config_loader.load_system()
agents_config = config_loader.load_agents()

# Get current standings
standings = standings_repo.load()
for player in standings['standings']:
    print(f"{player['rank']}. {player['display_name']}: {player['points']} pts")

# Log an interaction
logger.log_received('GAME_INVITATION', 'REF01', {'match_id': 'R1M1'})
logger.log_sent('GAME_JOIN_ACK', 'REF01', {'match_id': 'R1M1'})
```

### SDK Requirements Checklist

- [ ] All dataclass models match JSON schemas
- [ ] ConfigLoader validates required fields
- [ ] Repositories handle file not found gracefully
- [ ] Logger writes valid JSONLines format
- [ ] All timestamps are ISO-8601 UTC
- [ ] Thread-safe file operations (if needed)
- [ ] Type hints on all public methods

---

**Document Owner**: Assignment 7 Team  
**Last Updated**: December 19, 2025  
**Next Review**: As needed during implementation  
**Status**: ✅ Ready for Implementation


