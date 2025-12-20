# Player Protocol Contracts

**Protocol Version**: `league.v2`

Players are autonomous agents that:
- Register with the League Manager
- Respond to game invitations
- Make parity choices during games
- Receive game results and standings

---

## 1. Registration Contracts

### 1.1 Registration Request

#### LEAGUE_REGISTER_REQUEST

**Direction**: Player → League Manager  
**Endpoint**: `POST http://localhost:8000/mcp`  
**Sent when**: Player starts up

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_REGISTER_REQUEST",
  "player_id": "P01",
  "endpoint": "http://localhost:8101/mcp"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"LEAGUE_REGISTER_REQUEST"` |
| `player_id` | string | ✅ | Player identifier (e.g., "P01") |
| `endpoint` | string | ✅ | Player's HTTP endpoint |

**Expected response**: `LEAGUE_REGISTER_RESPONSE`

---

## 2. Game Response Contracts

### 2.1 Game Join Acknowledgment

#### GAME_JOIN_ACK

**Direction**: Player → Referee  
**Sent when**: Received `GAME_INVITATION`  
**Timeout**: Must respond within 5 seconds

```json
{
  "protocol": "league.v2",
  "message_type": "GAME_JOIN_ACK",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "P01",
  "timestamp": "2025-12-20T10:00:02.000Z"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"GAME_JOIN_ACK"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Match identifier |
| `conversation_id` | UUID | ✅ | **Must match invitation's conversation_id** |
| `sender` | string | ✅ | Player ID |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp |

**Important**: The `conversation_id` must be copied from the `GAME_INVITATION` message.

---

### 2.2 Parity Choice

#### PARITY_CHOICE

**Direction**: Player → Referee  
**Sent when**: Received `CHOOSE_PARITY_CALL`  
**Timeout**: Must respond within 30 seconds

```json
{
  "protocol": "league.v2",
  "message_type": "PARITY_CHOICE",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "conversation_id": "880e8400-e29b-41d4-a716-446655440003",
  "sender": "P01",
  "timestamp": "2025-12-20T10:00:10.000Z",
  "choice": "EVEN"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"PARITY_CHOICE"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Match identifier |
| `conversation_id` | UUID | ✅ | **Must match call's conversation_id** |
| `sender` | string | ✅ | Player ID |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp |
| `choice` | string | ✅ | `"EVEN"` or `"ODD"` |

**Valid choices**:
| Value | Description |
|-------|-------------|
| `"EVEN"` | Predicting drawn number will be even (2,4,6,8,10) |
| `"ODD"` | Predicting drawn number will be odd (1,3,5,7,9) |

**Invalid choices will result in error `E004` (INVALID_PARITY_CHOICE)**

---

## 3. Messages Received by Player

Players receive the following messages and should handle them appropriately:

### 3.1 From League Manager

| Message Type | Purpose | Player Action |
|--------------|---------|---------------|
| `LEAGUE_REGISTER_RESPONSE` | Registration confirmation | Store auth_token |
| `ROUND_ANNOUNCEMENT` | New round starting | Log/prepare |
| `LEAGUE_STANDINGS_UPDATE` | Current standings | Log/analyze |
| `ROUND_COMPLETED` | Round finished | Log |
| `LEAGUE_COMPLETED` | League finished | Shutdown |
| `LEAGUE_ERROR` | Error notification | Handle error |
| `SHUTDOWN_COMMAND` | Shutdown request | Clean shutdown |

### 3.2 From Referee

| Message Type | Purpose | Player Action |
|--------------|---------|---------------|
| `GAME_INVITATION` | Match starting | Send `GAME_JOIN_ACK` |
| `CHOOSE_PARITY_CALL` | Request choice | Send `PARITY_CHOICE` |
| `GAME_OVER` | Game result | Log result, update history |
| `GAME_ERROR` | Game error | Handle error |

---

## 4. Response Requirements

### 4.1 Timing Requirements

| Message | Response | Timeout |
|---------|----------|---------|
| `GAME_INVITATION` | `GAME_JOIN_ACK` | 5 seconds |
| `CHOOSE_PARITY_CALL` | `PARITY_CHOICE` | 30 seconds |

### 4.2 Consequences of Timeout

| Scenario | Result |
|----------|--------|
| Join timeout | Player forfeits match |
| Choice timeout | Technical loss (0 points) |
| Both timeout | Draw |

---

## 5. Choice Validation

The referee validates the choice field:

```python
VALID_CHOICES = ["even", "odd"]

def validate_choice(choice: str) -> bool:
    return choice.lower() in VALID_CHOICES
```

**Invalid choices**:
- `"EVEN"` - wrong case (must be lowercase)
- `"maybe"` - invalid value
- `""` - empty string
- `None` - null value

---

## Python Implementation

```python
from SHARED.contracts.player_contracts import (
    build_game_join_ack,
    build_parity_choice,
)

from SHARED.contracts.league_manager_contracts import (
    build_league_register_request,
)
```

### Example Usage

```python
from SHARED.contracts.player_contracts import build_parity_choice

# Build a parity choice message
message = build_parity_choice(
    league_id="league_2025_even_odd",
    round_id=1,
    match_id="R1M1",
    player_id="P01",
    choice="even",
    conversation_id="880e8400-e29b-41d4-a716-446655440003"
)
```

---

## 6. Player Strategies

Players can implement different strategies for choosing parity:

| Strategy | Description |
|----------|-------------|
| `random` | Random choice each game |
| `frequency` | Track opponent history, counter most common |
| `pattern` | Detect patterns in opponent choices |
| `timeout` | Deliberately timeout (for testing) |

Constants from `SHARED/agent_constants.py`:
```python
class StrategyType:
    RANDOM = "random"
    FREQUENCY = "frequency"
    PATTERN = "pattern"
    TIMEOUT = "timeout"
```

---

## 7. Player State Machine

```
INIT → REGISTERED → ACTIVE → SHUTDOWN
```

| State | Description |
|-------|-------------|
| `INIT` | Started, not yet registered |
| `REGISTERED` | Successfully registered with LM |
| `ACTIVE` | Participating in matches |
| `SHUTDOWN` | Shutting down |

---

## 8. Error Handling

Players should handle these error scenarios:

### 8.1 Connection Errors
- Retry with exponential backoff
- Max 3 retries before failing

### 8.2 Invalid Messages
- Log the error
- Ignore malformed messages

### 8.3 Game Errors
- Log `GAME_ERROR` messages
- Continue to next game

---

## 9. Conversation ID Tracking

**Critical**: Players must track and use the correct `conversation_id`:

1. When receiving `GAME_INVITATION`:
   - Extract `conversation_id`
   - Store it for this match

2. When responding with `GAME_JOIN_ACK`:
   - Use the same `conversation_id`

3. When receiving `CHOOSE_PARITY_CALL`:
   - Verify `conversation_id` matches
   - Use same ID in `PARITY_CHOICE`

```python
class Player:
    def __init__(self):
        self._current_conversation_id = None
    
    def handle_game_invitation(self, msg):
        self._current_conversation_id = msg["conversation_id"]
        return self.send_join_ack()
    
    def handle_choose_parity_call(self, msg):
        assert msg["conversation_id"] == self._current_conversation_id
        return self.send_parity_choice()
```
