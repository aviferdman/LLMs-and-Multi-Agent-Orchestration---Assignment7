# Assignment 7 - AI Agent League Competition

**Course**: LLMs and Multi-Agent Orchestration  
**Assignment Type**: Competitive Multi-Agent System  
**Version**: 2.0.0  
**Protocol**: league.v1  
**Last Updated**: December 19, 2025

---

## 📋 Table of Contents

1. [Assignment Overview](#assignment-overview)
2. [Project Structure](#project-structure)
3. [HTTP Server Architecture](#http-server-architecture)
4. [System Architecture](#system-architecture)
5. [Orchestrator Types](#orchestrator-types)
6. [Startup Sequence](#startup-sequence)
7. [Registration Protocol](#registration-protocol)
8. [Round Robin Scheduling](#round-robin-scheduling)
9. [Game Flow & State Machine](#game-flow--state-machine)
10. [Protocol Specification](#protocol-specification)
11. [Message Types & Schemas](#message-types--schemas)
12. [Game Rules: Even-Odd](#game-rules-even-odd)
13. [Agent Implementation Requirements](#agent-implementation-requirements)
14. [Assignment Phases](#assignment-phases)
15. [Grading Criteria](#grading-criteria)
16. [Critical Requirements](#critical-requirements)

---

## 📖 Assignment Overview

### Purpose

Create a **competitive AI agent league** where autonomous agents compete in games following a standardized communication protocol. The system demonstrates:

- **Multi-agent orchestration** using MCP (Model Context Protocol) over HTTP
- **Decoupled architecture** enabling extensibility
- **Protocol-driven communication** with JSON schemas
- **Parallel agent execution** with proper coordination
- **State management** across distributed systems

### Key Innovation

**Total Decoupling Between Layers**: The protocol enables agents to participate in any future league regardless of specific game rules. An agent built for this protocol can join new games without modification.

### Competition Format

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

## 📁 Project Structure

The project MUST include **3 main folders** at the base level:

```
assignment7/
├── SHARED/           # Shared resources, config, data, logs, SDK
├── agents/           # All agent implementations
└── doc/              # Documentation and examples
```

### SHARED/ Directory Structure

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
│   │       ├── R1M1.json             # Match R1M1 data
│   │       ├── R1M2.json             # Match R1M2 data
│   │       └── ...
│   └── players/
│       ├── P01/
│       │   └── history.json          # P01 match history
│       ├── P02/
│       │   └── history.json          # P02 match history
│       └── ...
│
├── logs/                             # Logging layer
│   ├── league/
│   │   └── league_2025_even_odd/
│   │       └── league.log.jsonl
│   ├── agents/
│   │   ├── REF01.log.jsonl
│   │   ├── P01.log.jsonl
│   │   ├── P02.log.jsonl
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

### agents/ Directory Structure

```
agents/
├── league_manager/
│   ├── main.py                       # Entry point
│   ├── handlers.py                   # Message handlers
│   ├── scheduler.py                  # Round scheduling
│   └── requirements.txt
│
├── referee_REF01/
│   ├── main.py                       # Entry point
│   ├── game_logic.py                 # Even/Odd rules
│   ├── handlers.py                   # Message handlers
│   └── requirements.txt
│
├── referee_REF02/
│   ├── main.py
│   ├── game_logic.py
│   ├── handlers.py
│   └── requirements.txt
│
├── player_P01/
│   ├── main.py                       # Entry point
│   ├── strategy.py                   # Playing strategy
│   ├── handlers.py                   # Message handlers
│   └── requirements.txt
│
├── player_P02/
│   ├── main.py
│   ├── strategy.py
│   ├── handlers.py
│   └── requirements.txt
│
├── player_P03/
│   ├── main.py
│   ├── strategy.py
│   ├── handlers.py
│   └── requirements.txt
│
└── player_P04/
    ├── main.py
    ├── strategy.py
    ├── handlers.py
    └── requirements.txt
```

### doc/ Directory Structure

```
doc/
├── protocol_spec.md                  # Protocol specification
├── message_examples/                 # JSON message examples
│   ├── registration/
│   │   ├── referee_register_request.json
│   │   └── player_register_request.json
│   ├── gameflow/
│   │   ├── game_start.json
│   │   ├── move_request.json
│   │   └── game_over.json
│   └── errors/
│       ├── timeout_error.json
│       └── invalid_move.json
└── diagrams/
    ├── architecture.png
    └── message_flow.png
```

---

## 🌐 HTTP Server Architecture

Every agent in the system acts as an **HTTP server** on a dedicated port:

| Agent Type | Agent ID | Port | Endpoint |
|------------|----------|------|----------|
| League Manager | - | 8000 | http://localhost:8000/mcp |
| Referee | REF01 | 8001 | http://localhost:8001/mcp |
| Referee | REF02 | 8002 | http://localhost:8002/mcp |
| Player | P01 | 8101 | http://localhost:8101/mcp |
| Player | P02 | 8102 | http://localhost:8102/mcp |
| Player | P03 | 8103 | http://localhost:8103/mcp |
| Player | P04 | 8104 | http://localhost:8104/mcp |

### Port Allocation Convention

- **8000**: League Manager (single instance)
- **8001-8099**: Referees (REF01=8001, REF02=8002, etc.)
- **8100-8199**: Players (P01=8101, P02=8102, etc.)

### HTTP Endpoint Requirements

Each agent MUST:
- Listen on its assigned port
- Expose `/mcp` endpoint for MCP protocol messages
- Accept POST requests with JSON body
- Return JSON responses
- Handle concurrent requests

```python
# Example FastAPI implementation
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/mcp")
async def handle_mcp(request: Request):
    message = await request.json()
    response = await process_message(message)
    return response
```

---

## 🏗️ System Architecture

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

---

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

## 🚀 Startup Sequence

**Critical startup sequence for proper system operation**:

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: League Manager starts FIRST (Port 8000)            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ STEP 2: Referees start and register with League Manager    │
│         REF01 → REFEREE_REGISTER_REQUEST → League Manager  │
│         REF02 → REFEREE_REGISTER_REQUEST → League Manager  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ STEP 3: Players start and register with League Manager     │
│         P01 → LEAGUE_REGISTER_REQUEST → League Manager     │
│         P02 → LEAGUE_REGISTER_REQUEST → League Manager     │
│         P03 → LEAGUE_REGISTER_REQUEST → League Manager     │
│         P04 → LEAGUE_REGISTER_REQUEST → League Manager     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ STEP 4: League starts ONLY after all registrations complete│
└─────────────────────────────────────────────────────────────┘
```

### Startup Order (MANDATORY)

1. **League Manager** – must start first
2. **Referees** – start and register with League Manager
3. **Players** – start and register with League Manager
4. **League start** – only after all registrations are complete

---

## 📝 Registration Protocol

### Referee Registration

Each referee, upon startup, invokes a `register_to_league` function:

```
Referee → League Manager: REFEREE_REGISTER_REQUEST
League Manager → Referee: REFEREE_REGISTER_RESPONSE
```

### Player Registration

Each player sends a registration request:

```
Player → League Manager: LEAGUE_REGISTER_REQUEST
League Manager → Player: LEAGUE_REGISTER_RESPONSE
```

### Post-Registration

After all players and referees have registered, the League Manager:
1. Executes `create_schedule` logic
2. Uses **Round Robin algorithm** to generate match schedule
3. Sends **ROUND_ANNOUNCEMENT** to all players

---

## 🗓️ Round Robin Scheduling

### Match Schedule for 4 Players

| Match ID | Player A | Player B |
|----------|----------|----------|
| R1M1 | P01 | P02 |
| R1M2 | P03 | P04 |
| R2M1 | P03 | P01 |
| R2M2 | P04 | P02 |
| R3M1 | P04 | P01 |
| R3M2 | P03 | P02 |

### Tournament Structure

- **Total Rounds**: 3
- **Matches per Round**: 2 (parallel)
- **Total Matches**: 6
- Each player faces each opponent **exactly once**

---

## 🎮 Game Flow & State Machine

### Game States

```
WAITING_FOR_PLAYERS → COLLECTING_CHOICES → DRAWING_NUMBER → FINISHED
```

### Complete Game Flow Sequence

#### Phase 1: Round Announcement

```
League Manager → All Players: ROUND_ANNOUNCEMENT
```
- From this moment, the round has **logically begun**
- Matches start only when referee summons participants

#### Phase 2: Game Invitation

```
Referee: Set game state to WAITING_FOR_PLAYERS
Referee → Player A: GAME_INVITATION
Referee → Player B: GAME_INVITATION
Player A → Referee: GAME_JOIN_ACK (within 5 seconds)
Player B → Referee: GAME_JOIN_ACK (within 5 seconds)
```

#### Phase 3: Collecting Choices

```
Referee: Transition to COLLECTING_CHOICES state
Referee → Player A: CHOOSE_PARITY_CALL
Referee → Player B: CHOOSE_PARITY_CALL
Player A → Referee: PARITY_CHOICE (value: "even" or "odd")
Player B → Referee: PARITY_CHOICE (value: "even" or "odd")
```

#### Phase 4: Drawing Number & Determining Winner

```
Referee: Transition to DRAWING_NUMBER state
Referee: Draw random number between 1 and 10
Referee: Invoke game rules module to determine winner
```

**Example**:
```python
drawn_number = 8
number_parity = "even"  # 8 is even

# P01 chose "even", P02 chose "odd"
# The drawn number 8 is even
# P01 matches the parity → P01 wins

winner_player_id = "P01"
status = "WIN"
```

#### Phase 5: Game Over

```
Referee: Transition to FINISHED state
Referee → Player A: GAME_OVER
Referee → Player B: GAME_OVER
Referee → League Manager: MATCH_RESULT_REPORT
```

### Round Completion

Round number N ends when **MATCH_RESULT_REPORT has been received for every game in the round**.

The League Manager then:
1. Declares the round **closed** (can move to next round)
2. Calculates ranking table:
   - Points
   - Wins
   - Draws
   - Losses
   - Games played
3. Sends **LEAGUE_STANDINGS_UPDATE** to all players
4. Sends **ROUND_COMPLETED** message to mark end of round

### League Completion

After all rounds are completed:
```
League Manager → All Players: LEAGUE_COMPLETED
```

---

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

---

### Agent States

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

> **Note**: This state machine models the complete lifecycle of an agent, including registration, participation, temporary suspension due to failures, and final shutdown.

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

## �️ Client Architecture

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

```python
import random
import time

def exponential_backoff(attempt: int, base_delay: float = 2.0, max_delay: float = 60.0) -> float:
    """Calculate delay with exponential backoff and jitter."""
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0, delay * 0.1)  # Add up to 10% jitter
    return delay + jitter
```

---

## �📡 Protocol Specification

### Protocol Version

```
Protocol: league.v1
```

### Protocol Version Compatibility

Upon registration, each agent declares the protocol version it supports. The League Manager checks compatibility before approving the registration.

**Version declaration in a registration request:**

```json
{
  "message_type": "LEAGUE_REGISTER_REQUEST",
  "player_meta": {
    "display_name": "Agent Alpha",
    "version": "1.0.0",
    "protocol_version": "2.1.0",
    "game_types": ["even_odd"]
  }
}
```

**Compatibility Rules:**
- The League Manager maintains a list of supported protocol versions
- Agents with incompatible protocol versions will receive a `REJECTED` status with reason `"Unsupported protocol version"`
- Minor version differences (e.g., 2.0.0 vs 2.1.0) are typically backward compatible
- Major version differences (e.g., 1.x vs 2.x) may be incompatible

**Version Compatibility Policy:**

| Property | Value |
|----------|-------|
| Current Version | `2.1.0` |
| Minimum Supported Version | `2.0.0` |

**Behavior:** Agents with a protocol version older than `2.0.0` will receive error `E018` (`PROTOCOL_VERSION_MISMATCH`).

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

### State Definition Principle

**At every moment, the state of the system is well-defined**:

- Every entity (league, round, game, player) has a unique ID
- Every message includes full context (IDs, round, match)
- State transitions are explicit and tracked
- No ambiguity about current state

### Response Timeouts

The following table defines the maximum allowed response time for each message type. If a response is not received within the timeout, it is considered a failure and may trigger a `TIMEOUT_ERROR` (E001).

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

## 📬 Message Types & Schemas

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
| `CHOOSE_PARITY_RESPONSE` | Player | Referee | Choice response |
| `GAME_OVER` | Referee | Both Players | Game over notification |
| `MATCH_RESULT_REPORT` | Referee | League Manager | Match result report |
| `LEAGUE_STANDINGS_UPDATE` | League Manager | All Players | Standings update |
| `LEAGUE_ERROR` | League Manager | Agent | League error notification |
| `GAME_ERROR` | Referee | Player | Game error notification |
| `LEAGUE_QUERY` | Player/Referee | League Manager | Information query |
| `LEAGUE_QUERY_RESPONSE` | League Manager | Player/Referee | Query response |

---

### 1. Referee Registration

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

#### REFEREE_REGISTER_RESPONSE

**Direction**: League Manager → Referee

```json
{
  "protocol": "league.v1",
  "message_type": "REFEREE_REGISTER_RESPONSE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 0,
  "match_id": "REGISTRATION",
  "conversation_id": "660e8400-e29b-41d4-a716-446655440001",
  "sender": "league_manager",
  "timestamp": "2025-12-13T21:30:01.000Z",
  "status": "ACCEPTED",
  "referee_id": "REF01"
}
```

---

### 2. Player Registration

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

#### LEAGUE_REGISTER_RESPONSE

**Direction**: League Manager → Player

```json
{
  "protocol": "league.v1",
  "message_type": "LEAGUE_REGISTER_RESPONSE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 0,
  "match_id": "REGISTRATION",
  "conversation_id": "660e8400-e29b-41d4-a716-446655440001",
  "sender": "league_manager",
  "timestamp": "2025-12-13T21:30:01.000Z",
  "status": "ACCEPTED",
  "player_id": "P01",
  "reason": null
}
```

**Status Values**:
- `ACCEPTED`: Registration successful
- `REJECTED`: Registration denied

**Optional Fields**:
- `reason`: String explaining rejection (only if status=REJECTED)

**Rejection Reasons**:
- "Unsupported game type"
- "Invalid endpoint"
- "Duplicate display name"
- "Registration closed"

---

### 3. Round Announcement

#### ROUND_ANNOUNCEMENT

**Direction**: League Manager → All Players

```json
{
  "protocol": "league.v1",
  "message_type": "ROUND_ANNOUNCEMENT",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "ANNOUNCEMENT",
  "conversation_id": "770e8400-e29b-41d4-a716-446655440002",
  "sender": "league_manager",
  "timestamp": "2025-12-13T22:00:00.000Z",
  "round_info": {
    "round_number": 1,
    "total_rounds": 3,
    "matches": [
      {"match_id": "R1M1", "player_a": "P01", "player_b": "P02", "referee": "REF01"},
      {"match_id": "R1M2", "player_a": "P03", "player_b": "P04", "referee": "REF02"}
    ]
  }
}
```

---

### 4. Game Invitation & Join

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

#### GAME_JOIN_ACK

**Direction**: Player → Referee

**Response time**: Within 5 seconds

```json
{
  "protocol": "league.v1",
  "message_type": "GAME_JOIN_ACK",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "player_P01",
  "timestamp": "2025-12-13T22:05:01.000Z",
  "status": "READY"
}
```

---

### 5. Choose Parity (Game Move)

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

---

### 6. Game Over

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
    "points_awarded": 2
  }
}
```

---

### 7. Match Result Report

#### MATCH_RESULT_REPORT

**Direction**: Referee → League Manager

```json
{
  "protocol": "league.v1",
  "message_type": "MATCH_RESULT_REPORT",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee_REF01",
  "timestamp": "2025-12-13T22:06:01.000Z",
  "result": {
    "winner_id": "P01",
    "loser_id": "P02",
    "drawn_number": 8,
    "winner_choice": "even",
    "loser_choice": "odd",
    "winner_points": 2,
    "loser_points": 0
  }
}
```

---

### 8. League Standings Update

#### LEAGUE_STANDINGS_UPDATE

**Direction**: League Manager → All Players

```json
{
  "protocol": "league.v1",
  "message_type": "LEAGUE_STANDINGS_UPDATE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "STANDINGS",
  "conversation_id": "990e8400-e29b-41d4-a716-446655440004",
  "sender": "league_manager",
  "timestamp": "2025-12-13T22:10:00.000Z",
  "standings": [
    {"rank": 1, "player_id": "P01", "points": 2, "wins": 1, "losses": 0, "draws": 0, "games_played": 1},
    {"rank": 1, "player_id": "P03", "points": 2, "wins": 1, "losses": 0, "draws": 0, "games_played": 1},
    {"rank": 3, "player_id": "P02", "points": 0, "wins": 0, "losses": 1, "draws": 0, "games_played": 1},
    {"rank": 3, "player_id": "P04", "points": 0, "wins": 0, "losses": 1, "draws": 0, "games_played": 1}
  ]
}
```

---

### 9. Round Completed

#### ROUND_COMPLETED

**Direction**: League Manager → All Players

```json
{
  "protocol": "league.v1",
  "message_type": "ROUND_COMPLETED",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "ROUND_END",
  "conversation_id": "990e8400-e29b-41d4-a716-446655440005",
  "sender": "league_manager",
  "timestamp": "2025-12-13T22:10:01.000Z",
  "round_summary": {
    "round_number": 1,
    "matches_completed": 2,
    "next_round": 2
  }
}
```

---

### 10. League Completed

#### LEAGUE_COMPLETED

**Direction**: League Manager → All Players

```json
{
  "protocol": "league.v1",
  "message_type": "LEAGUE_COMPLETED",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 3,
  "match_id": "FINAL_STANDINGS",
  "conversation_id": "AA0e8400-e29b-41d4-a716-446655440005",
  "sender": "league_manager",
  "timestamp": "2025-12-13T23:00:00.000Z",
  "final_standings": {
    "total_rounds": 3,
    "total_matches": 6,
    "champion": {
      "player_id": "P01",
      "display_name": "AlphaAgent",
      "points": 6,
      "wins": 3,
      "losses": 0
    },
    "rankings": [
      {"rank": 1, "player_id": "P01", "points": 6, "wins": 3, "losses": 0},
      {"rank": 2, "player_id": "P03", "points": 4, "wins": 2, "losses": 1},
      {"rank": 3, "player_id": "P02", "points": 2, "wins": 1, "losses": 2},
      {"rank": 4, "player_id": "P04", "points": 0, "wins": 0, "losses": 3}
    ]
  }
}
```

---

### 11. League Query

#### LEAGUE_QUERY

**Direction**: Player/Referee → League Manager  
**Expected Response**: `LEAGUE_QUERY_RESPONSE`

Players and referees can query the League Manager for information about the league status, upcoming matches, or current standings.

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_QUERY",
  "sender": "player:P01",
  "timestamp": "2025-01-15T14:00:00Z",
  "conversation_id": "conv_query001",
  "auth_token": "tok_p01_abc123",
  "league_id": "league_2025_even_odd",
  "query_type": "GET_NEXT_MATCH",
  "query_params": {
    "player_id": "P01"
  }
}
```

**Fields**:

| Field | Description |
|-------|-------------|
| `protocol` | Version of the league protocol |
| `message_type` | Always `LEAGUE_QUERY` for a query |
| `sender` | The player or referee making the request |
| `timestamp` | When the request was sent |
| `conversation_id` | Unique ID for this request/response pair |
| `auth_token` | Token issued during registration (`LEAGUE_REGISTER_RESPONSE` or `REFEREE_REGISTER_RESPONSE`) |
| `league_id` | The ID of the league being queried |
| `query_type` | Type of query (see below) |
| `query_params` | Parameters required for the query |

**Supported Query Types**:

| Query Type | Description | Required Params |
|------------|-------------|----------------|
| `GET_NEXT_MATCH` | Get player's next scheduled match | `player_id` |
| `GET_STANDINGS` | Get current league standings | None |
| `GET_LEAGUE_STATUS` | Get league status and progress | None |
| `GET_PLAYER_STATS` | Get statistics for a player | `player_id` |
| `GET_MATCH_HISTORY` | Get match history | `player_id` (optional) |

#### LEAGUE_QUERY_RESPONSE

**Direction**: League Manager → Player/Referee

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_QUERY_RESPONSE",
  "sender": "league_manager",
  "timestamp": "2025-01-15T14:00:01Z",
  "conversation_id": "conv_query001",
  "league_id": "league_2025_even_odd",
  "query_type": "GET_NEXT_MATCH",
  "status": "SUCCESS",
  "data": {
    "match_id": "R2M1",
    "round_id": 2,
    "opponent_id": "P03",
    "scheduled_time": "2025-01-15T15:00:00Z",
    "referee_id": "REF01"
  }
}
```

---

### 12. Error Messages

#### TIMEOUT_ERROR

```json
{
  "protocol": "league.v1",
  "message_type": "TIMEOUT_ERROR",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee_REF01",
  "timestamp": "2025-12-13T22:05:35.000Z",
  "error": {
    "code": "TIMEOUT",
    "player_id": "P01",
    "expected_message": "PARITY_CHOICE",
    "timeout_seconds": 30,
    "consequence": "FORFEIT"
  }
}
```

#### INVALID_MOVE_ERROR

```json
{
  "protocol": "league.v1",
  "message_type": "INVALID_MOVE_ERROR",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee_REF01",
  "timestamp": "2025-12-13T22:05:06.000Z",
  "error": {
    "code": "INVALID_MOVE",
    "player_id": "P01",
    "invalid_value": "maybe",
    "expected_values": ["even", "odd"],
    "consequence": "FORFEIT"
  }
}
```

#### Error Codes Reference

The following error codes are used in both `GAME_ERROR` and `LEAGUE_ERROR` messages to indicate failures or issues during game or league interactions:

| Code | Name | Description |
|------|------|-------------|
| `E001` | `TIMEOUT_ERROR` | Response not received in time |
| `E003` | `MISSING_REQUIRED_FIELD` | Required field missing in message |
| `E004` | `INVALID_PARITY_CHOICE` | Invalid parity choice (must be "even" or "odd") |
| `E005` | `PLAYER_NOT_REGISTERED` | Player not registered in the league |
| `E009` | `CONNECTION_ERROR` | Connection error communicating with agent |
| `E011` | `AUTH_TOKEN_MISSING` | Missing authentication token in request |
| `E012` | `AUTH_TOKEN_INVALID` | Invalid or expired authentication token |
| `E021` | `INVALID_TIMESTAMP` | Timestamp not in UTC/GMT format (must end with 'Z') |

---

## 🎲 Game Rules: Even-Odd (Updated)

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

   This matches the scoring rules from the league configuration:
   ```json
   "scoring": {
     "win_points": 3,
     "draw_points": 1,
     "loss_points": 0
   }
   ```

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

### Game-Specific Message Fields

#### In PARITY_CHOICE:
```json
{
  "choice": {
    "value": "even",
    "reasoning": "optional strategy explanation"
  }
}
```

#### In GAME_OVER:
```json
{
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

---

## 🎲 Legacy Game Rules: Even-Odd (Multi-Turn Version)

> **Note**: This section describes an alternative multi-turn version of the game for reference.

### 2. League Announcement

#### LEAGUE_START_ANNOUNCEMENT

**Direction**: League Manager → All Players

```json
{
  "protocol": "league.v1",
  "message_type": "LEAGUE_START_ANNOUNCEMENT",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "ANNOUNCEMENT",
  "conversation_id": "770e8400-e29b-41d4-a716-446655440002",
  "sender": "league_manager",
  "timestamp": "2025-12-13T22:00:00.000Z",
  "league_info": {
    "total_rounds": 6,
    "total_players": 4,
    "game_type": "even_odd",
    "schedule": [
      {
        "round_id": 1,
        "matches": [
          {"match_id": "R1M1", "player1": "player_001", "player2": "player_002"},
          {"match_id": "R1M2", "player1": "player_003", "player2": "player_004"}
        ]
      }
    ]
  }
}
```

---

### 3. Game Invitation

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
  "sender": "referee",
  "timestamp": "2025-12-13T22:05:00.000Z",
  "game_info": {
    "game_type": "even_odd",
    "opponent_id": "player_002",
    "your_role": "challenger",
    "timeout_seconds": 30
  }
}
```

**Roles**:
- `challenger`: Goes first
- `defender`: Goes second

#### GAME_INVITATION_RESPONSE

**Direction**: Player → Referee

```json
{
  "protocol": "league.v1",
  "message_type": "GAME_INVITATION_RESPONSE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "player_001",
  "timestamp": "2025-12-13T22:05:01.000Z",
  "status": "READY"
}
```

**Status Values**:
- `READY`: Ready to play
- `DECLINED`: Cannot play

---

### 4. Game Handshake

#### GAME_START

**Direction**: Referee → Both Players

```json
{
  "protocol": "league.v1",
  "message_type": "GAME_START",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee",
  "timestamp": "2025-12-13T22:05:02.000Z",
  "game_state": {
    "game_type": "even_odd",
    "current_turn": "player_001",
    "turn_number": 1,
    "rules": {
      "max_turns": 10,
      "timeout_per_turn": 30
    }
  }
}
```

---

### 5. Move Execution

#### MOVE_REQUEST

**Direction**: Referee → Player (whose turn it is)

```json
{
  "protocol": "league.v1",
  "message_type": "MOVE_REQUEST",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee",
  "timestamp": "2025-12-13T22:05:03.000Z",
  "game_state": {
    "turn_number": 1,
    "timeout_seconds": 30,
    "game_specific_state": {
      "previous_moves": []
    }
  }
}
```

#### MOVE_RESPONSE

**Direction**: Player → Referee

```json
{
  "protocol": "league.v1",
  "message_type": "MOVE_RESPONSE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "player_001",
  "timestamp": "2025-12-13T22:05:05.000Z",
  "move": {
    "action": "choose",
    "value": "even",
    "reasoning": "Strategic choice based on opponent history"
  }
}
```

**Move Structure for Even-Odd**:
- `action`: Always "choose"
- `value`: "even" or "odd"
- `reasoning`: Optional string explaining decision

---

### 6. Move Validation

#### MOVE_VALIDATION

**Direction**: Referee → Both Players

```json
{
  "protocol": "league.v1",
  "message_type": "MOVE_VALIDATION",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee",
  "timestamp": "2025-12-13T22:05:06.000Z",
  "validation": {
    "player_id": "player_001",
    "move": {"action": "choose", "value": "even"},
    "status": "VALID",
    "error": null
  }
}
```

**Status Values**:
- `VALID`: Move accepted
- `INVALID`: Move rejected

**Error Reasons**:
- "Invalid choice format"
- "Choice not in allowed values"
- "Timeout exceeded"
- "Malformed JSON"

---

### 7. Game End

#### GAME_RESULT

**Direction**: Referee → Both Players + League Manager

```json
{
  "protocol": "league.v1",
  "message_type": "GAME_RESULT",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee",
  "timestamp": "2025-12-13T22:06:00.000Z",
  "result": {
    "winner": "player_001",
    "loser": "player_002",
    "outcome": "WIN",
    "final_score": {
      "player_001": 6,
      "player_002": 4
    },
    "total_turns": 10,
    "game_summary": {
      "moves": [
        {"turn": 1, "player_001": "even", "player_002": "odd", "number": 7, "winner": "player_002"}
      ]
    }
  }
}
```

**Outcome Values**:
- `WIN`: Clear winner
- `DRAW`: Tie game
- `FORFEIT`: Player disconnected/timeout

---

### 8. Round End

#### ROUND_COMPLETE

**Direction**: League Manager → All Players

```json
{
  "protocol": "league.v1",
  "message_type": "ROUND_COMPLETE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "ROUND_SUMMARY",
  "conversation_id": "990e8400-e29b-41d4-a716-446655440004",
  "sender": "league_manager",
  "timestamp": "2025-12-13T22:10:00.000Z",
  "round_summary": {
    "matches_played": 2,
    "standings": [
      {"player_id": "player_001", "wins": 1, "losses": 0, "rank": 1},
      {"player_id": "player_003", "wins": 1, "losses": 0, "rank": 1},
      {"player_id": "player_002", "wins": 0, "losses": 1, "rank": 3},
      {"player_id": "player_004", "wins": 0, "losses": 1, "rank": 3}
    ]
  }
}
```

---

### 9. League End

#### LEAGUE_COMPLETE

**Direction**: League Manager → All Players

```json
{
  "protocol": "league.v1",
  "message_type": "LEAGUE_COMPLETE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 6,
  "match_id": "FINAL_STANDINGS",
  "conversation_id": "AA0e8400-e29b-41d4-a716-446655440005",
  "sender": "league_manager",
  "timestamp": "2025-12-13T23:00:00.000Z",
  "final_standings": {
    "total_rounds": 6,
    "total_matches": 12,
    "champion": {
      "player_id": "player_001",
      "display_name": "AlphaAgent",
      "wins": 5,
      "losses": 1,
      "win_rate": 0.833
    },
    "rankings": [
      {"rank": 1, "player_id": "player_001", "wins": 5, "losses": 1},
      {"rank": 2, "player_id": "player_003", "wins": 4, "losses": 2},
      {"rank": 3, "player_id": "player_002", "wins": 2, "losses": 4},
      {"rank": 4, "player_id": "player_004", "wins": 1, "losses": 5}
    ]
  }
}
```

---

## 🎲 Game Rules: Even-Odd

### Game Description

A simultaneous-move game where two players compete over multiple rounds.

### Rules

1. **Setup**:
   - 10 turns per game
   - Each turn, both players simultaneously choose "even" or "odd"

2. **Turn Execution**:
   - Referee requests moves from both players
   - Both players submit their choice
   - Referee generates a random number (0-99)
   - Winner determined by parity match

3. **Winning Condition**:
   - If number is even AND player chose "even" → Player wins the turn
   - If number is odd AND player chose "odd" → Player wins the turn
   - Otherwise → Opponent wins the turn

4. **Game Winner**:
   - Player who wins more turns (out of 10) wins the game
   - If tied after 10 turns → DRAW

### Example Turn

```
Turn 1:
  Player 1 chooses: "even"
  Player 2 chooses: "odd"
  Random number: 42 (even)
  Winner: Player 1 (matched parity)
  
Turn 2:
  Player 1 chooses: "odd"
  Player 2 chooses: "even"
  Random number: 17 (odd)
  Winner: Player 1 (matched parity)
```

### Game-Specific Message Fields

#### In MOVE_RESPONSE:
```json
{
  "move": {
    "action": "choose",
    "value": "even"  // or "odd"
  }
}
```

#### In GAME_RESULT:
```json
{
  "game_summary": {
    "moves": [
      {
        "turn": 1,
        "player_001": "even",
        "player_002": "odd",
        "number": 42,
        "winner": "player_001"
      }
    ]
  }
}
```

---

## 🤖 Agent Implementation Requirements

### 1. MCP Server

Each agent MUST implement an MCP server that:

```python
# Pseudocode structure
class AgentMCPServer:
    def __init__(self, player_id: str, endpoint: str):
        self.player_id = player_id
        self.endpoint = endpoint
        self.state = AgentState()
    
    async def handle_message(self, message: dict) -> dict:
        """
        Main message handler.
        
        Validates:
        1. JSON schema compliance
        2. Protocol version match
        3. Message type recognition
        
        Routes to appropriate handler.
        """
        validate_base_schema(message)
        
        message_type = message["message_type"]
        
        if message_type == "LEAGUE_REGISTER_RESPONSE":
            return await self.handle_registration(message)
        elif message_type == "GAME_INVITATION":
            return await self.handle_invitation(message)
        elif message_type == "MOVE_REQUEST":
            return await self.handle_move_request(message)
        # ... etc
```

### 2. Required Capabilities

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

### 3. Agent Components

#### Sensors
```python
class Sensors:
    """Observe environment and parse messages."""
    
    def receive_message(self, message: dict) -> ParsedMessage:
        """Receive and parse incoming message."""
        pass
    
    def extract_game_state(self, message: dict) -> GameState:
        """Extract current game state from message."""
        pass
```

#### Decision Model
```python
class DecisionModel:
    """Strategic decision making."""
    
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.opponent_model = OpponentModel()
    
    def choose_move(self, game_state: GameState) -> Move:
        """
        Decide on next move.
        
        Strategies can include:
        - Random selection
        - Frequency analysis
        - Pattern recognition
        - Markov models
        - Reinforcement learning
        """
        pass
    
    def update_opponent_model(self, opponent_move: Move):
        """Learn from opponent's moves."""
        pass
```

#### Actuators
```python
class Actuators:
    """Execute actions and send messages."""
    
    def send_message(self, message: dict) -> bool:
        """Send message via MCP."""
        pass
    
    def format_move(self, move: Move) -> dict:
        """Format move into protocol message."""
        pass
```

### 4. Strategy Examples

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

## 📅 Assignment Phases

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

**Grading**:
```
Final Rank:
  1st place:  100 points
  2nd place:   95 points
  3rd place:   90 points
  4-5:         85 points
  6-10:        80 points
  11-15:       75 points
  16-20:       70 points
  >20:         65 points

Protocol Compliance Bonus: +10 points (if 100% compliant)
Documentation Bonus:       +5 points (excellent docs)

DISQUALIFICATION: 0 points
  - Any protocol violation
  - Timeout in >5% of moves
  - Crashes/errors during games
```

**Critical Warning**:
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

## 🎯 Grading Criteria

### Total: 120 points possible (100 baseline + 20 bonus)

#### 1. Protocol Compliance (40 points)

- **Perfect compliance** (40 pts): 100% valid JSON schemas, all fields correct
- **Minor violations** (30 pts): <5% messages have optional field issues
- **Major violations** (10 pts): Missing required fields, type errors
- **Disqualified** (0 pts): Any critical protocol violation

**Testing**:
- Schema validator runs on all messages
- Message type coverage (all 9 types)
- Field validation (types, required/optional)

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

## ⚠️ Critical Requirements

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

---

## 📚 Implementation Checklist

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
- [ ] Build random number generator (0-99)
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

## 🔧 Technical Specifications

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
        "LEAGUE_REGISTER_REQUEST",
        "LEAGUE_REGISTER_RESPONSE",
        "LEAGUE_START_ANNOUNCEMENT",
        "GAME_INVITATION",
        "GAME_INVITATION_RESPONSE",
        "GAME_START",
        "MOVE_REQUEST",
        "MOVE_RESPONSE",
        "MOVE_VALIDATION",
        "GAME_RESULT",
        "ROUND_COMPLETE",
        "LEAGUE_COMPLETE"
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

### MCP Endpoint Format

```
mcp://<hostname>:<port>/<player_id>

Examples:
  mcp://localhost:5000/player_alpha
  mcp://192.168.1.100:8080/player_001
  mcp://agent-server.local:9000/my_agent
```

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
   Player → League: LEAGUE_REGISTER_REQUEST
   League → Player: LEAGUE_REGISTER_RESPONSE (status=ACCEPTED)

2. LEAGUE START
   League → All Players: LEAGUE_START_ANNOUNCEMENT

3. GAME INVITATION
   Referee → Player1: GAME_INVITATION
   Player1 → Referee: GAME_INVITATION_RESPONSE (status=READY)
   Referee → Player2: GAME_INVITATION
   Player2 → Referee: GAME_INVITATION_RESPONSE (status=READY)

4. GAME START
   Referee → Both: GAME_START

5. TURNS (×10)
   For each turn:
     Referee → Player1: MOVE_REQUEST
     Player1 → Referee: MOVE_RESPONSE (value="even")
     Referee → Both: MOVE_VALIDATION
     
     Referee → Player2: MOVE_REQUEST
     Player2 → Referee: MOVE_RESPONSE (value="odd")
     Referee → Both: MOVE_VALIDATION
     
     Referee generates random number
     Referee determines turn winner

6. GAME END
   Referee → Both + League: GAME_RESULT

7. ROUND END
   League → All: ROUND_COMPLETE

8. LEAGUE END
   League → All: LEAGUE_COMPLETE
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

## ⏰ Important Dates

- **Week 1**: Assignment released, private league development begins
- **Week 2**: Checkpoint - submit test results from private league
- **Week 3**: Private league finalization, strategy refinement
- **Week 4**: Class league submission deadline
- **Week 4 End**: Competition complete, rankings announced

---

**Good luck building your champion agent! 🏆**

Remember: Protocol compliance is EVERYTHING. Test thoroughly before submission!

---

## 📑 APPENDIX: Complete JSON-RPC Message Examples

This appendix provides complete JSON-RPC 2.0 formatted message examples for the entire game flow. All messages use **protocol version `league.v2`**.

---

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

---

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

> **Note**: P02, P03, P04 follow the same structure with their respective IDs and endpoints.

---

### 3. Round Announcement

#### LM → REF, P01, P02, P03, P04 : ROUND_ANNOUNCEMENT

```json
{
  "jsonrpc": "2.0",
  "method": "notify_round",
  "params": {
    "protocol": "league.v2",
    "message_type": "ROUND_ANNOUNCEMENT",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:10:00Z",
    "conversation_id": "conv_round1announce",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "matches": [
      {
        "match_id": "R1M1",
        "game_type": "even_odd",
        "player_A_id": "P01",
        "player_B_id": "P02",
        "referee_endpoint": "http://localhost:8001/mcp"
      },
      {
        "match_id": "R1M2",
        "game_type": "even_odd",
        "player_A_id": "P03",
        "player_B_id": "P04",
        "referee_endpoint": "http://localhost:8001/mcp"
      }
    ]
  },
  "id": 10
}
```

---

### 4. Game Invitation

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

#### REF → P02 : GAME_INVITATION

```json
{
  "jsonrpc": "2.0",
  "method": "handle_game_invitation",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_INVITATION",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:00Z",
    "conversation_id": "conv_r1m1002",
    "auth_token": "tok_ref01_abc123",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "match_id": "R1M1",
    "game_type": "even_odd",
    "role_in_match": "PLAYER_B",
    "opponent_id": "P01"
  },
  "id": 1002
}
```

---

### 5. Game Join Acknowledgment

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

#### P02 → REF : GAME_JOIN_ACK

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "GAME_JOIN_ACK",
    "sender": "player:P02",
    "timestamp": "2025-01-15T10:15:02Z",
    "conversation_id": "conv_r1m1002",
    "auth_token": "tok_p02_def456",
    "match_id": "R1M1",
    "player_id": "P02",
    "arrival_timestamp": "2025-01-15T10:15:02Z",
    "accept": true
  },
  "id": 1002
}
```

---

### 6. Choose Parity

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

#### REF → P02 : CHOOSE_PARITY_CALL

```json
{
  "jsonrpc": "2.0",
  "method": "choose_parity",
  "params": {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_CALL",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:15:05Z",
    "conversation_id": "conv_r1m1002",
    "auth_token": "tok_ref01_abc123",
    "match_id": "R1M1",
    "player_id": "P02",
    "game_type": "even_odd",
    "context": {
      "opponent_id": "P01",
      "round_id": 1,
      "your_standings": {"wins": 0, "losses": 0, "draws": 0}
    },
    "deadline": "2025-01-15T10:15:35Z"
  },
  "id": 1102
}
```

#### P02 → REF : CHOOSE_PARITY_RESPONSE

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_RESPONSE",
    "sender": "player:P02",
    "timestamp": "2025-01-15T10:15:12Z",
    "conversation_id": "conv_r1m1002",
    "auth_token": "tok_p02_def456",
    "match_id": "R1M1",
    "player_id": "P02",
    "parity_choice": "odd"
  },
  "id": 1102
}
```

---

### 7. Game Over

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

---

### 8. Standings Update

#### LM → All Players : LEAGUE_STANDINGS_UPDATE

```json
{
  "jsonrpc": "2.0",
  "method": "update_standings",
  "params": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_STANDINGS_UPDATE",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:20:00Z",
    "conversation_id": "conv_round1standings",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "standings": [
      {"rank": 1, "player_id": "P01", "display_name": "Agent Alpha", "played": 1, "wins": 1, "draws": 0, "losses": 0, "points": 3},
      {"rank": 2, "player_id": "P03", "display_name": "Agent Gamma", "played": 1, "wins": 0, "draws": 1, "losses": 0, "points": 1},
      {"rank": 3, "player_id": "P04", "display_name": "Agent Delta", "played": 1, "wins": 0, "draws": 1, "losses": 0, "points": 1},
      {"rank": 4, "player_id": "P02", "display_name": "Agent Beta", "played": 1, "wins": 0, "draws": 0, "losses": 1, "points": 0}
    ]
  },
  "id": 1401
}
```

---

### 9. Round & League Completion

#### LM → All : ROUND_COMPLETED

```json
{
  "jsonrpc": "2.0",
  "method": "notify_round_completed",
  "params": {
    "protocol": "league.v2",
    "message_type": "ROUND_COMPLETED",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:20:05Z",
    "conversation_id": "conv_round1complete",
    "league_id": "league_2025_even_odd",
    "round_id": 1,
    "matches_played": 2,
    "next_round_id": 2
  },
  "id": 1402
}
```

#### LM → All : LEAGUE_COMPLETED

```json
{
  "jsonrpc": "2.0",
  "method": "notify_league_completed",
  "params": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_COMPLETED",
    "sender": "league_manager",
    "timestamp": "2025-01-15T12:00:00Z",
    "conversation_id": "conv_leaguecomplete",
    "league_id": "league_2025_even_odd",
    "total_rounds": 3,
    "total_matches": 6,
    "champion": {
      "player_id": "P01",
      "display_name": "Agent Alpha",
      "points": 7
    },
    "final_standings": [
      {"rank": 1, "player_id": "P01", "points": 7},
      {"rank": 2, "player_id": "P03", "points": 5},
      {"rank": 3, "player_id": "P04", "points": 4},
      {"rank": 4, "player_id": "P02", "points": 2}
    ]
  },
  "id": 2001
}
```

---

### 10. Error Messages

#### GAME_ERROR (Timeout)

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
    "action_required": "CHOOSE_PARITY_RESPONSE",
    "retry_count": 0,
    "max_retries": 3,
    "consequence": "Technical loss if no response after retries"
  },
  "id": 1103
}
```

#### LEAGUE_ERROR (Authentication)

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "LEAGUE_ERROR",
    "sender": "league_manager",
    "timestamp": "2025-01-15T10:05:30Z",
    "conversation_id": "conv_error001",
    "error_code": "E012",
    "error_description": "AUTH_TOKEN_INVALID",
    "context": {
      "provided_token": "tok_invalid_xxx",
      "action": "LEAGUE_QUERY"
    }
  },
  "id": 1502
}
```

---

### Error Code Reference

| Error Code | Description | Consequence |
|------------|-------------|-------------|
| `E001` | `TIMEOUT_ERROR` | Technical loss after max retries |
| `E002` | `INVALID_CHOICE` | Must respond with "even" or "odd" |
| `E003` | `DUPLICATE_RESPONSE` | Ignored, first response used |
| `E010` | `REGISTRATION_CLOSED` | Cannot join league |
| `E011` | `PLAYER_NOT_FOUND` | Invalid player ID |
| `E012` | `AUTH_TOKEN_INVALID` | Action rejected |
| `E013` | `MATCH_NOT_FOUND` | Invalid match ID |
| `E018` | `PROTOCOL_VERSION_MISMATCH` | Registration rejected, agent version < 2.0.0 |
| `E020` | `INTERNAL_ERROR` | Contact support |

---

### Unresponsive Player Handling

When a player fails to respond within the timeout period:

1. The referee sends a `GAME_ERROR` message with `retryable = true`
2. The player receives up to **3 retry attempts**
3. If all retries are exhausted without a response, the player is assigned a **technical loss** (`TECHNICAL_LOSS`)

**Retry Flow:**

```
Player Timeout → GAME_ERROR (retry 1/3) → Wait → GAME_ERROR (retry 2/3) → Wait → GAME_ERROR (retry 3/3) → TECHNICAL_LOSS
```

**GAME_ERROR with Retry:**

```json
{
  "jsonrpc": "2.0",
  "method": "notify_game_error",
  "params": {
    "protocol": "league.v2",
    "message_type": "GAME_ERROR",
    "sender": "referee:REF01",
    "timestamp": "2025-01-15T10:16:00Z",
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

This ensures that unresponsive players are handled consistently while giving them multiple opportunities to respond.

---

## 📑 APPENDIX: Implementation Reference Code

This appendix provides reference implementations for each component using FastAPI and standard Python libraries.

---

### 1. Basic MCP Server

Implemented with FastAPI:

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

**Key Features:**
- Exposes a JSON-RPC endpoint `/mcp`
- Routes calls to the corresponding method handler based on `request.method`
- Returns results in standard MCP JSON-RPC format

---

### 2. Player Agent Implementation

**Required tools for the player agent:**
- `handle_game_invitation` – accept a game invitation
- `choose_parity` – select "even" or "odd"
- `notify_match_result` – receive match result

**Example implementation:**

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

**Key Features:**
- Uses random strategy for parity choice
- Logs match results for learning or analysis
- All timestamps in UTC format

---

### 3. Referee Implementation

**Required tools for the referee:**
- `register_to_league` – register itself with the league manager
- `start_match` – start a new match
- `collect_choices` – collect players' parity choices
- `draw_number` – randomly draw a number
- `finalize_match` – determine winner and report results

**Register referee example:**

```python
import requests

def register_to_league(league_endpoint, referee_info):
    payload = {
        "jsonrpc": "2.0",
        "method": "register_referee",
        "params": {
            "referee_meta": {
                "display_name": referee_info["name"],
                "version": "1.0.0",
                "game_types": ["even_odd"],
                "contact_endpoint": referee_info["endpoint"],
                "max_concurrent_matches": 2
            }
        },
        "id": 1
    }
    response = requests.post(league_endpoint, json=payload)
    result = response.json()
    return result.get("result", {}).get("referee_id")
```

**Determine winner logic:**

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

---

### 4. League Manager Implementation

**Required tools for the league manager:**
- `register_referee` – register a new referee
- `register_player` – register a new player
- `create_schedule` – create a match schedule (Round Robin)
- `report_match_result` – receive and process match results
- `get_standings` – return current leaderboard

**Example implementation:**

```python
class LeagueManager:
    def __init__(self):
        self.referees = {}  # referee_id -> info
        self.players = {}   # player_id -> info
        self.next_referee_id = 1

    def register_referee(self, params):
        referee_meta = params.get("referee_meta", {})
        referee_id = f"REF{self.next_referee_id:02d}"
        self.next_referee_id += 1

        self.referees[referee_id] = {
            "referee_id": referee_id,
            "display_name": referee_meta.get("display_name"),
            "endpoint": referee_meta.get("contact_endpoint"),
            "game_types": referee_meta.get("game_types", []),
            "max_concurrent": referee_meta.get("max_concurrent_matches", 1)
        }

        return {
            "message_type": "REFEREE_REGISTER_RESPONSE",
            "status": "ACCEPTED",
            "referee_id": referee_id,
            "reason": None
        }
```

**Round-robin schedule creation:**

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

---

### 5. MCP Tool Call Helper

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

### Implementation Summary

This setup provides a fully functional minimal ecosystem for the "Even/Odd" game:

| Component | Responsibility |
|-----------|---------------|
| **MCP Server** | Handles JSON-RPC requests |
| **Player Agents** | Respond to invitations, choose parity, log results |
| **Referees** | Manage matches, draw numbers, determine winners |
| **League Manager** | Register participants, schedule matches, update standings |

---

## 📑 APPENDIX: Resilience Patterns

Distributed systems must handle temporary failures. The protocol defines retry policies:

- **Maximum of 3 retries**
- **2-second delay between retries**
- **Exponential backoff** is recommended under high load

---

### 1. Retry Pattern

Implementation example with exponential backoff:

```python
import time
import requests
from typing import Optional, Dict, Any

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

**Key Features:**
- Retries failed requests up to 3 times
- Uses exponential backoff: `delay = base_delay * (multiplier ** attempt)`
- Returns a structured error if all retries fail

---

### 2. Circuit Breaker Pattern

When a service fails repeatedly, further attempts are blocked for a timeout period.

**Simple Circuit Breaker example:**

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

**Behavior:**
- After repeated failures (threshold), breaker goes `OPEN` and blocks requests
- After `reset_timeout`, breaker enters `HALF_OPEN` and allows a trial request
- Success resets breaker to `CLOSED`

This pattern ensures the system avoids cascading failures and improves resilience under network or service instability.

---

## 📑 APPENDIX: Structured Logging

The protocol requires all logs to be in **JSON format** to allow for easy analysis and unified error tracking.

### Log Message Schema

Each log message must include the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timestamp` | string | Yes | ISO 8601 timestamp of the log entry (UTC) |
| `level` | string | Yes | Log level: `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `agent_id` | string | Yes | Identifier of the agent producing the log |
| `message_type` | string | No | Type of message being logged |
| `conversation_id` | string | No | ID of the conversation related to the log |
| `message` | string | Yes | Human-readable log message |
| `data` | object | No | Additional structured data or context |

### Log Levels

| Level | Usage |
|-------|-------|
| `DEBUG` | Detailed debugging information |
| `INFO` | General operational events |
| `WARN` | Warning conditions that may require attention |
| `ERROR` | Error conditions that require immediate action |

### Example JSON Log

```json
{
  "timestamp": "2025-12-19T13:00:00Z",
  "level": "INFO",
  "agent_id": "PLAYER_01",
  "message_type": "GAME_JOIN_ACK",
  "conversation_id": "match_001",
  "message": "Player joined the match successfully.",
  "data": {
    "match_id": "R1M1",
    "player_name": "Agent Alpha"
  }
}
```

### Best Practices

1. **Always use UTC timestamps** with the `Z` suffix (ISO 8601 format)
2. **Include `conversation_id`** when logging message-related events for traceability
3. **Use appropriate log levels** to enable filtering in production
4. **Include relevant context** in the `data` field for debugging

---

## 📑 APPENDIX: Player Registration and Authenticated Messaging

This section describes how player agents register with the league and send authenticated messages.

---

### 1. Agent Credentials Dataclass

Stores information about a registered player:

```python
from dataclasses import dataclass

@dataclass
class AgentCredentials:
    agent_id: str
    auth_token: str
    league_id: str
```

| Field | Description |
|-------|-------------|
| `agent_id` | Unique identifier for the player |
| `auth_token` | Token for authenticated requests |
| `league_id` | The league the player is registered in |

---

### 2. Player Registration Function

Registers a player with the league manager and retrieves credentials:

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

**Behavior:**
- Sends a `LEAGUE_REGISTER_REQUEST` to the league manager
- Returns `AgentCredentials` if registration is accepted
- Returns `None` if registration fails

---

### 3. Authenticated Client

Wraps sending messages to MCP endpoints with authentication:

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

**Key Features:**
- Automatically includes `auth_token` and `league_id` in all requests
- Ensures that the MCP server can authenticate the player

---

### 4. Usage Summary

This setup allows a player agent to:

| Step | Action |
|------|--------|
| 1 | Register with the league using `register_player()` |
| 2 | Receive a secure `auth_token` upon successful registration |
| 3 | Send authenticated MCP messages using `AuthenticatedClient` |

The `AuthenticatedClient` automatically handles credentials, so agents don't need to manually add authentication tokens to each request.
