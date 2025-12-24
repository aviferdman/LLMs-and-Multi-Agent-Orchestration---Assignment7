# System Architecture

**Document Version**: 1.0  
**Last Updated**: 2025-12-20

---

## Overview

The AI Agent League Competition System implements a multi-agent architecture for running Even-Odd game tournaments. The system uses a three-layer design with clear separation of concerns.

---

## Architecture Diagram

```
                    ┌─────────────────────────────────────────┐
                    │           ORCHESTRATION LAYER           │
                    │  ┌─────────────────────────────────┐    │
                    │  │      League Manager (LM01)      │    │
                    │  │          Port: 8000             │    │
                    │  │  - Tournament orchestration     │    │
                    │  │  - Standings management         │    │
                    │  │  - Round scheduling             │    │
                    │  └─────────────────────────────────┘    │
                    └───────────────┬─────────────────────────┘
                                    │
                    ┌───────────────┴─────────────────────────┐
                    │           EXECUTION LAYER               │
                    │                                         │
                    │  ┌──────────────┐  ┌──────────────┐     │
                    │  │  Referee 01  │  │  Referee 02  │     │
                    │  │  Port: 8001  │  │  Port: 8002  │     │
                    │  │  - Game flow │  │  - Game flow │     │
                    │  │  - Rule      │  │  - Rule      │     │
                    │  │    enforce   │  │    enforce   │     │
                    │  └──────┬───────┘  └──────┬───────┘     │
                    └─────────┼─────────────────┼─────────────┘
                              │                 │
                    ┌─────────┴─────────────────┴─────────────┐
                    │           PARTICIPANT LAYER             │
                    │                                         │
                    │  ┌────────┐ ┌────────┐ ┌────────┐ ┌───┐ │
                    │  │ P01    │ │ P02    │ │ P03    │ │P04│ │
                    │  │ 8101   │ │ 8102   │ │ 8103   │ │8104│
                    │  │Random  │ │Freq    │ │Pattern │ │Rnd│ │
                    │  └────────┘ └────────┘ └────────┘ └───┘ │
                    └─────────────────────────────────────────┘
```

---

## Three-Layer Design

### Layer 1: Orchestration (League Manager)
- **Role**: Central coordinator for tournament management
- **Responsibilities**:
  - Accept referee and player registrations
  - Generate round-robin match schedules
  - Dispatch match assignments to referees
  - Collect and process match results
  - Maintain and broadcast standings
  - Signal round/league completion

### Layer 2: Execution (Referees)
- **Role**: Match execution and rule enforcement
- **Responsibilities**:
  - Invite players to matches
  - Draw random numbers (1-10)
  - Collect parity choices from players
  - Determine match winners
  - Report results to League Manager

### Layer 3: Participation (Players)
- **Role**: Game participation with strategy
- **Responsibilities**:
  - Register with League Manager
  - Respond to game invitations
  - Submit parity choices (even/odd)
  - Track opponent history for strategy

---

## Port Allocation

| Agent | Port | Endpoint | Description |
|-------|------|----------|-------------|
| League Manager | 8000 | /mcp | Central orchestrator |
| Referee 01 | 8001 | /mcp | Match referee |
| Referee 02 | 8002 | /mcp | Match referee |
| Player 01 | 8101 | /mcp | RandomStrategy |
| Player 02 | 8102 | /mcp | FrequencyStrategy |
| Player 03 | 8103 | /mcp | PatternStrategy |
| Player 04 | 8104 | /mcp | RandomStrategy |

---

## Communication Protocol

All agents communicate via HTTP POST requests to `/mcp` endpoints using JSON messages with these required fields:

```json
{
  "protocol": "league.v2",
  "message_type": "<MESSAGE_TYPE>",
  "timestamp": "2025-12-20T12:00:00.000Z",
  "conversation_id": "<UUID>",
  "sender": "<AGENT_ID>",
  "league_id": "<LEAGUE_ID>",
  "round_id": <ROUND_NUMBER>,
  "match_id": "<MATCH_ID>"
}
```

---

## Data Flow

### Registration Phase
1. Referees send `REFEREE_REGISTER_REQUEST` → LM responds with token
2. Players send `LEAGUE_REGISTER_REQUEST` → LM responds with token

### Match Execution Phase
1. LM sends `RUN_MATCH` → Referee
2. Referee sends `GAME_INVITATION` → Both Players
3. Players respond `GAME_JOIN_ACK` → Referee
4. Referee sends `CHOOSE_PARITY_CALL` → Both Players
5. Players respond `PARITY_CHOICE` → Referee
6. Referee sends `GAME_OVER` → Both Players
7. Referee sends `MATCH_RESULT_REPORT` → LM

### Round Completion Phase
1. LM broadcasts `ROUND_COMPLETED` to all
2. LM broadcasts `LEAGUE_STANDINGS_UPDATE` to all

---

## Key Design Decisions

1. **Stateless HTTP**: Each request is independent; state persisted in files
2. **Round-Robin Scheduling**: All players play each other exactly once
3. **Parallel Matches**: Multiple referees enable concurrent match execution
4. **Strategy Abstraction**: Players use pluggable strategy classes
5. **File-Based Persistence**: JSON files for standings and match history
---

## 🏛️ C4 Model Architecture

### C4 Level 1: System Context

**Purpose**: Shows how the League Competition System fits into the broader ecosystem.

```mermaid
C4Context
    title System Context - AI Agent League Competition System

    Person(user, "User", "Tournament operator who launches leagues, monitors matches, views standings")

    System(leagueSystem, "League Competition System", "Multi-agent system for Even-Odd game tournaments with real-time GUI")

    System_Ext(fileSystem, "File System", "Persistent storage for standings, logs, and match history")
    System_Ext(browser, "Web Browser", "Access to Streamlit GUI dashboard")

    Rel(user, leagueSystem, "Launches leagues, views results", "HTTP/WebSocket")
    Rel(leagueSystem, fileSystem, "Stores data", "File I/O")
    Rel(user, browser, "Interacts via", "HTTP")
    Rel(browser, leagueSystem, "API calls", "REST/WebSocket")
```

### C4 Level 2: Container Diagram

**Purpose**: Shows the high-level containers that make up the system.

```mermaid
C4Container
    title Container Diagram - League Competition System

    Person(user, "User", "Tournament operator")

    Container_Boundary(system, "League Competition System") {
        Container(gui, "Streamlit GUI", "Python/Streamlit", "Interactive dashboard for league management and visualization")
        
        Container(api, "REST API", "Python/FastAPI", "API endpoints and WebSocket for real-time updates")
        
        Container(leagueManager, "League Manager", "Python", "Tournament orchestration, scheduling, standings")
        
        Container(referees, "Referee Agents", "Python", "Match execution, rule enforcement, result calculation")
        
        Container(players, "Player Agents", "Python", "Game participation with pluggable strategies")
        
        Container(sdk, "League SDK", "Python Library", "Shared utilities: HTTP client, logging, validation")
        
        Container(storage, "Data Storage", "JSON Files", "Standings, match history, agent logs")
    }

    Rel(user, gui, "Uses", "HTTP")
    Rel(gui, api, "API calls", "REST/WebSocket")
    Rel(api, leagueManager, "Commands", "HTTP")
    Rel(leagueManager, referees, "Match dispatch", "HTTP")
    Rel(referees, players, "Game flow", "HTTP")
    Rel(leagueManager, storage, "Persist data", "File I/O")
    Rel(referees, storage, "Log matches", "File I/O")
    Rel_Back(sdk, leagueManager, "Uses")
    Rel_Back(sdk, referees, "Uses")
    Rel_Back(sdk, players, "Uses")
```

### C4 Level 3: Component Diagram (League Manager)

**Purpose**: Internal components of the League Manager container.

```mermaid
C4Component
    title Component Diagram - League Manager

    Container_Boundary(lm, "League Manager") {
        Component(httpHandler, "HTTP Handler", "Flask/HTTP", "Receives and routes incoming messages")
        
        Component(registration, "Registration Handler", "Python", "Handles referee and player registration")
        
        Component(scheduler, "Match Scheduler", "Python", "Generates round-robin match schedule")
        
        Component(dispatcher, "Match Dispatcher", "Python", "Assigns matches to available referees")
        
        Component(results, "Results Processor", "Python", "Processes match results, updates standings")
        
        Component(standings, "Standings Manager", "Python", "Calculates and broadcasts rankings")
        
        Component(persistence, "Persistence Layer", "Python", "Saves/loads state from JSON files")
    }

    Rel(httpHandler, registration, "Routes registration")
    Rel(httpHandler, results, "Routes results")
    Rel(registration, persistence, "Stores tokens")
    Rel(scheduler, dispatcher, "Provides schedule")
    Rel(dispatcher, httpHandler, "Sends match commands")
    Rel(results, standings, "Triggers update")
    Rel(standings, persistence, "Saves standings")
```

---

## 📊 UML Diagrams

### Sequence Diagram: Match Execution

```mermaid
sequenceDiagram
    participant LM as League Manager
    participant REF as Referee
    participant P1 as Player 1
    participant P2 as Player 2

    LM->>REF: RUN_MATCH (match_id, players)
    REF->>P1: GAME_INVITATION (match_id)
    REF->>P2: GAME_INVITATION (match_id)
    P1-->>REF: GAME_JOIN_ACK
    P2-->>REF: GAME_JOIN_ACK
    
    loop Each Round (Best of 5)
        REF->>REF: Draw random number (1-10)
        REF->>P1: CHOOSE_PARITY_CALL (number)
        REF->>P2: CHOOSE_PARITY_CALL (number)
        P1-->>REF: PARITY_CHOICE (even/odd)
        P2-->>REF: PARITY_CHOICE (even/odd)
        REF->>REF: Determine round winner
    end
    
    REF->>P1: GAME_OVER (result)
    REF->>P2: GAME_OVER (result)
    REF->>LM: MATCH_RESULT_REPORT (winner, scores)
```

### State Diagram: Match Lifecycle

```mermaid
stateDiagram-v2
    [*] --> SCHEDULED: Match created
    SCHEDULED --> INVITING: RUN_MATCH received
    INVITING --> WAITING_JOIN: Invitations sent
    WAITING_JOIN --> IN_PROGRESS: Both players joined
    WAITING_JOIN --> ABANDONED: Timeout/rejection
    IN_PROGRESS --> ROUND_N: Playing rounds
    ROUND_N --> IN_PROGRESS: More rounds needed
    ROUND_N --> COMPLETED: Winner determined
    IN_PROGRESS --> ABANDONED: Player disconnect
    COMPLETED --> REPORTED: Results sent to LM
    REPORTED --> [*]
    ABANDONED --> [*]
```

### Class Diagram: Core Components

```mermaid
classDiagram
    class LeagueManager {
        -players: Dict[str, PlayerInfo]
        -referees: Dict[str, RefereeInfo]
        -standings: Dict[str, int]
        +register_player(request)
        +register_referee(request)
        +start_round()
        +process_result(result)
        +get_standings()
    }
    
    class Referee {
        -referee_id: str
        -current_match: MatchState
        +handle_run_match(match)
        +invite_players()
        +collect_choices()
        +determine_winner()
        +report_result()
    }
    
    class Player {
        -player_id: str
        -strategy: Strategy
        -history: OpponentHistory
        +handle_invitation(invite)
        +make_choice(number)
        +update_history(opponent, choice)
    }
    
    class Strategy {
        <<interface>>
        +choose(number, history): str
    }
    
    class RandomStrategy {
        +choose(number, history): str
    }
    
    class FrequencyStrategy {
        +choose(number, history): str
    }
    
    class PatternStrategy {
        +choose(number, history): str
    }
    
    LeagueManager --> Referee: dispatches to
    Referee --> Player: communicates with
    Player --> Strategy: uses
    Strategy <|-- RandomStrategy
    Strategy <|-- FrequencyStrategy
    Strategy <|-- PatternStrategy
```

---

## 🔄 Deployment Architecture

### Local Development

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Machine                       │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Streamlit   │  │ FastAPI     │  │ Agent Processes     │ │
│  │ GUI         │  │ Server      │  │ ┌─────┐ ┌─────────┐ │ │
│  │ :8501       │  │ :8080       │  │ │ LM  │ │ REF 1-2 │ │ │
│  └─────────────┘  └─────────────┘  │ │:8000│ │:8001-02 │ │ │
│                                     │ └─────┘ └─────────┘ │ │
│                                     │ ┌─────────────────┐ │ │
│                                     │ │ Players 1-4     │ │ │
│                                     │ │ :8101-8104      │ │ │
│                                     │ └─────────────────┘ │ │
│                                     └─────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               Shared File System                     │   │
│  │  SHARED/data/   SHARED/logs/   SHARED/config/       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Production (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Ingress Controller                 │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        │                                    │
│  ┌────────────────┬────┴────────────┬────────────────┐    │
│  │                │                  │                │    │
│  │  ┌──────────┐  │  ┌──────────┐   │  ┌──────────┐  │    │
│  │  │ GUI Pod  │  │  │ API Pod  │   │  │ LM Pod   │  │    │
│  │  │ (x2)     │  │  │ (x2)     │   │  │ (x1)     │  │    │
│  │  └──────────┘  │  └──────────┘   │  └──────────┘  │    │
│  │                │                  │                │    │
│  │  ┌──────────┐  │  ┌──────────┐   │  ┌──────────┐  │    │
│  │  │ Referee  │  │  │ Player   │   │  │ Redis    │  │    │
│  │  │ Pods(x4) │  │  │ Pods(x8) │   │  │ Cluster  │  │    │
│  │  └──────────┘  │  └──────────┘   │  └──────────┘  │    │
│  └────────────────┴─────────────────┴────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Persistent Volume Claims (PVC)             │   │
│  │     standings/   logs/   config/   match-history/   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Related Documents

- [DESIGN_DOCUMENT.md](DESIGN_DOCUMENT.md) - Detailed design decisions
- [protocol_spec.md](protocol_spec.md) - Protocol specification
- [ADRs/](ADRs/) - Architectural Decision Records
- [BUILDING_BLOCKS.md](BUILDING_BLOCKS.md) - Component documentation