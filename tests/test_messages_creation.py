"""Unit tests for message creation utilities.

Tests message creation and formatting utilities.
These tests verify protocol-compliant message structures.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import re

from SHARED.constants import Field, MessageType
from SHARED.contracts.base_contract import create_base_message, create_game_message
from SHARED.protocol_constants import generate_timestamp as format_timestamp


def test_create_game_message():
    """Test creating a game message with required fields."""
    msg = create_game_message(
        message_type=MessageType.GAME_INVITATION,
        sender_type="referee",
        sender_id="REF01",
        league_id="league_2025",
        round_id=1,
        match_id="R1M1",
    )
    assert all(k in msg for k in [Field.PROTOCOL, Field.TIMESTAMP, Field.CONVERSATION_ID, Field.MESSAGE_TYPE])
    assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION and msg[Field.TIMESTAMP].endswith("Z")


def test_format_timestamp():
    """Test timestamp formatting to ISO-8601 with Z."""
    ts = format_timestamp()
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", ts) and ts.endswith("Z")


if __name__ == "__main__":
    print("=" * 60)
    print("MESSAGE CREATION TESTS")
    print("=" * 60)

    tests = [
        ("create_game_message", test_create_game_message),
        ("format_timestamp", test_format_timestamp),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            print(f"Testing {name}...", end=" ")
            test_func()
            print("✓")
            passed += 1
        except Exception as e:
            print(f"✗ {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"SUMMARY: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ ALL MESSAGE CREATION TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
