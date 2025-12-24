# Architecture Decision Records (ADRs) Index

## Overview

This directory contains Architecture Decision Records (ADRs) documenting significant architectural decisions made during the development of the AI Agent League Competition System.

## ADR Format

Each ADR follows the standard format:
- **Status**: Accepted, Proposed, Deprecated, or Superseded
- **Context**: The problem or situation that led to the decision
- **Decision**: What was decided
- **Alternatives Considered**: Other options evaluated
- **Consequences**: Pros, cons, and trade-offs
- **References**: Related documents or resources

---

## ADR Index

### Core Architecture

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](001-three-layer-architecture.md) | Three-Layer Architecture | Accepted | 2025-01 |
| [ADR-002](002-http-protocol-choice.md) | HTTP Protocol Choice | Accepted | 2025-01 |
| [ADR-003](003-json-message-format.md) | JSON Message Format | Accepted | 2025-01 |

### Infrastructure

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-004](004-file-based-persistence.md) | File-Based Persistence | Accepted | 2025-01 |
| [ADR-005](005-fastapi-framework.md) | FastAPI Framework | Accepted | 2025-01 |

### Analysis & Research

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-006](006-statistical-methods.md) | Statistical Methods | Accepted | 2025-01 |

---

## Categories

### Communication & Protocol
- ADR-002: HTTP Protocol Choice
- ADR-003: JSON Message Format

### System Design
- ADR-001: Three-Layer Architecture
- ADR-005: FastAPI Framework

### Data & Storage
- ADR-004: File-Based Persistence

### Analysis
- ADR-006: Statistical Methods

---

## Decision Timeline

```
2025-01 ─┬─ ADR-001: Three-Layer Architecture
         ├─ ADR-002: HTTP Protocol Choice
         ├─ ADR-003: JSON Message Format
         ├─ ADR-004: File-Based Persistence
         ├─ ADR-005: FastAPI Framework
         └─ ADR-006: Statistical Methods
```

---

## How to Add New ADRs

1. Create a new file: `NNN-title-with-dashes.md`
2. Use the template below
3. Update this README index

### Template

```markdown
# ADR-NNN: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Date
YYYY-MM-DD

## Context
[Describe the problem/situation]

## Decision
[What was decided]

## Alternatives Considered
[Other options evaluated]

## Consequences
### Positive
- [Benefit 1]

### Negative
- [Drawback 1]

## References
- [Related documents]
```

---

## References

- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) by Michael Nygard
- [ADR GitHub Organization](https://adr.github.io/)
