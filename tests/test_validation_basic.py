#!/usr/bin/env python3
"""Basic validation tests - message, timestamp, UUID."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from SHARED.league_sdk.validation import (
    validate_message, validate_timestamp, validate_uuid
)
from SHARED.constants import Field, MessageType
from SHARED.protocol_constants import PROTOCOL_VERSION

def test_validate_message():
    """Test basic message validation."""
    print("Testing validate_message...")
    
    # Valid message
    valid_msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.CONVERSATION_ID: "123e4567-e89b-12d3-a456-426614174000",
        Field.TIMESTAMP: "2025-01-01T12:00:00Z",
        Field.MESSAGE_TYPE: MessageType.GAME_INVITATION
    }
    assert validate_message(valid_msg), "Valid message should pass"
    
    # Missing field
    invalid_msg = {Field.PROTOCOL: PROTOCOL_VERSION}
    assert not validate_message(invalid_msg), "Incomplete message should fail"
    
    print("  ✓ validate_message works correctly")
    return True

def test_validate_timestamp():
    """Test timestamp validation."""
    print("Testing validate_timestamp...")
    
    # Valid timestamps
    assert validate_timestamp("2025-01-01T12:00:00Z"), "Valid timestamp should pass"
    assert validate_timestamp("2025-12-31T23:59:59Z"), "Valid timestamp should pass"
    
    # Invalid timestamps
    assert not validate_timestamp("2025-01-01T12:00:00"), "Missing Z should fail"
    assert not validate_timestamp("invalid"), "Invalid format should fail"
    assert not validate_timestamp("2025-13-01T12:00:00Z"), "Invalid month should fail"
    
    print("  ✓ validate_timestamp works correctly")
    return True

def test_validate_uuid():
    """Test UUID validation."""
    print("Testing validate_uuid...")
    
    # Valid UUIDs
    assert validate_uuid("123e4567-e89b-12d3-a456-426614174000"), "Valid UUID should pass"
    assert validate_uuid("AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"), "Uppercase UUID should pass"
    
    # Invalid UUIDs
    assert not validate_uuid("invalid"), "Invalid format should fail"
    assert not validate_uuid("123e4567-e89b-12d3-a456"), "Incomplete UUID should fail"
    assert not validate_uuid("123e4567e89b12d3a456426614174000"), "Missing dashes should fail"
    
    print("  ✓ validate_uuid works correctly")
    return True

def main():
    """Run basic validation tests."""
    print("=" * 60)
    print("BASIC VALIDATION TESTS")
    print("=" * 60)
    
    tests = [
        test_validate_message,
        test_validate_timestamp,
        test_validate_uuid
    ]
    
    try:
        results = [test() for test in tests]
        passed = sum(results)
        total = len(results)
        
        print("\n" + "=" * 60)
        print(f"SUMMARY: {passed}/{total} tests passed")
        print("=" * 60)
        
        if passed == total:
            print("\n✅ ALL BASIC VALIDATION TESTS PASSED!")
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
