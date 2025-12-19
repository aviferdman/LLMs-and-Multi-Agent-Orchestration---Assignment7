# Assignment 7 - Task-Specific Requirements

**Document Version**: 2.1  
**Created**: December 13, 2025  
**Updated**: December 19, 2025  
**Status**: Planning Phase  

---

## 📋 Overview

This document defines the **task-specific requirements** for Assignment 7: AI Agent League Competition. The project implements a multi-agent system where autonomous agents compete in an Even-Odd game following a standardized MCP-based protocol.

> **Important**: This document complements [GENERAL_PROJECT_REQUIREMENTS.md](GENERAL_PROJECT_REQUIREMENTS.md), which defines general requirements applicable to all assignments (documentation standards, code quality, testing, configuration, security, etc.). All requirements in that document apply to this assignment.

---

## 🎯 Competition Format

### Overview

- **4 players** running in parallel
- **Round-robin tournament** (each player plays every other player)
- **3 tournament rounds** with **6 matches total**
- **Ranking system** based on wins/losses
- **Point System**: Winner gets **3 points**, Draw gives **1 point each**, Loser gets **0 points**
- **Two-phase competition**:
  1. **Private League**: Local development and testing
  2. **Class League**: Competitive ranking for grades

### Key Dates

- **Private League Testing**: December 18-20, 2024
- **Class League Competition**: After December 20, 2024
- **Submission Deadline**: January 8, 2025 at 23:59

---

## 📊 Assignment 7 Grading Breakdown

Based on the assignment specification and multi-agent competition requirements:

| Category | Weight | Description |
|----------|--------|-------------|
| **Project Structure** | 20% | 3-folder architecture, SDK implementation |
| **Protocol Compliance** | 25% | Message formats, state machines, timeouts |
| **Agent Implementation** | 25% | League Manager, Referees, Players |
| **Testing & QA** | 15% | Protocol, integration, edge case tests |
| **Documentation** | 15% | Protocol spec, architecture, examples |

### Detailed Grading (Total: 120 points possible)

#### 1. Protocol Compliance (40 points)

- **Perfect compliance** (40 pts): 100% valid JSON schemas, all fields correct
- **Minor violations** (30 pts): <5% messages have optional field issues
- **Major violations** (10 pts): Missing required fields, type errors
- **Disqualified** (0 pts): Any critical protocol violation

#### 2. Competition Performance (30 points)

Based on class ranking:
- Top 20%: 30 points
- Top 40%: 25 points
- Top 60%: 20 points
- Top 80%: 15 points
- Bottom 20%: 10 points

#### 3. Agent Implementation Quality (20 points)

- **Code quality** (10 pts): Clean, documented, tested
- **Architecture** (5 pts): Sensors, decision model, actuators clearly separated
- **Error handling** (5 pts): Graceful handling of all edge cases

#### 4. Documentation (10 points)

- Strategy explanation (5 pts)
- Test results (3 pts)
- Architecture documentation (2 pts)

#### 5. Bonus Points

- **Protocol compliance bonus** (+10 pts): Zero violations in competition
- **Documentation excellence** (+5 pts): Exceptional documentation
- **Innovation bonus** (+5 pts): Novel strategy with strong performance

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

## 🏗️ SYSTEM ARCHITECTURE

### Core Design Principles

#### 1. Game-Agnostic Layers

The league management layer and the refereeing layer must be **completely independent** of any specific game.

**No game-specific rules, assumptions, or logic may leak into:**
- League scheduling
- Registration
- Ranking
- Match orchestration

> **Game logic must exist only in the game module.**

#### 2. Full Modularity and Replaceability

Every major system component must be **independently replaceable** without affecting other components.

**The system must support swapping:**
- Game rules (e.g., Even/Odd → another game)
- Protocol version or protocol implementation
- Transport layer (HTTP ↔ STDIO ↔ future transports)
- Agent implementations (player, referee, league)

> **No component may rely on concrete implementations of another component—only on well-defined interfaces.**

#### 3. Unified, Stable Protocol Contract

All communication must use **JSON** and follow a **fixed, explicit message schema**.

**Message structure must remain consistent regardless of:**
- Game type
- Transport mechanism
- Agent role

> **Protocol changes must be versioned and backward-compatibility rules must be enforced.**

### Design Enforcement Rules

| Rule | Violation Indicator |
|------|---------------------|
| Game-Agnostic Layers | If replacing a game requires changes in league or referee code, **the design is invalid** |
| Transport Independence | If changing transport (HTTP ↔ STDIO) affects business logic, **the design is invalid** |
| Separation of Concerns | If protocol handling is mixed with game logic, **the design is invalid** |

> ⚠️ **You must always prioritize extensibility, isolation, and long-term evolvability over short-term convenience.**

### Components Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LEAGUE MANAGER (Port 8000)               │
│  - Player/Referee Registration                              │
│  - Schedule Management (Round Robin)                        │
│  - Ranking Calculation                                      │
│  - Single Source of Truth: standings, schedule, round status│
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
┌────────▼─────────┐     ┌────────▼─────────┐
│ REFEREE REF01    │     │ REFEREE REF02    │
│ (Port 8001)      │     │ (Port 8002)      │
│ - Match Init     │     │ - Match Init     │
│ - Move Valid.    │     │ - Move Valid.    │
│ - Game State     │     │ - Game State     │
│ - Winner Annc.   │     │ - Winner Annc.   │
└────────┬─────────┘     └────────┬─────────┘
         │                         │
    ┌────┴────┐               ┌────┴────┐
    │         │               │         │
┌───▼──┐  ┌──▼───┐       ┌───▼──┐  ┌──▼───┐
│ P01  │  │ P02  │       │ P03  │  │ P04  │
│:8101 │  │:8102 │       │:8103 │  │:8104 │
└──────┘  └──────┘       └──────┘  └──────┘
```

---

## 🎭 Orchestrator Types

In the system, there are **two types of Orchestrators**:

### 1. League Manager (Top-Level Orchestrator)

**Single Source of Truth for**:
- Standings table
- Match schedule
- Current round status

**Responsibilities**:
- Register referees and players
- Create round-robin schedule
- Track round completion
- Calculate and update rankings
- Announce round and league completion

### 2. Referees (Local Orchestrators)

**Single Source of Truth for**:
- State of their own match
- Game progress within the match
- Move validation results

**Responsibilities**:
- Initialize individual games
- Manage game state machine
- Collect and validate player moves
- Determine winners
- Report results to League Manager

---

## 🎯 Three-Layer Architecture

### Layer 1: League Layer

**Responsibilities**:
- Player registration and verification
- Game schedule creation (round-robin)
- Ranking calculation and leaderboard
- Tournament lifecycle management

**Does NOT**:
- Know specific game rules
- Validate individual moves
- Execute game logic

### Layer 2: Referee Layer

**Responsibilities**:
- Game initialization between two players
- Handshake management
- Move collection from players
- Move validation (delegates to game layer)
- Winner announcement
- Result reporting to league

**Does NOT**:
- Know ranking algorithms
- Implement game rules directly
- Manage multiple games simultaneously (one referee per game)

### Layer 3: Game Layer

**Responsibilities**:
- Define game-specific rules
- Validate individual moves
- Determine winner conditions
- Game state management

**Does NOT**:
- Know about players or registration
- Handle communication protocols
- Manage tournaments

### Decoupling Benefits

1. **Extensibility**: Add new games without changing league/referee
2. **Testability**: Test each layer independently
3. **Reusability**: Agents work with any game following the protocol
4. **Maintainability**: Changes isolated to relevant layer

---

## 🤖 Agent States

Each agent follows a well-defined lifecycle with the following states:

| State | Description |
|-------|-------------|
| `INIT` | The agent exists but has not yet registered |
| `REGISTERED` | The agent has successfully registered and received an `auth_token` |
| `ACTIVE` | The agent is operational and participating in matches |
| `SUSPENDED` | The agent is temporarily inactive (not participating) |
| `SHUTDOWN` | The agent has completed activity and is no longer operational |

### Agent State Transitions

```
        ┌─────────────────────────────────────────────────────┐
        │                                                     │
        │         ┌──────────┐                                │
        │         │   INIT   │                                │
        │         └────┬─────┘                                │
        │              │ register                             │
        │              ▼                                      │
        │         ┌──────────────┐                            │
        │         │  REGISTERED  │                            │
        │         └──────┬───────┘                            │
        │                │ league_start                       │
        │                ▼                                    │
        │           ┌────────┐     timeout/recover            │
        │           │ ACTIVE │◄─────────────────┐             │
        │           └───┬────┘                  │             │
        │               │                       │             │
        │               │ timeout           ┌───┴──────┐      │
        │               └──────────────────►│ SUSPENDED│      │
        │                                   └───┬──────┘      │
        │                                       │ max_fail    │
        │   league_end                          │             │
        │       │                               │             │
        │       ▼                               ▼             │
        │   ┌──────────┐◄───────────────────────┘             │
        │   │ SHUTDOWN │                                      │
        │   └──────────┘                                      │
        │       ▲                                             │
        │       │ error (from any state)                      │
        └───────┴─────────────────────────────────────────────┘
```

**State Transition Table**:

| From State | Trigger / Condition | To State |
|------------|---------------------|----------|
| `INIT` | `register` | `REGISTERED` |
| `REGISTERED` | `league_start` | `ACTIVE` |
| `ACTIVE` | `league_end` | `SHUTDOWN` |
| `ACTIVE` | `timeout` / `recover` | `SUSPENDED` |
| `SUSPENDED` | `max_fail` | `SHUTDOWN` |
| `INIT`, `REGISTERED`, `ACTIVE` | `error` | `SHUTDOWN` |

---

## 🖥️ Client Architecture

Each agent in the system acts as a **client**, because it initiates requests to servers as needed.

### Client Layers

| Layer | Responsibility |
|-------|---------------|
| **Language Model (LLM)** | Makes decisions and initiates actions |
| **Client Interface** | The API layer the model interacts with |
| **Core System** | Manages sessions and tool registration |
| **Message Processing** | Converts internal messages to and from JSON |
| **Communication Layer** | Translates messages to HTTP or STDIO |

### Mandatory Modules

#### 1. Session Manager

**Responsibilities:**
- Manages the lifecycle of connections
- Performs handshake to verify successful connection
- Manages heartbeats (periodic health checks)
- Implements retry logic for automatic reconnection

#### 2. Tool Registry

**Responsibilities:**
- Maintains a list of available tools from all servers
- Centralizes tool metadata for LLM usage
- Handles tool name collisions between different servers

#### 3. Message Queue

**Responsibilities:**
- Manages queues for incoming and outgoing messages
- Handles message prioritization
- Prevents overload and message flooding

### Error Handling

#### Error Types

| Error Type | Description | Retry Strategy |
|------------|-------------|----------------|
| **Transient errors** | Temporary failures (e.g., network issues, high load) | Retrying is appropriate |
| **Permanent errors** | Non-recoverable failures (e.g., missing file, authorization failure) | Retrying is not useful |
| **Timeout errors** | Request exceeds allowed time | Timeout duration may be increased |

#### Exponential Backoff Strategy

The delay between retries increases exponentially:

| Attempt | Delay |
|---------|-------|
| 1 | Short delay (e.g., 2 seconds) |
| 2 | Double the delay (e.g., 4 seconds) |
| 3 | Four times the delay (e.g., 8 seconds) |
| ... | Continues exponentially |

> **Important:** Random jitter should be added to the delay to prevent multiple processes from retrying simultaneously (thundering herd problem).

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
    "win_points": 3,
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
      "points": 9,
      "games_played": 3
    },
    {
      "rank": 2,
      "player_id": "P03",
      "display_name": "Agent Gamma",
      "wins": 2,
      "draws": 0,
      "losses": 1,
      "points": 6,
      "games_played": 3
    },
    {
      "rank": 3,
      "player_id": "P02",
      "display_name": "Agent Beta",
      "wins": 1,
      "draws": 0,
      "losses": 2,
      "points": 3,
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
    "points_awarded": 3
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
    "total_points": 9
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
      "points_earned": 3,
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
      "points_earned": 3,
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
{"timestamp": "2025-01-15T10:15:10Z", "agent_id": "P01", "direction": "RECEIVED", "message_type": "GAME_OVER", "level": "INFO", "peer": "REF01", "details": {"match_id": "R1M1", "result": "WIN", "points_earned": 3}}
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

## � PROTOCOL SPECIFICATION

### Protocol Version

```
Protocol: league.v1
Current Version: 2.1.0
Minimum Supported Version: 2.0.0
```

### Base Message Structure

**Every message MUST include these fields**:

```json
{
  "protocol": "league.v1",
  "message_type": "<MESSAGE_TYPE>",
  "league_id": "<UUID>",
  "round_id": 1,
  "match_id": "R1M3",
  "conversation_id": "<UUID>",
  "sender": "league_manager | referee | player_<player_id>",
  "timestamp": "2025-12-13T21:30:00.000Z"
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ Yes | Protocol version identifier (always "league.v1") |
| `message_type` | string | ✅ Yes | Type of message (see Message Types) |
| `league_id` | UUID | ✅ Yes | Unique identifier for the league instance |
| `round_id` | integer | ✅ Yes | Current round number (1-indexed) |
| `match_id` | string | ✅ Yes | Match identifier format: "R{round}M{match}" |
| `conversation_id` | UUID | ✅ Yes | Unique identifier for this message thread |
| `sender` | string | ✅ Yes | Sender identity (league_manager, referee, player_<id>) |
| `timestamp` | ISO-8601 | ✅ Yes | Message timestamp in UTC |

### Time Zone Requirement – UTC/GMT Mandatory

**All timestamps in the protocol MUST be in the UTC/GMT time zone.**

This requirement ensures consistency between agents operating from different geographic locations. Timestamps must follow the ISO-8601 format with the `Z` suffix indicating UTC:

```
✅ Correct:   "2025-01-15T10:30:00Z"
✅ Correct:   "2025-01-15T10:30:00.000Z"
❌ Invalid:   "2025-01-15T10:30:00+02:00"
❌ Invalid:   "2025-01-15T10:30:00-05:00"
❌ Invalid:   "2025-01-15 10:30:00"
```

> **⚠️ Important**: An agent that sends a message with a time zone other than UTC will receive error `E021` (`INVALID_TIMESTAMP`). This error results in the message being rejected.

### Response Timeouts

The following table defines the maximum allowed response time for each message type:

| Message Type | Timeout (seconds) | Notes |
|--------------|-------------------|-------|
| `REFEREE_REGISTER` | 10 | Referee registration to league |
| `LEAGUE_REGISTER` | 10 | Player registration to league |
| `GAME_JOIN_ACK` | 5 | Player confirms arrival to match |
| `CHOOSE_PARITY` | 30 | Player selects even/odd choice |
| `GAME_OVER` | 5 | Referee sends game result |
| `MATCH_RESULT_REPORT` | 10 | Referee reports match result to league |
| `LEAGUE_QUERY` | 10 | Player or referee requests info |
| **Default** | 10 | Default response timeout |

> **Important**: Agents MUST respond within the specified timeout. Failure to respond in time results in:
> - For `GAME_JOIN_ACK`: Player forfeits the match
> - For `CHOOSE_PARITY`: Player receives a technical loss (0 points)
> - For other messages: May trigger retry or error handling

---

## 📬 MESSAGE TYPES & SCHEMAS

### Complete Message Type List (Protocol v2.1)

The following table summarizes all **18 message types** in protocol v2.1:

| Message Type | Sender | Receiver | Purpose / Action |
|--------------|--------|----------|------------------|
| `REFEREE_REGISTER_REQUEST` | Referee | League Manager | Referee registration |
| `REFEREE_REGISTER_RESPONSE` | League Manager | Referee | Registration confirmation |
| `LEAGUE_REGISTER_REQUEST` | Player | League Manager | Player registration |
| `LEAGUE_REGISTER_RESPONSE` | League Manager | Player | Registration confirmation |
| `ROUND_ANNOUNCEMENT` | League Manager | All Players | Round announcement |
| `ROUND_COMPLETED` | League Manager | All Players | Round completion notification |
| `LEAGUE_COMPLETED` | League Manager | Everyone | League completion notification |
| `GAME_INVITATION` | Referee | Player | Game invitation |
| `GAME_JOIN_ACK` | Player | Referee | Join acknowledgment |
| `CHOOSE_PARITY_CALL` | Referee | Player | Choice request |
| `CHOOSE_PARITY_RESPONSE` | Player | Referee | Choice response (PARITY_CHOICE) |
| `GAME_OVER` | Referee | Both Players | Game over notification |
| `MATCH_RESULT_REPORT` | Referee | League Manager | Match result report |
| `LEAGUE_STANDINGS_UPDATE` | League Manager | All Players | Standings update |
| `LEAGUE_ERROR` | League Manager | Agent | League error notification |
| `GAME_ERROR` | Referee | Player | Game error notification |
| `LEAGUE_QUERY` | Player/Referee | League Manager | Information query |
| `LEAGUE_QUERY_RESPONSE` | League Manager | Player/Referee | Query response |

### Registration Messages

#### REFEREE_REGISTER_REQUEST

**Direction**: Referee → League Manager

```json
{
  "protocol": "league.v1",
  "message_type": "REFEREE_REGISTER_REQUEST",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 0,
  "match_id": "REGISTRATION",
  "conversation_id": "660e8400-e29b-41d4-a716-446655440001",
  "sender": "referee_REF01",
  "timestamp": "2025-12-13T21:30:00.000Z",
  "referee_meta": {
    "referee_id": "REF01",
    "contact_endpoint": "http://localhost:8001/mcp",
    "supported_games": ["even_odd"]
  }
}
```

#### LEAGUE_REGISTER_REQUEST

**Direction**: Player → League Manager

```json
{
  "protocol": "league.v1",
  "message_type": "LEAGUE_REGISTER_REQUEST",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 0,
  "match_id": "REGISTRATION",
  "conversation_id": "660e8400-e29b-41d4-a716-446655440001",
  "sender": "player_candidate",
  "timestamp": "2025-12-13T21:30:00.000Z",
  "player_meta": {
    "display_name": "AlphaAgent",
    "version": "1.0.0",
    "protocol_version": "2.1.0",
    "game_types": ["even_odd"],
    "contact_endpoint": "http://localhost:8101/mcp"
  }
}
```

**Required Fields**:
- `player_meta.display_name`: Human-readable agent name
- `player_meta.version`: Semantic version (MAJOR.MINOR.PATCH)
- `player_meta.protocol_version`: Protocol version the agent supports
- `player_meta.game_types`: Array of supported games (MUST include "even_odd")
- `player_meta.contact_endpoint`: HTTP endpoint for communication

### Game Flow Messages

#### GAME_INVITATION

**Direction**: Referee → Player

```json
{
  "protocol": "league.v1",
  "message_type": "GAME_INVITATION",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee_REF01",
  "timestamp": "2025-12-13T22:05:00.000Z",
  "game_info": {
    "game_type": "even_odd",
    "opponent_id": "P02",
    "timeout_seconds": 5
  }
}
```

#### CHOOSE_PARITY_CALL

**Direction**: Referee → Player

```json
{
  "protocol": "league.v1",
  "message_type": "CHOOSE_PARITY_CALL",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee_REF01",
  "timestamp": "2025-12-13T22:05:02.000Z",
  "game_state": {
    "game_type": "even_odd",
    "timeout_seconds": 30
  }
}
```

#### PARITY_CHOICE

**Direction**: Player → Referee

```json
{
  "protocol": "league.v1",
  "message_type": "PARITY_CHOICE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "player_P01",
  "timestamp": "2025-12-13T22:05:05.000Z",
  "choice": {
    "value": "even",
    "reasoning": "Strategic choice based on probability"
  }
}
```

**Choice Values**:
- `"even"`: Player predicts the drawn number will be even
- `"odd"`: Player predicts the drawn number will be odd

#### GAME_OVER

**Direction**: Referee → Both Players

```json
{
  "protocol": "league.v1",
  "message_type": "GAME_OVER",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee_REF01",
  "timestamp": "2025-12-13T22:06:00.000Z",
  "result": {
    "drawn_number": 8,
    "number_parity": "even",
    "winner_id": "P01",
    "loser_id": "P02",
    "winner_choice": "even",
    "loser_choice": "odd",
    "points_awarded": 3
  }
}
```

### Error Codes Reference

| Code | Name | Description |
|------|------|-------------|
| `E001` | `TIMEOUT_ERROR` | Response not received in time |
| `E003` | `MISSING_REQUIRED_FIELD` | Required field missing in message |
| `E004` | `INVALID_PARITY_CHOICE` | Invalid parity choice (must be "even" or "odd") |
| `E005` | `PLAYER_NOT_REGISTERED` | Player not registered in the league |
| `E009` | `CONNECTION_ERROR` | Connection error communicating with agent |
| `E011` | `AUTH_TOKEN_MISSING` | Missing authentication token in request |
| `E012` | `AUTH_TOKEN_INVALID` | Invalid or expired authentication token |
| `E018` | `PROTOCOL_VERSION_MISMATCH` | Registration rejected, agent version < 2.0.0 |
| `E021` | `INVALID_TIMESTAMP` | Timestamp not in UTC/GMT format (must end with 'Z') |

---

## 🎲 GAME RULES: EVEN-ODD

### Game Description

A **single-round simultaneous-move game** where two players compete by predicting the parity of a randomly drawn number.

### Rules

1. **Setup**:
   - Each match consists of **1 game round**
   - Both players choose **simultaneously** (hidden from each other)
   - Referee draws a random number **1-10** (inclusive)

2. **Choice Execution**:
   - Referee sends `CHOOSE_PARITY_CALL` to both players simultaneously
   - Each player responds with `PARITY_CHOICE` (value: "even" or "odd")
   - Both choices must be received within 30 seconds

3. **Winning Condition**:
   - Referee draws a random number between 1 and 10
   - Determines the parity of the number (even/odd)
   - Player whose choice **matches** the drawn number's parity **wins**

4. **Scoring** (Points System):

   | Outcome | Winner Points | Loser Points |
   |---------|---------------|---------------|
   | Win | 3 | 0 |
   | Draw | 1 | 1 |
   | Loss | 0 | 0 |

### Example Game

```
Match R1M1: P01 vs P02
────────────────────────────

Step 1: CHOOSE_PARITY_CALL sent to both players

Step 2: Choices received
  P01 chooses: "even"
  P02 chooses: "odd"

Step 3: Number drawn
  drawn_number = 8
  number_parity = "even"

Step 4: Determine winner
  P01 chose "even", number is even → P01 WINS
  P02 chose "odd", number is even → P02 LOSES

Step 5: Points awarded
  P01: +3 points (win)
  P02: +0 points (loss)
```

---

## �📚 CRITICAL REQUIREMENTS (Must Have)

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

- [ ] Winner: **3 points**
- [ ] Draw: **1 point each**
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

### Agent Architecture

Each agent implements:

```
┌─────────────────────────────────────┐
│           AGENT                      │
│  ┌─────────────────────────────┐   │
│  │  SENSORS                     │   │
│  │  - Message Reception         │   │
│  │  - State Observation         │   │
│  └──────────┬───────────────────┘   │
│             │                        │
│  ┌──────────▼───────────────────┐   │
│  │  DECISION MODEL              │   │
│  │  - Strategy Logic            │   │
│  │  - Move Selection            │   │
│  │  - Opponent Modeling         │   │
│  └──────────┬───────────────────┘   │
│             │                        │
│  ┌──────────▼───────────────────┐   │
│  │  ACTUATORS                   │   │
│  │  - Message Sending           │   │
│  │  - Move Execution            │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │  MCP SERVER                  │   │
│  │  - Protocol Handler          │   │
│  │  - JSON Schema Validation    │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Required Agent Capabilities

**Must Implement**:
- ✅ JSON schema validation for all messages
- ✅ MCP endpoint listening
- ✅ Timeout handling (30 seconds per move)
- ✅ State management (game history, opponent modeling)
- ✅ Error handling and recovery
- ✅ Logging all interactions

**Must Support**:
- ✅ Concurrent game handling (if referee allows)
- ✅ Graceful disconnection handling
- ✅ Message replay/recovery

### Strategy Examples

**Random Strategy**:
```python
def random_strategy(game_state: GameState) -> str:
    return random.choice(["even", "odd"])
```

**Frequency Counter**:
```python
def frequency_strategy(game_state: GameState) -> str:
    # Count opponent's previous choices
    choices = [m.opponent_choice for m in game_state.history]
    even_count = choices.count("even")
    odd_count = choices.count("odd")
    
    # Choose opposite of most frequent
    if even_count > odd_count:
        return "odd"
    else:
        return "even"
```

**Pattern Matching**:
```python
def pattern_strategy(game_state: GameState) -> str:
    # Look for patterns in last N moves
    recent = game_state.history[-5:]
    # Predict next move and counter
    predicted = predict_next(recent)
    return "odd" if predicted == "even" else "even"
```

---

## ⚠️ CRITICAL REQUIREMENTS

### MUST HAVE (Disqualification if missing)

1. ✅ **Exact protocol compliance**
   - All messages match schemas exactly
   - All required fields present
   - Correct data types
   - Valid UUIDs for IDs

2. ✅ **MCP server implementation**
   - Listens on declared endpoint
   - Responds within timeout
   - Handles concurrent messages

3. ✅ **Game type support**
   - Declares "even_odd" in registration
   - Implements even-odd game logic
   - Returns valid moves ("even" or "odd")

4. ✅ **Timeout compliance**
   - All moves within 30 seconds
   - No hanging requests
   - Graceful timeout handling

5. ✅ **Error-free operation**
   - No crashes during games
   - No exceptions in message handling
   - Proper cleanup on disconnect

### SHOULD HAVE (Points deduction if missing)

1. **Comprehensive testing**
   - Edge case coverage
   - Timeout scenarios
   - Malformed message handling
   - Concurrent game handling

2. **State management**
   - Track game history
   - Maintain opponent models
   - Update after each move

3. **Logging**
   - All messages logged
   - Strategy decisions logged
   - Errors logged with context

4. **Documentation**
   - Strategy description
   - Architecture diagrams
   - Test results
   - Known limitations

### Disqualification Warning

```
⚠️ DISQUALIFICATION CONDITIONS ⚠️

Your agent will be IMMEDIATELY DISQUALIFIED if:

1. ANY message violates JSON schema
2. ANY required field is missing
3. ANY field has wrong type
4. Protocol version mismatch
5. Timeout >30 seconds on ANY move
6. Crash/exception during game
7. Invalid MCP endpoint
8. Unsupported game type claim

There is ZERO tolerance for protocol violations.
Test thoroughly in private league!
```

---

## 📅 ASSIGNMENT PHASES

### Phase 1: Private League (Development)

**Duration**: Weeks 1-3

**Objectives**:
1. Implement agent with MCP server
2. Create local league infrastructure
3. Test against simple agents
4. Debug protocol compliance
5. Refine strategy

**Deliverables**:
- Working agent implementation
- Local league manager
- Test suite (edge cases, timeouts, malformed messages)
- Strategy documentation
- Minimum 10 successful games vs random agents

**Testing Against**:
- Random agent (baseline)
- Deterministic agent (always "even" or "odd")
- Mirror agent (copies your last move)
- Your own previous versions

**Success Criteria**:
- ✅ 100% protocol compliance (all messages valid JSON schemas)
- ✅ No timeouts in 50 consecutive games
- ✅ Win rate >60% vs random agent over 100 games
- ✅ Graceful handling of all error conditions

---

### Phase 2: Class League (Competition)

**Duration**: Week 4

**Objectives**:
1. Submit agent to class league
2. Compete against all classmates
3. Achieve highest possible ranking

**Competition Format**:
- **Round-robin**: Each agent plays every other agent once
- **Parallel matches**: Multiple games run simultaneously
- **Rankings**: Based on wins/losses, tiebreaker by head-to-head

**Submission Requirements**:
- Agent code + dependencies
- MCP endpoint configuration
- Strategy description (max 500 words)
- Test results from private league

---

## ⏰ Important Dates

- **Week 1**: Assignment released, private league development begins
- **Week 2**: Checkpoint - submit test results from private league
- **Week 3**: Private league finalization, strategy refinement
- **Week 4**: Class league submission deadline
- **Week 4 End**: Competition complete, rankings announced

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

## 📊 ASSIGNMENT 7-SPECIFIC DOCUMENTATION

> **Note**: General documentation requirements (VISUALIZATION_QUALITY.md, API.md, TEST_COVERAGE_REPORT.md, REFERENCES.md, ADRs, etc.) are defined in [GENERAL_PROJECT_REQUIREMENTS.md](GENERAL_PROJECT_REQUIREMENTS.md).

### Assignment 7-Specific Documents

In addition to general documentation, this assignment requires:

1. **MATHEMATICAL_FOUNDATIONS.md** (Assignment 7-specific content):
   - Probability calculations for Even-Odd game
   - Expected value analysis for random choice
   - Ranking calculations (points-based)
   - Round-robin scheduling mathematics

2. **AGENT_STRATEGY.md** (per player):
   - Strategy explanation (max 500 words)
   - Decision-making logic
   - Any opponent modeling used

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
- [ ] Point allocation (3-1-0: Win-Draw-Loss)

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

## � APPENDIX: Implementation Checklist

### Pre-Development

- [ ] Read and understand complete protocol specification
- [ ] Review all message schemas
- [ ] Understand even-odd game rules
- [ ] Set up development environment
- [ ] Create project structure (3-layer architecture)

### Development Phase

#### League Layer
- [ ] Implement player registration handler
- [ ] Create schedule generation (round-robin)
- [ ] Implement ranking calculation
- [ ] Build leaderboard display
- [ ] Add registration validation

#### Referee Layer
- [ ] Implement game initialization
- [ ] Create handshake protocol
- [ ] Build move collection system
- [ ] Add move validation (delegate to game layer)
- [ ] Implement winner announcement
- [ ] Add result reporting to league

#### Game Layer (Even-Odd)
- [ ] Implement move validation
- [ ] Add winner determination logic
- [ ] Create game state management
- [ ] Build random number generator (1-10)
- [ ] Add turn-by-turn tracking

#### Agent Implementation
- [ ] Create MCP server
- [ ] Implement sensors (message parsing)
- [ ] Build decision model
- [ ] Implement actuators (message sending)
- [ ] Add state management
- [ ] Create strategy system

#### Testing
- [ ] JSON schema validation tests
- [ ] Message type coverage tests
- [ ] Edge case tests (timeouts, errors)
- [ ] Integration tests (full games)
- [ ] Performance tests (concurrent games)
- [ ] Private league testing (100+ games)

#### Documentation
- [ ] Strategy explanation (500 words)
- [ ] Architecture documentation
- [ ] Test results summary
- [ ] Known limitations
- [ ] Setup instructions

### Pre-Submission

- [ ] Run schema validator on all messages
- [ ] Verify 100% protocol compliance
- [ ] Test timeout handling
- [ ] Verify MCP endpoint accessibility
- [ ] Test against 3+ opponent types
- [ ] Achieve >60% win rate vs random
- [ ] Zero crashes in 50+ consecutive games
- [ ] Complete all documentation
- [ ] Package submission (code + docs)

---

## � Technical Specifications

### JSON Schema Validation

All messages must validate against these schemas:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "protocol",
    "message_type",
    "league_id",
    "round_id",
    "match_id",
    "conversation_id",
    "sender",
    "timestamp"
  ],
  "properties": {
    "protocol": {
      "type": "string",
      "const": "league.v1"
    },
    "message_type": {
      "type": "string",
      "enum": [
        "REFEREE_REGISTER_REQUEST",
        "REFEREE_REGISTER_RESPONSE",
        "LEAGUE_REGISTER_REQUEST",
        "LEAGUE_REGISTER_RESPONSE",
        "ROUND_ANNOUNCEMENT",
        "ROUND_COMPLETED",
        "LEAGUE_COMPLETED",
        "GAME_INVITATION",
        "GAME_JOIN_ACK",
        "CHOOSE_PARITY_CALL",
        "CHOOSE_PARITY_RESPONSE",
        "GAME_OVER",
        "MATCH_RESULT_REPORT",
        "LEAGUE_STANDINGS_UPDATE",
        "LEAGUE_ERROR",
        "GAME_ERROR",
        "LEAGUE_QUERY",
        "LEAGUE_QUERY_RESPONSE"
      ]
    },
    "league_id": {
      "type": "string",
      "format": "uuid"
    },
    "round_id": {
      "type": "integer",
      "minimum": 0
    },
    "match_id": {
      "type": "string"
    },
    "conversation_id": {
      "type": "string",
      "format": "uuid"
    },
    "sender": {
      "type": "string",
      "pattern": "^(league_manager|referee|player_.+)$"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

### HTTP/MCP Endpoint Format

All agents communicate via HTTP endpoints exposing an `/mcp` path:

```
http://<hostname>:<port>/mcp

Examples:
  http://localhost:8000/mcp   # League Manager
  http://localhost:8001/mcp   # Referee REF01
  http://localhost:8101/mcp   # Player P01
  http://localhost:8102/mcp   # Player P02
```

### Port Allocation Convention

| Range | Agent Type | Examples |
|-------|------------|----------|
| 8000 | League Manager | Single instance |
| 8001-8099 | Referees | REF01=8001, REF02=8002 |
| 8100-8199 | Players | P01=8101, P02=8102, P03=8103, P04=8104 |

### UUID Generation

All UUIDs must be RFC 4122 compliant:

```python
import uuid

league_id = str(uuid.uuid4())  # "550e8400-e29b-41d4-a716-446655440000"
```

### ISO-8601 Timestamps

All timestamps in UTC with milliseconds:

```python
from datetime import datetime, timezone

timestamp = datetime.now(timezone.utc).isoformat()
# "2025-12-13T21:30:00.123456+00:00"
```

---

## 📖 Example Message Flow

### Complete Game Sequence

```
1. REGISTRATION PHASE
   Referee → League: REFEREE_REGISTER_REQUEST
   League → Referee: REFEREE_REGISTER_RESPONSE (status=ACCEPTED)
   Player → League: LEAGUE_REGISTER_REQUEST
   League → Player: LEAGUE_REGISTER_RESPONSE (status=ACCEPTED)

2. ROUND ANNOUNCEMENT
   League → All Players: ROUND_ANNOUNCEMENT (round schedule)

3. GAME INVITATION
   Referee → Player1: GAME_INVITATION
   Player1 → Referee: GAME_JOIN_ACK (within 5s)
   Referee → Player2: GAME_INVITATION
   Player2 → Referee: GAME_JOIN_ACK (within 5s)

4. PARITY CHOICE (Single-Round Simultaneous)
   Referee → Player1: CHOOSE_PARITY_CALL
   Referee → Player2: CHOOSE_PARITY_CALL
   Player1 → Referee: PARITY_CHOICE (value="even" or "odd") (within 30s)
   Player2 → Referee: PARITY_CHOICE (value="even" or "odd") (within 30s)
   
   Referee: Draw random number 1-10
   Referee: Determine winner based on parity match

5. GAME END
   Referee → Player1: GAME_OVER (result, points)
   Referee → Player2: GAME_OVER (result, points)
   Referee → League: MATCH_RESULT_REPORT

6. ROUND END
   League → All: ROUND_COMPLETED (after all matches in round)

7. LEAGUE END
   League → All: LEAGUE_COMPLETED (standings, winner)
```

---

## 🎓 Learning Objectives

By completing this assignment, you will:

1. **Master protocol-driven communication**
   - Design robust communication protocols
   - Handle distributed system coordination
   - Ensure message reliability

2. **Implement multi-agent systems**
   - Agent architecture (sensors, decision, actuators)
   - Concurrent agent execution
   - State management across agents

3. **Build decoupled architectures**
   - Layer separation
   - Interface design
   - Extensibility patterns

4. **Develop strategic AI**
   - Game theory concepts
   - Opponent modeling
   - Strategy optimization

5. **Practice software engineering**
   - JSON schema validation
   - Error handling
   - Testing distributed systems
   - Documentation

---

## 📞 Support & Resources

### Getting Help

1. **Protocol Questions**: Review this specification thoroughly
2. **Implementation Issues**: Test in private league first
3. **Bug Reports**: Include message logs and schema validation results
4. **Strategy Discussion**: Allowed in general terms, not specific implementations

### Resources

- JSON Schema Validator: https://www.jsonschemavalidator.net/
- MCP Documentation: [Course materials]
- UUID Generator: `python -c "import uuid; print(uuid.uuid4())"`
- ISO-8601 Reference: https://en.wikipedia.org/wiki/ISO_8601

---

## �📦 APPENDIX: JSON-RPC Message Examples

This appendix provides complete JSON-RPC 2.0 formatted message examples for the entire game flow.

> **Note on Protocol Version**: The examples below show `"protocol": "league.v2"` as copied from the original specification appendix. However, the official protocol version is `league.v1` as stated in the specification header. Use `league.v1` in your implementation unless instructed otherwise.

### 1. Referee Registration

#### REF → LM : REFEREE_REGISTER_REQUEST

```json
{
  "jsonrpc": "2.0",
  "method": "register_referee",
  "params": {
    "protocol": "league.v2",
    "message_type": "REFEREE_REGISTER_REQUEST",
    "sender": "referee:alpha",
    "timestamp": "2025-01-15T10:00:00Z",
    "conversation_id": "conv_refalphareg001",
    "referee_meta": {
      "display_name": "Referee Alpha",
      "version": "1.0.0",
      "game_types": ["even_odd"],
      "contact_endpoint": "http://localhost:8001/mcp",
      "max_concurrent_matches": 2
    }
  },
  "id": 1
}
```

#### LM → REF : REFEREE_REGISTER_RESPONSE

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "REFEREE_REGISTER_RESPONSE",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:00:01Z",
    "conversation_id": "conv_refalphareg001",
    "status": "ACCEPTED",
    "referee_id": "REF01",
    "auth_token": "tok_ref01_abc123",
    "league_id": "league_2025_even_odd",
    "reason": null
  },
  "id": 1
}
```

### 2. Player Registration

#### P01 → LM : LEAGUE_REGISTER_REQUEST

```json
{
  "jsonrpc": "2.0",
  "method": "register_player",
  "params": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_REGISTER_REQUEST",
    "sender": "player:alpha",
    "timestamp": "2025-01-15T10:05:00Z",
    "conversation_id": "conv_playeralphareg001",
    "player_meta": {
      "display_name": "Agent Alpha",
      "version": "1.0.0",
      "game_types": ["even_odd"],
      "contact_endpoint": "http://localhost:8101/mcp"
    }
  },
  "id": 1
}
```

#### LM → P01 : LEAGUE_REGISTER_RESPONSE

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_REGISTER_RESPONSE",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:05:01Z",
    "conversation_id": "conv_playeralphareg001",
    "status": "ACCEPTED",
    "player_id": "P01",
    "auth_token": "tok_p01_xyz789",
    "league_id": "league_2025_even_odd",
    "reason": null
  },
  "id": 1
}
```

### 3. Game Flow Messages

#### REF → P01 : GAME_INVITATION

```json
{
  "jsonrpc": "2.0",
  "method": "handle_game_invitation",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_INVITATION",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:00Z",
    "conversation_id": "conv_r1m1001",
    "auth_token": "tok_ref01_abc123",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "match_id": "R1M1",
    "game_type": "even_odd",
    "role_in_match": "PLAYER_A",
    "opponent_id": "P02"
  },
  "id": 1001
}
```

#### P01 → REF : GAME_JOIN_ACK

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "GAME_JOIN_ACK",
    "sender": "player:P01",
    "timestamp": "2025-01-15T10:15:01Z",
    "conversation_id": "conv_r1m1001",
    "auth_token": "tok_p01_xyz789",
    "match_id": "R1M1",
    "player_id": "P01",
    "arrival_timestamp": "2025-01-15T10:15:01Z",
    "accept": true
  },
  "id": 1001
}
```

#### REF → P01 : CHOOSE_PARITY_CALL

```json
{
  "jsonrpc": "2.0",
  "method": "choose_parity",
  "params": {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_CALL",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:05Z",
    "conversation_id": "conv_r1m1001",
    "auth_token": "tok_ref01_abc123",
    "match_id": "R1M1",
    "player_id": "P01",
    "game_type": "even_odd",
    "context": {
      "opponent_id": "P02",
      "round_id": 1,
      "your_standings": {"wins": 0, "losses": 0, "draws": 0}
    },
    "deadline": "2025-01-15T10:15:35Z"
  },
  "id": 1101
}
```

#### P01 → REF : CHOOSE_PARITY_RESPONSE

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_RESPONSE",
    "sender": "player:P01",
    "timestamp": "2025-01-15T10:15:10Z",
    "conversation_id": "conv_r1m1001",
    "auth_token": "tok_p01_xyz789",
    "match_id": "R1M1",
    "player_id": "P01",
    "parity_choice": "even"
  },
  "id": 1101
}
```

#### REF → P01, P02 : GAME_OVER

```json
{
  "jsonrpc": "2.0",
  "method": "notify_match_result",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_OVER",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:30Z",
    "conversation_id": "conv_r1m1001",
    "auth_token": "tok_ref01_abc123",
    "match_id": "R1M1",
    "game_type": "even_odd",
    "game_result": {
      "status": "WIN",
      "winner_player_id": "P01",
      "drawn_number": 8,
      "number_parity": "even",
      "choices": {"P01": "even", "P02": "odd"},
      "reason": "P01 chose even, number was 8 (even)"
    }
  },
  "id": 1201
}
```

#### REF → LM : MATCH_RESULT_REPORT

```json
{
  "jsonrpc": "2.0",
  "method": "report_match_result",
  "params": {
    "protocol": "league.v2",
    "message_type": "MATCH_RESULT_REPORT",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:35Z",
    "conversation_id": "conv_r1m1report",
    "auth_token": "tok_ref01_abc123",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "match_id": "R1M1",
    "game_type": "even_odd",
    "result": {
      "winner": "P01",
      "score": {"P01": 3, "P02": 0},
      "details": {
        "drawn_number": 8,
        "choices": {"P01": "even", "P02": "odd"}
      }
    }
  },
  "id": 1301
}
```

### 4. Error Messages

#### GAME_ERROR (Timeout with Retry)

```json
{
  "jsonrpc": "2.0",
  "method": "notify_game_error",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_ERROR",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:16:00Z",
    "conversation_id": "conv_r1m1001",
    "match_id": "R1M1",
    "error_code": "E001",
    "error_description": "TIMEOUT_ERROR",
    "affected_player": "P02",
    "retryable": true,
    "retry_count": 1,
    "max_retries": 3,
    "consequence": "Technical loss if no response after retries"
  },
  "id": 1103
}
```

---

## 📦 APPENDIX: Resilience Patterns

### Retry Pattern

Implementation example with exponential backoff:

```python
import time
import requests
from typing import Dict, Any

class RetryConfig:
    MAX_RETRIES = 3
    BASE_DELAY = 2.0  # seconds
    BACKOFF_MULTIPLIER = 2.0

def call_with_retry(endpoint: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Send MCP request with retry logic."""
    last_error = None
    for attempt in range(RetryConfig.MAX_RETRIES):
        try:
            response = requests.post(
                endpoint,
                json={
                    "jsonrpc": "2.0",
                    "method": method,
                    "params": params,
                    "id": 1
                },
                timeout=30
            )
            return response.json()
        except (requests.Timeout, requests.ConnectionError) as e:
            last_error = e
            if attempt < RetryConfig.MAX_RETRIES - 1:
                # Exponential backoff delay
                delay = RetryConfig.BASE_DELAY * (RetryConfig.BACKOFF_MULTIPLIER ** attempt)
                time.sleep(delay)
    return {
        "error": {
            "error_code": "E005",
            "error_description": f"Max retries exceeded: {last_error}"
        }
    }
```

### Circuit Breaker Pattern

When a service fails repeatedly, further attempts are blocked for a timeout period.

```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if datetime.now() - self.last_failure > timedelta(seconds=self.reset_timeout):
                self.state = "HALF_OPEN"
                return True
            return False
        # HALF_OPEN allows one trial
        return True

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure = datetime.now()
        if self.failures >= self.threshold:
            self.state = "OPEN"
```

**Circuit Breaker States:**

| State | Description |
|-------|-------------|
| `CLOSED` | Normal operation, requests pass through |
| `OPEN` | After repeated failures (threshold), blocks all requests |
| `HALF_OPEN` | After `reset_timeout`, allows one trial request |

---

## 📦 APPENDIX: Player Registration and Authenticated Messaging

### Agent Credentials Dataclass

```python
from dataclasses import dataclass

@dataclass
class AgentCredentials:
    agent_id: str
    auth_token: str
    league_id: str
```

### Player Registration Function

```python
import requests
from typing import Optional

def register_player(league_endpoint: str, player_info: dict) -> Optional[AgentCredentials]:
    """Register player and store auth token."""
    payload = {
        "jsonrpc": "2.0",
        "method": "register_player",
        "params": {
            "protocol": "league.v2",
            "message_type": "LEAGUE_REGISTER_REQUEST",
            "sender": f"player:{player_info['name']}",
            "player_meta": player_info
        },
        "id": 1
    }
    response = requests.post(league_endpoint, json=payload)
    result = response.json().get("result", {})

    if result.get("status") == "ACCEPTED":
        return AgentCredentials(
            agent_id=result["player_id"],
            auth_token=result["auth_token"],
            league_id=result["league_id"]
        )
    return None
```

### Authenticated Client

```python
class AuthenticatedClient:
    def __init__(self, credentials: AgentCredentials):
        self.creds = credentials

    def send_message(self, endpoint: str, message_type: str, params: dict) -> dict:
        """Send authenticated message."""
        payload = {
            "jsonrpc": "2.0",
            "method": "mcp_message",
            "params": {
                "protocol": "league.v2",
                "message_type": message_type,
                "sender": f"player:{self.creds.agent_id}",
                "auth_token": self.creds.auth_token,
                "league_id": self.creds.league_id,
                **params
            },
            "id": 1
        }
        response = requests.post(endpoint, json=payload)
        return response.json()
```

---

## 📦 APPENDIX: Reference Implementation Code

### Basic MCP Server

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int = 1

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: dict = {}
    id: int = 1

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    if request.method == "tool_name":
        result = handle_tool(request.params)
        return MCPResponse(result=result, id=request.id)
    return MCPResponse(result={"error": "Unknown method"})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8101)
```

### Player Agent Implementation

```python
import random
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI()

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int = 1

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    if request.method == "handle_game_invitation":
        return handle_invitation(request.params)
    elif request.method == "choose_parity":
        return handle_choose_parity(request.params)
    elif request.method == "notify_match_result":
        return handle_result(request.params)
    return {"error": "Unknown method"}

def handle_invitation(params):
    return {
        "message_type": "GAME_JOIN_ACK",
        "match_id": params.get("match_id"),
        "arrival_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "accept": True
    }

def handle_choose_parity(params):
    choice = random.choice(["even", "odd"])
    return {
        "message_type": "CHOOSE_PARITY_RESPONSE",
        "match_id": params.get("match_id"),
        "player_id": params.get("player_id"),
        "parity_choice": choice
    }

def handle_result(params):
    print(f"Match result: {params}")
    return {"status": "ok"}
```

### Referee: Determine Winner Logic

```python
def determine_winner(choice_a, choice_b, number):
    is_even = (number % 2 == 0)
    parity = "even" if is_even else "odd"
    a_correct = (choice_a == parity)
    b_correct = (choice_b == parity)

    if a_correct and not b_correct:
        return "PLAYER_A"
    elif b_correct and not a_correct:
        return "PLAYER_B"
    else:
        return "DRAW"
```

### Round-Robin Schedule Creation

```python
from itertools import combinations

def create_schedule(players):
    matches = []
    round_num = 1
    match_num = 1

    for p1, p2 in combinations(players, 2):
        matches.append({
            "match_id": f"R{round_num}M{match_num}",
            "player_A_id": p1,
            "player_B_id": p2
        })
        match_num += 1

    return matches
```

### MCP Tool Call Helper

```python
import requests

def call_mcp_tool(endpoint, method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(endpoint, json=payload)
    return response.json()

# Example: call player's choose_parity
result = call_mcp_tool(
    "http://localhost:8101/mcp",
    "choose_parity",
    {"match_id": "R1M1", "player_id": "P01"}
)
```

---

## �📋 Related Documents

| Document | Purpose |
|----------|---------|
| [GENERAL_PROJECT_REQUIREMENTS.md](GENERAL_PROJECT_REQUIREMENTS.md) | General requirements for all assignments (documentation, code quality, testing, security) |
| [ASSIGNMENT_SPECIFICATION.md](ASSIGNMENT_SPECIFICATION.md) | Complete technical specification for Assignment 7 |

> **Note**: For general requirements (file size limits, test coverage thresholds, documentation standards, security best practices, etc.), refer to GENERAL_PROJECT_REQUIREMENTS.md. This document focuses only on Assignment 7-specific requirements.

---

**Document Owner**: Assignment 7 Team  
**Last Updated**: December 19, 2025  
**Next Review**: As needed during implementation  
**Status**: ✅ Ready for Implementation


