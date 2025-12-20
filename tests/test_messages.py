"""Unit tests for SHARED.league_sdk.messages module.

Tests message creation, validation, and formatting utilities.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from SHARED.league_sdk.messages import (
    create_base_message,
    validate_message,
    format_timestamp,
    build_game_invitation,
    build_game_join_ack,
    build_choose_parity_call,
    build_parity_choice,
    build_game_over,
    build_match_result_report
)
from SHARED.constants import MessageType
import re

def test_create_base_message():
    """Test creating a base message with required fields."""
    msg = create_base_message(MessageType.GAME_INVITATION, "league_2025", 1, "R1M1", "REF01")
    assert all(k in msg for k in ["protocol", "timestamp", "conversation_id", "message_type"])
    assert msg["message_type"] == MessageType.GAME_INVITATION and msg["timestamp"].endswith("Z")

def test_format_timestamp():
    """Test timestamp formatting to ISO-8601 with Z."""
    ts = format_timestamp()
    assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z', ts) and ts.endswith("Z")

def test_validate_message_valid():
    """Test validation of valid message."""
    msg = create_base_message(MessageType.GAME_INVITATION, "league_2025", 1, "R1M1", "REF01")
    assert validate_message(msg) == True

def test_validate_message_missing_field():
    """Test validation catches missing required field."""
    assert validate_message({"protocol": "league.v2"}) == False

def test_build_game_invitation():
    """Test building game invitation message."""
    msg = build_game_invitation("league_2025", 1, "R1M1", "REF01", "P01", "P02")
    assert msg["message_type"] == "GAME_INVITATION" and msg["player_id"] == "P01"

def test_build_game_join_ack():
    """Test building game join acknowledgment."""
    msg = build_game_join_ack("league_2025", 1, "R1M1", "P01", "conv-123")
    assert msg["message_type"] == "GAME_JOIN_ACK" and msg["conversation_id"] == "conv-123"

def test_build_choose_parity_call():
    """Test building choose parity call message."""
    msg = build_choose_parity_call("league_2025", 1, "R1M1", "REF01", "P01")
    assert msg["message_type"] == "CHOOSE_PARITY_CALL" and msg["player_id"] == "P01"

def test_build_parity_choice():
    """Test building parity choice message."""
    msg = build_parity_choice("league_2025", 1, "R1M1", "P01", "EVEN", "conv-123")
    assert msg["message_type"] == "PARITY_CHOICE" and msg["choice"] == "EVEN"

def test_build_game_over():
    """Test building game over message."""
    msg = build_game_over("league_2025", 1, "R1M1", "REF01", "PLAYER_A", 4, "EVEN", "ODD")
    assert msg["winner"] == "PLAYER_A" and msg["drawn_number"] == 4

def test_build_match_result_report():
    """Test building match result report message."""
    msg = build_match_result_report("league_2025", 1, "R1M1", "REF01", "P01", "P02", "PLAYER_A")
    assert msg["player_a"] == "P01" and msg["winner"] == "PLAYER_A"

if __name__ == "__main__":
    print("=" * 60)
    print("MESSAGE UTILITIES TESTS")
    print("=" * 60)
    
    tests = [
        ("create_base_message", test_create_base_message),
        ("format_timestamp", test_format_timestamp),
        ("validate_message_valid", test_validate_message_valid),
        ("validate_message_missing_field", test_validate_message_missing_field),
        ("build_game_invitation", test_build_game_invitation),
        ("build_game_join_ack", test_build_game_join_ack),
        ("build_choose_parity_call", test_build_choose_parity_call),
        ("build_parity_choice", test_build_parity_choice),
        ("build_game_over", test_build_game_over),
        ("build_match_result_report", test_build_match_result_report),
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
        print("\n✅ ALL MESSAGE TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
