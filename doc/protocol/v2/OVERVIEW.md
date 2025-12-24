# Protocol Overview

**Protocol Version**: `league.v2`

## Base Message Structure

Every protocol message MUST include these base fields:

```json
{
  "protocol": "league.v2",
  "message_type": "<MESSAGE_TYPE>",
  "league_id": "<string>",
  "round_id": <integer>,
  "match_id": "<string>",
  "conversation_id": "<UUID>",
  "sender": "<string>",
  "timestamp": "<ISO-8601 UTC>"
}
```

## Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Protocol version (always `"league.v2"`) |
| `message_type` | string | ✅ | Message type identifier |
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number (0 for registration) |
| `match_id` | string | ✅ | Match identifier (format: `R{round}M{match}`) |
| `conversation_id` | UUID | ✅ | Unique conversation thread ID |
| `sender` | string | ✅ | Sender identity |
| `timestamp` | ISO-8601 | ✅ | UTC timestamp ending with `Z` |

## Timestamp Requirements

**All timestamps MUST be in UTC and end with `Z`**:

```
✅ Valid:   "2025-12-20T10:30:00.000Z"
✅ Valid:   "2025-12-20T10:30:00Z"
❌ Invalid: "2025-12-20T10:30:00+02:00"
❌ Invalid: "2025-12-20 10:30:00"
```

## Message Types Summary

### Registration Messages
| Type | Direction | Purpose |
|------|-----------|---------|
| `REFEREE_REGISTER_REQUEST` | Referee → LM | Referee registration |
| `REFEREE_REGISTER_RESPONSE` | LM → Referee | Registration response |
| `LEAGUE_REGISTER_REQUEST` | Player → LM | Player registration |
| `LEAGUE_REGISTER_RESPONSE` | LM → Player | Registration response |

### League Control Messages
| Type | Direction | Purpose |
|------|-----------|---------|
| `START_LEAGUE` | Launcher → LM | Start the league |
| `LEAGUE_STATUS` | LM → Launcher | League status response |

### Round Lifecycle Messages
| Type | Direction | Purpose |
|------|-----------|---------|
| `ROUND_ANNOUNCEMENT` | LM → All | Announce new round |
| `RUN_MATCH` | LM → Referee | Assign match to referee |
| `RUN_MATCH_ACK` | Referee → LM | Match assignment ack |
| `ROUND_COMPLETED` | LM → All | Round completion |
| `LEAGUE_STANDINGS_UPDATE` | LM → All | Updated standings |
| `LEAGUE_COMPLETED` | LM → All | League completion |

### Game Flow Messages
| Type | Direction | Purpose |
|------|-----------|---------|
| `GAME_INVITATION` | Referee → Player | Invite to game |
| `GAME_JOIN_ACK` | Player → Referee | Join confirmation |
| `CHOOSE_PARITY_CALL` | Referee → Player | Request choice |
| `PARITY_CHOICE` | Player → Referee | Player's choice |
| `GAME_OVER` | Referee → Players | Game result |
| `MATCH_RESULT_REPORT` | Referee → LM | Report result |
| `MATCH_RESULT_ACK` | LM → Referee | Result acknowledged |

### Error Messages
| Type | Direction | Purpose |
|------|-----------|---------|
| `LEAGUE_ERROR` | LM → Agent | League-level error |
| `GAME_ERROR` | Referee → Player | Game-level error |

### Shutdown Messages
| Type | Direction | Purpose |
|------|-----------|---------|
| `SHUTDOWN_COMMAND` | LM → All | Shutdown command |
| `SHUTDOWN_ACK` | Agent → LM | Shutdown acknowledged |

## Response Timeouts

| Message Type | Timeout | Consequence |
|--------------|---------|-------------|
| `GAME_JOIN_ACK` | 5s | Player forfeits |
| `PARITY_CHOICE` | 30s | Player loses (technical loss) |
| Registration | 10s | Registration fails |
| Default | 10s | Retry or error |

## Status Values

| Value | Description |
|-------|-------------|
| `ok` | Generic success |
| `registered` | Registration successful |
| `recorded` | Result recorded |
| `acknowledged` | Message acknowledged |
| `error` | Operation failed |
| `success` | Operation succeeded |
| `failure` | Operation failed |

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| `E001` | `TIMEOUT_ERROR` | Response timeout |
| `E003` | `MISSING_REQUIRED_FIELD` | Required field missing |
| `E004` | `INVALID_PARITY_CHOICE` | Invalid choice (not "even"/"odd") |
| `E005` | `PLAYER_NOT_REGISTERED` | Player not registered |
| `E009` | `CONNECTION_ERROR` | Connection failed |
| `E011` | `AUTH_TOKEN_MISSING` | Missing auth token |
| `E012` | `AUTH_TOKEN_INVALID` | Invalid auth token |
| `E021` | `INVALID_TIMESTAMP` | Invalid timestamp format |

## Constants Reference

From `SHARED/protocol_constants.py`:

```python
PROTOCOL_VERSION = "league.v2"
MCP_PATH = "/mcp"
LOCALHOST = "localhost"
SERVER_HOST = "0.0.0.0"
HTTP_PROTOCOL = "http"
```

## Port Allocation

| Agent Type | Port Range | Example |
|------------|------------|---------|
| League Manager | 8000 | `http://localhost:8000/mcp` |
| Referees | 8001-8099 | REF01=8001, REF02=8002 |
| Players | 8100-8199 | P01=8101, P02=8102, etc. |
