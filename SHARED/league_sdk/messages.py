"""Protocol message utilities."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from SHARED.protocol_constants import PROTOCOL_VERSION


def format_timestamp() -> str:
    """Generate ISO-8601 UTC timestamp with Z suffix."""
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


def create_base_message(
    message_type: str,
    league_id: str,
    round_id: int,
    match_id: str,
    sender: str,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create base protocol message with required fields."""
    return {
        "protocol": PROTOCOL_VERSION,
        "message_type": message_type,
        "league_id": league_id,
        "round_id": round_id,
        "match_id": match_id,
        "conversation_id": conversation_id or str(uuid.uuid4()),
        "sender": sender,
        "timestamp": format_timestamp(),
    }


def build_game_invitation(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    player_id: str,
    opponent_id: str,
) -> Dict[str, Any]:
    """Build GAME_INVITATION message."""
    msg = create_base_message(
        "GAME_INVITATION", league_id, round_id, match_id, referee_id
    )
    msg.update({"player_id": player_id, "opponent_id": opponent_id})
    return msg


def build_game_join_ack(
    league_id: str, round_id: int, match_id: str, player_id: str, conversation_id: str
) -> Dict[str, Any]:
    """Build GAME_JOIN_ACK message."""
    return create_base_message(
        "GAME_JOIN_ACK", league_id, round_id, match_id, player_id, conversation_id
    )


def build_choose_parity_call(
    league_id: str, round_id: int, match_id: str, referee_id: str, player_id: str
) -> Dict[str, Any]:
    """Build CHOOSE_PARITY_CALL message."""
    msg = create_base_message(
        "CHOOSE_PARITY_CALL", league_id, round_id, match_id, referee_id
    )
    msg["player_id"] = player_id
    return msg


def build_parity_choice(
    league_id: str,
    round_id: int,
    match_id: str,
    player_id: str,
    choice: str,
    conversation_id: str,
) -> Dict[str, Any]:
    """Build PARITY_CHOICE message."""
    msg = create_base_message(
        "PARITY_CHOICE", league_id, round_id, match_id, player_id, conversation_id
    )
    msg["choice"] = choice
    return msg


def build_game_over(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    winner: str,
    drawn_number: int,
    player_a_choice: str,
    player_b_choice: str,
) -> Dict[str, Any]:
    """Build GAME_OVER message."""
    msg = create_base_message("GAME_OVER", league_id, round_id, match_id, referee_id)
    msg.update(
        {
            "winner": winner,
            "drawn_number": drawn_number,
            "player_a_choice": player_a_choice,
            "player_b_choice": player_b_choice,
        }
    )
    return msg


def build_match_result_report(
    league_id: str,
    round_id: int,
    match_id: str,
    referee_id: str,
    player_a: str,
    player_b: str,
    winner: str,
) -> Dict[str, Any]:
    """Build MATCH_RESULT_REPORT message."""
    msg = create_base_message(
        "MATCH_RESULT_REPORT", league_id, round_id, match_id, referee_id
    )
    msg.update({"player_a": player_a, "player_b": player_b, "winner": winner})
    return msg


def validate_message(message: Dict[str, Any]) -> bool:
    """Validate protocol message has required fields."""
    required_fields = [
        "protocol",
        "message_type",
        "league_id",
        "round_id",
        "match_id",
        "conversation_id",
        "sender",
        "timestamp",
    ]
    return (
        all(field in message for field in required_fields)
        and message["protocol"] == PROTOCOL_VERSION
        and message["timestamp"].endswith("Z")
    )
