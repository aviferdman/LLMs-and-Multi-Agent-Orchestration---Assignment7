# Skill: Protocol Validation

## Message Schema Validation for league.v2 Protocol

---

## 📋 Overview

The `protocol_validation` skill provides comprehensive validation of messages against the league.v2 protocol specification. This skill ensures all inter-agent communication conforms to the defined contracts.

---

## 🎯 Capabilities

### 1. Schema Validation
- Validate required fields presence
- Check field types and formats
- Verify enum values
- Validate nested objects

### 2. Protocol Compliance
- Check protocol version (`league.v2`)
- Validate message_type against allowed types
- Verify timestamp format (ISO 8601)
- Check UUID format for IDs

### 3. Contract Verification
- Validate against contract definitions
- Check sender/receiver roles
- Verify conversation_id chains
- Validate round/match context

---

## 🔧 Usage

### Basic Validation

```python
from SHARED.league_sdk.validation import validate_message

message = {
    "protocol": "league.v2",
    "message_type": "GAME_INVITATION",
    "timestamp": "2025-12-24T10:00:00.000Z",
    "conversation_id": "abc-123",
    "sender": "REF01",
    "league_id": "LEAGUE_001",
    "round_id": 1,
    "match_id": "MATCH_001"
}

is_valid = validate_message(message)
```

### Detailed Validation

```python
from SHARED.league_sdk.validation import validate_with_details

result = validate_with_details(message)
if not result.valid:
    for error in result.errors:
        print(f"Error: {error.field} - {error.message}")
```

---

## 📊 Validation Rules

### Required Fields (All Messages)

| Field | Type | Format |
|-------|------|--------|
| protocol | string | "league.v2" |
| message_type | string | Valid message type |
| timestamp | string | ISO 8601 |
| conversation_id | string | UUID format |
| sender | string | Agent ID |

### Message-Specific Fields

| Message Type | Additional Required Fields |
|--------------|---------------------------|
| GAME_INVITATION | league_id, match_id, players |
| PARITY_CHOICE | choice (even/odd), number |
| MATCH_RESULT_REPORT | winner, scores, rounds_played |

---

## ✅ Validation Checklist

```
[ ] Protocol Validation
    [ ] protocol == "league.v2"
    [ ] message_type is valid
    [ ] timestamp is ISO 8601
    [ ] conversation_id is UUID

[ ] Field Validation
    [ ] All required fields present
    [ ] Field types correct
    [ ] Enum values valid
    [ ] Nested objects valid

[ ] Context Validation
    [ ] sender is valid agent
    [ ] league_id exists
    [ ] match_id format correct
    [ ] round_id is positive integer
```

---

## 🔗 Related Files

- [SHARED/contracts/](../../SHARED/contracts/) - Contract definitions
- [doc/protocol_spec.md](../../doc/protocol_spec.md) - Protocol specification
- [SHARED/league_sdk/validation.py](../../SHARED/league_sdk/validation.py) - Implementation

---

**Status**: Ready for use  
**Last Updated**: December 24, 2025
