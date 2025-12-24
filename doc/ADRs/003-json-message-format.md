# ADR 003: JSON Message Format

**Status**: Accepted  
**Date**: 2025-12-20  
**Context**: Protocol Message Structure

## Context

All agents need a standardized message format for communication. The format must support various message types, be extensible, and include metadata for debugging and auditing.

## Decision

We use a **standardized JSON message format** with the following structure:

```json
{
  "protocol_version": "league.v2",
  "message_id": "uuid-v4",
  "timestamp": "2025-12-20T14:30:00.000Z",
  "message_type": "GAME_INVITATION",
  "sender_id": "REF01",
  "recipient_id": "P01",
  "payload": {
    // Message-specific data
  }
}
```

## Message Structure

### Required Fields (All Messages)
1. **protocol_version**: `"league.v2"` - Protocol version identifier
2. **message_id**: UUID v4 - Unique identifier for each message
3. **timestamp**: ISO-8601 UTC with 'Z' suffix - When message was created
4. **message_type**: Enum - One of 15 defined message types
5. **sender_id**: String - ID of sending agent
6. **recipient_id**: String - ID of receiving agent (or "ALL")
7. **payload**: Object - Message-specific data

### Optional Fields
- **auth_token**: String - Authentication token (for registration responses)
- **correlation_id**: UUID - For request/response matching

## Message Types (15 Total)

### Registration (2)
1. `REFEREE_REGISTER_REQUEST`
2. `LEAGUE_REGISTER_REQUEST`

### Match Lifecycle (5)
3. `GAME_INVITATION`
4. `GAME_JOIN_ACK`
5. `CHOOSE_PARITY_CALL`
6. `PARITY_CHOICE`
7. `GAME_OVER`

### Tournament Lifecycle (5)
8. `ROUND_ANNOUNCEMENT`
9. `ROUND_COMPLETED`
10. `LEAGUE_STANDINGS_UPDATE`
11. `LEAGUE_COMPLETED`
12. `MATCH_RESULT_REPORT`

### Control (3)
13. `START_LEAGUE`
14. `STOP_LEAGUE`
15. `HEARTBEAT`

## Rationale

### Why This Format?
1. **Consistency**: Same structure for all messages
2. **Traceability**: message_id + timestamp enable complete audit trail
3. **Routing**: sender_id + recipient_id clearly identify communication path
4. **Versioning**: protocol_version enables future compatibility
5. **Type Safety**: message_type enables validation and routing
6. **Debugging**: Human-readable, easy to log and inspect

### Timestamp Format
- **ISO-8601**: International standard
- **UTC**: No timezone ambiguity
- **'Z' Suffix**: Explicitly indicates UTC
- **Millisecond Precision**: Adequate for ordering

## Validation Rules

1. **Protocol Version**: Must be exactly `"league.v2"`
2. **Message ID**: Must be valid UUID v4 format
3. **Timestamp**: Must match ISO-8601 and end with 'Z'
4. **Message Type**: Must be one of 15 defined types
5. **Payload**: Must contain required fields for message type

## Example Messages

See `doc/message_examples/` for complete examples of all 15 message types.

## Consequences

### Positive
- Clear, unambiguous message structure
- Easy to validate with JSON Schema
- Excellent debugging and logging
- Supports message tracking and auditing
- Extensible via payload field

### Negative
- Verbose (larger than binary protocols)
- Repeated metadata in every message
- JSON parsing overhead
- No built-in compression

## Alternatives Considered

1. **Protocol Buffers**: Rejected - harder to debug, requires schema files
2. **MessagePack**: Rejected - binary format harder to inspect
3. **XML**: Rejected - too verbose, less common in modern systems
4. **Custom Binary Protocol**: Rejected - reinventing the wheel
5. **Minimal JSON**: Rejected - lacks necessary metadata

## Related Decisions
- ADR 002: HTTP Protocol Choice
- ADR 001: Three-Layer Architecture

## Migration Path

If protocol changes needed:
1. Update `protocol_version` to `"league.v3"`
2. Maintain backward compatibility for v2
3. Document breaking changes
4. Provide migration guide
