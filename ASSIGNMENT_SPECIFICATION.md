# Assignment 7 - AI Agent League Competition with MCP Protocol

**Course**: LLMs and Multi-Agent Orchestration  
**Assignment Type**: Competitive Multi-Agent System using Model Context Protocol  
**Version**: 2.0.0  
**Protocol**: league.v1 (Based on MCP Standards)   
**Last Updated**: December 14, 2025

---

## 📋 Table of Contents

1. [MCP Protocol Introduction](#mcp-protocol-introduction)
2. [Assignment Overview](#assignment-overview)
3. [MCP Client-Server Architecture](#mcp-client-server-architecture)
4. [System Architecture](#system-architecture)
5. [Three-Layer Architecture](#three-layer-architecture)
6. [Protocol Components](#protocol-components)
7. [Client Architecture](#client-architecture)
8. [Working with Multiple Servers](#working-with-multiple-servers)
9. [Information Security](#information-security)
10. [Protocol Specification](#protocol-specification)
11. [Message Types & Schemas](#message-types--schemas)
12. [Game Rules: Even-Odd](#game-rules-even-odd)
13. [Agent Implementation Requirements](#agent-implementation-requirements)
14. [Assignment Phases](#assignment-phases)
15. [Grading Criteria](#grading-criteria)
16. [Critical Requirements](#critical-requirements)

---

## 🌟 MCP Protocol Introduction

### Development Background

The Model Context Protocol (MCP) is a unified communication protocol developed by Anthropic to enable standardized communication between Language Model (LLM) agents and external services. This protocol represents a revolution in the AI ecosystem.

**Historical Development:**
- **First communication method** - Files
- **Internet protocol** - HTTP for standard data transfer  
- **Physical data transfer** - USB standard protocol
- **AI agent communication** - MCP protocol

### The Problem MCP Solves

**Before MCP**: Each agent required unique integration for each service:
- **Complex integrations**: O(n×m) complexity - For example, 5 agents × 5 services = 25 integrations
- **Maintenance difficulties**
- **Scalability issues**

**With MCP**: Complexity reduces to O(n+m) - For example, 5 agents + 5 services = only 10 connections
- **Unified communication standard**
- **Simplified architecture** 
- **Enhanced scalability**

---

## 🔄 MCP Client-Server Architecture

### Basic Definitions

**Client**:
- Initiates requests to server
- Contains the Language Model (LLM)
- Manages sessions, messages, tools, and resources
- Acts as the "brain" of the system

**Server**: 
- Responds to requests - passive behavior
- Provides Tools and Resources
- Acts as the "hands and feet" of the system
- Performs deterministic operations

**Important Note**: In MCP, the client is not truly a pure client and the server is not truly a pure server - both can send and receive requests.

### Connection Lifecycle

1. **Initialize Phase**: Connection establishment between client and server
2. **Operation Phase**: Client sends requests, server returns list of tools and capabilities  
3. **Close Phase**: Orderly closure and resource cleanup

---

## 🧩 Protocol Components

### 3.1 Tools

Tools are functions that enable the model to perform active operations or calculations.

**Tool Definition Structure**:
- **name**: Unique identifier for the tool
- **description**: Explains to the model what the tool does
- **input_schema**: Parameter definitions in JSON Schema format

**Example**: Calculator tool that accepts operands and operator, performs operation, and returns result.

### 3.2 Resources

Resources are information sources that the model can read but not modify (Read-Only).

**Examples**:
- Database content
- Internet pages
- PDF files  
- Images

### 3.3 Prompts

Prompts are prepared templates for guiding the model to perform specific tasks.

---

## 🏛️ Client Architecture

### Client Layers

1. **Language Model (LLM)**: Initiates operations and makes decisions
2. **Client Interface**: The API through which users interact with the model
3. **System Core**: Manages tool registration and sessions
4. **Message Processing**: Handles JSON message conversion
5. **Communication Layer**: Translates to STDIO and HTTP protocols

### Required Modules

#### 4.2.1 Session Manager
- Manages connection lifecycles
- Performs successful connection verification (Handshake)
- Handles periodic checks (Heartbeat)
- Manages automatic reconnection with Retry Logic

#### 4.2.2 Tool Registry  
- Maintains list of available tools from each server
- Centralizes information for LLM usage
- Handles name conflicts between different servers

#### 4.2.3 Message Queue
- Manages incoming and outgoing message queues
- Handles priorities
- Prevents overflow

### Error Handling

**Error Types**:
- **Transient**: Temporary errors worth retrying (load, network)
- **Permanent**: Fixed errors not worth retrying (permissions, missing file)
- **Timeout**: Time overruns - can increase wait time

**Exponential Backoff Strategy**:
Wait time between attempts grows exponentially:
- 1st attempt: Short wait
- 2nd attempt: Double wait  
- 3rd attempt: 4x wait
- And so on...

**Important**: Add Jitter (random noise) to prevent synchronized processes that trigger simultaneously.

---

## 🌐 Working with Multiple Servers

### Star Topology
The client centralizes communication with multiple servers:
- Presents unified tool list to LLM
- Manages name conflicts in namespaces
- Routes requests to appropriate server

### Load Balancing
**Distribution Strategies**:
- **Round Robin**: Equal circular distribution
- **Least Connections**: Route to least busy server
- **Weighted**: Priority to stronger servers

---

## 🔒 Information Security

### Common Threats
**Prompt Injection attacks via internet content**:
- Attackers insert malicious instructions into innocent internet pages
- LLM reads the content and executes the instructions
- Currently no complete solution to this problem

### Recommended Defenses
- Work within Sandbox environments or Docker containers
- Limit file access permissions
- Set damage boundaries in advance
- Complete logging of all operations

---

## 📖 Assignment Overview

### Purpose

Create a **competitive AI agent league** where autonomous agents compete in games following a standardized communication protocol. The system demonstrates:

- **Multi-agent orchestration** using MCP (Model Context Protocol)
- **Decoupled architecture** enabling extensibility
- **Protocol-driven communication** with JSON schemas
- **Parallel agent execution** with proper coordination
- **State management** across distributed systems

### Key Innovation

**Total Decoupling Between Layers**: The protocol enables agents to participate in any future league regardless of specific game rules. An agent built for this protocol can join new games without modification.

### Competition Format

- **4 agents** running in parallel
- **Round-robin tournament** (each agent plays every other agent)
- **Ranking system** based on wins/losses
- **Two-phase competition**:
  1. **Private League**: Local development and testing
  2. **Class League**: Competitive ranking for grades

---

## 🏗️ System Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                      LEAGUE LAYER                            │
│  - Player Registration                                       │
│  - Schedule Management                                       │
│  - Ranking Calculation                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐     ┌───────▼──────────┐
│  REFEREE LAYER   │ ... │  REFEREE LAYER   │
│  - Game Init     │     │  - Game Init     │
│  - Move Valid.   │     │  - Move Valid.   │
│  - Winner Annc.  │     │  - Winner Annc.  │
└───────┬──────────┘     └───────┬──────────┘
        │                         │
   ┌────┴────┐               ┌────┴────┐
   │         │               │         │
┌──▼──┐   ┌─▼───┐        ┌──▼──┐   ┌─▼───┐
│ P1  │   │ P2  │        │ P3  │   │ P4  │
│Agent│   │Agent│        │Agent│   │Agent│
└─────┘   └─────┘        └─────┘   └─────┘
```

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

## 📡 Protocol Specification

### Protocol Version

```
Protocol: league.v1
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

### State Definition Principle

**At every moment, the state of the system is well-defined**:

- Every entity (league, round, game, player) has a unique ID
- Every message includes full context (IDs, round, match)
- State transitions are explicit and tracked
- No ambiguity about current state

---

## 📬 Message Types & Schemas

### 1. Player Registration

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
    "game_types": ["even_odd"],
    "contact_endpoint": "mcp://player-alpha"
  }
}
```

**Required Fields**:
- `player_meta.display_name`: Human-readable agent name
- `player_meta.version`: Semantic version (MAJOR.MINOR.PATCH)
- `player_meta.game_types`: Array of supported games (MUST include "even_odd")
- `player_meta.contact_endpoint`: MCP endpoint for communication

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
  "player_id": "player_001",
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
- "Invalid MCP endpoint"
- "Duplicate display name"
- "Registration closed"

---

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
    "current_player": "player_001",
    "rules": {
      "single_round": true,
      "timeout_per_move": 30
    }
  }
}
```

---

### 5. Play Execution

#### PLAY_REQUEST

**Direction**: Referee → Player (whose turn it is)

```json
{
  "protocol": "league.v1",
  "message_type": "PLAY_REQUEST",
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
      "previous_plays": []
    }
  }
}
```

#### PLAY_RESPONSE

**Direction**: Player → Referee

```json
{
  "protocol": "league.v1",
  "message_type": "PLAY_RESPONSE",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "player_001",
  "timestamp": "2025-12-13T22:05:05.000Z",
  "play": {
    "action": "choose",
    "value": "even",
    "reasoning": "Strategic choice based on opponent history"
  }
}
```

**Play Structure for Even-Odd**:
- `action`: Always "choose"
- `value`: "even" or "odd"
- `reasoning`: Optional string explaining decision

---

### 6. Play Validation

#### PLAY_VALIDATION

**Direction**: Referee → Both Players

```json
{
  "protocol": "league.v1",
  "message_type": "PLAY_VALIDATION",
  "league_id": "550e8400-e29b-41d4-a716-446655440000",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "referee",
  "timestamp": "2025-12-13T22:05:06.000Z",
  "validation": {
    "player_id": "player_001",
    "play": {"action": "choose", "value": "even"},
    "status": "VALID",
    "error": null
  }
}
```

**Status Values**:
- `VALID`: Play accepted
- `INVALID`: Play rejected

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
    "game_summary": {
      "player_001_choice": "even",
      "player_002_choice": "odd",
      "random_number": 42,
      "number_parity": "even",
      "winner_reason": "player_001 correct, player_002 wrong"
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

A simultaneous-move game where two players compete over multiple rounds, as specified in PDF section 7.2.

### Rules (Per PDF Section 7.2)

1. **Setup**:
   - Single round per game
   - Both players simultaneously choose "even" or "odd"

2. **Game Execution**:
   - Referee requests moves from both players
   - Both players submit their choice
   - **Referee generates a random number** (judge generates number per PDF)
   - Winner determined by parity match

3. **Winning Condition (Exact PDF Rules)**:
   - **If both players are correct OR both are wrong** → **TIE**
   - **If one player is correct and one is wrong** → **The correct player wins**
   - Example: Number is 7 (odd), Player1 chose "odd", Player2 chose "even" → Player1 wins

4. **Timeout Rules (Per PDF Section 7.2)**:
   - **30 seconds to respond**
   - **3 attempts before disqualification**

5. **Game Result**:
   - Winner determined after single round
   - Result can be WIN, LOSS, or TIE

### Example Games (Following PDF Rules)

```
Game 1 (Player 1 vs Player 2):
  Player 1 chooses: "even"
  Player 2 chooses: "odd"  
  Random number: 42 (even)
  Result: Player 1 correct, Player 2 wrong → Player 1 WINS THE GAME

Game 2 (Player 1 vs Player 3):
  Player 1 chooses: "even"
  Player 3 chooses: "even"
  Random number: 17 (odd)
  Result: Both players wrong → GAME ENDS IN TIE

Game 3 (Player 2 vs Player 4):
  Player 2 chooses: "odd"
  Player 4 chooses: "even"
  Random number: 33 (odd)
  Result: Player 2 correct, Player 4 wrong → Player 2 WINS THE GAME
```

### Game-Specific Message Fields

#### In PLAY_RESPONSE:
```json
{
  "play": {
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
        elif message_type == "PLAY_REQUEST":
            return await self.handle_play_request(message)
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
        "PLAY_REQUEST",
        "PLAY_RESPONSE",
        "PLAY_VALIDATION",
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

5. SINGLE GAME
   Referee → Player1: MOVE_REQUEST
   Player1 → Referee: MOVE_RESPONSE (value="even")
   Referee → Both: MOVE_VALIDATION
   
   Referee → Player2: MOVE_REQUEST
   Player2 → Referee: MOVE_RESPONSE (value="odd")
   Referee → Both: MOVE_VALIDATION
   
   Referee generates random number
   Referee determines game winner immediately

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
