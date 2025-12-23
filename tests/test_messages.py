"""Unit tests for SHARED.league_sdk.messages module.

Tests message creation, validation, and formatting utilities.
These tests verify protocol-compliant message structures.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import re

from SHARED.constants import Field, MessageType
from SHARED.contracts import (
    build_choose_parity_call,
    build_choose_parity_response,
    build_game_invitation,
    build_game_join_ack,
    build_game_over,
    build_match_result_report,
)
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


def test_build_game_invitation():
    """Test building game invitation message."""
    msg = build_game_invitation(
        league_id="league_2025",
        round_id=1,
        match_id="R1M1",
        referee_id="REF01",
        player_id="P01",
        opponent_id="P02",
        role_in_match="player_a",
        game_type="even_odd",
    )
    assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
    assert msg[Field.ROLE_IN_MATCH] == "player_a"
    assert msg[Field.GAME_TYPE] == "even_odd"


def test_build_game_join_ack():
    """Test building game join acknowledgment."""
    msg = build_game_join_ack(
        match_id="R1M1",
        player_id="P01",
        conversation_id="conv-123",
        accept=True,
    )
    assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_JOIN_ACK and msg[Field.CONVERSATION_ID] == "conv-123"
    assert msg[Field.ACCEPT] is True


def test_build_choose_parity_call():
    """Test building choose parity call message."""
    msg = build_choose_parity_call(
        league_id="league_2025",
        round_id=1,
        match_id="R1M1",
        referee_id="REF01",
        player_id="P01",
        opponent_id="P02",
        player_standings={},
        timeout_seconds=30,
    )
    assert msg[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL and msg[Field.PLAYER_ID] == "P01"
    assert Field.DEADLINE in msg


def test_build_choose_parity_response():
    """Test building choose parity response message (new name for PARITY_CHOICE)."""
    msg = build_choose_parity_response(
        match_id="R1M1",
        player_id="P01",
        parity_choice="EVEN",
        conversation_id="conv-123",
    )
    assert msg[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_RESPONSE and msg[Field.PARITY_CHOICE] == "EVEN"


def test_build_game_over():
    """Test building game over message."""
    msg = build_game_over(
        league_id="league_2025",
        round_id=1,
        match_id="R1M1",
        referee_id="REF01",
        status="WIN",
        winner_player_id="P01",
        drawn_number=4,
        number_parity="even",
        choices={"P01": "EVEN", "P02": "ODD"},
        reason="Player P01 chose correctly",
    )
    assert msg[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
    assert msg[Field.GAME_RESULT]["winner_player_id"] == "P01"


def test_build_match_result_report():
    """Test building match result report message."""
    msg = build_match_result_report(
        league_id="league_2025",
        round_id=1,
        match_id="R1M1",
        referee_id="REF01",
        winner="P01",
        score={"P01": 1, "P02": 0},
        drawn_number=4,
        choices={"P01": "EVEN", "P02": "ODD"},
    )
    assert msg[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
    assert msg[Field.RESULT]["winner"] == "P01"


if __name__ == "__main__":
    print("=" * 60)
    print("MESSAGE UTILITIES TESTS")
    print("=" * 60)

    tests = [
        ("create_game_message", test_create_game_message),
        ("format_timestamp", test_format_timestamp),
        ("build_game_invitation", test_build_game_invitation),
        ("build_game_join_ack", test_build_game_join_ack),
        ("build_choose_parity_call", test_build_choose_parity_call),
        ("build_choose_parity_response", test_build_choose_parity_response),
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
