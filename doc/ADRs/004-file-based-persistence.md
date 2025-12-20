# ADR 004: File-Based Persistence

**Status**: Accepted  
**Date**: 2025-12-20  
**Context**: Data Storage Strategy

## Context

The league system needs to persist tournament data including standings, match results, and player histories. We need a simple, reliable storage mechanism that supports the assignment requirements without over-engineering.

## Decision

We use **file-based JSON storage** organized in a hierarchical directory structure:

```
SHARED/data/
├── leagues/
│   └── {league_id}/
│       └── standings.json
├── matches/
│   └── {league_id}/
│       └── {match_id}.json
└── players/
    └── {player_id}/
        └── history.json
```

## Data Storage Design

### 1. Standings Repository
**File**: `SHARED/data/leagues/{league_id}/standings.json`

```json
{
  "league_id": "league_2025_even_odd",
  "last_updated": "2025-12-20T14:30:00.000Z",
  "standings": [
    {
      "player_id": "P01",
      "wins": 2,
      "losses": 0,
      "draws": 1,
      "games_played": 3,
      "points": 7
    }
  ]
}
```

### 2. Match Repository
**File**: `SHARED/data/matches/{league_id}/{match_id}.json`

```json
{
  "match_id": "R1_M1_P01_P02",
  "round_number": 1,
  "player1_id": "P01",
  "player2_id": "P02",
  "referee_id": "REF01",
  "winner_id": "P01",
  "player1_score": 3,
  "player2_score": 2,
  "status": "completed",
  "timestamp": "2025-12-20T14:30:00.000Z"
}
```

### 3. Player History Repository
**File**: `SHARED/data/players/{player_id}/history.json`

```json
{
  "player_id": "P01",
  "matches": [
    {
      "match_id": "R1_M1_P01_P02",
      "opponent_id": "P02",
      "result": "win",
      "score": "3-2",
      "timestamp": "2025-12-20T14:30:00.000Z"
    }
  ]
}
```

## Rationale

### Why File-Based Storage?
1. **Simplicity**: No database server needed
2. **Human-Readable**: JSON files can be inspected directly
3. **Version Control**: Files can be committed to git
4. **Zero Setup**: Works out of the box
5. **Debugging**: Easy to examine and modify for testing
6. **Assignment Scope**: Appropriate for educational project

### Directory Organization
- **By Entity Type**: leagues/, matches/, players/
- **By ID**: Each entity gets its own file/directory
- **Hierarchical**: Matches grouped by league

## Operations

### Repository Classes
1. **StandingsRepository**: Load/save/update standings
2. **MatchRepository**: Save/load/list matches
3. **PlayerHistoryRepository**: Save/load/append player history

### Atomic Operations
- **Read**: Load entire JSON file
- **Write**: Write entire JSON file (atomic with temp file + rename)
- **Update**: Read → Modify → Write

## Consequences

### Positive
- **Zero Infrastructure**: No database server to manage
- **Simple Backup**: Copy entire data/ directory
- **Easy Reset**: Delete data/ to start fresh
- **Debugging**: Inspect files with any text editor
- **Portable**: Works on any OS with Python
- **Git-Friendly**: Can track changes to data

### Negative
- **Concurrency**: No built-in locking (handled at application level)
- **Performance**: File I/O slower than in-memory or database
- **Scalability**: Not suitable for large datasets
- **Atomicity**: Must implement atomic writes manually
- **Querying**: No SQL-like query capabilities

## Scalability Considerations

Current implementation handles:
- ✅ 4 players
- ✅ 2 referees
- ✅ 6 matches per league
- ✅ 3 rounds

For scaling beyond 100+ players or 1000+ matches, consider:
- SQLite for better query performance
- Redis for real-time data
- PostgreSQL for production deployment

## Error Handling

1. **Missing Files**: Return empty structure or None
2. **Corrupt JSON**: Log error and return default
3. **Permission Errors**: Fail fast with clear message
4. **Concurrent Writes**: Last write wins (acceptable for scope)

## Alternatives Considered

1. **SQLite**: Rejected - overkill for 6 matches, adds complexity
2. **Redis**: Rejected - requires external service
3. **PostgreSQL**: Rejected - too heavy for assignment
4. **In-Memory Only**: Rejected - data lost on restart
5. **CSV Files**: Rejected - harder to parse nested structures
6. **Pickle**: Rejected - not human-readable, Python-specific

## Related Decisions
- ADR 001: Three-Layer Architecture
- ADR 003: JSON Message Format

## Migration Path

If database needed later:
1. Keep Repository interface unchanged
2. Implement DatabaseRepository class
3. Provide migration script: JSON → DB
4. Update instantiation code only
