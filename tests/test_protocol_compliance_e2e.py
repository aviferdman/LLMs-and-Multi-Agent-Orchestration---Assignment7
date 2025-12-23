"""End-to-end protocol compliance tests.

Validates that the entire message flow through the system complies
with the protocol specification in doc/protocol/v2/CONTRACTS.md.

This test simulates a complete game lifecycle:
1. Agent registration
2. Match invitation and join
3. Parity choice collection
4. Game resolution
5. Result reporting
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.contracts import (
    build_choose_parity_call,
    build_choose_parity_response,
    build_game_invitation,
    build_game_join_ack,
    build_game_over,
    build_match_result_report,
)
from SHARED.contracts.league_manager_contracts import (
    build_league_register_request,
    build_league_register_response,
    build_referee_register_request,
    build_referee_register_response,
    build_run_match,
    build_match_result_ack,
)
from SHARED.contracts.round_lifecycle_contracts import (
    build_round_announcement,
    build_round_completed,
    build_league_standings_update,
    build_league_completed,
)
from SHARED.contracts.base_contract import validate_base_message


class TestCompleteGameLifecycle:
    """Test complete game lifecycle message flow."""

    def test_registration_flow(self):
        """Test player and referee registration message flow."""
        # Player registration request
        player_reg = build_league_register_request(
            player_id="P01",
            display_name="Test Player 1",
            version="1.0.0",
            contact_endpoint="http://localhost:8101/mcp",
        )
        assert player_reg[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_REQUEST
        assert Field.PLAYER_META in player_reg
        assert validate_base_message(player_reg)

        # Player registration response
        player_resp = build_league_register_response(
            player_id="P01",
            status=Status.ACCEPTED,
        )
        assert player_resp[Field.MESSAGE_TYPE] == MessageType.LEAGUE_REGISTER_RESPONSE
        assert player_resp[Field.STATUS] == Status.ACCEPTED
        assert validate_base_message(player_resp)

        # Referee registration request
        ref_reg = build_referee_register_request(
            referee_id="REF01",
            display_name="Test Referee 1",
            version="1.0.0",
            contact_endpoint="http://localhost:8001/mcp",
        )
        assert ref_reg[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_REQUEST
        assert Field.REFEREE_META in ref_reg
        assert validate_base_message(ref_reg)

        # Referee registration response
        ref_resp = build_referee_register_response(
            referee_id="REF01",
            status=Status.ACCEPTED,
        )
        assert ref_resp[Field.MESSAGE_TYPE] == MessageType.REFEREE_REGISTER_RESPONSE
        assert validate_base_message(ref_resp)

    def test_match_invitation_flow(self):
        """Test match invitation and join message flow."""
        # Game invitation from referee
        invitation = build_game_invitation(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            role_in_match="player_a",
            game_type="even_odd",
        )
        assert invitation[Field.MESSAGE_TYPE] == MessageType.GAME_INVITATION
        assert invitation[Field.ROLE_IN_MATCH] == "player_a"
        assert invitation[Field.GAME_TYPE] == "even_odd"
        assert validate_base_message(invitation)

        # Player join acknowledgment
        join_ack = build_game_join_ack(
            match_id="R1M1",
            player_id="P01",
            conversation_id=invitation[Field.CONVERSATION_ID],
            accept=True,
        )
        assert join_ack[Field.MESSAGE_TYPE] == MessageType.GAME_JOIN_ACK
        assert join_ack[Field.ACCEPT] is True
        assert Field.ARRIVAL_TIMESTAMP in join_ack
        assert validate_base_message(join_ack)

    def test_parity_choice_flow(self):
        """Test parity choice collection message flow."""
        # Parity call from referee
        parity_call = build_choose_parity_call(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            player_id="P01",
            opponent_id="P02",
            player_standings={"wins": 0, "losses": 0, "draws": 0},
            timeout_seconds=30,
        )
        assert parity_call[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_CALL
        assert Field.DEADLINE in parity_call
        assert Field.CONTEXT in parity_call
        assert parity_call[Field.CONTEXT]["opponent_id"] == "P02"
        assert validate_base_message(parity_call)

        # Player parity response
        parity_response = build_choose_parity_response(
            match_id="R1M1",
            player_id="P01",
            parity_choice="EVEN",
            conversation_id=parity_call[Field.CONVERSATION_ID],
        )
        assert parity_response[Field.MESSAGE_TYPE] == MessageType.CHOOSE_PARITY_RESPONSE
        assert parity_response[Field.PARITY_CHOICE] == "EVEN"
        assert validate_base_message(parity_response)

    def test_game_resolution_flow(self):
        """Test game resolution message flow."""
        # Game over notification
        game_over = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="WIN",
            winner_player_id="P01",
            drawn_number=4,
            number_parity="even",
            choices={"P01": "EVEN", "P02": "ODD"},
            reason="P01 correctly predicted even parity",
        )
        assert game_over[Field.MESSAGE_TYPE] == MessageType.GAME_OVER
        assert Field.GAME_RESULT in game_over
        assert game_over[Field.GAME_RESULT]["status"] == "WIN"
        assert game_over[Field.GAME_RESULT]["winner_player_id"] == "P01"
        assert game_over[Field.GAME_RESULT]["drawn_number"] == 4
        assert validate_base_message(game_over)

        # Match result report to LM
        result_report = build_match_result_report(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            winner="P01",
            score={"P01": 1, "P02": 0},
            drawn_number=4,
            choices={"P01": "EVEN", "P02": "ODD"},
        )
        assert result_report[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_REPORT
        assert Field.RESULT in result_report
        assert result_report[Field.RESULT]["winner"] == "P01"
        assert validate_base_message(result_report)

        # Match result acknowledgment
        result_ack = build_match_result_ack(
            match_id="R1M1",
            conversation_id=result_report[Field.CONVERSATION_ID],
        )
        assert result_ack[Field.MESSAGE_TYPE] == MessageType.MATCH_RESULT_ACK
        assert validate_base_message(result_ack)

    def test_round_lifecycle_flow(self):
        """Test round and league lifecycle message flow."""
        # Round announcement
        matches = [
            {
                "match_id": "R1M1",
                "player_A_id": "P01",
                "player_B_id": "P02",
                "game_type": "even_odd",
                "referee_endpoint": "http://localhost:8001/mcp",
            },
        ]
        round_ann = build_round_announcement(
            league_id="league_2025",
            round_id=1,
            matches=matches,
        )
        assert round_ann[Field.MESSAGE_TYPE] == MessageType.ROUND_ANNOUNCEMENT
        assert Field.MATCHES in round_ann
        assert validate_base_message(round_ann)

        # Round completed
        summary = {"total_matches": 1, "wins": 1, "draws": 0, "technical_losses": 0}
        round_comp = build_round_completed(
            league_id="league_2025",
            round_id=1,
            matches_completed=1,
            summary=summary,
            next_round_id=2,
        )
        assert round_comp[Field.MESSAGE_TYPE] == MessageType.ROUND_COMPLETED
        assert validate_base_message(round_comp)

        # Standings update
        standings = [
            {"player_id": "P01", "wins": 1, "losses": 0, "draws": 0, "points": 3},
            {"player_id": "P02", "wins": 0, "losses": 1, "draws": 0, "points": 0},
        ]
        standings_update = build_league_standings_update(
            league_id="league_2025",
            round_id=1,
            standings=standings,
        )
        assert standings_update[Field.MESSAGE_TYPE] == MessageType.LEAGUE_STANDINGS_UPDATE
        assert Field.STANDINGS in standings_update
        assert validate_base_message(standings_update)

        # League completed
        final_standings = standings
        champion = {"player_id": "P01", "total_wins": 3, "total_points": 9}
        league_comp = build_league_completed(
            league_id="league_2025",
            final_standings=final_standings,
            total_matches=3,
            champion=champion,
            total_rounds=3,
        )
        assert league_comp[Field.MESSAGE_TYPE] == MessageType.LEAGUE_COMPLETED
        assert Field.CHAMPION in league_comp
        assert league_comp[Field.CHAMPION]["player_id"] == "P01"
        assert validate_base_message(league_comp)


class TestProtocolCompliance:
    """Test protocol field compliance across all messages."""

    def test_all_messages_have_protocol_version(self):
        """All messages must include correct protocol version."""
        messages = [
            build_league_register_request("P01", "Player", "1.0", "http://localhost:8101/mcp"),
            build_referee_register_request("REF01", "Referee", "1.0", "http://localhost:8001/mcp"),
            build_game_invitation("lg", 1, "R1M1", "REF01", "P01", "P02", "player_a"),
            build_game_join_ack("R1M1", "P01", "conv-1", True),
            build_choose_parity_call("lg", 1, "R1M1", "REF01", "P01", "P02", {}, 30),
            build_choose_parity_response("R1M1", "P01", "EVEN", "conv-1"),
            build_game_over("lg", 1, "R1M1", "REF01", "WIN", "P01", 4, "even", {}, "normal"),
            build_match_result_report("lg", 1, "R1M1", "REF01", "P01", {}, 4, {}),
        ]

        for msg in messages:
            assert msg[Field.PROTOCOL] == PROTOCOL_VERSION, \
                f"{msg[Field.MESSAGE_TYPE]} has wrong protocol version"

    def test_all_messages_have_utc_timestamp(self):
        """All messages must have UTC timestamp ending with Z."""
        messages = [
            build_league_register_request("P01", "Player", "1.0", "http://localhost:8101/mcp"),
            build_game_invitation("lg", 1, "R1M1", "REF01", "P01", "P02", "player_a"),
            build_choose_parity_response("R1M1", "P01", "EVEN", "conv-1"),
        ]

        for msg in messages:
            assert msg[Field.TIMESTAMP].endswith("Z"), \
                f"{msg[Field.MESSAGE_TYPE]} timestamp doesn't end with Z"

    def test_sender_format_compliance(self):
        """Sender field must use prefixed format (e.g., 'player:P01')."""
        # Player messages
        player_msg = build_game_join_ack("R1M1", "P01", "conv-1", True)
        assert player_msg[Field.SENDER].startswith("player:"), \
            f"Player sender should start with 'player:' but got {player_msg[Field.SENDER]}"

        # Referee messages
        ref_msg = build_game_invitation("lg", 1, "R1M1", "REF01", "P01", "P02", "player_a")
        assert ref_msg[Field.SENDER].startswith("referee:"), \
            f"Referee sender should start with 'referee:' but got {ref_msg[Field.SENDER]}"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_draw_game_result(self):
        """Test GAME_OVER with draw result."""
        game_over = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="DRAW",
            winner_player_id=None,
            drawn_number=4,
            number_parity="even",
            choices={"P01": "EVEN", "P02": "EVEN"},
            reason="Both players chose the same parity",
        )
        assert game_over[Field.GAME_RESULT]["status"] == "DRAW"
        assert game_over[Field.GAME_RESULT]["winner_player_id"] is None
        assert validate_base_message(game_over)

    def test_timeout_game_result(self):
        """Test GAME_OVER with timeout result."""
        game_over = build_game_over(
            league_id="league_2025",
            round_id=1,
            match_id="R1M1",
            referee_id="REF01",
            status="TECHNICAL_LOSS",
            winner_player_id="P02",
            drawn_number=0,
            number_parity="even",
            choices={"P01": "NO_RESPONSE", "P02": "ODD"},
            reason="P01 timed out",
        )
        assert game_over[Field.GAME_RESULT]["status"] == "TECHNICAL_LOSS"
        assert game_over[Field.GAME_RESULT]["reason"] == "P01 timed out"
        assert validate_base_message(game_over)

    def test_rejected_registration(self):
        """Test rejected registration response."""
        response = build_league_register_response(
            player_id="P99",
            status=Status.REJECTED,
            reason="League is full",
        )
        assert response[Field.STATUS] == Status.REJECTED
        assert response.get(Field.REASON) == "League is full"
        assert validate_base_message(response)


if __name__ == "__main__":
    print("=" * 60)
    print("END-TO-END PROTOCOL COMPLIANCE TESTS")
    print("=" * 60)

    test_classes = [
        ("TestCompleteGameLifecycle", TestCompleteGameLifecycle),
        ("TestProtocolCompliance", TestProtocolCompliance),
        ("TestEdgeCases", TestEdgeCases),
    ]

    passed = 0
    failed = 0

    for class_name, test_class in test_classes:
        print(f"\n{class_name}:")
        print("-" * 40)
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    print(f"  {method_name}...", end=" ")
                    getattr(instance, method_name)()
                    print("✓")
                    passed += 1
                except Exception as e:
                    print(f"✗ {e}")
                    failed += 1

    print()
    print("=" * 60)
    print(f"SUMMARY: {passed}/{passed + failed} tests passed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ ALL E2E PROTOCOL COMPLIANCE TESTS PASSED!")
    else:
        print(f"\n❌ {failed} test(s) failed")
