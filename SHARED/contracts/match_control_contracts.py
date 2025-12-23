"""Match control contract builders.

Handles match assignment and control messages.
"""

from typing import Any, Dict, Optional

from SHARED.constants import PROTOCOL_VERSION, Field, MessageType, Status
from SHARED.protocol_constants import (
    format_sender,
    generate_conversation_id,
    generate_timestamp,
)


def build_match_result_ack(
    match_id: str,
    status: str = Status.RECORDED,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build MATCH_RESULT_ACK message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.MATCH_RESULT_ACK,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.MATCH_ID: match_id,
        Field.STATUS: status,
    }


def build_start_league(
    league_id: str,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build START_LEAGUE message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.START_LEAGUE,
        Field.SENDER: "launcher",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
    }


def build_league_status(
    league_id: str,
    status: str,
    current_round: int = 0,
    total_rounds: int = 0,
    matches_completed: int = 0,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build LEAGUE_STATUS response message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.LEAGUE_STATUS,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.STATUS: status,
        "current_round": current_round,
        "total_rounds": total_rounds,
        "matches_completed": matches_completed,
    }


def build_run_match(
    league_id: str,
    round_id: int,
    match_id: str,
    player_a_id: str,
    player_a_endpoint: str,
    player_b_id: str,
    player_b_endpoint: str,
    game_type: str = "even_odd",
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build RUN_MATCH message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.RUN_MATCH,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.LEAGUE_ID: league_id,
        Field.ROUND_ID: round_id,
        Field.MATCH_ID: match_id,
        Field.GAME_TYPE: game_type,
        Field.PLAYER_A_ID: player_a_id,
        Field.PLAYER_A_ENDPOINT: player_a_endpoint,
        Field.PLAYER_B_ID: player_b_id,
        Field.PLAYER_B_ENDPOINT: player_b_endpoint,
    }


def build_shutdown_command(
    reason: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build SHUTDOWN_COMMAND message."""
    msg = {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.SHUTDOWN_COMMAND,
        Field.SENDER: "league_manager",
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
    }
    if reason:
        msg[Field.REASON] = reason
    return msg


def build_shutdown_ack(
    sender_type: str,
    sender_id: str,
    status: str = Status.ACKNOWLEDGED,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build SHUTDOWN_ACK message."""
    return {
        Field.PROTOCOL: PROTOCOL_VERSION,
        Field.MESSAGE_TYPE: MessageType.SHUTDOWN_ACK,
        Field.SENDER: format_sender(sender_type, sender_id),
        Field.TIMESTAMP: generate_timestamp(),
        Field.CONVERSATION_ID: conversation_id or generate_conversation_id(),
        Field.STATUS: status,
    }
