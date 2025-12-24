# Building Blocks - System Components

**Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete

---

## Overview

This document describes the major building blocks (components) of the AI Agent League Competition System. Each component has specific responsibilities and interacts with others through well-defined protocols.

---

## 1. League Manager

### Purpose
The League Manager is the central orchestrator that coordinates the entire tournament. It manages registrations, schedules matches, tracks standings, and announces results.

### Key Responsibilities
- **Agent Registration**: Accept and validate registrations from referees and players
- **Tournament Scheduling**: Generate round-robin match schedule
- **Match Orchestration**: Coordinate match execution across rounds
- **Standings Management**: Calculate and update player rankings
- **Round Management**: Announce rounds and track completion
- **Results Broadcasting**: Distribute standings updates to all participants

### Implementation Details
- **Framework**: FastAPI (Python web framework)
- **Port**: 8000
- **Protocol**: HTTP/JSON
- **State Management**: File-based persistence

### Key Modules
1. **main.py** (82 lines)
   - FastAPI application initialization
   - `/mcp` endpoint for message handling
   - Request routing and error handling

2. **handlers.py** (106 lines)
   - `handle_referee_register()` - Process referee registrations
   - `handle_league_register()` - Process player registrations
   - `handle_match_result_report()` - Process match results

3. **scheduler.py** (70 lines)
   - `generate_round_robin_schedule()` - Create complete tournament schedule
   - Round-robin algorithm implementation
   - Referee assignment logic

4. **ranking.py** (70 lines)
   - `calculate_rankings()` - Sort players by points and wins
   - `update_standings()` - Update player statistics after matches
   - Tie-breaking logic (points, then wins)

### Data Managed
- **Standings**: Player rankings, points, wins, draws, losses
- **Match Schedule**: All matches with assigned referees
- **Registration Data**: Referee and player information

---

## 2. Referee Agent

### Purpose
Referees manage individual matches between two players. They enforce game rules, validate player actions, track game state, and report results to the League Manager.

### Key Responsibilities
- **Match Setup**: Initialize match and invite players
- **Game Flow Control**: Manage state transitions from setup to completion
- **Rule Enforcement**: Validate moves according to Even-Odd game rules
- **Result Determination**: Calculate match outcomes and declare winners
- **Result Reporting**: Send match results to League Manager

### Implementation Details
- **Framework**: FastAPI (Python web framework)
- **Instances**: 2 referees (REF01 on port 8001, REF02 on port 8002)
- **Protocol**: HTTP/JSON
- **State Management**: In-memory state machine

### Key Modules
1. **generic_referee.py** (122 lines)
   - FastAPI application for referee
   - `/mcp` endpoint for message handling
   - Match orchestration logic

2. **referee_game_logic.py** (37 lines)
   - `EvenOddGameRules` class
   - `draw_number()` - Generate random number 1-10
   - `get_parity()` - Determine if number is even or odd
   - `determine_winner()` - Calculate match outcome
   - `validate_parity_choice()` - Validate player choices

3. **referee_match_state.py** (96 lines)
   - `MatchStateMachine` class - FSM implementation
   - `MatchContext` class - Match state container
   - State transitions: SETUP → READY → PLAYING → FINISHED
   - Message handlers for state updates

4. **referee_http_handlers.py** (23 lines)
   - HTTP endpoint handlers
   - Message routing

5. **referee_match_runner.py** (60 lines)
   - Match execution orchestration
   - Player invitation and coordination

### Game Rules (Even-Odd)
1. Referee draws a random number (1-10)
2. Player A chooses "even" or "odd"
3. Player B gets the opposite parity
4. Number's parity determines winner
5. If number = 5, it's a draw

### State Machine
```
SETUP → READY → PLAYING → FINISHED
  ↓       ↓        ↓          ↓
Initial  Both    Choices   Result
        joined   made      reported
```

---

## 3. Player Agent

### Purpose
Players compete in matches by making strategic decisions. They receive invitations, choose parities, and adapt their strategies based on historical data.

### Key Responsibilities
- **Match Participation**: Respond to game invitations
- **Strategy Execution**: Make parity choices using configured strategy
- **History Tracking**: Record opponent choices for learning
- **Adaptation**: Adjust strategy based on past matches

### Implementation Details
- **Framework**: FastAPI (Python web framework)
- **Instances**: 4 players (P01-P04 on ports 8101-8104)
- **Protocol**: HTTP/JSON
- **State Management**: In-memory with history persistence

### Key Modules
1. **generic_player.py** (115 lines)
   - FastAPI application for player
   - `/mcp` endpoint for message handling
   - Strategy initialization and execution
   - Message handlers:
     - `handle_round_announcement()` - Prepare for new round
     - `handle_game_invitation()` - Accept match invitation
     - `handle_choose_parity_call()` - Make parity choice
     - `handle_game_over()` - Record match result

2. **player_strategies.py** (56 lines)
   - `RandomStrategy` - Random parity selection
   - `FrequencyStrategy` - Based on opponent's historical choices
   - `PatternStrategy` - Detects alternating patterns

### Strategy Descriptions

#### RandomStrategy
- **Logic**: 50/50 random choice
- **Use Case**: Baseline comparison, unpredictable
- **Advantages**: Cannot be exploited
- **Disadvantages**: Cannot exploit patterns

#### FrequencyStrategy
- **Logic**: Chooses opposite of opponent's most frequent past choice
- **Use Case**: Exploit predictable opponents
- **Advantages**: Adapts to opponent tendencies
- **Disadvantages**: Vulnerable to counter-adaptation

#### PatternStrategy
- **Logic**: Detects alternating patterns, defaults to frequency if no pattern
- **Use Case**: Exploit alternating strategies
- **Advantages**: Can recognize and counter patterns
- **Disadvantages**: Needs sufficient history

### Player Configuration
Each player is configured with:
- **player_id**: Unique identifier (P01-P04)
- **display_name**: Human-readable name
- **endpoint**: "localhost"
- **port**: Unique port (8101-8104)
- **game_types**: ["even_odd"]
- **strategy**: One of the three strategies

---

## 4. League SDK

### Purpose
The League SDK is a shared library providing common functionality used by all agents. It handles configuration, data persistence, messaging, logging, and validation.

### Key Responsibilities
- **Configuration Management**: Load and parse JSON configuration files
- **Data Persistence**: Repository pattern for file-based storage
- **Message Building**: Create protocol-compliant messages
- **Validation**: Validate message format and content
- **Logging**: Structured logging in JSONL format
- **HTTP Communication**: Send messages between agents

### Key Modules

#### Configuration (3 modules, 174 lines total)
1. **config_models.py** (59 lines)
   - `SystemConfig` - System-wide settings
   - `LeagueConfig` - League tournament settings
   - `PlayerConfig` - Player agent configuration
   - `RefereeConfig` - Referee agent configuration
   - `GameConfig` - Game-specific metadata

2. **config_loader.py** (79 lines)
   - `load_system_config()` - Load system.json
   - `load_league_config()` - Load league configuration
   - `load_agent_config()` - Load agent configurations
   - `load_game_config()` - Load game registry

#### Data Persistence (1 module, 112 lines)
3. **repositories.py** (112 lines)
   - `StandingsRepository` - Manage player rankings
     - `load()`, `save()`, `update_player()`
   - `MatchRepository` - Store match results
     - `save_match()`, `load_match()`, `list_matches()`
   - `PlayerHistoryRepository` - Track player match history
     - `save_history()`, `load_history()`, `append_match()`

#### Protocol & Messaging (4 modules, 200 lines total)
4. **messages.py** (56 lines)
   - `create_base_message()` - Base message structure
   - `validate_message()` - Message validation
   - `format_timestamp()` - ISO-8601 UTC with Z
   - Message builders for all 10 message types

5. **validation.py** (145 lines)
   - `validate_message_structure()` - Check required fields
   - `validate_timestamp()` - ISO-8601 format with Z
   - `validate_uuid()` - UUID v4 format
   - `validate_message_type()` - Valid enum value
   - `get_validation_errors()` - Comprehensive validation

6. **http_client.py** (62 lines)
   - `send_message()` - Send HTTP POST request
   - `send_with_retry()` - Retry logic with exponential backoff
   - Timeout handling
   - Error handling

7. **logger.py** (63 lines)
   - `LeagueLogger` class
   - `log_message()` - JSONL format logging
   - `log_error()` - Error logging
   - `log_state_change()` - State transition logging

#### Additional Modules
8. **transport.py** (65 lines) - Network communication layer
9. **agent_comm.py** (31 lines) - Agent-to-agent communication helpers
10. **session_manager.py** (84 lines) - Session lifecycle management

### Design Patterns Used
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Message creation
- **Strategy Pattern**: Player strategies
- **State Machine Pattern**: Referee match management

---

## 5. Configuration Files

### System Configuration (`system.json`)
```json
{
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

### Agent Configuration (`agents_config.json`)
Defines all agents:
- League Manager (LM01, port 8000)
- 2 Referees (REF01, REF02, ports 8001-8002)
- 4 Players (P01-P04, ports 8101-8104)

### League Configuration (`league_2025_even_odd.json`)
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

### Game Registry (`games_registry.json`)
Registers available games:
- Even-Odd game metadata
- Rules version
- Max players (2)

---

## 6. Data Storage

### File Structure
```
SHARED/data/
├── leagues/
│   └── league_2025_even_odd/
│       └── standings.json
├── matches/
│   └── league_2025_even_odd/
│       ├── match_R1_M1.json
│       ├── match_R1_M2.json
│       └── ...
└── players/
    ├── P01/
    │   └── history.json
    ├── P02/
    │   └── history.json
    └── ...
```

### Data Formats

#### Standings Format
```json
{
  "version": "1.0",
  "last_updated": "2025-12-20T10:30:00Z",
  "standings": [
    {
      "player_id": "P01",
      "points": 9,
      "wins": 3,
      "draws": 0,
      "losses": 0,
      "games_played": 3,
      "rank": 1
    }
  ]
}
```

#### Match Result Format
```json
{
  "match_id": "match_R1_M1",
  "round": 1,
  "players": ["P01", "P02"],
  "referee": "REF01",
  "number_drawn": 7,
  "player_a_choice": "odd",
  "player_b_choice": "even",
  "winner": "PLAYER_A",
  "timestamp": "2025-12-20T10:15:00Z"
}
```

---

## 7. Protocol Messages

### Message Types (10 total)
1. **REFEREE_REGISTER_REQUEST** - Referee → League Manager
2. **LEAGUE_REGISTER_REQUEST** - Player → League Manager
3. **ROUND_ANNOUNCEMENT** - League Manager → All Players
4. **GAME_INVITATION** - Referee → Players
5. **GAME_JOIN_ACK** - Player → Referee
6. **CHOOSE_PARITY_CALL** - Referee → Player
7. **PARITY_CHOICE** - Player → Referee
8. **GAME_OVER** - Referee → Players
9. **MATCH_RESULT_REPORT** - Referee → League Manager
10. **LEAGUE_STANDINGS_UPDATE** - League Manager → All Players

### Common Message Structure
```json
{
  "message_type": "MESSAGE_TYPE",
  "protocol_version": "league.v2",
  "timestamp": "2025-12-20T10:00:00Z",
  "message_id": "uuid-v4",
  "sender_id": "agent_id",
  "recipient_id": "agent_id",
  "payload": {}
}
```

---

## 8. Testing Components

### Test Categories
1. **Unit Tests** (78 tests) - Test individual modules
2. **Integration Tests** (8 tests) - Test component interactions
3. **Edge Case Tests** (24 tests) - Test boundary conditions
4. **Protocol Tests** (23 tests) - Test message compliance
5. **Line Count Tests** (6 tests) - Verify file size compliance

### Test Coverage
- **Overall**: 54% (exceeds 50% requirement)
- **SDK Core**: 83% average
- **Game Logic**: 79% average
- **Critical Modules**: 7 at 100%, 2 at ≥90%

---

## Component Interaction Flow

### Registration Phase
```
Player → League Manager: LEAGUE_REGISTER_REQUEST
League Manager → Player: Response (auth_token)

Referee → League Manager: REFEREE_REGISTER_REQUEST
League Manager → Referee: Response (auth_token)
```

### Match Execution Phase
```
League Manager → Players: ROUND_ANNOUNCEMENT

Referee → Players: GAME_INVITATION
Players → Referee: GAME_JOIN_ACK

Referee → Player A: CHOOSE_PARITY_CALL
Player A → Referee: PARITY_CHOICE

Referee → Player B: CHOOSE_PARITY_CALL
Player B → Referee: PARITY_CHOICE

Referee → Players: GAME_OVER
Referee → League Manager: MATCH_RESULT_REPORT

League Manager → Players: LEAGUE_STANDINGS_UPDATE
```

---

## Technology Stack

### Core Technologies
- **Language**: Python 3.9+
- **Web Framework**: FastAPI 0.104+
- **HTTP Client**: httpx 0.25+
- **Testing**: pytest 7.4+
- **Coverage**: pytest-cov 4.1+

### Design Principles
- **Modularity**: Each component is independent
- **Single Responsibility**: Each module has one job
- **Configuration-Driven**: Behavior controlled by JSON files
- **Protocol-Based**: Well-defined message contracts
- **File Size Compliance**: All files <150 lines

---

## Deployment

### Starting the System
1. Start League Manager: `python agents/league_manager/main.py`
2. Start Referees: `python agents/launch_referee_01.py` and `launch_referee_02.py`
3. Start Players: `python agents/launch_player_0X.py` (X=1-4)
4. Run Tournament: `python run_league.py`

### Port Allocation
- **8000**: League Manager
- **8001-8002**: Referees
- **8101-8104**: Players

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-20  
**Status**: Complete ✅
