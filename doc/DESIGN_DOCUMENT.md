# Assignment 7: AI Agent League Competition - Comprehensive Design Document

**Document Version**: 1.0  
**Created**: December 19, 2025  
**Status**: Design Phase  
**Protocol Version**: league.v1  
**Target Completion**: January 8, 2025  

---

## 📋 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [Architecture Design](#3-architecture-design)
4. [Core Design Principles](#4-core-design-principles)
5. [Component Design](#5-component-design)
6. [Data Models & Schemas](#6-data-models--schemas)
7. [Protocol Specification](#7-protocol-specification)
8. [Implementation Strategy](#8-implementation-strategy)
9. [Testing Strategy](#9-testing-strategy)
10. [Quality Assurance](#10-quality-assurance)
11. [Risk Management](#11-risk-management)
12. [Timeline & Milestones](#12-timeline--milestones)

---

## 1. Executive Summary

### 1.1 Project Purpose

Design and implement a **competitive multi-agent system** where autonomous AI agents compete in an Even-Odd game following a standardized MCP (Model Context Protocol) over HTTP communication.

**Key Objectives**:
- Demonstrate decoupled architecture enabling complete modularity
- Implement protocol-driven communication with strict JSON schema compliance
- Create distributed agent orchestration with proper state management
- Design game-agnostic system supporting future extensibility

### 1.2 Key Innovation

**Total Decoupling Between Layers**: The protocol enables agents to participate in any future league regardless of specific game rules. An agent built for this protocol can join new games without modification to core logic.

### 1.3 Success Criteria

| Criterion | Target | Critical |
|-----------|--------|----------|
| Protocol Compliance | 100% valid messages | ✅ Yes |
| Test Coverage | ≥70% (≥85% critical) | ✅ Yes |
| File Size Compliance | All files <150 lines | ✅ Yes |
| Documentation | 12+ complete documents | ✅ Yes |
| Competition Rank | Top 40% of class | ⚠️ Medium |
| Statistical Rigor | p-values, effect sizes | ✅ Yes |

### 1.4 Project Scope

**In Scope**:
- ✅ League management (registration, scheduling, ranking)
- ✅ 2 Referee agents for Even-Odd game
- ✅ 4 Player agents with configurable strategies
- ✅ HTTP/MCP protocol implementation
- ✅ Complete data persistence layer
- ✅ Comprehensive logging system
- ✅ Testing framework (unit, integration, edge cases)
- ✅ Publication-quality documentation

**Out of Scope**:
- ❌ GUI/web interface (CLI only)
- ❌ Real-time visualization during gameplay
- ❌ Machine learning model training
- ❌ Games other than Even-Odd (future extension)
- ❌ Distributed deployment across machines

---

## 2. System Overview

### 2.1 System Context Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              AI AGENT LEAGUE COMPETITION SYSTEM              │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           LEAGUE MANAGER (Port 8000)                  │  │
│  │  • Registration    • Scheduling    • Rankings         │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│         ┌─────────────┴────────────┐                       │
│         │                          │                       │
│  ┌──────▼────────┐        ┌───────▼────────┐             │
│  │ REFEREE REF01 │        │ REFEREE REF02  │             │
│  │  (Port 8001)  │        │  (Port 8002)   │             │
│  └──────┬────────┘        └───────┬────────┘             │
│         │                          │                       │
│    ┌────┴────┐                ┌────┴────┐                 │
│    │         │                │         │                 │
│  ┌─▼──┐  ┌──▼──┐         ┌──▼──┐  ┌──▼──┐               │
│  │P01 │  │ P02 │         │ P03 │  │ P04 │               │
│  │8101│  │8102 │         │8103 │  │8104 │               │
│  └────┘  └─────┘         └─────┘  └─────┘               │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Port Allocation

| Agent Type | Agent ID | Port | Endpoint |
|------------|----------|------|----------|
| League Manager | LM01 | 8000 | http://localhost:8000/mcp |
| Referee | REF01 | 8001 | http://localhost:8001/mcp |
| Referee | REF02 | 8002 | http://localhost:8002/mcp |
| Player | P01 | 8101 | http://localhost:8101/mcp |
| Player | P02 | 8102 | http://localhost:8102/mcp |
| Player | P03 | 8103 | http://localhost:8103/mcp |
| Player | P04 | 8104 | http://localhost:8104/mcp |

### 2.3 Tournament Structure

**Format**: Round-robin with 4 players
- **Total Rounds**: 3
- **Matches per Round**: 2 (parallel)
- **Total Matches**: 6
- **Each player faces**: Every other player exactly once

**Match Schedule**:
| Match ID | Round | Player A | Player B | Referee |
|----------|-------|----------|----------|---------|
| R1M1 | 1 | P01 | P02 | REF01 |
| R1M2 | 1 | P03 | P04 | REF02 |
| R2M1 | 2 | P03 | P01 | REF01 |
| R2M2 | 2 | P04 | P02 | REF02 |
| R3M1 | 3 | P04 | P01 | REF01 |
| R3M2 | 3 | P03 | P02 | REF02 |

**Scoring System**:
- Win: **3 points**
- Draw: **1 point each**
- Loss: **0 points**

---

## 3. Architecture Design

### 3.1 Three-Layer Architecture

The system follows strict layering to ensure game-agnostic design:

**Layer 1: League Layer**
- **Purpose**: Tournament orchestration
- **Responsibilities**: Registration, scheduling, ranking
- **Does NOT**: Know game rules, validate moves

**Layer 2: Referee Layer**
- **Purpose**: Match orchestration
- **Responsibilities**: Game initialization, move collection, result reporting
- **Does NOT**: Know ranking algorithms, implement game rules directly

**Layer 3: Game Layer**
- **Purpose**: Game-specific logic
- **Responsibilities**: Move validation, winner determination
- **Does NOT**: Handle communication, manage tournaments

### 3.2 Mandatory Project Structure

```
assignment7/
├── SHARED/                          # Shared resources
│   ├── config/                      # Configuration files
│   │   ├── system.json
│   │   ├── agents/
│   │   │   └── agents_config.json
│   │   ├── leagues/
│   │   │   └── league_2025_even_odd.json
│   │   ├── games/
│   │   │   └── games_registry.json
│   │   └── defaults/
│   │       ├── referee.json
│   │       └── player.json
│   ├── data/                        # Runtime data
│   │   ├── leagues/
│   │   │   └── league_2025_even_odd/
│   │   │       ├── standings.json
│   │   │       └── rounds.json
│   │   ├── matches/
│   │   │   └── league_2025_even_odd/
│   │   │       ├── R1M1.json
│   │   │       └── ...
│   │   └── players/
│   │       ├── P01/
│   │       │   └── history.json
│   │       └── ...
│   ├── logs/                        # Logging
│   │   ├── league/
│   │   │   └── league_2025_even_odd/
│   │   │       └── league.log.jsonl
│   │   └── agents/
│   │       ├── REF01.log.jsonl
│   │       ├── P01.log.jsonl
│   │       └── ...
│   └── league_sdk/                  # Python SDK
│       ├── __init__.py
│       ├── config_models.py
│       ├── config_loader.py
│       ├── repositories.py
│       └── logger.py
├── agents/                          # Agent implementations
│   ├── league_manager/
│   │   ├── main.py
│   │   ├── handlers.py
│   │   └── scheduler.py
│   ├── referee_REF01/
│   │   ├── main.py
│   │   ├── game_logic.py
│   │   └── handlers.py
│   ├── referee_REF02/
│   ├── player_P01/
│   │   ├── main.py
│   │   ├── strategy.py
│   │   └── handlers.py
│   ├── player_P02/
│   ├── player_P03/
│   └── player_P04/
└── doc/                             # Documentation
    ├── protocol_spec.md
    ├── ARCHITECTURE.md
    ├── BUILDING_BLOCKS.md
    ├── EDGE_CASES.md
    ├── message_examples/
    ├── diagrams/
    └── ADRs/
```

---

## 4. Core Design Principles

### 4.1 Game-Agnostic Layers (CRITICAL)

**Principle**: League and referee layers must be completely independent of any specific game.

**Enforcement**:
- ❌ INVALID: `if game_type == "even_odd":` in league/referee code
- ✅ VALID: Delegate to `GameRules` interface

**Test**: If replacing Even-Odd with Chess requires changes in league/referee → DESIGN FAILS

### 4.2 Full Modularity

**Principle**: Every component must be independently replaceable.

**Replaceable Components**:
1. Game Rules (Even-Odd → Chess → Poker)
2. Protocol Version (v1 → v2 with backward compatibility)
3. Transport Layer (HTTP → STDIO → WebSocket)
4. Agent Implementations (any player/referee)

### 4.3 Protocol Stability

**Principle**: JSON protocol with fixed message schema.

**Base Message Fields** (IMMUTABLE):
```json
{
  "protocol": "league.v1",
  "message_type": "<TYPE>",
  "league_id": "<UUID>",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "<UUID>",
  "sender": "<IDENTITY>",
  "timestamp": "2025-12-19T18:30:00.000Z"
}
```

### 4.4 State Machine Enforcement

**Agent States**:
```
INIT → REGISTERED → ACTIVE → SUSPENDED → SHUTDOWN
```

**Match States**:
```
WAITING_FOR_PLAYERS → COLLECTING_CHOICES → DRAWING_NUMBER → FINISHED
```

---

## 5. Component Design

### 5.1 League Manager

**Responsibilities**:
- Player/referee registration
- Round-robin schedule generation
- Ranking calculation
- Round/league lifecycle management

**Key Algorithms**:

**Round-Robin Scheduling**:
```python
from itertools import combinations

def create_schedule(players: List[str]) -> List[List[Match]]:
    """Generate round-robin schedule for 4 players."""
    all_pairings = list(combinations(players, 2))  # 6 matches
    # Distribute across 3 rounds (2 matches per round)
    schedule = []
    for i in range(0, len(all_pairings), 2):
        round_matches = all_pairings[i:i+2]
        schedule.append(round_matches)
    return schedule
```

**Ranking Calculation**:
```python
def calculate_rankings(standings: List[dict]) -> List[dict]:
    """Sort by points (primary) and wins (tiebreaker)."""
    return sorted(
        standings,
        key=lambda p: (p["points"], p["wins"]),
        reverse=True
    )
```

### 5.2 Referee Agent

**Responsibilities**:
- Match initialization
- Player invitation and handshake
- Move collection with timeout enforcement
- Winner determination (delegates to game layer)
- Result reporting

**Game State Machine**:

```
┌─────────────────────────────────────┐
│     WAITING_FOR_PLAYERS             │
│  • Send GAME_INVITATION             │
│  • Wait 5s for GAME_JOIN_ACK        │
└────────────┬────────────────────────┘
             │ Both joined
             ▼
┌─────────────────────────────────────┐
│     COLLECTING_CHOICES              │
│  • Send CHOOSE_PARITY_CALL          │
│  • Wait 30s for PARITY_CHOICE       │
└────────────┬────────────────────────┘
             │ Both choices received
             ▼
┌─────────────────────────────────────┐
│     DRAWING_NUMBER                  │
│  • Draw random 1-10                 │
│  • Determine winner                 │
└────────────┬────────────────────────┘
             │ Winner determined
             ▼
┌─────────────────────────────────────┐
│     FINISHED                        │
│  • Send GAME_OVER                   │
│  • Send MATCH_RESULT_REPORT         │
└─────────────────────────────────────┘
```

**Even-Odd Game Rules**:
```python
class EvenOddGameRules:
    def draw_number(self) -> int:
        return random.randint(1, 10)
    
    def get_parity(self, number: int) -> str:
        return "even" if number % 2 == 0 else "odd"
    
    def determine_winner(self, choice_a, choice_b, number):
        parity = self.get_parity(number)
        if choice_a == parity and choice_b != parity:
            return "PLAYER_A"
        elif choice_b == parity and choice_a != parity:
            return "PLAYER_B"
        else:
            return "DRAW"
```

### 5.3 Player Agent

**Architecture**: Sensors → Decision Model → Actuators

**Sensors**:
- Parse incoming messages
- Extract game state and context

**Decision Model**:
- Choose strategy (Random, Frequency, Pattern)
- Make move decision
- Update opponent model

**Actuators**:
- Format response messages
- Send to referee

**Strategy Implementations**:

1. **Random Strategy** (Baseline):
```python
def choose_parity(game_state) -> str:
    return random.choice(["even", "odd"])
```

2. **Frequency Strategy**:
```python
def choose_parity(game_state) -> str:
    history = game_state.opponent_history
    even_count = history.count("even")
    odd_count = history.count("odd")
    # Counter most frequent
    return "odd" if even_count > odd_count else "even"
```

3. **Pattern Strategy**:
```python
def choose_parity(game_state) -> str:
    recent = game_state.opponent_history[-3:]
    if recent == ["even", "odd", "even"]:
        return "even"  # Predict "odd", counter it
    # ... pattern detection logic
    return random.choice(["even", "odd"])
```

---

## 6. Data Models & Schemas

### 6.1 Configuration Models

```python
@dataclass
class SystemConfig:
    schema_version: str
    protocol_version: str = "league.v1"
    timeouts: dict
    retry_policy: dict

@dataclass
class LeagueConfig:
    league_id: str
    game_type: str
    scoring: dict  # win_points, draw_points, loss_points
    total_rounds: int
    
@dataclass
class PlayerConfig:
    player_id: str
    display_name: str
    endpoint: str
    game_types: List[str]
```

### 6.2 Runtime Data Models

```python
@dataclass
class Standings:
    league_id: str
    version: int
    last_updated: str
    standings: List[PlayerStanding]

@dataclass
class PlayerStanding:
    rank: int
    player_id: str
    wins: int
    losses: int
    draws: int
    points: int
    games_played: int

@dataclass
class MatchData:
    match_id: str
    league_id: str
    round_id: int
    referee_id: str
    lifecycle: MatchLifecycle
    players: dict
    transcript: List[dict]
    result: MatchResult
```

### 6.3 Protocol Message Schema

**Base Schema** (JSON Schema):
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "required": [
    "protocol", "message_type", "league_id",
    "round_id", "match_id", "conversation_id",
    "sender", "timestamp"
  ],
  "properties": {
    "protocol": {"const": "league.v1"},
    "message_type": {
      "enum": [
        "REFEREE_REGISTER_REQUEST",
        "LEAGUE_REGISTER_REQUEST",
        "ROUND_ANNOUNCEMENT",
        "GAME_INVITATION",
        "GAME_JOIN_ACK",
        "CHOOSE_PARITY_CALL",
        "PARITY_CHOICE",
        "GAME_OVER",
        "MATCH_RESULT_REPORT",
        "LEAGUE_STANDINGS_UPDATE",
        "ROUND_COMPLETED",
        "LEAGUE_COMPLETED"
      ]
    },
    "timestamp": {
      "type": "string",
      "pattern": ".*Z$"
    }
  }
}
```

---

## 7. Protocol Specification

### 7.1 Critical Protocol Rules

**Timestamp Format** (MANDATORY):
- Format: ISO-8601 UTC
- Must end with `Z`
- ✅ Valid: `"2025-12-19T18:30:00.000Z"`
- ❌ Invalid: `"2025-12-19T18:30:00+02:00"`

**Response Timeouts**:
| Message Type | Timeout | Consequence |
|--------------|---------|-------------|
| GAME_JOIN_ACK | 5s | Player forfeits |
| PARITY_CHOICE | 30s | Technical loss |
| LEAGUE_REGISTER | 10s | Rejected |

**Error Codes**:
- `E001`: TIMEOUT_ERROR
- `E004`: INVALID_PARITY_CHOICE
- `E012`: AUTH_TOKEN_INVALID
- `E021`: INVALID_TIMESTAMP

### 7.2 Message Flow

```
1. STARTUP (Launcher)
   Launcher: Starts all agent processes (LM, Referees, Players)

2. SELF-REGISTRATION (Agents → LM)
   Each agent registers itself on startup:
     Referee → LM: REFEREE_REGISTER_REQUEST
     LM → Referee: REFEREE_REGISTER_RESPONSE (with auth_token)
     Player → LM: LEAGUE_REGISTER_REQUEST
     LM → Player: LEAGUE_REGISTER_RESPONSE (with auth_token)

3. LEAGUE START (Launcher → LM)
   Launcher → LM: START_LEAGUE
   LM → Launcher: LEAGUE_STATUS (started)

4. MATCH EXECUTION (LM → Referee → Players)
   For each match in schedule:
     LM → Referee: RUN_MATCH (with player endpoints)
     Referee → LM: RUN_MATCH_ACK
     
     Referee → Player A: GAME_INVITATION
     Player A → Referee: GAME_JOIN_ACK
     Referee → Player B: GAME_INVITATION
     Player B → Referee: GAME_JOIN_ACK
     
     Referee → Player A: CHOOSE_PARITY_CALL
     Player A → Referee: PARITY_CHOICE (30s timeout)
     Referee → Player B: CHOOSE_PARITY_CALL
     Player B → Referee: PARITY_CHOICE (30s timeout)
     
     Referee: Determines winner (draws number, compares choices)
     
     Referee → Player A: GAME_OVER
     Referee → Player B: GAME_OVER
     Referee → LM: MATCH_RESULT_REPORT
     LM → Referee: MATCH_RESULT_ACK
     LM: Updates standings

5. LEAGUE COMPLETION
   LM: All rounds complete
   LM: Finalizes standings
```

---

## 8. Implementation Strategy

### 8.1 Development Phases

**Phase 1: Foundation** (Days 1-3)
- Project structure setup
- league_sdk implementation
- Configuration files
- Logging infrastructure

**Phase 2: League Manager** (Days 4-6)
- HTTP server (FastAPI)
- Registration handlers
- Scheduler service
- Ranking service

**Phase 3: Referee Agents** (Days 7-9)
- HTTP server
- State machine
- Game rules module
- Move collection with timeouts

**Phase 4: Player Agents** (Days 10-12)
- HTTP server
- Strategy implementations
- Opponent modeling
- History tracking

**Phase 5: Testing** (Days 13-15)
- Unit tests (≥70% coverage)
- Integration tests
- Edge case tests (10+)
- Protocol compliance tests

**Phase 6: Documentation** (Days 16-18)
- Complete 12+ documents
- Visualizations (300 DPI)
- Statistical analysis
- Final polish

### 8.2 File Size Enforcement

**Rule**: NO file >150 lines

**Strategy**:
- Break large modules into sub-modules
- Extract utility functions
- Use clear imports
- Single responsibility per file

---

## 9. Testing Strategy

### 9.1 Test Coverage Requirements

- **Overall**: ≥70%
- **Critical modules**: ≥85%
- **Edge cases**: 10+ documented and tested

### 9.2 Test Categories

**Unit Tests**:
- ConfigLoader
- Schedulers
- Game rules
- Strategy implementations

**Integration Tests**:
- Full registration flow
- Complete match execution
- Full tournament run

**Edge Case Tests** (10+):
1. Empty dataset
2. Malformed messages
3. Invalid parity choice
4. Player timeout on join
5. Player timeout on choice
6. Duplicate registration
7. Missing auth token
8. Invalid timestamp format
9. Network disconnection
10. Concurrent message handling

### 9.3 Protocol Compliance Tests

- JSON schema validation
- Required fields present
- Correct data types
- UUID format validation
- Timestamp format validation

---

## 10. Quality Assurance

### 10.1 Code Quality Metrics

- Pylint score: ≥8.5/10
- All files <150 lines
- 100% type hints
- 100% function docstrings

### 10.2 Documentation Quality

- All 12+ documents complete
- No broken links
- Table of contents in major docs
- Screenshots/diagrams included

### 10.3 Research Quality

- Statistical significance (p-values)
- Effect sizes (Cohen's d)
- 95% confidence intervals
- Publication-quality visualizations (300 DPI)

---

## 11. Risk Management

### 11.1 Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Protocol violations | Disqualification | Extensive testing, schema validation |
| Timeout issues | Match losses | Retry logic, performance optimization |
| State machine bugs | Match failures | Comprehensive state tests |
| File size violations | Grade penalty | Automated checks, modular design |

### 11.2 Schedule Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Late start | Incomplete project | Start immediately, clear milestones |
| Scope creep | Delayed completion | Strict scope definition, MVP focus |
| Testing delays | Poor quality | Test-driven development |

---

## 12. Timeline & Milestones

### 12.1 Project Schedule

**Week 1** (Dec 18-20):
- M1: Project structure complete
- M2: SDK implementation done
- M3: League Manager functional

**Week 2** (Dec 21-27):
- M4: Referees functional
- M5: Players functional
- M6: Integration tests passing

**Week 3** (Dec 28-Jan 3):
- M7: All edge cases tested
- M8: Documentation complete
- M9: Statistical analysis done

**Week 4** (Jan 4-8):
- M10: Final testing
- M11: Peer review
- M12: Submission ready

### 12.2 Critical Milestones

| Milestone | Date | Deliverable | Success Criteria |
|-----------|------|-------------|------------------|
| M1 | Dec 20 | Project setup | Package installable |
| M6 | Dec 27 | Full system | 6-match tournament runs |
| M8 | Jan 3 | Documentation | All 12+ docs complete |
| M12 | Jan 8 | Submission | All requirements met |

---

## 13. Conclusion

This design document provides a comprehensive blueprint for implementing Assignment 7. The system architecture ensures:

✅ **Game-agnostic design** for future extensibility  
✅ **Protocol compliance** with zero tolerance for violations  
✅ **Modular components** that are independently testable  
✅ **Clear separation of concerns** across three layers  
✅ **Comprehensive documentation** meeting academic standards  

**Next Steps**:
1. Review and approve this design
2. Begin Phase 1: Foundation implementation
3. Follow test-driven development approach
4. Maintain daily progress tracking

---

**Document Prepared By**: Design Team  
**Review Status**: Pending approval  
**Version Control**: Track changes in git with clear commit messages  
**Related Documents**: PRD.md, ARCHITECTURE.md, protocol_spec.md
