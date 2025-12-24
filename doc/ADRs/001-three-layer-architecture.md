# ADR 001: Three-Layer Architecture

**Status**: Accepted  
**Date**: 2025-12-20  
**Context**: League Competition System Design

## Context

We need to design a scalable, maintainable architecture for an AI agent league competition system where multiple players compete in matches orchestrated by referees, all managed by a central league manager.

## Decision

We adopt a **three-layer architecture** with clear separation of concerns:

### Layer 1: League Manager (Orchestration)
- **Responsibility**: Tournament orchestration, scheduling, standings management
- **Port**: 8000
- **Components**: 
  - Match scheduler
  - Round orchestration
  - Standings calculator
  - Agent registry

### Layer 2: Referee Agents (Match Management)
- **Responsibility**: Individual match execution, game rules enforcement
- **Ports**: 8001-8002 (multiple referees)
- **Components**:
  - Game rules engine
  - Match state machine
  - Player coordination

### Layer 3: Player Agents (Game Participants)
- **Responsibility**: Game strategy execution, move decisions
- **Ports**: 8101-8104 (4 players)
- **Components**:
  - Strategy implementation
  - Move decision logic
  - History tracking

## Rationale

### Advantages
1. **Separation of Concerns**: Each layer has distinct responsibilities
2. **Scalability**: Can add more referees/players without changing architecture
3. **Testability**: Each layer can be tested independently
4. **Maintainability**: Changes in one layer don't affect others
5. **Protocol Clarity**: Clear message flows between layers

### Communication Pattern
- HTTP/JSON protocol between all layers
- Asynchronous message passing
- RESTful endpoints for each agent

## Consequences

### Positive
- Clear boundaries enable parallel development
- Easy to add new game types (extend referee layer)
- Simple to implement different player strategies
- Network-based allows distributed deployment

### Negative
- Network latency between layers
- More complex than monolithic design
- Requires careful error handling for network failures
- Need for agent registration/discovery

## Alternatives Considered

1. **Monolithic Architecture**: Rejected - too tightly coupled
2. **Microservices with Message Queue**: Rejected - over-engineered for scope
3. **Peer-to-Peer**: Rejected - difficult to coordinate tournaments

## Related Decisions
- ADR 002: HTTP Protocol Choice
- ADR 003: JSON Message Format
