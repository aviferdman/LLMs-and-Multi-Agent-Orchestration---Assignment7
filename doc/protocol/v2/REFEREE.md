# Referee Protocol Contracts

**Protocol Version**: `league.v2`

The Referee is the local orchestrator responsible for:
- Running individual matches
- Managing game flow
- Collecting player choices
- Determining winners
- Reporting results to League Manager

---

## 1. Game Flow Contracts

### 1.1 Game Invitation

#### GAME_INVITATION

**Direction**: Referee → Player  
**Sent when**: Match is about to start  
**Expected response**: `GAME_JOIN_ACK` within 5 seconds

```json
{
  "protocol": "league.v2",
  "message_type": "GAME_INVITATION",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "REF01",
  "timestamp": "2025-12-20T10:00:00.000Z",
  "player_id": "P01",
  "opponent_id": "P02"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"GAME_INVITATION"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Match identifier |
| `conversation_id` | UUID | ✅ | Conversation thread ID |
| `sender` | string | ✅ | Referee ID |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp |
| `player_id` | string | ✅ | Target player ID |
| `opponent_id` | string | ✅ | Opponent's player ID |

---

### 1.2 Choose Parity Call

#### CHOOSE_PARITY_CALL

**Direction**: Referee → Player  
**Sent when**: Both players joined, game starts  
**Expected response**: `PARITY_CHOICE` within 30 seconds

```json
{
  "protocol": "league.v2",
  "message_type": "CHOOSE_PARITY_CALL",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "REF01",
  "timestamp": "2025-12-20T10:00:05.000Z",
  "player_id": "P01"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"CHOOSE_PARITY_CALL"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Match identifier |
| `conversation_id` | UUID | ✅ | Conversation thread ID |
| `sender` | string | ✅ | Referee ID |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp |
| `player_id` | string | ✅ | Target player ID |

---

### 1.3 Game Over

#### GAME_OVER

**Direction**: Referee → Both Players  
**Sent when**: Game finished, winner determined

```json
{
  "protocol": "league.v2",
  "message_type": "GAME_OVER",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "REF01",
  "timestamp": "2025-12-20T10:00:35.000Z",
  "winner": "P01",
  "drawn_number": 8,
  "player_a_choice": "EVEN",
  "player_b_choice": "ODD"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"GAME_OVER"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Match identifier |
| `conversation_id` | UUID | ✅ | Conversation thread ID |
| `sender` | string | ✅ | Referee ID |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp |
| `winner` | string | ✅ | Winner ID (`"P01"`, `"P02"`, or `"draw"`) |
| `drawn_number` | integer | ✅ | Random number drawn (1-10) |
| `player_a_choice` | string | ✅ | Player A's choice (`"even"` or `"odd"`) |
| `player_b_choice` | string | ✅ | Player B's choice (`"even"` or `"odd"`) |

**Winner values**:
| Value | Description |
|-------|-------------|
| `"P01"`, `"P02"`, etc. | Specific player won |
| `"DRAW"` | Both players made same choice |
| `"PLAYER_A"` | Generic: first player won |
| `"PLAYER_B"` | Generic: second player won |

---

## 2. Result Reporting Contracts

### 2.1 Match Result Report

#### MATCH_RESULT_REPORT

**Direction**: Referee → League Manager  
**Sent when**: Game completed, reporting result

```json
{
  "protocol": "league.v2",
  "message_type": "MATCH_RESULT_REPORT",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "REF01",
  "timestamp": "2025-12-20T10:00:36.000Z",
  "player_a": "P01",
  "player_b": "P02",
  "winner": "P01"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"MATCH_RESULT_REPORT"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Match identifier |
| `conversation_id` | UUID | ✅ | Conversation thread ID |
| `sender` | string | ✅ | Referee ID |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp |
| `player_a` | string | ✅ | First player ID |
| `player_b` | string | ✅ | Second player ID |
| `winner` | string | ✅ | Winner ID or `"draw"` |

---

## 3. Match Assignment Response

### RUN_MATCH_ACK

**Direction**: Referee → League Manager  
**Sent when**: Received RUN_MATCH, acknowledging assignment

```json
{
  "protocol": "league.v2",
  "message_type": "RUN_MATCH_ACK",
  "match_id": "R1M1",
  "status": "acknowledged"
}
```

---

## 4. Error Contracts

### GAME_ERROR

**Direction**: Referee → Player  
**Sent when**: Game-level error occurs

```json
{
  "protocol": "league.v2",
  "message_type": "GAME_ERROR",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "REF01",
  "timestamp": "2025-12-20T10:00:35.000Z",
  "error_code": "E001",
  "error_message": "Response timeout - player did not respond in time",
  "details": {
    "player_id": "P01",
    "expected_message": "PARITY_CHOICE",
    "timeout_seconds": 30
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"GAME_ERROR"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Match identifier |
| `conversation_id` | UUID | ✅ | Conversation thread ID |
| `sender` | string | ✅ | Referee ID |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp |
| `error_code` | string | ✅ | Error code |
| `error_message` | string | ✅ | Human-readable message |
| `details` | object | ❌ | Additional context |

**Common error codes for referee**:
| Code | Description |
|------|-------------|
| `E001` | Timeout - player didn't respond |
| `E004` | Invalid parity choice |
| `E009` | Connection error to player |

---

## 5. Timeout Handling

The referee must handle timeouts gracefully:

### Join Timeout (5 seconds)
- If player doesn't send `GAME_JOIN_ACK` within 5 seconds
- Result: Player forfeits, opponent wins

### Choice Timeout (30 seconds)
- If player doesn't send `PARITY_CHOICE` within 30 seconds
- Result: Player loses (technical loss)

### Both Players Timeout
- If both players timeout
- Result: Draw

---

## Python Implementation

```python
from SHARED.contracts.referee_contracts import (
    build_game_invitation,
    build_choose_parity_call,
    build_game_over,
    build_match_result_report,
    build_game_error,
)

from SHARED.contracts.league_manager_contracts import (
    build_run_match_ack,
)
```

---

## Game State Machine

```
WAITING_FOR_PLAYERS → COLLECTING_CHOICES → DRAWING_NUMBER → FINISHED
```

| State | Description | Next State |
|-------|-------------|------------|
| `WAITING_FOR_PLAYERS` | Sent invitations, waiting for joins | `COLLECTING_CHOICES` |
| `COLLECTING_CHOICES` | Both joined, waiting for choices | `DRAWING_NUMBER` |
| `DRAWING_NUMBER` | Drawing number, determining winner | `FINISHED` |
| `FINISHED` | Game complete, result reported | - |
