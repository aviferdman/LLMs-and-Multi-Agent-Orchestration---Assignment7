"""End-to-end protocol compliance tests - Part 2: Round Lifecycle & Protocol Compliance.

Validates round lifecycle messages and protocol field compliance.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType
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
    build_referee_register_request,
)
from SHARED.contracts.round_lifecycle_contracts import (
    build_round_announcement,
    build_round_completed,
    build_league_standings_update,
    build_league_completed,
)
from SHARED.contracts.base_contract import validate_base_message
from SHARED.contracts.jsonrpc_helpers import extract_jsonrpc_params


def get_params(msg):
    """Extract params from JSON-RPC message."""
    return extract_jsonrpc_params(msg)


class TestRoundLifecycleFlow:
    """Test round and league lifecycle message flow."""

    def test_round_announcement(self):
        """Test round announcement message."""
        matches = [{"match_id": "R1M1", "player_A_id": "P01", "player_B_id": "P02",
                    "game_type": "even_odd", "referee_endpoint": "http://localhost:8001/mcp"}]
        round_ann = build_round_announcement(league_id="league_2025", round_id=1, matches=matches)
        params = get_params(round_ann)
        assert params[Field.MESSAGE_TYPE] == MessageType.ROUND_ANNOUNCEMENT
        assert Field.MATCHES in params
        assert validate_base_message(params)

    def test_round_completed(self):
        """Test round completed message."""
        summary = {"total_matches": 1, "wins": 1, "draws": 0, "technical_losses": 0}
        round_comp = build_round_completed(
            league_id="league_2025", round_id=1, matches_completed=1,
            summary=summary, next_round_id=2)
        params = get_params(round_comp)
        assert params[Field.MESSAGE_TYPE] == MessageType.ROUND_COMPLETED
        assert validate_base_message(params)

    def test_standings_update(self):
        """Test league standings update message."""
        standings = [{"player_id": "P01", "wins": 1, "losses": 0, "draws": 0, "points": 3},
                     {"player_id": "P02", "wins": 0, "losses": 1, "draws": 0, "points": 0}]
        standings_update = build_league_standings_update(
            league_id="league_2025", round_id=1, standings=standings)
        params = get_params(standings_update)
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_STANDINGS_UPDATE
        assert Field.STANDINGS in params
        assert validate_base_message(params)

    def test_league_completed(self):
        """Test league completed message."""
        standings = [{"player_id": "P01", "wins": 1, "losses": 0, "draws": 0, "points": 3},
                     {"player_id": "P02", "wins": 0, "losses": 1, "draws": 0, "points": 0}]
        champion = {"player_id": "P01", "total_wins": 3, "total_points": 9}
        league_comp = build_league_completed(
            league_id="league_2025", final_standings=standings,
            total_matches=3, champion=champion, total_rounds=3)
        params = get_params(league_comp)
        assert params[Field.MESSAGE_TYPE] == MessageType.LEAGUE_COMPLETED
        assert Field.CHAMPION in params
        assert params[Field.CHAMPION]["player_id"] == "P01"
        assert validate_base_message(params)


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
            params = get_params(msg)
            assert params[Field.PROTOCOL] == PROTOCOL_VERSION, \
                f"{params[Field.MESSAGE_TYPE]} has wrong protocol version"

    def test_all_messages_have_utc_timestamp(self):
        """All messages must have UTC timestamp ending with Z."""
        messages = [
            build_league_register_request("P01", "Player", "1.0", "http://localhost:8101/mcp"),
            build_game_invitation("lg", 1, "R1M1", "REF01", "P01", "P02", "player_a"),
            build_choose_parity_response("R1M1", "P01", "EVEN", "conv-1"),
        ]
        for msg in messages:
            params = get_params(msg)
            assert params[Field.TIMESTAMP].endswith("Z"), \
                f"{params[Field.MESSAGE_TYPE]} timestamp doesn't end with Z"

    def test_sender_format_compliance(self):
        """Sender field must use prefixed format (e.g., 'player:P01')."""
        player_msg = build_game_join_ack("R1M1", "P01", "conv-1", True)
        params = get_params(player_msg)
        assert params[Field.SENDER].startswith("player:"), \
            f"Player sender should start with 'player:' but got {params[Field.SENDER]}"

        ref_msg = build_game_invitation("lg", 1, "R1M1", "REF01", "P01", "P02", "player_a")
        params = get_params(ref_msg)
        assert params[Field.SENDER].startswith("referee:"), \
            f"Referee sender should start with 'referee:' but got {params[Field.SENDER]}"
