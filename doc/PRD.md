# Product Requirements Document (PRD)
# Assignment 7 - AI Agent League Competition

**Document Version**: 1.0.0  
**Created**: December 19, 2025  
**Last Updated**: December 19, 2025  
**Status**: Approved for Implementation  
**Author**: Assignment 7 Team

---

## 📋 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Overview](#2-project-overview)
3. [Stakeholders](#3-stakeholders)
4. [KPIs & Success Metrics](#4-kpis--success-metrics)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Grading Criteria](#7-grading-criteria)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [Out-of-Scope](#9-out-of-scope)
10. [Dependencies](#10-dependencies)
11. [Constraints](#11-constraints)
12. [Assumptions](#12-assumptions)
13. [Risks & Mitigations](#13-risks--mitigations)
14. [Timeline & Milestones](#14-timeline--milestones)
15. [Glossary](#15-glossary)

---

## 1. Executive Summary

### 1.1 Purpose

This document defines the product requirements for **Assignment 7: AI Agent League Competition**, a multi-agent system where autonomous agents compete in a structured tournament using the MCP (Model Context Protocol) over HTTP. The system demonstrates advanced concepts in distributed systems, protocol-driven communication, and strategic AI decision-making.

### 1.2 Vision Statement

Create a **competitive AI agent league platform** that enables autonomous agents to participate in games following a standardized, extensible communication protocol. The architecture must be **fully decoupled**, allowing any component (game rules, transport layer, persistence) to be replaced without affecting others.

### 1.3 Key Innovation

**Total Decoupling Between Layers**: The protocol enables agents to participate in any future league regardless of specific game rules. An agent built for this protocol can join new games without modification.

### 1.4 Competition Summary

| Attribute | Value |
|-----------|-------|
| Players | 4 (P01-P04) |
| Referees | 2 (REF01-REF02) |
| Tournament Format | Round-robin |
| Total Rounds | 3 |
| Matches per Round | 2 (parallel) |
| Total Matches | 6 |
| Game Type | Even-Odd (single-round simultaneous) |
| Scoring | Win=3, Draw=1, Loss=0 |

---

## 2. Project Overview

### 2.1 Problem Statement

Multi-agent systems require standardized communication protocols and decoupled architectures to enable:
- Interoperability between different agent implementations
- Scalability for large-scale competitions
- Extensibility for new game types and rules
- Reliability in distributed environments

### 2.2 Solution Overview

Build a three-layer architecture system:

```
┌─────────────────────────────────────────────────────────────┐
│                    LEAGUE LAYER (Port 8000)                  │
│  League Manager: Registration, Scheduling, Rankings          │
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                  │
┌────────▼─────────┐              ┌────────▼─────────┐
│ REFEREE LAYER    │              │ REFEREE LAYER    │
│ REF01 (8001)     │              │ REF02 (8002)     │
│ Game Orchestration│             │ Game Orchestration│
└────────┬─────────┘              └────────┬─────────┘
         │                                  │
    ┌────┴────┐                        ┌────┴────┐
    │         │                        │         │
┌───▼──┐  ┌──▼───┐                ┌───▼──┐  ┌──▼───┐
│GAME  │  │GAME  │                │GAME  │  │GAME  │
│LAYER │  │LAYER │                │LAYER │  │LAYER │
│P01   │  │P02   │                │P03   │  │P04   │
│:8101 │  │:8102 │                │:8103 │  │:8104 │
└──────┘  └──────┘                └──────┘  └──────┘
```

### 2.3 Key Features

1. **Protocol-Driven Communication**: JSON-based MCP protocol (league.v2)
2. **Decoupled Architecture**: Game-agnostic league and referee layers
3. **Parallel Execution**: 2 concurrent matches per round
4. **State Management**: Comprehensive logging and data persistence
5. **Recovery Support**: File-based credential persistence
6. **Extensibility**: Pluggable games, strategies, and transports

---

## 3. Stakeholders

### 3.1 Primary Stakeholders

| Role | Responsibility | Interest Level |
|------|----------------|----------------|
| **Students** | Implement agents, compete in league | High |
| **Course Instructor** | Evaluate submissions, run class league | High |
| **Teaching Assistants** | Support students, test infrastructure | High |

### 3.2 Secondary Stakeholders

| Role | Responsibility | Interest Level |
|------|----------------|----------------|
| **DevOps** | Monitor system health, logs | Medium |
| **Future Developers** | Extend system with new games | Medium |

### 3.3 Tertiary Stakeholders

| Role | Responsibility | Interest Level |
|------|----------------|----------------|
| **Academic Community** | Reference architecture for multi-agent systems | Low |

---

## 4. KPIs & Success Metrics

### 4.1 Protocol Compliance Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| JSON Schema Validation | 100% | All messages pass schema validation |
| Message Field Compliance | 100% | All required fields present |
| Timestamp Format | 100% | All timestamps in UTC (ISO-8601) |
| UUID Format | 100% | All IDs are RFC 4122 compliant |

### 4.2 Performance Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| Registration Response Time | <10s | Time from request to response |
| Game Join Acknowledgment | <5s | Player join timeout |
| Parity Choice Response | <30s | Player move timeout |
| Match Completion | <60s | Total match duration |
| Concurrent Match Support | 2 | Parallel matches per round |

### 4.3 Reliability Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| System Uptime | 99.9% | During competition period |
| Message Delivery | 100% | No lost messages |
| Error Recovery | 100% | Graceful handling of all errors |
| Zero Crashes | 50+ games | Consecutive games without crash |

### 4.4 Quality Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| Test Coverage | ≥70% | Overall code coverage |
| Critical Module Coverage | ≥85% | Protocol, handlers, game logic |
| Documentation Completeness | 100% | All required documents |
| Code Files | <150 lines each | Max lines per file |

### 4.5 Competition Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| Win Rate vs Random | >60% | Over 100 games |
| Protocol Violations | 0 | Zero violations in competition |
| Disqualifications | 0 | No agent disqualified |

---

## 5. Functional Requirements

### 5.1 League Manager Requirements (FR-100 Series)

#### FR-101: HTTP Server
- **Priority**: P0 (Must Have)
- **Description**: League Manager MUST run as HTTP server on port 8000
- **Acceptance**: Server responds to POST requests at `/mcp` endpoint

#### FR-102: Referee Registration
- **Priority**: P0 (Must Have)
- **Description**: MUST accept and validate `REFEREE_REGISTER_REQUEST` messages
- **Acceptance**: Returns `REFEREE_REGISTER_RESPONSE` with status and auth_token

#### FR-103: Player Registration
- **Priority**: P0 (Must Have)
- **Description**: MUST accept and validate `LEAGUE_REGISTER_REQUEST` messages
- **Acceptance**: Returns `LEAGUE_REGISTER_RESPONSE` with player_id and auth_token

#### FR-104: Round-Robin Schedule Generation
- **Priority**: P0 (Must Have)
- **Description**: MUST generate round-robin schedule after all registrations complete
- **Acceptance**: 3 rounds, 2 matches per round, each player faces each other exactly once

#### FR-105: Round Announcement
- **Priority**: P0 (Must Have)
- **Description**: MUST send `ROUND_ANNOUNCEMENT` to all players with match schedule
- **Acceptance**: All players receive round information before matches begin

#### FR-106: Match Result Tracking
- **Priority**: P0 (Must Have)
- **Description**: MUST receive and process `MATCH_RESULT_REPORT` from referees
- **Acceptance**: Results stored, standings updated

#### FR-107: Standings Calculation
- **Priority**: P0 (Must Have)
- **Description**: MUST calculate standings using scoring system (Win=3, Draw=1, Loss=0)
- **Acceptance**: Correct point totals, proper ranking by points

#### FR-108: Standings Broadcast
- **Priority**: P0 (Must Have)
- **Description**: MUST send `LEAGUE_STANDINGS_UPDATE` after each round
- **Acceptance**: All players receive current standings

#### FR-109: Round Completion
- **Priority**: P0 (Must Have)
- **Description**: MUST send `ROUND_COMPLETED` after all matches in round finish
- **Acceptance**: Message sent only when all match results received

#### FR-110: League Completion
- **Priority**: P0 (Must Have)
- **Description**: MUST send `LEAGUE_COMPLETED` after all rounds finish
- **Acceptance**: Final standings, champion identified

### 5.2 Referee Requirements (FR-200 Series)

#### FR-201: HTTP Server
- **Priority**: P0 (Must Have)
- **Description**: Referee MUST run as HTTP server on assigned port (8001-8002)
- **Acceptance**: Server responds to POST requests at `/mcp` endpoint

#### FR-202: League Registration
- **Priority**: P0 (Must Have)
- **Description**: MUST register with League Manager on startup
- **Acceptance**: Sends `REFEREE_REGISTER_REQUEST`, receives valid response

#### FR-203: Game State Machine
- **Priority**: P0 (Must Have)
- **Description**: MUST implement 4-state game state machine
- **States**: `WAITING_FOR_PLAYERS` → `COLLECTING_CHOICES` → `DRAWING_NUMBER` → `FINISHED`
- **Acceptance**: Correct state transitions, no invalid states

#### FR-204: Game Invitation
- **Priority**: P0 (Must Have)
- **Description**: MUST send `GAME_INVITATION` to both players
- **Acceptance**: Both players receive invitation with opponent info

#### FR-205: Join Acknowledgment Collection
- **Priority**: P0 (Must Have)
- **Description**: MUST collect `GAME_JOIN_ACK` from both players within 5 seconds
- **Acceptance**: Timeout handling, forfeit on failure

#### FR-206: Parity Choice Collection
- **Priority**: P0 (Must Have)
- **Description**: MUST send `CHOOSE_PARITY_CALL` and collect `PARITY_CHOICE` within 30 seconds
- **Acceptance**: Simultaneous requests, valid choice validation ("even" or "odd")

#### FR-207: Random Number Drawing
- **Priority**: P0 (Must Have)
- **Description**: MUST draw random number between 1 and 10 (inclusive)
- **Acceptance**: Fair distribution, cryptographically secure random

#### FR-208: Winner Determination
- **Priority**: P0 (Must Have)
- **Description**: MUST determine winner based on parity match
- **Acceptance**: Correct winner identification, draw handling

#### FR-209: Game Over Notification
- **Priority**: P0 (Must Have)
- **Description**: MUST send `GAME_OVER` to both players with result
- **Acceptance**: Both players receive complete result information

#### FR-210: Match Result Report
- **Priority**: P0 (Must Have)
- **Description**: MUST send `MATCH_RESULT_REPORT` to League Manager
- **Acceptance**: League Manager receives and processes result

#### FR-211: Error Handling
- **Priority**: P0 (Must Have)
- **Description**: MUST handle timeout and invalid move errors
- **Acceptance**: Proper error codes (E001, E004), forfeit handling

### 5.3 Player Requirements (FR-300 Series)

#### FR-301: HTTP Server
- **Priority**: P0 (Must Have)
- **Description**: Player MUST run as HTTP server on assigned port (8101-8104)
- **Acceptance**: Server responds to POST requests at `/mcp` endpoint

#### FR-302: League Registration
- **Priority**: P0 (Must Have)
- **Description**: MUST register with League Manager on startup
- **Acceptance**: Sends `LEAGUE_REGISTER_REQUEST`, receives player_id

#### FR-303: Round Announcement Handling
- **Priority**: P0 (Must Have)
- **Description**: MUST handle `ROUND_ANNOUNCEMENT` messages
- **Acceptance**: Stores schedule, prepares for matches

#### FR-304: Game Invitation Response
- **Priority**: P0 (Must Have)
- **Description**: MUST respond to `GAME_INVITATION` with `GAME_JOIN_ACK` within 5 seconds
- **Acceptance**: Timely response, correct format

#### FR-305: Parity Choice Response
- **Priority**: P0 (Must Have)
- **Description**: MUST respond to `CHOOSE_PARITY_CALL` with `PARITY_CHOICE` within 30 seconds
- **Acceptance**: Valid choice ("even" or "odd"), timely response

#### FR-306: Game Over Handling
- **Priority**: P0 (Must Have)
- **Description**: MUST handle `GAME_OVER` messages
- **Acceptance**: Updates internal state, logs result

#### FR-307: Standings Update Handling
- **Priority**: P0 (Must Have)
- **Description**: MUST handle `LEAGUE_STANDINGS_UPDATE` messages
- **Acceptance**: Updates internal standings view

#### FR-308: Strategy Implementation
- **Priority**: P1 (Should Have)
- **Description**: SHOULD implement strategy for choosing parity
- **Acceptance**: Non-trivial strategy, documented approach

#### FR-309: Opponent Modeling
- **Priority**: P2 (Nice to Have)
- **Description**: MAY implement opponent modeling for improved strategy
- **Acceptance**: Tracks opponent history, adjusts strategy

### 5.4 Protocol Requirements (FR-400 Series)

#### FR-401: Base Message Structure
- **Priority**: P0 (Must Have)
- **Description**: ALL messages MUST include required base fields
- **Fields**: protocol, message_type, league_id, round_id, match_id, conversation_id, sender, timestamp
- **Acceptance**: Schema validation passes

#### FR-402: Protocol Version
- **Priority**: P0 (Must Have)
- **Description**: Protocol MUST be "league.v2" (or "league.v1" per spec header)
- **Acceptance**: Version matches expected value

#### FR-403: Timestamp Format
- **Priority**: P0 (Must Have)
- **Description**: ALL timestamps MUST be ISO-8601 UTC format with 'Z' suffix
- **Acceptance**: Format: "2025-01-15T10:30:00Z" or "2025-01-15T10:30:00.000Z"

#### FR-404: UUID Format
- **Priority**: P0 (Must Have)
- **Description**: league_id and conversation_id MUST be RFC 4122 compliant UUIDs
- **Acceptance**: Valid UUID format validation

#### FR-405: Message Type Enumeration
- **Priority**: P0 (Must Have)
- **Description**: message_type MUST be one of 18 defined types
- **Types**: REFEREE_REGISTER_REQUEST, REFEREE_REGISTER_RESPONSE, LEAGUE_REGISTER_REQUEST, LEAGUE_REGISTER_RESPONSE, ROUND_ANNOUNCEMENT, ROUND_COMPLETED, LEAGUE_COMPLETED, GAME_INVITATION, GAME_JOIN_ACK, CHOOSE_PARITY_CALL, CHOOSE_PARITY_RESPONSE, GAME_OVER, MATCH_RESULT_REPORT, LEAGUE_STANDINGS_UPDATE, LEAGUE_ERROR, GAME_ERROR, LEAGUE_QUERY, LEAGUE_QUERY_RESPONSE
- **Acceptance**: All message types validated

#### FR-406: Authentication Tokens
- **Priority**: P1 (Should Have)
- **Description**: Auth tokens SHOULD be included after registration
- **Acceptance**: Tokens validated for protected operations

### 5.5 Data Layer Requirements (FR-500 Series)

#### FR-501: Configuration Layer
- **Priority**: P0 (Must Have)
- **Description**: MUST implement configuration loading from SHARED/config/
- **Files**: system.json, agents_config.json, league config, games_registry.json
- **Acceptance**: All config files loaded and validated

#### FR-502: Runtime Data Layer
- **Priority**: P0 (Must Have)
- **Description**: MUST persist runtime data to SHARED/data/
- **Files**: standings.json, rounds.json, match files, player history
- **Acceptance**: Data persisted correctly, survives restart

#### FR-503: Logging Layer
- **Priority**: P0 (Must Have)
- **Description**: MUST log to SHARED/logs/ in JSONLines format
- **Files**: league logs, agent logs, system logs
- **Acceptance**: All significant events logged with proper schema

#### FR-504: SDK Implementation
- **Priority**: P0 (Must Have)
- **Description**: MUST implement league_sdk with ConfigLoader, Repositories, Logger
- **Acceptance**: SDK usable by all agents

### 5.6 Client Architecture Requirements (FR-600 Series)

Each agent acts as a **client**, initiating requests to servers as needed. The following mandatory modules MUST be implemented.

#### FR-601: Client Layer Architecture
- **Priority**: P0 (Must Have)
- **Description**: Client MUST implement the 5-layer architecture
- **Layers**:
  | Layer | Responsibility |
  |-------|---------------|
  | Language Model (LLM) | Makes decisions and initiates actions |
  | Client Interface | The API layer the model interacts with |
  | Core System | Manages sessions and tool registration |
  | Message Processing | Converts internal messages to and from JSON |
  | Communication Layer | Translates messages to HTTP or STDIO |
- **Acceptance**: All 5 layers clearly separated in implementation

#### FR-602: Session Manager
- **Priority**: P0 (Must Have)
- **Description**: MUST implement Session Manager module
- **Responsibilities**:
  - Manage the lifecycle of connections
  - Perform handshake to verify successful connection
  - Manage heartbeats (periodic health checks)
  - Implement retry logic for automatic reconnection
- **Acceptance**: Session lifecycle fully managed, reconnection works

#### FR-603: Tool Registry
- **Priority**: P0 (Must Have)
- **Description**: MUST implement Tool Registry module
- **Responsibilities**:
  - Maintain a list of available tools from all servers
  - Centralize tool metadata for LLM usage
  - Handle tool name collisions between different servers
- **Acceptance**: Tools discoverable, metadata accessible, collisions handled

#### FR-604: Message Queue
- **Priority**: P0 (Must Have)
- **Description**: MUST implement Message Queue module
- **Responsibilities**:
  - Manage queues for incoming and outgoing messages
  - Handle message prioritization
  - Prevent overload and message flooding
- **Acceptance**: Messages queued properly, prioritization works, no flooding

#### FR-605: Error Type Handling
- **Priority**: P0 (Must Have)
- **Description**: MUST handle all three error types appropriately
- **Error Types**:
  | Error Type | Description | Retry Strategy |
  |------------|-------------|----------------|
  | Transient errors | Temporary failures (network issues, high load) | Retry appropriate |
  | Permanent errors | Non-recoverable failures (missing file, auth failure) | No retry |
  | Timeout errors | Request exceeds allowed time | May increase timeout |
- **Acceptance**: Each error type handled with appropriate strategy

#### FR-606: Exponential Backoff
- **Priority**: P0 (Must Have)
- **Description**: MUST implement exponential backoff with jitter for retries
- **Parameters**:
  - Base delay: 2 seconds
  - Maximum delay: 60 seconds
  - Jitter: up to 10% random variation
- **Formula**: `delay = min(base_delay * (2 ** attempt), max_delay) + jitter`
- **Acceptance**: Retry delays follow exponential pattern with jitter

### 5.7 Agent Architecture Requirements (FR-700 Series)

Each agent MUST implement the following component architecture.

#### FR-701: Agent Component Structure
- **Priority**: P0 (Must Have)
- **Description**: Agent MUST implement 4-component architecture
- **Components**:
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
- **Acceptance**: All 4 components clearly separated (5 points in grading)

#### FR-702: Sensors Implementation
- **Priority**: P0 (Must Have)
- **Description**: MUST implement Sensors component
- **Capabilities**:
  - Receive and parse incoming messages
  - Extract current game state from messages
  - Observe environment state
- **Interface**:
  - `receive_message(message: dict) -> ParsedMessage`
  - `extract_game_state(message: dict) -> GameState`
- **Acceptance**: Messages parsed correctly, game state extracted

#### FR-703: Decision Model Implementation
- **Priority**: P0 (Must Have)
- **Description**: MUST implement Decision Model component
- **Capabilities**:
  - Strategic decision making with pluggable strategy
  - Move selection based on game state
  - Opponent modeling and learning
- **Interface**:
  - `choose_move(game_state: GameState) -> Move`
  - `update_opponent_model(opponent_move: Move)`
- **Strategy Options**:
  - Random selection
  - Frequency analysis
  - Pattern recognition
  - Markov models
  - Reinforcement learning
- **Acceptance**: Strategy implemented, opponent learning functional

#### FR-704: Actuators Implementation
- **Priority**: P0 (Must Have)
- **Description**: MUST implement Actuators component
- **Capabilities**:
  - Execute actions via MCP protocol
  - Format moves into protocol messages
  - Send messages to other agents
- **Interface**:
  - `send_message(message: dict) -> bool`
  - `format_move(move: Move) -> dict`
- **Acceptance**: Messages sent correctly, moves formatted per protocol

#### FR-705: MCP Server Implementation
- **Priority**: P0 (Must Have)
- **Description**: MUST implement MCP Server component
- **Capabilities**:
  - Protocol handling for league.v2 messages
  - JSON schema validation for all incoming messages
  - Route messages to appropriate handlers
- **Required Validations**:
  - JSON structure validation
  - Protocol version match
  - Message type recognition
  - Required field presence
- **Acceptance**: All messages validated, routing correct

#### FR-706: Agent State Machine
- **Priority**: P0 (Must Have)
- **Description**: Agent MUST follow defined lifecycle states
- **States**:
  | State | Description |
  |-------|-------------|
  | `INIT` | Agent exists but has not registered |
  | `REGISTERED` | Successfully registered, received auth_token |
  | `ACTIVE` | Operational, participating in matches |
  | `SUSPENDED` | Temporarily inactive |
  | `SHUTDOWN` | Completed activity, no longer operational |
- **Transitions**:
  | From State | Trigger | To State |
  |------------|---------|----------|
  | INIT | register | REGISTERED |
  | REGISTERED | league_start | ACTIVE |
  | ACTIVE | league_end | SHUTDOWN |
  | ACTIVE | timeout/recover | SUSPENDED |
  | SUSPENDED | max_fail | SHUTDOWN |
  | Any | error | SHUTDOWN |
- **Acceptance**: All states reachable, transitions correct

#### FR-707: Required Agent Capabilities
- **Priority**: P0 (Must Have)
- **Description**: Agent MUST support these capabilities
- **Must Implement**:
  - ✅ JSON schema validation for all messages
  - ✅ MCP endpoint listening
  - ✅ Timeout handling (30 seconds per move)
  - ✅ State management (game history, opponent modeling)
  - ✅ Error handling and recovery
  - ✅ Logging all interactions
- **Must Support**:
  - ✅ Concurrent game handling (if referee allows)
  - ✅ Graceful disconnection handling
  - ✅ Message replay/recovery
- **Acceptance**: All capabilities demonstrable

---

## 6. Non-Functional Requirements

### 6.1 Performance (NFR-100 Series)

#### NFR-101: Response Time
- **Requirement**: All API responses within timeout limits
- **Target**: Registration <10s, Join <5s, Move <30s
- **Measurement**: Response time logging

#### NFR-102: Throughput
- **Requirement**: Support concurrent matches
- **Target**: 2 parallel matches per round
- **Measurement**: Match completion metrics

#### NFR-103: Resource Usage
- **Requirement**: Reasonable memory and CPU usage
- **Target**: <512MB per agent, <25% CPU per agent
- **Measurement**: Resource monitoring

### 6.2 Reliability (NFR-200 Series)

#### NFR-201: Error Handling
- **Requirement**: Graceful error handling without crashes
- **Target**: Zero crashes in 50+ consecutive games
- **Measurement**: Error logs, crash reports

#### NFR-202: Recovery
- **Requirement**: Support credential recovery after restart
- **Target**: Agents can recover session state
- **Measurement**: Recovery success rate

#### NFR-203: Message Delivery
- **Requirement**: Reliable message delivery
- **Target**: 100% delivery rate
- **Measurement**: Message acknowledgment tracking

### 6.3 Maintainability (NFR-300 Series)

#### NFR-301: Code Quality
- **Requirement**: Clean, documented, tested code
- **Target**: Pylint score ≥8.5, type hints 100%
- **Measurement**: Linter reports

#### NFR-302: File Size
- **Requirement**: Small, focused files
- **Target**: All files <150 lines
- **Measurement**: Line count analysis

#### NFR-303: Documentation
- **Requirement**: Comprehensive documentation
- **Target**: 100% public API documented
- **Measurement**: Documentation coverage

### 6.4 Extensibility (NFR-400 Series)

#### NFR-401: Game Agnostic
- **Requirement**: League/referee layers independent of game rules
- **Target**: Replace game without changing league code
- **Measurement**: Interface compliance

#### NFR-402: Transport Independence
- **Requirement**: Support multiple transports
- **Target**: HTTP now, STDIO/WebSocket future
- **Measurement**: Transport abstraction layer

#### NFR-403: Pluggable Strategies
- **Requirement**: Swappable player strategies
- **Target**: Strategy interface with multiple implementations
- **Measurement**: Strategy plug-in mechanism

### 6.5 Security (NFR-500 Series)

#### NFR-501: No Hardcoded Secrets
- **Requirement**: No API keys or secrets in code
- **Target**: All secrets in environment variables
- **Measurement**: Code scanning

#### NFR-502: Input Validation
- **Requirement**: Validate all inputs
- **Target**: All messages schema-validated
- **Measurement**: Validation failure rate

---

## 7. Grading Criteria

### 7.1 Overview

**Total Points Possible**: 120 (100 baseline + 20 bonus)

### 7.2 Protocol Compliance (40 Points)

| Level | Points | Criteria |
|-------|--------|----------|
| Perfect compliance | 40 | 100% valid JSON schemas, all fields correct |
| Minor violations | 30 | <5% messages have optional field issues |
| Major violations | 10 | Missing required fields, type errors |
| Disqualified | 0 | Any critical protocol violation |

**Testing Requirements**:
- Schema validator runs on all messages
- Message type coverage (all 18 types)
- Field validation (types, required/optional)

### 7.3 Competition Performance (30 Points)

Based on class ranking:

| Ranking | Points |
|---------|--------|
| Top 20% | 30 |
| Top 40% | 25 |
| Top 60% | 20 |
| Top 80% | 15 |
| Bottom 20% | 10 |

### 7.4 Agent Implementation Quality (20 Points)

| Category | Points | Criteria |
|----------|--------|----------|
| Code quality | 10 | Clean, documented, tested |
| Architecture | 5 | Sensors, decision model, actuators clearly separated |
| Error handling | 5 | Graceful handling of all edge cases |

### 7.5 Documentation (10 Points)

| Category | Points | Criteria |
|----------|--------|----------|
| Strategy explanation | 5 | 500+ words explaining approach |
| Test results | 3 | Documented test outcomes |
| Architecture documentation | 2 | System design documented |

### 7.6 Bonus Points (Up to 20)

| Category | Points | Criteria |
|----------|--------|----------|
| Protocol compliance bonus | +10 | Zero violations in competition |
| Documentation excellence | +5 | Exceptional documentation |
| Innovation bonus | +5 | Novel strategy with strong performance |

### 7.7 Critical Requirements (Disqualification if Missing)

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

---

## 8. Acceptance Criteria

### 8.1 P0: Must Have (Critical for Launch)

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-001 | League Manager starts on port 8000 | Test server startup |
| AC-002 | Referees start on ports 8001-8002 | Test server startup |
| AC-003 | Players start on ports 8101-8104 | Test server startup |
| AC-004 | All agents expose /mcp endpoint | HTTP POST test |
| AC-005 | Registration flow completes successfully | Integration test |
| AC-006 | Round-robin schedule generated correctly | Unit test |
| AC-007 | Game state machine transitions correctly | State test |
| AC-008 | Parity choices validated ("even"/"odd" only) | Validation test |
| AC-009 | Winner determined correctly | Game logic test |
| AC-010 | Standings calculated correctly | Calculation test |
| AC-011 | All message types conform to schema | Schema validation |
| AC-012 | Timestamps in UTC format | Format validation |
| AC-013 | Timeout handling works (5s join, 30s move) | Timeout test |
| AC-014 | Full league completes without errors | End-to-end test |

### 8.2 P1: Should Have (Important for Quality)

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-101 | Test coverage ≥70% | Coverage report |
| AC-102 | All 10+ edge cases handled | Edge case tests |
| AC-103 | JSONLines logging implemented | Log inspection |
| AC-104 | Configuration loaded from files | Config test |
| AC-105 | Player history persisted | File inspection |
| AC-106 | Strategy documentation provided | Document review |
| AC-107 | Error codes properly used | Error test |

### 8.3 P2: Nice to Have (Enhancements)

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-201 | Opponent modeling implemented | Strategy test |
| AC-202 | Win rate >60% vs random | Competition test |
| AC-203 | Multiple strategy implementations | Code inspection |
| AC-204 | Recovery from restart works | Recovery test |
| AC-205 | Concurrent request handling | Concurrency test |

---

## 9. Out-of-Scope

### 9.1 Explicitly Excluded

| Item | Reason |
|------|--------|
| Web UI / Dashboard | Console logging sufficient for assignment |
| Database Integration | JSON files for persistence |
| Multi-node Deployment | Single machine localhost |
| LLM Integration | Placeholder for future (modular design) |
| Real-time Analytics | Post-game analysis sufficient |
| User Authentication | Internal system only |
| Load Balancing | Single league manager |
| Rate Limiting | Trusted internal agents |

### 9.2 Future Considerations

| Item | Timeline |
|------|----------|
| Class League Infrastructure | After December 20, 2024 |
| Additional Game Types | Future assignments |
| Distributed Deployment | Production version |
| LLM-powered Strategies | Phase 2 |

---

## 10. Dependencies

### 10.1 External Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | ≥3.8 | Runtime environment |
| FastAPI | Latest | HTTP server framework |
| uvicorn | Latest | ASGI server |
| httpx | Latest | HTTP client |
| pydantic | Latest | Data validation |

### 10.2 Internal Dependencies

| Component | Depends On |
|-----------|------------|
| League Manager | league_sdk, config files |
| Referees | league_sdk, League Manager |
| Players | league_sdk, League Manager, Referees |
| Tests | All components |

### 10.3 Service Dependencies

| Service | Requirement |
|---------|-------------|
| Localhost Network | Ports 8000-8104 available |
| File System | Read/write to SHARED/ directory |

---

## 11. Constraints

### 11.1 Technical Constraints

| Constraint | Description |
|------------|-------------|
| TC-001 | Single machine execution (localhost) |
| TC-002 | HTTP transport only (STDIO future) |
| TC-003 | JSON file persistence (no database) |
| TC-004 | Python implementation required |
| TC-005 | Port assignments fixed (8000, 8001-8002, 8101-8104) |
| TC-006 | Protocol version fixed (league.v2) |

### 11.2 Academic Constraints

| Constraint | Description |
|------------|-------------|
| AC-001 | Submission deadline: January 8, 2025 at 23:59 |
| AC-002 | Individual submission required |
| AC-003 | Strategy sharing prohibited (general discussion allowed) |
| AC-004 | Must participate in class league after December 20 |

### 11.3 Design Constraints

| Constraint | Description |
|------------|-------------|
| DC-001 | 3-folder structure required (SHARED, agents, doc) |
| DC-002 | Game-agnostic league/referee layers |
| DC-003 | Files <150 lines |
| DC-004 | Protocol compliance is zero-tolerance |

### 11.4 Operational Constraints

| Constraint | Description |
|------------|-------------|
| OC-001 | Startup order: League Manager → Referees → Players |
| OC-002 | All agents must register before league starts |
| OC-003 | Timeouts strictly enforced (5s join, 30s move) |

---

## 12. Assumptions

### 12.1 Technical Assumptions

| ID | Assumption | Status |
|----|------------|--------|
| TA-001 | Python 3.8+ available on all systems | ✅ Validated |
| TA-002 | Required ports (8000-8104) available | ⚠️ Verify |
| TA-003 | Localhost network reliable | ✅ Validated |
| TA-004 | Sufficient disk space for logs/data | ⚠️ Monitor |
| TA-005 | No firewall blocking localhost | ⚠️ Verify |

### 12.2 Process Assumptions

| ID | Assumption | Status |
|----|------------|--------|
| PA-001 | Students have Python experience | ✅ Validated |
| PA-002 | Protocol specification is complete | ✅ Validated |
| PA-003 | Class league infrastructure exists | 🔄 In Progress |
| PA-004 | Grading criteria are final | ✅ Validated |

### 12.3 Business Assumptions

| ID | Assumption | Status |
|----|------------|--------|
| BA-001 | Assignment worth significant grade portion | ✅ Validated |
| BA-002 | Competition ranking affects grade | ✅ Validated |
| BA-003 | Protocol compliance is mandatory | ✅ Validated |

---

## 13. Risks & Mitigations

### 13.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Protocol ambiguity | Medium | High | Clarification notes in PRD |
| Port conflicts | Low | Medium | Document port requirements |
| Message loss | Low | High | Retry logic with exponential backoff |
| Race conditions | Medium | Medium | Proper state management |
| Timeout edge cases | Medium | Medium | Comprehensive timeout testing |

### 13.2 Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | Medium | Medium | Strict adherence to requirements |
| Integration issues | Medium | High | Early integration testing |
| Late bug discovery | Medium | High | Continuous testing |

### 13.3 Quality Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Low test coverage | Medium | Medium | Coverage targets in milestones |
| Documentation gaps | Low | Medium | Documentation checklist |
| Code quality issues | Low | Medium | Linting and code review |

---

## 14. Timeline & Milestones

### 14.1 Development Timeline

| Phase | Duration | Dates |
|-------|----------|-------|
| Phase 1: SDK & Infrastructure | 2 days | Dec 19-20 |
| Phase 2: League Manager | 1 day | Dec 21 |
| Phase 3: Referees | 1 day | Dec 22 |
| Phase 4: Players | 2 days | Dec 23-24 |
| Phase 5: Integration | 2 days | Dec 25-26 |
| Phase 6: Testing | 3 days | Dec 27-29 |
| Phase 7: Documentation | 2 days | Dec 30-31 |
| Phase 8: Polish & Submit | 7 days | Jan 1-8 |

### 14.2 Milestone Definitions

#### M1: SDK Complete (Dec 20)
- [ ] ConfigLoader implemented
- [ ] Repositories implemented
- [ ] Logger implemented
- [ ] Unit tests passing

#### M2: League Manager Complete (Dec 21)
- [ ] HTTP server running
- [ ] Registration handlers working
- [ ] Schedule generation working
- [ ] Standings calculation working

#### M3: Referees Complete (Dec 22)
- [ ] Game state machine working
- [ ] Move collection working
- [ ] Winner determination working
- [ ] Result reporting working

#### M4: Players Complete (Dec 24)
- [ ] Registration working
- [ ] Game response handlers working
- [ ] Basic strategy implemented
- [ ] Logging complete

#### M5: Integration Complete (Dec 26)
- [ ] Full league runs end-to-end
- [ ] All agents communicate correctly
- [ ] No integration errors

#### M6: Testing Complete (Dec 29)
- [ ] Coverage ≥70%
- [ ] All edge cases tested
- [ ] Protocol compliance verified

#### M7: Documentation Complete (Dec 31)
- [ ] All required documents created
- [ ] Architecture diagrams done
- [ ] API documented

#### M8: Submission Ready (Jan 8)
- [ ] Final testing complete
- [ ] All files committed
- [ ] Submission package prepared

### 14.3 Key Dates

| Date | Event |
|------|-------|
| December 18-20, 2024 | Private League Testing |
| December 20, 2024 | Class League Competition Begins |
| January 8, 2025 23:59 | Submission Deadline |

---

## 15. Glossary

| Term | Definition |
|------|------------|
| **Agent** | An autonomous software entity that participates in the league |
| **League Manager** | Top-level orchestrator that manages the tournament |
| **Referee** | Local orchestrator that manages individual matches |
| **Player** | Competing agent that makes game decisions |
| **MCP** | Model Context Protocol - communication standard |
| **Round-Robin** | Tournament format where each player faces every other player |
| **Parity** | Whether a number is even or odd |
| **Auth Token** | Authentication credential issued during registration |
| **JSONLines** | Log format with one JSON object per line |
| **Protocol Compliance** | Adherence to message schema and rules |
| **State Machine** | Formal model of game/agent states and transitions |
| **SDK** | Software Development Kit - shared library for agents |
| **Session Manager** | Module managing connection lifecycle, handshakes, heartbeats, retry logic |
| **Tool Registry** | Module maintaining list of available tools, centralizing metadata |
| **Message Queue** | Module managing incoming/outgoing message queues and prioritization |
| **Sensors** | Agent component for receiving messages and observing state |
| **Decision Model** | Agent component for strategic decision making and move selection |
| **Actuators** | Agent component for sending messages and executing moves |
| **Exponential Backoff** | Retry strategy with increasing delays between attempts |
| **Jitter** | Random variation added to delays to prevent thundering herd |

---

## Appendix A: Message Type Reference

| Message Type | Direction | Purpose |
|--------------|-----------|---------|
| REFEREE_REGISTER_REQUEST | Referee → LM | Register referee |
| REFEREE_REGISTER_RESPONSE | LM → Referee | Confirm registration |
| LEAGUE_REGISTER_REQUEST | Player → LM | Register player |
| LEAGUE_REGISTER_RESPONSE | LM → Player | Confirm registration |
| ROUND_ANNOUNCEMENT | LM → All | Announce round schedule |
| ROUND_COMPLETED | LM → All | Round finished |
| LEAGUE_COMPLETED | LM → All | League finished |
| GAME_INVITATION | Referee → Player | Invite to match |
| GAME_JOIN_ACK | Player → Referee | Accept invitation |
| CHOOSE_PARITY_CALL | Referee → Player | Request parity choice |
| CHOOSE_PARITY_RESPONSE | Player → Referee | Submit parity choice |
| GAME_OVER | Referee → Players | Game result |
| MATCH_RESULT_REPORT | Referee → LM | Report match result |
| LEAGUE_STANDINGS_UPDATE | LM → All | Current standings |
| LEAGUE_ERROR | LM → Agent | Error notification |
| GAME_ERROR | Referee → Player | Game error |
| LEAGUE_QUERY | Agent → LM | Query league info |
| LEAGUE_QUERY_RESPONSE | LM → Agent | Query response |

---

## Appendix B: Error Codes

| Code | Name | Description |
|------|------|-------------|
| E001 | TIMEOUT_ERROR | Response not received in time |
| E003 | MISSING_REQUIRED_FIELD | Required field missing |
| E004 | INVALID_PARITY_CHOICE | Invalid choice (not "even"/"odd") |
| E005 | PLAYER_NOT_REGISTERED | Player not in league |
| E009 | CONNECTION_ERROR | Network communication failure |
| E011 | AUTH_TOKEN_MISSING | Missing auth token |
| E012 | AUTH_TOKEN_INVALID | Invalid/expired auth token |
| E018 | PROTOCOL_VERSION_MISMATCH | Unsupported protocol version |
| E021 | INVALID_TIMESTAMP | Timestamp not UTC format |

---

## Appendix C: Round-Robin Schedule (4 Players)

| Round | Match 1 | Match 2 |
|-------|---------|---------|
| R1 | P01 vs P02 | P03 vs P04 |
| R2 | P03 vs P01 | P04 vs P02 |
| R3 | P04 vs P01 | P03 vs P02 |

---

## Appendix D: Required Edge Cases (Minimum 10)

| # | Edge Case | Scenario | Expected Handling |
|---|-----------|----------|-------------------|
| 1 | Empty response | Agent returns empty JSON | Return error E003, forfeit match |
| 2 | Malformed JSON | Invalid JSON structure | Return parsing error, retry once |
| 3 | Invalid parity choice | Choice not "even" or "odd" | Return E004, forfeit match |
| 4 | Timeout on join | No GAME_JOIN_ACK in 5s | Player forfeits match |
| 5 | Timeout on move | No parity choice in 30s | Player receives technical loss |
| 6 | Connection refused | Agent not listening on port | Return E009, retry with backoff |
| 7 | Missing required field | Protocol field missing | Return E003, reject message |
| 8 | Invalid timestamp | Timestamp not UTC format | Return E021, reject message |
| 9 | Protocol version mismatch | Unsupported protocol version | Return E018, reject registration |
| 10 | Invalid auth token | Token missing or expired | Return E011/E012, reject request |
| 11 | Duplicate registration | Agent registers twice | Return existing credentials |
| 12 | Out-of-order messages | Wrong state for message type | Return state error, log warning |

---

## Appendix E: Timeout Reference

| Operation | Timeout | Failure Consequence |
|-----------|---------|---------------------|
| Referee registration | 10s | Registration rejected |
| Player registration | 10s | Registration rejected |
| Game join acknowledgment | 5s | Player forfeits match |
| Parity choice | 30s | Technical loss (0 points) |
| Game over notification | 5s | Log warning, continue |
| Match result report | 10s | Retry, escalate if fail |
| League query | 10s | Return error, client retry |
| Default | 10s | Depends on context |

---

## Appendix F: Exponential Backoff Reference

```python
import random
import time

def exponential_backoff(attempt: int, base_delay: float = 2.0, max_delay: float = 60.0) -> float:
    """
    Calculate delay with exponential backoff and jitter.
    
    Parameters:
        attempt: Current retry attempt (0-indexed)
        base_delay: Initial delay in seconds (default: 2.0)
        max_delay: Maximum delay cap in seconds (default: 60.0)
    
    Returns:
        Delay in seconds with jitter applied
    
    Example delays:
        Attempt 0: ~2s
        Attempt 1: ~4s
        Attempt 2: ~8s
        Attempt 3: ~16s
        Attempt 4: ~32s
        Attempt 5+: ~60s (capped)
    """
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0, delay * 0.1)  # Add up to 10% jitter
    return delay + jitter
```

---

## Appendix G: Disqualification Conditions

**ZERO TOLERANCE violations that result in immediate disqualification:**

1. ❌ ANY message violates JSON schema
2. ❌ ANY required field is missing
3. ❌ ANY field has wrong type
4. ❌ Protocol version mismatch
5. ❌ Timeout >30 seconds on ANY move
6. ❌ Crash/exception during game
7. ❌ Invalid MCP endpoint
8. ❌ Unsupported game type claim

> ⚠️ **WARNING**: There is ZERO tolerance for protocol violations. Test thoroughly in private league!

---

**Document Approval**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | Assignment 7 Team | Dec 19, 2025 | ✅ |
| Technical Lead | Assignment 7 Team | Dec 19, 2025 | ✅ |
| QA Lead | Assignment 7 Team | Dec 19, 2025 | ✅ |

---

*End of Product Requirements Document*
