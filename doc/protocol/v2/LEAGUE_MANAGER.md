# League Manager Protocol Contracts

**Protocol Version**: `league.v2`

The League Manager is the central orchestrator responsible for:
- Agent registration (referees and players)
- Round-robin scheduling
- Match assignment
- Standings management
- League lifecycle

---

## 1. Registration Contracts

### 1.1 Referee Registration

#### REFEREE_REGISTER_REQUEST

**Direction**: Referee → League Manager  
**Endpoint**: `POST /mcp`

```json
{
  "protocol": "league.v2",
  "message_type": "REFEREE_REGISTER_REQUEST",
  "referee_id": "REF01",
  "endpoint": "http://localhost:8001/mcp"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"REFEREE_REGISTER_REQUEST"` |
| `referee_id` | string | ✅ | Unique referee identifier (e.g., "REF01") |
| `endpoint` | string | ✅ | HTTP endpoint for referee communication |

#### REFEREE_REGISTER_RESPONSE

**Direction**: League Manager → Referee

```json
{
  "protocol": "league.v2",
  "message_type": "REFEREE_REGISTER_RESPONSE",
  "referee_id": "REF01",
  "auth_token": "tok_ref01_abc123",
  "status": "registered"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"REFEREE_REGISTER_RESPONSE"` |
| `referee_id` | string | ✅ | Assigned referee ID |
| `auth_token` | string | ✅ | Authentication token for future requests |
| `status` | string | ✅ | `"registered"` or `"error"` |

---

### 1.2 Player Registration

#### LEAGUE_REGISTER_REQUEST

**Direction**: Player → League Manager  
**Endpoint**: `POST /mcp`

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
| `player_id` | string | ✅ | Unique player identifier (e.g., "P01") |
| `endpoint` | string | ✅ | HTTP endpoint for player communication |

#### LEAGUE_REGISTER_RESPONSE

**Direction**: League Manager → Player

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_REGISTER_RESPONSE",
  "player_id": "P01",
  "league_id": "league_2025_even_odd",
  "auth_token": "tok_p01_xyz789",
  "status": "registered"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"LEAGUE_REGISTER_RESPONSE"` |
| `player_id` | string | ✅ | Assigned player ID |
| `league_id` | string | ✅ | League identifier |
| `auth_token` | string | ✅ | Authentication token |
| `status` | string | ✅ | `"registered"` or `"error"` |

---

## 2. League Control Contracts

### 2.1 Start League

#### START_LEAGUE

**Direction**: Launcher → League Manager  
**Endpoint**: `POST /mcp`

```json
{
  "protocol": "league.v2",
  "message_type": "START_LEAGUE",
  "league_id": "league_2025_even_odd",
  "sender": "launcher"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"START_LEAGUE"` |
| `league_id` | string | ✅ | League to start |
| `sender` | string | ✅ | Sender identifier |

#### LEAGUE_STATUS

**Direction**: League Manager → Launcher (response)

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_STATUS",
  "league_id": "league_2025_even_odd",
  "status": "running",
  "current_round": 1,
  "total_rounds": 3,
  "matches_completed": 0
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"LEAGUE_STATUS"` |
| `league_id` | string | ✅ | League identifier |
| `status` | string | ✅ | `"running"`, `"completed"`, `"error"` |
| `current_round` | integer | ✅ | Current round number |
| `total_rounds` | integer | ✅ | Total rounds in league |
| `matches_completed` | integer | ✅ | Number of completed matches |

---

## 3. Round Lifecycle Contracts

### 3.1 Round Announcement

#### ROUND_ANNOUNCEMENT

**Direction**: League Manager → All Agents  
**Sent when**: New round begins

```json
{
  "protocol": "league.v2",
  "message_type": "ROUND_ANNOUNCEMENT",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "total_rounds": 3,
  "matches": [
    {
      "match_id": "R1M1",
      "player_a": "P01",
      "player_b": "P02",
      "referee_id": "REF01"
    },
    {
      "match_id": "R1M2",
      "player_a": "P03",
      "player_b": "P04",
      "referee_id": "REF02"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"ROUND_ANNOUNCEMENT"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Round number (1-indexed) |
| `total_rounds` | integer | ✅ | Total rounds in tournament |
| `matches` | array | ✅ | List of matches in this round |

**Match object**:
| Field | Type | Description |
|-------|------|-------------|
| `match_id` | string | Match identifier (e.g., "R1M1") |
| `player_a` | string | First player ID |
| `player_b` | string | Second player ID |
| `referee_id` | string | Assigned referee ID |

---

### 3.2 Match Assignment

#### RUN_MATCH

**Direction**: League Manager → Referee  
**Sent when**: Round starts, referee needs to run a match

```json
{
  "protocol": "league.v2",
  "message_type": "RUN_MATCH",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "match_id": "R1M1",
  "referee_id": "REF01",
  "player_a": "P01",
  "player_a_endpoint": "http://localhost:8101/mcp",
  "player_b": "P02",
  "player_b_endpoint": "http://localhost:8102/mcp"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"RUN_MATCH"` |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Round number |
| `match_id` | string | ✅ | Match identifier |
| `referee_id` | string | ✅ | Target referee ID |
| `player_a` | string | ✅ | First player ID |
| `player_a_endpoint` | string | ✅ | First player's endpoint |
| `player_b` | string | ✅ | Second player ID |
| `player_b_endpoint` | string | ✅ | Second player's endpoint |

#### RUN_MATCH_ACK

**Direction**: Referee → League Manager

```json
{
  "protocol": "league.v2",
  "message_type": "RUN_MATCH_ACK",
  "match_id": "R1M1",
  "status": "acknowledged"
}
```

---

### 3.3 Match Result Acknowledgment

#### MATCH_RESULT_ACK

**Direction**: League Manager → Referee  
**Sent when**: Match result received and recorded

```json
{
  "protocol": "league.v2",
  "message_type": "MATCH_RESULT_ACK",
  "match_id": "R1M1",
  "status": "recorded"
}
```

---

### 3.4 Round Completed

#### ROUND_COMPLETED

**Direction**: League Manager → All Agents  
**Sent when**: All matches in round completed

```json
{
  "protocol": "league.v2",
  "message_type": "ROUND_COMPLETED",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "results": [
    {
      "match_id": "R1M1",
      "winner": "P01",
      "player_a": "P01",
      "player_b": "P02"
    },
    {
      "match_id": "R1M2",
      "winner": "P03",
      "player_a": "P03",
      "player_b": "P04"
    }
  ]
}
```

---

### 3.5 League Standings Update

#### LEAGUE_STANDINGS_UPDATE

**Direction**: League Manager → All Agents  
**Sent when**: After each round completion

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_STANDINGS_UPDATE",
  "league_id": "league_2025_even_odd",
  "round_id": 1,
  "standings": [
    {
      "rank": 1,
      "player_id": "P01",
      "wins": 1,
      "losses": 0,
      "draws": 0,
      "points": 3,
      "games_played": 1
    },
    {
      "rank": 1,
      "player_id": "P03",
      "wins": 1,
      "losses": 0,
      "draws": 0,
      "points": 3,
      "games_played": 1
    }
  ]
}
```

**Standings entry**:
| Field | Type | Description |
|-------|------|-------------|
| `rank` | integer | Current rank (1-indexed) |
| `player_id` | string | Player identifier |
| `wins` | integer | Number of wins |
| `losses` | integer | Number of losses |
| `draws` | integer | Number of draws |
| `points` | integer | Total points |
| `games_played` | integer | Games played |

---

### 3.6 League Completed

#### LEAGUE_COMPLETED

**Direction**: League Manager → All Agents  
**Sent when**: All rounds completed

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_COMPLETED",
  "league_id": "league_2025_even_odd",
  "total_matches": 6,
  "final_standings": [
    {
      "rank": 1,
      "player_id": "P02",
      "wins": 2,
      "losses": 0,
      "draws": 1,
      "points": 7,
      "games_played": 3
    }
  ]
}
```

---

## 4. Error Contracts

### LEAGUE_ERROR

**Direction**: League Manager → Agent  
**Sent when**: League-level error occurs

```json
{
  "protocol": "league.v2",
  "message_type": "LEAGUE_ERROR",
  "league_id": "league_2025_even_odd",
  "error_code": "E005",
  "error_message": "Player not registered",
  "details": {
    "player_id": "P99"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Must be `"league.v2"` |
| `message_type` | string | ✅ | Must be `"LEAGUE_ERROR"` |
| `league_id` | string | ✅ | League identifier |
| `error_code` | string | ✅ | Error code (see OVERVIEW.md) |
| `error_message` | string | ✅ | Human-readable message |
| `details` | object | ❌ | Additional error context |

---

## Python Implementation

```python
from SHARED.contracts.league_manager_contracts import (
    build_referee_register_request,
    build_referee_register_response,
    build_league_register_request,
    build_league_register_response,
    build_start_league,
    build_league_status,
    build_run_match,
    build_run_match_ack,
    build_match_result_ack,
)

from SHARED.contracts.round_lifecycle_contracts import (
    build_round_announcement,
    build_round_completed,
    build_league_completed,
    build_league_standings_update,
    build_league_error,
)
```
