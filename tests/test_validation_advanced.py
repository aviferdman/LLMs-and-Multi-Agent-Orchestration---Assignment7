#!/usr/bin/env python3
"""Advanced validation tests - message types, fields, protocol, errors."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from SHARED.league_sdk.validation import (
    validate_message_type, validate_required_fields,
    validate_protocol_version, get_validation_errors
)
from SHARED.constants import Field, MessageType

def test_validate_message_type():
    """Test message type validation."""
    print("Testing validate_message_type...")
    
    # Valid types
    assert validate_message_type(MessageType.GAME_INVITATION), "Valid type should pass"
    assert validate_message_type(MessageType.GAME_OVER), "Valid type should pass"
    
    # Invalid type
    assert not validate_message_type("INVALID_TYPE"), "Invalid type should fail"
    
    print("  ✓ validate_message_type works correctly")
    return True

def test_validate_required_fields():
    """Test required fields validation."""
    print("Testing validate_required_fields...")
    
    message = {
        "field1": "value1",
        "field2": "value2"
    }
    
    # All required fields present
    result = validate_required_fields(message, ["field1", "field2"])
    assert result is None, "Should return None when all fields present"
    
    # Missing required fields
    result = validate_required_fields(message, ["field1", "field3"])
    assert result is not None, "Should return error when fields missing"
    assert "field3" in result, "Error should mention missing field"
    
    print("  ✓ validate_required_fields works correctly")
    return True

def test_validate_protocol_version():
    """Test protocol version validation."""
    print("Testing validate_protocol_version...")
    
    assert validate_protocol_version("league.v2"), "Correct version should pass"
    assert not validate_protocol_version("league.v1"), "Wrong version should fail"
    assert not validate_protocol_version("invalid"), "Invalid version should fail"
    
    print("  ✓ validate_protocol_version works correctly")
    return True

def test_get_validation_errors():
    """Test comprehensive validation."""
    print("Testing get_validation_errors...")
    
    # Fully valid message
    valid_msg = {
        Field.PROTOCOL: "league.v2",
        Field.CONVERSATION_ID: "123e4567-e89b-12d3-a456-426614174000",
        Field.TIMESTAMP: "2025-01-01T12:00:00Z",
        Field.MESSAGE_TYPE: MessageType.GAME_INVITATION
    }
    errors = get_validation_errors(valid_msg)
    assert len(errors) == 0, f"Valid message should have no errors, got: {errors}"
    
    # Message with multiple errors
    invalid_msg = {
        Field.PROTOCOL: "wrong",
        Field.CONVERSATION_ID: "invalid-uuid",
        Field.TIMESTAMP: "invalid-timestamp",
        Field.MESSAGE_TYPE: "INVALID_TYPE"
    }
    errors = get_validation_errors(invalid_msg)
    assert len(errors) > 0, "Invalid message should have errors"
    
    # Missing required fields
    incomplete_msg = {}
    errors = get_validation_errors(incomplete_msg)
    assert len(errors) > 0, "Incomplete message should have errors"
    
    print(f"  ✓ get_validation_errors works correctly")
    return True

def main():
    """Run advanced validation tests."""
    print("=" * 60)
    print("ADVANCED VALIDATION TESTS")
    print("=" * 60)
    
    tests = [
        test_validate_message_type,
        test_validate_required_fields,
        test_validate_protocol_version,
        test_get_validation_errors
    ]
    
    try:
        results = [test() for test in tests]
        passed = sum(results)
        total = len(results)
        
        print("\n" + "=" * 60)
        print(f"SUMMARY: {passed}/{total} tests passed")
        print("=" * 60)
        
        if passed == total:
            print("\n✅ ALL ADVANCED VALIDATION TESTS PASSED!")
            return 0
        else:
            print(f"\n❌ {total - passed} tests failed")
            return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
