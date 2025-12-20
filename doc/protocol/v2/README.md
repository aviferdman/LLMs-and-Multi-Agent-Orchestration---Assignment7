# Protocol Contracts Documentation

**Protocol Version**: `league.v2`  
**Last Updated**: December 20, 2025

This folder contains the complete protocol contract specifications for all agents in the system.

## Directory Structure

```
protocol/
└── v2/
    ├── README.md              # This file
    ├── OVERVIEW.md            # Protocol overview and base message structure
    └── CONTRACTS.md           # All protocol contracts (unified reference)
```

## Quick Reference

| Document | Description |
|----------|-------------|
| [OVERVIEW.md](OVERVIEW.md) | Base message structure, field definitions, timestamps |
| [CONTRACTS.md](CONTRACTS.md) | Complete contract reference (League Manager, Referee, Player, Errors) |

## Message Flow Summary

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           REGISTRATION PHASE                             │
├─────────────────────────────────────────────────────────────────────────┤
│  Referee → LM:    REFEREE_REGISTER_REQUEST                              │
│  LM → Referee:    REFEREE_REGISTER_RESPONSE                             │
│  Player → LM:     LEAGUE_REGISTER_REQUEST                               │
│  LM → Player:     LEAGUE_REGISTER_RESPONSE                              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           ROUND LIFECYCLE                                │
├─────────────────────────────────────────────────────────────────────────┤
│  LM → All:        ROUND_ANNOUNCEMENT                                    │
│  LM → Referee:    RUN_MATCH                                             │
│  Referee → LM:    RUN_MATCH_ACK                                         │
│  LM → All:        ROUND_COMPLETED                                       │
│  LM → All:        LEAGUE_STANDINGS_UPDATE                               │
│  LM → All:        LEAGUE_COMPLETED                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           GAME FLOW                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Referee → Player: GAME_INVITATION                                      │
│  Player → Referee: GAME_JOIN_ACK                                        │
│  Referee → Player: CHOOSE_PARITY_CALL                                   │
│  Player → Referee: PARITY_CHOICE                                        │
│  Referee → Player: GAME_OVER                                            │
│  Referee → LM:     MATCH_RESULT_REPORT                                  │
│  LM → Referee:     MATCH_RESULT_ACK                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Implementation

The Python implementation of these contracts is in:
- `SHARED/contracts/base_contract.py`
- `SHARED/contracts/league_manager_contracts.py`
- `SHARED/contracts/referee_contracts.py`
- `SHARED/contracts/player_contracts.py`
- `SHARED/contracts/round_lifecycle_contracts.py`
