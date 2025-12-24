# League Protocol Specification

**Protocol Version**: `league.v2`  
**Last Updated**: December 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Transport Layer](#transport-layer)
3. [Message Types](#message-types)
4. [Agent Registration](#agent-registration)
5. [Game Flow](#game-flow)
6. [Error Handling](#error-handling)
7. [Timeouts](#timeouts)

---

## Overview

The League Protocol (`league.v2`) defines the communication standard between agents in a multi-agent game league system. The protocol supports:

- **League Manager**: Orchestrates leagues, rounds, and standings
- **Referees**: Manage individual matches and enforce game rules
- **Players**: Participate in matches and make game decisions

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     League Manager                          │
│                    (Orchestrator)                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Referee  │    │ Referee  │    │ Referee  │
    │  REF01   │    │  REF02   │    │   ...    │
    └────┬─────┘    └────┬─────┘    └──────────┘
         │               │
    ┌────┴────┐     ┌────┴────┐
    ▼         ▼     ▼         ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ P01  │ │ P02  │ │ P03  │ │ P04  │
└──────┘ └──────┘ └──────┘ └──────┘
```

---

## Transport Layer

### JSON-RPC 2.0 Envelope

All protocol messages are wrapped in JSON-RPC 2.0 envelopes for transport.

#### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "<message_type>",
  "params": {
    "protocol": "league.v2",
    "message_type": "<MESSAGE_TYPE>",
    "sender": "<agent_id>",
    "timestamp": "<ISO-8601>",
    "conversation_id": "<unique_id>",
    ...message_specific_fields
  },
  "id": <sequential_integer>
}
```

#### Response Format

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocol": "league.v2",
    "message_type": "<RESPONSE_TYPE>",
    ...response_fields
  },
  "id": <matching_request_id>
}
```

#### Error Format

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": <integer>,
    "message": "<error_description>"
  },
  "id": <request_id>
}
```

### Common Fields

All messages include these base fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | ✅ | Always `"league.v2"` |
| `message_type` | string | ✅ | Message type identifier |
| `sender` | string | ✅ | Sender identifier (e.g., `"player:P01"`) |
| `timestamp` | ISO-8601 | ✅ | Message creation time |
| `conversation_id` | string | ✅ | Conversation tracking ID |

---

## Message Types

### League Manager Messages

| Message Type | Direction | Description |
|--------------|-----------|-------------|
| `ROUND_ANNOUNCEMENT` | LM → All | Announces new round with matches |
| `ROUND_COMPLETED` | LM → Players | Notifies round completion |
| `LEAGUE_STANDINGS_UPDATE` | LM → Players | Updates standings after round |
| `LEAGUE_COMPLETED` | LM → All | Announces league completion |
| `LEAGUE_QUERY_RESPONSE` | LM → Agent | Response to queries |
| `LEAGUE_ERROR` | LM → Agent | League-level errors |

### Referee Messages

| Message Type | Direction | Description |
|--------------|-----------|-------------|
| `REFEREE_REGISTER_REQUEST` | Ref → LM | Register referee |
| `GAME_INVITATION` | Ref → Player | Invite to match |
| `CHOOSE_PARITY_CALL` | Ref → Player | Request parity choice |
| `GAME_OVER` | Ref → Players | Announce game result |
| `MATCH_RESULT_REPORT` | Ref → LM | Report match result |
| `GAME_ERROR` | Ref → Player | Game-level errors |

### Player Messages

| Message Type | Direction | Description |
|--------------|-----------|-------------|
| `LEAGUE_REGISTER_REQUEST` | Player → LM | Register player |
| `GAME_JOIN_ACK` | Player → Ref | Accept game invitation |
| `CHOOSE_PARITY_RESPONSE` | Player → Ref | Submit parity choice |
| `LEAGUE_QUERY` | Player → LM | Query league info |

---

## Agent Registration

### Referee Registration

**Message**: `REFEREE_REGISTER_REQUEST`  
**Direction**: Referee → League Manager  
**Endpoint**: `POST /mcp`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_type` | string | ✅ | `"REFEREE_REGISTER_REQUEST"` |
| `referee_meta` | object | ✅ | Referee metadata |
| `referee_meta.display_name` | string | ✅ | Human-readable name |
| `referee_meta.version` | string | ✅ | Agent version |
| `referee_meta.game_types` | array | ✅ | Supported games |
| `referee_meta.contact_endpoint` | string | ✅ | HTTP endpoint |
| `referee_meta.max_concurrent_matches` | integer | ❌ | Max simultaneous matches |

**Response**: `REFEREE_REGISTER_RESPONSE`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | ✅ | `"ACCEPTED"` or `"REJECTED"` |
| `referee_id` | string | ✅ | Assigned referee ID |
| `reason` | string | ❌ | Rejection reason |

### Player Registration

**Message**: `LEAGUE_REGISTER_REQUEST`  
**Direction**: Player → League Manager  
**Endpoint**: `POST /mcp`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_type` | string | ✅ | `"LEAGUE_REGISTER_REQUEST"` |
| `player_meta` | object | ✅ | Player metadata |
| `player_meta.display_name` | string | ✅ | Human-readable name |
| `player_meta.version` | string | ✅ | Agent version |
| `player_meta.game_types` | array | ✅ | Supported games |
| `player_meta.contact_endpoint` | string | ✅ | HTTP endpoint |

**Response**: `LEAGUE_REGISTER_RESPONSE`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | ✅ | `"ACCEPTED"` or `"REJECTED"` |
| `player_id` | string | ✅ | Assigned player ID |
| `reason` | string | ❌ | Rejection reason |

---

## Game Flow

### Match Lifecycle

```
1. GAME_INVITATION (Referee → Player)
   └── Player has 5 seconds to respond
   
2. GAME_JOIN_ACK (Player → Referee)
   └── Both players must acknowledge
   
3. CHOOSE_PARITY_CALL (Referee → Player)
   └── Player has 30 seconds to respond
   
4. CHOOSE_PARITY_RESPONSE (Player → Referee)
   └── Choice: "even" or "odd"
   
5. GAME_OVER (Referee → Both Players)
   └── Contains winner, drawn number, choices
   
6. MATCH_RESULT_REPORT (Referee → League Manager)
   └── Official result recording
```

### Game Invitation

**Message**: `GAME_INVITATION`  
**Timeout**: 5 seconds

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `league_id` | string | ✅ | League identifier |
| `round_id` | integer | ✅ | Current round number |
| `match_id` | string | ✅ | Unique match ID |
| `game_type` | string | ✅ | Game type (e.g., `"even_odd"`) |
| `role_in_match` | string | ✅ | `"PLAYER_A"` or `"PLAYER_B"` |
| `opponent_id` | string | ✅ | Opponent's player ID |

### Parity Choice (Even/Odd Game)

**Request**: `CHOOSE_PARITY_CALL`  
**Timeout**: 30 seconds

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `match_id` | string | ✅ | Match identifier |
| `player_id` | string | ✅ | Target player ID |
| `game_type` | string | ✅ | `"even_odd"` |
| `context` | object | ✅ | Game context |
| `context.opponent_id` | string | ✅ | Opponent ID |
| `context.round_id` | integer | ✅ | Round number |
| `context.your_standings` | object | ✅ | Player's current stats |
| `deadline` | ISO-8601 | ✅ | Response deadline |

**Response**: `CHOOSE_PARITY_RESPONSE`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `match_id` | string | ✅ | Match identifier |
| `player_id` | string | ✅ | Player ID |
| `parity_choice` | string | ✅ | `"even"` or `"odd"` |

### Game Result

**Message**: `GAME_OVER`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `match_id` | string | ✅ | Match identifier |
| `game_type` | string | ✅ | Game type |
| `game_result` | object | ✅ | Result details |
| `game_result.status` | string | ✅ | `"WIN"`, `"DRAW"`, or `"TECHNICAL_LOSS"` |
| `game_result.winner_player_id` | string | ❌ | Winner ID (if WIN) |
| `game_result.drawn_number` | integer | ✅ | Random number drawn |
| `game_result.number_parity` | string | ✅ | `"even"` or `"odd"` |
| `game_result.choices` | object | ✅ | Player choices map |
| `game_result.reason` | string | ❌ | Human-readable explanation |

---

## Error Handling

### Error Codes

| Code | Name | Description | Severity |
|------|------|-------------|----------|
| `E001` | `TIMEOUT_ERROR` | Response timeout exceeded | High |
| `E003` | `MISSING_REQUIRED_FIELD` | Required field missing | High |
| `E004` | `INVALID_PARITY_CHOICE` | Invalid choice value | High |
| `E005` | `PLAYER_NOT_REGISTERED` | Unknown player ID | High |
| `E009` | `CONNECTION_ERROR` | Network failure | Critical |
| `E011` | `AUTH_TOKEN_MISSING` | No auth token provided | High |
| `E012` | `AUTH_TOKEN_INVALID` | Invalid auth token | High |
| `E021` | `INVALID_TIMESTAMP` | Malformed timestamp | Medium |

### Error Message Structure

**Message**: `GAME_ERROR` / `LEAGUE_ERROR`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error_code` | string | ✅ | Error code (e.g., `"E001"`) |
| `error_description` | string | ✅ | Error name |
| `affected_player` | string | ✅ | Impacted player ID |
| `action_required` | string | ✅ | Expected action |
| `retry_info` | object | ❌ | Retry details |
| `retry_info.retry_count` | integer | ❌ | Current retry attempt |
| `retry_info.max_retries` | integer | ❌ | Maximum retries allowed |
| `retry_info.next_retry_at` | ISO-8601 | ❌ | Next retry time |
| `consequence` | string | ❌ | Result if not resolved |

---

## Timeouts

### Response Timeouts

| Message Type | Timeout | Consequence |
|--------------|---------|-------------|
| `GAME_JOIN_ACK` | 5 seconds | Player forfeits match |
| `CHOOSE_PARITY_RESPONSE` | 30 seconds | Technical loss |
| Registration messages | 10 seconds | Registration fails |
| All other messages | 10 seconds | Retry or error |

### Retry Policy

- **Max Retries**: 3 attempts
- **Retry Delay**: Exponential backoff (1s, 2s, 4s)
- **Circuit Breaker**: Opens after 5 consecutive failures

---

## Appendix: Message Examples

See the `messageexamples/` directory for complete JSON examples:

- `registration/` - Agent registration messages
- `gameflow/` - Game flow messages
- `errors/` - Error messages

---

*End of Protocol Specification*
